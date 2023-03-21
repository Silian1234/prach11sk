from django import template

register = template.Library()


@register.filter
def has_group(groups, group):
    return groups.filter(name=group)
