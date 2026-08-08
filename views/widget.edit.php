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
		(new CWidgetFieldIntegerBoxView($data['fields']['initial_depth']))
			->setFieldHint(makeHelpIcon(_tn('Initial tree depth when no saved expansion state exists.')))
	)
	->addField(
		new CWidgetFieldCheckBoxView($data['fields']['recursive'])
	)
	->addField(
		new CWidgetFieldCheckBoxView($data['fields']['show_host_count'])
	)
	->addField(
		new CWidgetFieldColorView($data['fields']['folder_font_color'])
	)
	->addField(
		new CWidgetFieldColorView($data['fields']['host_font_color'])
	)
	->includeJsFile('widget.edit.js.php')
	->addJavaScript('widget_tree_navigator_form.init();')
	->show();
