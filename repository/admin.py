from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Role)
admin.site.register(models.Permission)
admin.site.register(models.Permission2Role)
admin.site.register(models.User)
admin.site.register(models.User2Role)
admin.site.register(models.Menu)
admin.site.register(models.Projects)
admin.site.register(models.Envlists)
admin.site.register(models.Workorders)