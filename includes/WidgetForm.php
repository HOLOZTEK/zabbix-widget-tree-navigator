<?php declare(strict_types = 0);

namespace Modules\TreeNavigator\Includes;

use Zabbix\Widgets\CWidgetForm;
use Zabbix\Widgets\Fields\{
	CWidgetFieldCheckBox,
	CWidgetFieldMultiSelectGroup,
	CWidgetFieldRadioButtonList,
	CWidgetFieldTextBox
};

class WidgetForm extends CWidgetForm {

	public function addFields(): self {
		return $this
			->addField(
				(new CWidgetFieldTextBox('root_name', _tn('Root name')))
					->setMaxLength(255)
			)
			->addField(
				(new CWidgetFieldRadioButtonList('show_mode', _tn('Display mode'), [
					0 => _tn('Host groups only'),
					1 => _tn('Host groups and hosts'),
				]))->setDefault(1)
			)
			->addField(
				new CWidgetFieldMultiSelectGroup('groupids', _tn('Host groups'))
			)
			->addField(
				(new CWidgetFieldCheckBox('recursive', _tn('Sub-groups'), _tn('Include sub-groups')))
					->setDefault(1)
			);
	}
}
