<?php declare(strict_types = 0);

/**
 * Tree Navigator widget view.
 *
 * @var CView  $this
 * @var array  $data
 */

$nodes       = $data['tree']['nodes'];
$roots       = $data['tree']['roots'];
$show_mode   = (int)  $data['show_mode'];
$recursive   = (bool) $data['recursive'];
$root_name = $data['root_name'];

$view = new CWidgetView($data);

if (empty($roots)) {
	$view->show();
	return;
}

// ── Recursive node renderer ───────────────────────────────────────────────────

$render_node = null;
$render_node = static function(string $path) use (&$render_node, $nodes, $show_mode): CTag {
	$node        = $nodes[$path];
	$has_children = !empty($node['children']);
	$has_hosts   = $show_mode === 1 && !empty($node['hosts']);
	$is_real     = $node['groupid'] !== null;

	// Row
	$row = (new CDiv())->addClass('tn-row');

	// Toggle (+/-)
	if ($has_children || $has_hosts) {
		$row->addItem((new CSpan())->addClass('tn-toggle js-tn-toggle'));
	}
	else {
		$row->addItem((new CSpan())->addClass('tn-toggle-ph'));
	}

	// Folder icon
	$folder = (new CSpan())->addClass('tn-folder js-tn-folder');

	if ($is_real) {
		$folder->setAttribute('data-host-count',           (string) $node['host_count'])
		       ->setAttribute('data-recursive-host-count', (string) $node['recursive_host_count']);
	}

	$row->addItem($folder);

	// Group label (clickable only for real groups)
	$label = (new CSpan(htmlspecialchars($node['label'])))->addClass('tn-group-label');

	if ($is_real) {
		$label->addClass('js-tn-group-label')
		      ->setAttribute('data-groupid',        $node['groupid'])
		      ->setAttribute('data-child-groupids', implode(',', $node['child_groupids']));
	}

	$row->addItem($label);

	// Children container
	$children_ul = null;

	if ($has_children || $has_hosts) {
		$children_ul = (new CTag('ul', true))->addClass('tn-children');

		// Sub-groups
		foreach ($node['children'] as $child_path) {
			$children_ul->addItem($render_node($child_path));
		}

		// Hosts (show_mode = 1 only)
		if ($has_hosts) {
			foreach ($node['hosts'] as $host) {
				$type     = $host['device_type'] ?? 'server';
				$host_row = (new CDiv())->addClass('tn-row');

				// Host icon – clicking opens Zabbix host menu
				$host_row->addItem(
					(new CSpan())
						->addClass('tn-host-icon hm-icon hm-icon-' . $type . ' js-tn-host-icon')
						->setAttribute('data-menu-popup', json_encode(
							['type' => 'host', 'data' => ['hostid' => (string) $host['hostid']]],
							JSON_UNESCAPED_UNICODE
						))
				);

				// Host label – clicking broadcasts the host
				$host_row->addItem(
					(new CSpan(htmlspecialchars($host['name'])))
						->addClass('tn-host-label js-tn-host-label')
						->setAttribute('data-hostid',         (string) $host['hostid'])
						->setAttribute('data-parent-groupid', $node['groupid'] ?? '')
				);

				$children_ul->addItem(
					(new CTag('li', true, $host_row))->addClass('tn-node tn-host')
				);
			}
		}
	}

	// Group <li>
	$li = (new CTag('li', true))->addClass('tn-node tn-group');
	$li->setAttribute('data-path', $path);

	if ($is_real) {
		$li->setAttribute('data-groupid', $node['groupid']);
	}

	$li->addItem($row);

	if ($children_ul !== null) {
		$li->addItem($children_ul);
	}

	return $li;
};

// ── Server root node ──────────────────────────────────────────────────────────

$server_children = (new CTag('ul', true))->addClass('tn-children');

foreach ($roots as $root_path) {
	$server_children->addItem($render_node($root_path));
}

$server_row = (new CDiv())->addClass('tn-row');
$server_row->addItem((new CSpan())->addClass('tn-toggle js-tn-toggle'));
$server_row->addItem((new CSpan())->addClass('tn-root-icon'));
$server_row->addItem(
	(new CSpan(htmlspecialchars($root_name)))->addClass('tn-group-label tn-server-label')
);

$server_li = (new CTag('li', true))->addClass('tn-node tn-group tn-server-root');
$server_li->setAttribute('data-path', '__server_root__');
$server_li->addItem($server_row);
$server_li->addItem($server_children);

// ── Root tree ─────────────────────────────────────────────────────────────────

$tree_ul = (new CTag('ul', true))->addClass('tn-tree');
$tree_ul->addItem($server_li);

$container = (new CDiv($tree_ul))
	->addClass('tn-container')
	->setAttribute('data-recursive', $recursive ? '1' : '0');

$view->addItem($container)->show();
