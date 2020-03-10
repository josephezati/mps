from django import template
from hm.models import*
register = template.Library()

@register.simple_tag
def get_class(pk, attr):
    obj = getattr(Classe.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def get_stream(pk, attr):
    obj = getattr(Stream.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def get_term(pk, attr):
    obj = getattr(Term.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def get_child(pk, attr):
    obj = getattr(Student.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def get_current_class(pk, attr):
    obj = getattr(ClassInformation.objects.get(pk=int(pk)), attr)
    return obj