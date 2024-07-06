from django import template

from main.models import Vacancy


register = template.Library()


@register.simple_tag()
def company_names():
    companies = set()
    for el in Vacancy.objects.all():
        companies.add(el.employer.replace(' ', '*'))
    return companies

@register.simple_tag()
def clear_name(name):
    return name.replace('*', ' ')
