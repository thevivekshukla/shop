from django.contrib import admin
from django.contrib.auth.admin import Group

from .models import Item, Rating, Buy, UserItemRelation

from rest_framework.authtoken.models import Token
# Register your models here.

admin.site.register(Item)
admin.site.register(Rating)
admin.site.register(Buy)
admin.site.register(UserItemRelation)


admin.site.unregister(Token)
admin.site.unregister(Group)
