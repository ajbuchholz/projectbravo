from django import template

register = template.Library()


@register.simple_tag
def status_icon(value):
    if value == "success":
        return "check-circle"
    elif value == "warning":
        return "exclamation-circle"
    elif value == "error":
        return "minus-circle"
    elif value == "info":
        return "info-circle"
    else:
        return "dot-circle"


@register.simple_tag
def status_title(value):
    if value == "success":
        return "Success"
    elif value == "warning":
        return "Warning"
    elif value == "error":
        return "Error"
    elif value == "info":
        return "Information"
    else:
        return "Alert"
    
@register.simple_tag
def status_color(value):
    if value == "success":
        return "success"
    elif value == "warning":
        return "warning"
    elif value == "error":
        return "danger"
    elif value == "info":
        return "info"
    else:
        return "secondary"
