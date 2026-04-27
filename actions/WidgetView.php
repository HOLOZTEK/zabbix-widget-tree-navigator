<?php declare(strict_types = 0);

namespace Modules\TreeNavigator\Actions;

use API,
	CControllerDashboardWidgetView,
	CControllerResponseData;

class WidgetView extends CControllerDashboardWidgetView {

	protected function doAction(): void {
		$show_mode      = (int)  ($this->fields_values['show_mode'] ?? 1);
		$recursive      = (bool) ($this->fields_values['recursive'] ?? true);
		$groupids_filter = $this->fields_values['groupids'] ?: null;
		$root_name    = trim($this->fields_values['root_name'] ?? '');

		if ($root_name === '') {
			$root_name = 'Zabbix';
		}

		// ── Fetch all host groups ─────────────────────────────────────────────

		$all_groups = API::HostGroup()->get([
			'output'      => ['groupid', 'name'],
			'preservekeys' => true
		]);

		$no_data = [
			'name'        => $this->getInput('name', $this->widget->getDefaultName()),
			'tree'        => ['nodes' => [], 'roots' => []],
			'show_mode'   => $show_mode,
			'recursive'   => $recursive,
			'root_name' => $root_name,
			'user'        => ['debug_mode' => $this->getDebugMode()]
		];

		if (!$all_groups) {
			$this->setResponse(new CControllerResponseData($no_data));
			return;
		}

		// ── Determine relevant groups ─────────────────────────────────────────

		$relevant_groups = ($groupids_filter !== null)
			? $this->filterGroups($all_groups, $groupids_filter)
			: $all_groups;

		if (!$relevant_groups) {
			$this->setResponse(new CControllerResponseData($no_data));
			return;
		}

		$relevant_groupids = array_column($relevant_groups, 'groupid');

		// ── Fetch hosts ───────────────────────────────────────────────────────
		// Always fetch to compute host counts for folder icon tooltip.
		// Fetch name/device info only when show_mode = 1.

		$host_params = [
			'output'          => ($show_mode === 1) ? ['hostid', 'host', 'name'] : ['hostid'],
			'selectHostGroups' => ['groupid'],
			'groupids'        => $relevant_groupids,
			'preservekeys'    => true
		];

		if ($show_mode === 1) {
			$host_params['selectInventory']       = ['type', 'os'];
			$host_params['selectParentTemplates'] = ['name'];
		}

		$hosts = API::Host()->get($host_params);

		$host_count_by_group = [];
		$hosts_by_group      = [];

		foreach ($hosts as $host) {
			foreach ($host['hostgroups'] as $hg) {
				$gid = $hg['groupid'];

				if (!in_array($gid, $relevant_groupids, true)) {
					continue;
				}

				$host_count_by_group[$gid] = ($host_count_by_group[$gid] ?? 0) + 1;

				if ($show_mode === 1) {
					$hosts_by_group[$gid][] = [
						'hostid'      => $host['hostid'],
						'name'        => $host['name'],
						'device_type' => $this->detectDeviceType($host)
					];
				}
			}
		}

		// Sort hosts alphabetically within each group
		foreach ($hosts_by_group as &$group_hosts) {
			usort($group_hosts, static fn($a, $b) => strcmp($a['name'], $b['name']));
		}
		unset($group_hosts);

		// ── Build and return tree ─────────────────────────────────────────────

		$tree = $this->buildTree($relevant_groups, $host_count_by_group, $hosts_by_group);

		$this->setResponse(new CControllerResponseData([
			'name'        => $this->getInput('name', $this->widget->getDefaultName()),
			'tree'        => $tree,
			'show_mode'   => $show_mode,
			'recursive'   => $recursive,
			'root_name' => $root_name,
			'user'        => ['debug_mode' => $this->getDebugMode()]
		]));
	}

	// ── Helpers ───────────────────────────────────────────────────────────────

	/**
	 * Return only the groups that are in the filter or are ancestors of filtered groups.
	 */
	private function filterGroups(array $all_groups, array $filter_groupids): array {
		$filter_names = [];

		foreach ($all_groups as $g) {
			if (in_array($g['groupid'], $filter_groupids, true)) {
				$filter_names[] = $g['name'];
			}
		}

		if (!$filter_names) {
			return [];
		}

		$relevant = [];

		foreach ($all_groups as $key => $g) {
			if (in_array($g['groupid'], $filter_groupids, true)) {
				$relevant[$key] = $g;
				continue;
			}

			// Include ancestor nodes (groups whose name is a prefix of a filtered group)
			foreach ($filter_names as $filter_name) {
				if (str_starts_with($filter_name, $g['name'] . '/')) {
					$relevant[$key] = $g;
					break;
				}
			}
		}

		return $relevant;
	}

	/**
	 * Build a flat node map with parent-child relationships derived from "/" in group names.
	 *
	 * Each node:
	 *   path            – full slash-separated path (unique key)
	 *   label           – last segment of the path (display name)
	 *   groupid         – real Zabbix groupid, or null for virtual parent nodes
	 *   host_count      – number of hosts directly assigned to this group
	 *   children        – ordered list of child paths
	 *   hosts           – host entries for this group (empty when show_mode=0)
	 *   child_groupids  – all descendant real groupids (for recursive broadcast)
	 */
	private function buildTree(array $groups, array $host_count_by_group, array $hosts_by_group): array {
		usort($groups, static fn($a, $b) => strcmp($a['name'], $b['name']));

		$nodes = [];

		// ── Create a node for every path component ────────────────────────────
		foreach ($groups as $group) {
			$parts = explode('/', $group['name']);
			$path  = '';

			foreach ($parts as $i => $part) {
				$prev = $path;
				$path = ($i === 0) ? $part : ($path . '/' . $part);

				if (!isset($nodes[$path])) {
					$nodes[$path] = [
						'path'                 => $path,
						'label'                => $part,
						'groupid'              => null,
						'host_count'           => 0,
						'recursive_host_count' => 0,
						'children'             => [],
						'hosts'                => [],
						'child_groupids'       => [],
					];
				}

				if ($prev !== '' && isset($nodes[$prev])
						&& !in_array($path, $nodes[$prev]['children'], true)) {
					$nodes[$prev]['children'][] = $path;
				}
			}

			// Assign real data to the leaf node
			$gid                          = $group['groupid'];
			$nodes[$group['name']]['groupid']    = (string) $gid;
			$nodes[$group['name']]['host_count'] = (int) ($host_count_by_group[$gid] ?? 0);
			$nodes[$group['name']]['hosts']      = $hosts_by_group[$gid] ?? [];
		}

		// ── Compute child_groupids and recursive_host_count bottom-up ─────────
		// Process deepest paths first so children are resolved before parents.
		$all_paths = array_keys($nodes);
		usort($all_paths, static fn($a, $b) => substr_count($b, '/') <=> substr_count($a, '/'));

		foreach ($all_paths as $path) {
			$ids = [];

			if ($nodes[$path]['groupid'] !== null) {
				$ids[] = $nodes[$path]['groupid'];
			}

			foreach ($nodes[$path]['children'] as $child_path) {
				foreach ($nodes[$child_path]['child_groupids'] as $cid) {
					if (!in_array($cid, $ids, true)) {
						$ids[] = $cid;
					}
				}
			}

			$nodes[$path]['child_groupids'] = $ids;
		}

		// ── Compute recursive_host_count (own hosts + all descendants) ────────
		foreach ($all_paths as $path) {
			$count = $nodes[$path]['host_count'];

			foreach ($nodes[$path]['children'] as $child_path) {
				$count += $nodes[$child_path]['recursive_host_count'];
			}

			$nodes[$path]['recursive_host_count'] = $count;
		}

		// ── Find root nodes ───────────────────────────────────────────────────
		$roots = [];

		foreach (array_keys($nodes) as $path) {
			$slash = strrpos($path, '/');

			if ($slash === false || !isset($nodes[substr($path, 0, $slash)])) {
				$roots[] = $path;
			}
		}

		sort($roots);

		return ['nodes' => $nodes, 'roots' => $roots];
	}

	/**
	 * Detect the OS/device type from host inventory and linked templates.
	 */
	private function detectDeviceType(array $host): string {
		$inv      = is_array($host['inventory']) ? $host['inventory'] : [];
		$inv_os   = strtolower($inv['os']   ?? '');
		$inv_type = strtolower($inv['type'] ?? '');
		$tmpl     = strtolower(implode(' ', array_column($host['parentTemplates'] ?? [], 'name')));

		if (preg_match('/linux|ubuntu|debian|centos|rhel|alma|rocky|fedora|suse/', $inv_os)
				|| preg_match('/linux|ubuntu|debian|centos|rhel|alma|rocky|fedora|suse/', $tmpl)) {
			return 'linux';
		}

		if (str_contains($inv_os, 'windows') || str_contains($tmpl, 'windows')) {
			return 'windows';
		}

		if (preg_match('/cisco|juniper|arista|huawei|fortinet|paloalto|mikrotik|extreme|f5/', $tmpl)
				|| in_array($inv_type, ['network device', 'switch', 'router', 'firewall', 'load balancer'], true)) {
			return 'network';
		}

		if (str_contains($tmpl, 'vmware') || str_contains($tmpl, 'hyper-v')
				|| str_contains($inv_type, 'virtual')) {
			return 'virtual';
		}

		return 'server';
	}
}
