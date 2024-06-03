from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User

admin.site.register(User) #adiciona a classe User ao admin do django

admin.site.register(Room) #adiciona a classe Room ao admin do django
admin.site.register(Topic) #adiciona a classe Topic ao admin do django
admin.site.register(Message) #adiciona a classe Message ao admin do django