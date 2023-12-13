from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Response)
admin.site.register(models.Blog)
admin.site.register(models.BlogResponse)
admin.site.register(models.Poll)
admin.site.register(models.Choice)