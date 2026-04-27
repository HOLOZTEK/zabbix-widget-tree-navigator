<?php declare(strict_types = 0);

/**
 * Tree Navigator widget edit form view.
 *
 * @var CView  $this
 * @var array  $data
 */

(new CWidgetFormView($data))
	->addField(
		new CWidgetFieldTextBoxView($data['fields']['root_name'])
	)
	->addField(
		new CWidgetFieldRadioButtonListView($data['fields']['show_mode'])
	)
	->addField(
		new CWidgetFieldMultiSelectGroupView($data['fields']['groupids'])
	)
	->addField(
		new CWidgetFieldCheckBoxView($data['fields']['recursive'])
	)
	->show();
