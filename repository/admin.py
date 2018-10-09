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
admin.site.register(models.IDC)
admin.site.register(models.Host)
admin.site.register(models.RemoteUser)
admin.site.register(models.HostToRemoteUser)
admin.site.register(models.Task)
admin.site.register(models.TaskLogDetail)
admin.site.register(models.AppVersion)
admin.site.register(models.AppModuleList)
admin.site.register(models.AppToHostToRemoteUser)