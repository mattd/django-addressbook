from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.tag
def render_formset_template_for(parser, token):
    """
    Renders a template matching the app_name.module_name of the given formset 
    in the given template directory, falling back to default.html.
    
    If called as ``{% render_formset_template_for story_formset in "includes/formsets" %}``
    it would first look for includes/formsets/news.stories.html and then
    for includes/formsets/default.html
    
    This is particularly useful when dealing with a group of formsets of unknown type as 
    it keeps nasty nested {% if %} blocks out and allows you to customize where desired.
    
    The formset passed to the tag will be available in the rendered template 
    as ``formset``. The current context is also made available.
    """
    try:
        tag_name, formset, in_var, template_dir = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments '[formset] in [template_dir]'" % token.contents.split()[0]
    if not (in_var == 'in'):
        raise template.TemplateSyntaxError, "%s tag's second argument must be the keyword 'in'" % tag_name
    if not (template_dir[0] == template_dir[-1] and template_dir[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%s tag's final argument should be in quotes" % tag_name
    return RenderFormsetTemplateForNode(formset, template_dir[1:-1])
    
class RenderFormsetTemplateForNode(template.Node):
    def __init__(self, formset, template_dir):
        self.formset = template.Variable(formset)
        # Normalize template_dirs that end in /
        if template_dir[-1] == "/":
            self.template_dir = template_dir[:-1]
        else:
            self.template_dir = template_dir

    def render(self, context):
        try:
            formset = self.formset.resolve(context)
            ctype_str = "%s.%s" % (formset.model._meta.app_label, 
                                   formset.model._meta.module_name)
            context.push()
            context['formset'] = formset 
            return render_to_string(["%s/%s.html" % (self.template_dir, ctype_str), 
                                     "%s/default.html" % self.template_dir],
                                     context)
        except template.VariableDoesNotExist:
            return ''
