# Generated by Django 4.2 on 2024-08-21 23:35

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wcoa.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wcoa', '0042_alter_ohiindicatorpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ohidashboard',
            name='body',
            field=wagtail.fields.StreamField([('Clear', wcoa.blocks.CTARowDivider()), ('Column', wagtail.blocks.StructBlock([('width', wagtail.blocks.ChoiceBlock(choices=[('1', '1/12'), ('2', '2/12'), ('3', '3/12'), ('4', '4/12'), ('5', '5/12'), ('6', '6/12'), ('7', '7/12'), ('8', '8/12'), ('9', '9/12'), ('10', '10/12'), ('11', '11/12'), ('12', '12/12')], icon='arrow-right', label='Width', required=False)), ('content', wagtail.blocks.StreamBlock([('Score', wagtail.blocks.StructBlock([('state', wagtail.blocks.ChoiceBlock(choices=[('West Coast', 'West Coast'), ('CA', 'California'), ('OR', 'Oregon'), ('WA', 'Washington')])), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('year', wagtail.blocks.IntegerBlock(help_text='Year of the report', required=False)), ('report', wagtail.blocks.URLBlock(help_text='URL to the report', required=False))])), ('WYSIWYG', wagtail.blocks.RichTextBlock(required=False)), ('Chart', wagtail.blocks.StreamBlock([('chart_block', wagtail.blocks.StructBlock([('chart_type', wagtail.blocks.ChoiceBlock(choices=[('line', 'Line Chart'), ('bar', 'Vertical Bar Chart'), ('bar_horizontal', 'Horizontal Bar Chart'), ('area', 'Area Chart'), ('multi', 'Combo Line/Bar/Area Chart'), ('pie', 'Pie Chart'), ('doughnut', 'Doughnut Chart'), ('radar', 'Radar Chart'), ('polar', 'Polar Chart'), ('waterfall', 'Waterfall Chart')], label='Chart Type')), ('title', wagtail.blocks.CharBlock(required=False)), ('datasets', wagtail.blocks.TextBlock(default='{"data":[], "options":{}}')), ('settings', wagtail.blocks.StructBlock([('show_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show legend', required=False)), ('html_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Use HTML legend', required=False)), ('legend_position', wagtail.blocks.ChoiceBlock(choices=[('top', 'Top'), ('bottom', 'Bottom'), ('left', 'Left'), ('right', 'Right')], group='General', label='Legend position')), ('reverse_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Reverse legend', required=False)), ('show_values_on_chart', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show values on chart', required=False)), ('precision', wagtail.blocks.IntegerBlock(default=1, group='General', label='Precision in labels/tooltips')), ('show_grid', wagtail.blocks.BooleanBlock(default=True, group='General', label='Show Chart Grid', required=False)), ('x_label', wagtail.blocks.CharBlock(group='General', label='X axis label', required=False)), ('stacking', wagtail.blocks.ChoiceBlock(choices=[('none', 'No stacking'), ('stacked', 'Stacked'), ('stacked_100', 'Stacked 100%')], group='General', label='Stacking')), ('unit_override', wagtail.blocks.CharBlock(group='General', label='Unit override', required=False)), ('y_left_min', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis minimum value', required=False)), ('y_left_max', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis maximum value', required=False)), ('y_left_step_size', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis step size', required=False)), ('y_left_label', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis label', required=False)), ('y_left_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Left_Axis', label='Left Y axis data type', required=False)), ('y_left_precision', wagtail.blocks.IntegerBlock(default=0, group='Left_Axis', label='Left Y axis tick precision')), ('y_left_show', wagtail.blocks.BooleanBlock(default=True, group='Left_Axis', label='Show left axis numbers', required=False)), ('y_right_min', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis minimum value', required=False)), ('y_right_max', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis maximum value', required=False)), ('y_right_step_size', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis step size', required=False)), ('y_right_label', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis label', required=False)), ('y_right_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Right_Axis', label='Right Y axis data type', required=False)), ('y_right_precision', wagtail.blocks.IntegerBlock(default=0, group='Right_Axis', label='Right Y axis tick precision')), ('y_right_show', wagtail.blocks.BooleanBlock(default=True, group='Right_Axis', label='Show right axis numbers', required=False)), ('pie_border_width', wagtail.blocks.IntegerBlock(default=2, group='Pie_Chart', label='Width of pie slice border')), ('pie_border_color', wagtail.blocks.CharBlock(default='#fff', group='Pie_Chart', label='Color of pie slice border'))]))], colors=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')]))])), ('Accordion', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('items', wagtail.blocks.StreamBlock([('item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(required=False))]))]))]))], required=False)), ('full_image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('cover_image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('text_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')], icon='color_palette', required=False)), ('background_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 0.5)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 0.5)', 'Blue'), ('rgba(152, 171, 55, 0.5)', 'Green'), ('rgba(242, 191, 76, 0.5)', 'Yellow'), ('rgba(250, 35, 18, 0.5)', 'Red'), ('rgba(77, 77, 79, 0.5)', 'Grey')], icon='color', required=False)), ('border_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')], icon='color_palette', required=False)), ('border_width', wagtail.blocks.IntegerBlock(default='', help_text='Width of the border in pixels', max_value=10, min_value=0, required=False)), ('link', wagtail.blocks.URLBlock(help_text='Wrap column in a link', required=False))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='ohidashboard',
            name='body_below_framework',
            field=wagtail.fields.StreamField([('Clear', wcoa.blocks.CTARowDivider()), ('Column', wagtail.blocks.StructBlock([('width', wagtail.blocks.ChoiceBlock(choices=[('1', '1/12'), ('2', '2/12'), ('3', '3/12'), ('4', '4/12'), ('5', '5/12'), ('6', '6/12'), ('7', '7/12'), ('8', '8/12'), ('9', '9/12'), ('10', '10/12'), ('11', '11/12'), ('12', '12/12')], icon='arrow-right', label='Width', required=False)), ('content', wagtail.blocks.StreamBlock([('Score', wagtail.blocks.StructBlock([('state', wagtail.blocks.ChoiceBlock(choices=[('West Coast', 'West Coast'), ('CA', 'California'), ('OR', 'Oregon'), ('WA', 'Washington')])), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('year', wagtail.blocks.IntegerBlock(help_text='Year of the report', required=False)), ('report', wagtail.blocks.URLBlock(help_text='URL to the report', required=False))])), ('WYSIWYG', wagtail.blocks.RichTextBlock(required=False)), ('Chart', wagtail.blocks.StreamBlock([('chart_block', wagtail.blocks.StructBlock([('chart_type', wagtail.blocks.ChoiceBlock(choices=[('line', 'Line Chart'), ('bar', 'Vertical Bar Chart'), ('bar_horizontal', 'Horizontal Bar Chart'), ('area', 'Area Chart'), ('multi', 'Combo Line/Bar/Area Chart'), ('pie', 'Pie Chart'), ('doughnut', 'Doughnut Chart'), ('radar', 'Radar Chart'), ('polar', 'Polar Chart'), ('waterfall', 'Waterfall Chart')], label='Chart Type')), ('title', wagtail.blocks.CharBlock(required=False)), ('datasets', wagtail.blocks.TextBlock(default='{"data":[], "options":{}}')), ('settings', wagtail.blocks.StructBlock([('show_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show legend', required=False)), ('html_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Use HTML legend', required=False)), ('legend_position', wagtail.blocks.ChoiceBlock(choices=[('top', 'Top'), ('bottom', 'Bottom'), ('left', 'Left'), ('right', 'Right')], group='General', label='Legend position')), ('reverse_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Reverse legend', required=False)), ('show_values_on_chart', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show values on chart', required=False)), ('precision', wagtail.blocks.IntegerBlock(default=1, group='General', label='Precision in labels/tooltips')), ('show_grid', wagtail.blocks.BooleanBlock(default=True, group='General', label='Show Chart Grid', required=False)), ('x_label', wagtail.blocks.CharBlock(group='General', label='X axis label', required=False)), ('stacking', wagtail.blocks.ChoiceBlock(choices=[('none', 'No stacking'), ('stacked', 'Stacked'), ('stacked_100', 'Stacked 100%')], group='General', label='Stacking')), ('unit_override', wagtail.blocks.CharBlock(group='General', label='Unit override', required=False)), ('y_left_min', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis minimum value', required=False)), ('y_left_max', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis maximum value', required=False)), ('y_left_step_size', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis step size', required=False)), ('y_left_label', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis label', required=False)), ('y_left_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Left_Axis', label='Left Y axis data type', required=False)), ('y_left_precision', wagtail.blocks.IntegerBlock(default=0, group='Left_Axis', label='Left Y axis tick precision')), ('y_left_show', wagtail.blocks.BooleanBlock(default=True, group='Left_Axis', label='Show left axis numbers', required=False)), ('y_right_min', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis minimum value', required=False)), ('y_right_max', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis maximum value', required=False)), ('y_right_step_size', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis step size', required=False)), ('y_right_label', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis label', required=False)), ('y_right_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Right_Axis', label='Right Y axis data type', required=False)), ('y_right_precision', wagtail.blocks.IntegerBlock(default=0, group='Right_Axis', label='Right Y axis tick precision')), ('y_right_show', wagtail.blocks.BooleanBlock(default=True, group='Right_Axis', label='Show right axis numbers', required=False)), ('pie_border_width', wagtail.blocks.IntegerBlock(default=2, group='Pie_Chart', label='Width of pie slice border')), ('pie_border_color', wagtail.blocks.CharBlock(default='#fff', group='Pie_Chart', label='Color of pie slice border'))]))], colors=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')]))])), ('Accordion', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('items', wagtail.blocks.StreamBlock([('item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(required=False))]))]))]))], required=False)), ('full_image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('cover_image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('text_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')], icon='color_palette', required=False)), ('background_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 0.5)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 0.5)', 'Blue'), ('rgba(152, 171, 55, 0.5)', 'Green'), ('rgba(242, 191, 76, 0.5)', 'Yellow'), ('rgba(250, 35, 18, 0.5)', 'Red'), ('rgba(77, 77, 79, 0.5)', 'Grey')], icon='color', required=False)), ('border_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')], icon='color_palette', required=False)), ('border_width', wagtail.blocks.IntegerBlock(default='', help_text='Width of the border in pixels', max_value=10, min_value=0, required=False)), ('link', wagtail.blocks.URLBlock(help_text='Wrap column in a link', required=False))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='ohiindicatorpage',
            name='body',
            field=wagtail.fields.StreamField([('Clear', wcoa.blocks.CTARowDivider()), ('Column', wagtail.blocks.StructBlock([('width', wagtail.blocks.ChoiceBlock(choices=[('1', '1/12'), ('2', '2/12'), ('3', '3/12'), ('4', '4/12'), ('5', '5/12'), ('6', '6/12'), ('7', '7/12'), ('8', '8/12'), ('9', '9/12'), ('10', '10/12'), ('11', '11/12'), ('12', '12/12')], icon='arrow-right', label='Width', required=False)), ('content', wagtail.blocks.StreamBlock([('Score', wagtail.blocks.StructBlock([('state', wagtail.blocks.ChoiceBlock(choices=[('West Coast', 'West Coast'), ('CA', 'California'), ('OR', 'Oregon'), ('WA', 'Washington')])), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('year', wagtail.blocks.IntegerBlock(help_text='Year of the report', required=False)), ('report', wagtail.blocks.URLBlock(help_text='URL to the report', required=False))])), ('WYSIWYG', wagtail.blocks.RichTextBlock(required=False)), ('Chart', wagtail.blocks.StreamBlock([('chart_block', wagtail.blocks.StructBlock([('chart_type', wagtail.blocks.ChoiceBlock(choices=[('line', 'Line Chart'), ('bar', 'Vertical Bar Chart'), ('bar_horizontal', 'Horizontal Bar Chart'), ('area', 'Area Chart'), ('multi', 'Combo Line/Bar/Area Chart'), ('pie', 'Pie Chart'), ('doughnut', 'Doughnut Chart'), ('radar', 'Radar Chart'), ('polar', 'Polar Chart'), ('waterfall', 'Waterfall Chart')], label='Chart Type')), ('title', wagtail.blocks.CharBlock(required=False)), ('datasets', wagtail.blocks.TextBlock(default='{"data":[], "options":{}}')), ('settings', wagtail.blocks.StructBlock([('show_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show legend', required=False)), ('html_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Use HTML legend', required=False)), ('legend_position', wagtail.blocks.ChoiceBlock(choices=[('top', 'Top'), ('bottom', 'Bottom'), ('left', 'Left'), ('right', 'Right')], group='General', label='Legend position')), ('reverse_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Reverse legend', required=False)), ('show_values_on_chart', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show values on chart', required=False)), ('precision', wagtail.blocks.IntegerBlock(default=1, group='General', label='Precision in labels/tooltips')), ('show_grid', wagtail.blocks.BooleanBlock(default=True, group='General', label='Show Chart Grid', required=False)), ('x_label', wagtail.blocks.CharBlock(group='General', label='X axis label', required=False)), ('stacking', wagtail.blocks.ChoiceBlock(choices=[('none', 'No stacking'), ('stacked', 'Stacked'), ('stacked_100', 'Stacked 100%')], group='General', label='Stacking')), ('unit_override', wagtail.blocks.CharBlock(group='General', label='Unit override', required=False)), ('y_left_min', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis minimum value', required=False)), ('y_left_max', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis maximum value', required=False)), ('y_left_step_size', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis step size', required=False)), ('y_left_label', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis label', required=False)), ('y_left_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Left_Axis', label='Left Y axis data type', required=False)), ('y_left_precision', wagtail.blocks.IntegerBlock(default=0, group='Left_Axis', label='Left Y axis tick precision')), ('y_left_show', wagtail.blocks.BooleanBlock(default=True, group='Left_Axis', label='Show left axis numbers', required=False)), ('y_right_min', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis minimum value', required=False)), ('y_right_max', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis maximum value', required=False)), ('y_right_step_size', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis step size', required=False)), ('y_right_label', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis label', required=False)), ('y_right_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Right_Axis', label='Right Y axis data type', required=False)), ('y_right_precision', wagtail.blocks.IntegerBlock(default=0, group='Right_Axis', label='Right Y axis tick precision')), ('y_right_show', wagtail.blocks.BooleanBlock(default=True, group='Right_Axis', label='Show right axis numbers', required=False)), ('pie_border_width', wagtail.blocks.IntegerBlock(default=2, group='Pie_Chart', label='Width of pie slice border')), ('pie_border_color', wagtail.blocks.CharBlock(default='#fff', group='Pie_Chart', label='Color of pie slice border'))]))], colors=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')]))])), ('Accordion', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('items', wagtail.blocks.StreamBlock([('item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('content', wagtail.blocks.RichTextBlock(required=False))]))]))]))], required=False)), ('full_image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('cover_image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('text_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')], icon='color_palette', required=False)), ('background_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 0.5)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 0.5)', 'Blue'), ('rgba(152, 171, 55, 0.5)', 'Green'), ('rgba(242, 191, 76, 0.5)', 'Yellow'), ('rgba(250, 35, 18, 0.5)', 'Red'), ('rgba(77, 77, 79, 0.5)', 'Grey')], icon='color', required=False)), ('border_color', wagtail.blocks.ChoiceBlock(choices=[('rgba(255, 255, 255, 1)', 'White'), ('rgba(0, 0, 0, 1)', 'Black'), ('rgba(46, 46, 47, 1)', 'Black (Light)'), ('rgba(48, 112, 247, 1)', 'Blue'), ('rgba(152, 171, 55, 1)', 'Green'), ('rgba(242,191,76,1)', 'Yellow'), ('rgba(250, 35, 18, 1)', 'Red'), ('rgba(77,77,79,1)', 'Grey')], icon='color_palette', required=False)), ('border_width', wagtail.blocks.IntegerBlock(default='', help_text='Width of the border in pixels', max_value=10, min_value=0, required=False)), ('link', wagtail.blocks.URLBlock(help_text='Wrap column in a link', required=False))]))]),
        ),
    ]
