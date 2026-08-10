<?php declare(strict_types = 0);

namespace Modules\HoloztekTreeNavigator\Includes;

use Zabbix\Widgets\CWidgetForm;
use Zabbix\Widgets\Fields\{
	CWidgetFieldCheckBox,
	CWidgetFieldColor,
	CWidgetFieldIntegerBox,
	CWidgetFieldMultiSelectGroup,
	CWidgetFieldRadioButtonList,
	CWidgetFieldTextBox
};

class WidgetForm extends CWidgetForm {

	public function addFields(): self {
		return $this
			->addField(
				(new CWidgetFieldTextBox('root_name', _holoztek_tn('Root name')))
					->setMaxLength(255)
			)
			->addField(
				(new CWidgetFieldRadioButtonList('show_mode', _holoztek_tn('Display mode'), [
					0 => _holoztek_tn('Host groups only'),
					1 => _holoztek_tn('Host groups and hosts'),
				]))->setDefault(1)
			)
			->addField(
				new CWidgetFieldMultiSelectGroup('groupids', _holoztek_tn('Host groups'))
			)
			->addField(
				(new CWidgetFieldIntegerBox('initial_depth', _holoztek_tn('Initial depth'), 0, 10))
					->setDefault(1)
			)
			->addField(
				(new CWidgetFieldCheckBox('recursive', _holoztek_tn('Sub-groups'), _holoztek_tn('Include sub-groups')))
					->setDefault(1)
			)
			->addField(
				(new CWidgetFieldCheckBox('show_host_count', _holoztek_tn('Host count'), _holoztek_tn('Show host count in tooltip')))
					->setDefault(1)
			)
			->addField(
				(new CWidgetFieldColor('folder_font_color', _holoztek_tn('Folder text color')))
					->setDefault('333333')
			)
			->addField(
				(new CWidgetFieldColor('host_font_color', _holoztek_tn('Host text color')))
					->setDefault('444444')
			);
	}
}
