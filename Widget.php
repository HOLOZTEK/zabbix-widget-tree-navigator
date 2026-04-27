<?php declare(strict_types = 0);

namespace Modules\TreeNavigator;

use Zabbix\Core\CWidget;

class Widget extends CWidget {

	public function init(): void {
		require_once __DIR__ . '/includes/helpers.php';
		bindtextdomain('tree-navigator', __DIR__ . '/locale');
		bind_textdomain_codeset('tree-navigator', 'UTF-8');
	}

	public function getDefaultName(): string {
		return _tn('Tree navigator');
	}
}
