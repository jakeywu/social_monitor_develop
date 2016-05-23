# __author__ = 'jakey'

from django.contrib import admin
from django.contrib.auth.models import User
from schedule.models import SchedulePlan, MonitorKeys


@admin.register(MonitorKeys)
class MonitorKeyAdmin(admin.ModelAdmin):
    fields = ("keys_name", "author", "group")
    list_display = ["keys_name", "timestamp", "author", "group", "id"]
    search_fields = ("keys_name", )
    list_per_page = 50

    def get_list_filter(self, request):
        if request.user.is_superuser:
            self.list_filter = ("timestamp", "group",)
        else:
            self.list_filter = ("timestamp", )
        qs = super(MonitorKeyAdmin, self).get_list_filter(request)
        return qs

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "author" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(pk=request.user.pk)
            kwargs["initial"] = request.user

        if db_field.name == "group" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.groups.all()
            kwargs["initial"] = request.user.groups.all()[0]

        return super(MonitorKeyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(MonitorKeyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group__in=request.user.groups.all())

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


@admin.register(SchedulePlan)
class SchedulePlanAdmin(admin.ModelAdmin):
    fields = ("push_interval_time", "group")
    list_display = ["push_interval_time", "group", "id"]
    search_fields = ("group", )
    ordering = ("id", )
    list_per_page = 50

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "group" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.groups.all()
            kwargs["initial"] = request.user.groups.all()[0]

        return super(SchedulePlanAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(SchedulePlanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group__in=request.user.groups.all())
