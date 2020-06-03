from django.apps import apps
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.models import User

from HallOfFame.permissions import is_admin


class DefaultAdminSite(AdminSite):
    site_header = "DefaultAdminSite"
    site_title = "DefaultAdminSite Portal"
    index_title = "Welcome to DefaultAdminSite Portal"

    def has_permission(self, request):
        flag = False
        if not request.user.is_anonymous:
            flag = is_admin(request.user)
            flag = flag or request.user.is_superuser
        return super().has_permission(request) and flag


default_admin_site = DefaultAdminSite(name='admin')

models = apps.get_app_config('hallOfFameClient').get_models()

default_admin_site.register(User)

for model in models:
    try:
        default_admin_site.register(model)
    except AlreadyRegistered:
        pass

