from django.template import Library
from django.utils.html import format_html_join, format_html, mark_safe
from django.utils.encoding import smart_bytes 
from django.utils.html import linebreaks

register = Library()


@register.filter
def replace(value):
    #value = value.decode("utf-8")
    #value = value.split('\n')
    #value = [[v] for v in value if v != ""]
    #value = format_html_join('\n', '<p>{}</p>', value)
    return linebreaks(value)#smart_bytes(value)
