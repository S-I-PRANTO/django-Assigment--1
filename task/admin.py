from django.contrib import admin
from task.models import Event,Category
admin.site.register(Event)
admin.site.register(Category)
# admin.site.register(Participant)