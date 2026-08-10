<?php declare(strict_types = 0);

/**
 * Tree Navigator widget view.
 *
 * @var CView  $this
 * @var array  $data
 */

$nodes           = $data['tree']['nodes'];
$roots           = $data['tree']['roots'];
$show_mode       = (int)  $data['show_mode'];
$recursive       = (bool) $data['recursive'];
$show_host_count = (bool) $data['show_host_count'];
$initial_depth   = (int)  $data['initial_depth'];
$root_name       = $data['root_name'];
$folder_font_color = $data['folder_font_color'];
$host_font_color   = $data['host_font_color'];

$view = new CWidgetView($data);

if (empty($roots)) {
	$view->show();
	return;
}

// ── Recursive node renderer ───────────────────────────────────────────────────

$render_node = null;
$render_node = static function(string $path) use (&$render_node, $nodes, $show_mode, $show_host_count): CTag {
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

	// Multi-select checkbox (hidden via CSS unless multi-select mode is active)
	if ($is_real) {
		$row->addItem(
			(new CTag('input', false))
				->setAttribute('type', 'checkbox')
				->setAttribute('class', 'tn-checkbox js-tn-checkbox js-tn-group-checkbox')
				->setAttribute('data-groupid', $node['groupid'])
		);
	}

	// Folder icon
	$folder = (new CSpan())->addClass('tn-folder js-tn-folder');

	if ($is_real && $show_host_count) {
		$folder->setAttribute('data-host-count',           (string) $node['host_count'])
		       ->setAttribute('data-recursive-host-count', (string) $node['recursive_host_count']);
	}

	$row->addItem($folder);

	// Group label (clickable only for real groups)
	$label = (new CSpan($node['label']))->addClass('tn-group-label');

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

				// Multi-select checkbox (hidden via CSS unless multi-select mode is active)
				$host_row->addItem(
					(new CTag('input', false))
						->setAttribute('type', 'checkbox')
						->setAttribute('class', 'tn-checkbox js-tn-checkbox js-tn-host-checkbox')
						->setAttribute('data-hostid', (string) $host['hostid'])
				);

				// Host icon – clicking opens Zabbix host menu
				$host_row->addItem(
					(new CSpan())
						->addClass('tn-host-icon tn-host-type-icon tn-host-type-icon-' . $type . ' js-tn-host-icon')
						->setAttribute('data-menu-popup', json_encode(
							['type' => 'host', 'data' => ['hostid' => (string) $host['hostid']]],
							JSON_UNESCAPED_UNICODE
						))
				);

				// Host label – clicking broadcasts the host
				$host_row->addItem(
					(new CSpan($host['name']))
						->addClass('tn-host-label js-tn-host-label')
						->setAttribute('data-hostid', (string) $host['hostid'])
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
	(new CSpan($root_name))->addClass('tn-group-label tn-server-label')
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
	->setAttribute('data-recursive',     $recursive ? '1' : '0')
	->setAttribute('data-initial-depth', (string) $initial_depth);

// ── Wrapper ───────────────────────────────────────────────────────────────────

$wrapper = (new CDiv())
	->addClass('tn-wrapper')
	->setAttribute('data-label-host-count',    _holoztek_tn('Hosts: {0}'))
	->setAttribute('data-label-more-results',  _holoztek_tn('and {0} more'))
	->setAttribute('data-label-multi-on',      _holoztek_tn('Switch to single-select'))
	->setAttribute('data-label-multi-off',     _holoztek_tn('Switch to multi-select'))
	->setAttribute('style',
		'--tn-folder-color: ' . $folder_font_color . '; --tn-host-color: ' . $host_font_color . ';'
	);

// ── Toolbar: multi-select toggle (always) + search area (show_mode = 1 only) ──

$mode_toggle = (new CTag('button', true))
	->setAttribute('type', 'button')
	->setAttribute('class', 'tn-mode-toggle js-tn-mode-toggle')
	->setAttribute('title', _holoztek_tn('Switch to multi-select'));

$toolbar = (new CDiv())
	->addClass('tn-toolbar')
	->addItem($mode_toggle);

if ($show_mode === 1) {
	$search_toggle = (new CTag('button', true))
		->setAttribute('type', 'button')
		->setAttribute('class', 'tn-search-toggle js-tn-search-toggle')
		->setAttribute('title', _holoztek_tn('Search hosts'));

	$search_count = (new CSpan())->addClass('tn-search-count js-tn-search-count');

	$search_prev = (new CTag('button', true, '▲'))
		->setAttribute('type', 'button')
		->setAttribute('class', 'tn-search-nav-btn js-tn-search-prev')
		->setAttribute('title', _holoztek_tn('Previous match'));

	$search_next = (new CTag('button', true, '▼'))
		->setAttribute('type', 'button')
		->setAttribute('class', 'tn-search-nav-btn js-tn-search-next')
		->setAttribute('title', _holoztek_tn('Next match'));

	$search_nav = (new CDiv())
		->addClass('tn-search-nav')
		->addItem($search_count)
		->addItem($search_prev)
		->addItem($search_next);

	$search_input = (new CTag('input', false))
		->setAttribute('type', 'text')
		->setAttribute('class', 'tn-search-input js-tn-search-input')
		->setAttribute('placeholder', _holoztek_tn('Search hosts...'))
		->setAttribute('autocomplete', 'off')
		->setAttribute('spellcheck', 'false');

	$search_clear = (new CTag('button', true, '×'))
		->setAttribute('type', 'button')
		->setAttribute('class', 'tn-search-clear js-tn-search-clear')
		->setAttribute('title', _holoztek_tn('Clear'))
		->setAttribute('style', 'display:none');

	$search_input_wrap = (new CDiv())
		->addClass('tn-search-input-wrap')
		->addItem($search_input)
		->addItem($search_clear);

	$search_input_row = (new CDiv())
		->addClass('tn-search-input-row')
		->addItem($search_input_wrap)
		->addItem($search_nav);

	$search_dropdown = (new CTag('ul', true))
		->addClass('tn-search-dropdown js-tn-search-dropdown');

	$search_bar = (new CDiv())
		->addClass('tn-search-bar js-tn-search-bar')
		->setAttribute('style', 'display:none')
		->addItem($search_input_row)
		->addItem($search_dropdown);

	$search_area = (new CDiv())
		->addClass('tn-search-area')
		->addItem($search_toggle)
		->addItem($search_bar);

	$toolbar->addItem($search_area);
}

$wrapper->addItem($toolbar);
$wrapper->addItem($container);

$view->addItem($wrapper)->show();
