from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dict(dictionary).get(key)


@register.filter
def get_enroll_user(event):
    users = []
    for enroll in event.enrolls.all():
        users.append(enroll.user)
    return users


@register.filter
def get_favorite_user(event):
    users = []
    for favorite in event.favorites.all():
        users.append(favorite.user)
    return users
