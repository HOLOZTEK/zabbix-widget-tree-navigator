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
		new CWidgetFieldIntegerBoxView($data['fields']['initial_depth'])
	)
	->addField(
		new CWidgetFieldCheckBoxView($data['fields']['recursive'])
	)
	->addField(
		new CWidgetFieldCheckBoxView($data['fields']['show_host_count'])
	)
	->show();
