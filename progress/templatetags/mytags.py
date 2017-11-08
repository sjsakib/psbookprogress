from django import template

register = template.Library()


@register.inclusion_tag('progress/show_users.html')
def show_users(users, user):
    return {'users': users, 'user': user}
