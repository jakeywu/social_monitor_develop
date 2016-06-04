# __author__ = 'jakey'

from django.contrib import admin
from news.models import CrawlerNews, MonitorNews, ReleaseNews
from schedule.models import MonitorKeys
from import_export.admin import ImportExportActionModelAdmin


@admin.register(MonitorNews)
class MonitorNewsAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 50
    search_fields = ("news_title", "news_source")
    fields = ("news_title", "news_url", "news_source", "news_abstract", "news_content", "monitorkeys", "news_positive")
    list_display = ["news_title", "news_source", "news_time", "monitorkeys", "news_positive", "id"]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            self.list_filter = ("news_time", "news_positive", "monitorkeys__group", )
        else:
            self.list_filter = ("news_time", "news_positive", )
        return super(MonitorNewsAdmin, self).get_list_filter(request)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "monitorkeys" and not request.user.is_superuser:
            kwargs["queryset"] = MonitorKeys.objects.filter(group__in=request.user.groups.all())
        return super(MonitorNewsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(MonitorNewsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(monitorkeys__group__in=request.user.groups.all())


@admin.register(CrawlerNews)
class CrawlerNewsAdmin(admin.ModelAdmin):
    fields = ("news_title", "news_url", "news_source", "news_abstract", "news_content", "monitorkeys", "group", "news_time")
    list_display = ["news_title", "news_source", "news_time", "monitorkeys", "id", "group"]
    search_fields = ("news_title", "news_source")
    ordering = ["id"]
    list_per_page = 50

    def get_list_filter(self, request):
        if request.user.is_superuser:
            self.list_filter = ("news_time", "monitorkeys__group", )
        else:
            self.list_filter = ("news_time", )
        qs = super(CrawlerNewsAdmin, self).get_list_filter(request)
        return qs

    def get_queryset(self, request):
        qs = super(CrawlerNewsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group__in=request.user.groups.all())


@admin.register(ReleaseNews)
class ReleaseNewsAdmin(ImportExportActionModelAdmin):
    fields = ("release_title", "release_path", "release_type", "release_media", )
    list_display = ["release_title", "release_path", "release_type", "release_media", ]
    ordering = ["id"]
    list_per_page = 50
