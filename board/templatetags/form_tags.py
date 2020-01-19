from django import template

register = template.Library()


@register.filter
def field_type(f):
    return f.field.widget.__class__.__name__


@register.filter
def input_class(f):
    css_class = ''
    if f.form.is_bound:
        if f.errors:
            css_class = 'is-invalid'
        elif field_type(f) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)