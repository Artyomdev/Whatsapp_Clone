from django import template

register = template.Library()
def modify_name(value , arg2):
    x = value.messages.all().exclude(user = arg2).filter(okundu = False).count()
    return x
register.filter('get', modify_name)