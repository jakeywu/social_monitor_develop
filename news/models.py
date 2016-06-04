# __author__ = 'jakey'

import os
import time
from uuid import uuid4
from django.db import models
from django.utils.timezone import now
from schedule.models import MonitorKeys
from django.contrib.auth.models import Group

Release_News_CHOICES = (
    (1, '正面新闻'),
    (2, '负面新闻'),
    (3, '待定新闻')
)

MEDIA_CHOICES = (
    ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
    ),
    ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
    ),
    ('unknown', 'Unknown'),
)


class CrawlerNews(models.Model):
    news_title = models.CharField(verbose_name="新闻标题", max_length=200, db_index=True)
    news_time = models.DateTimeField(verbose_name="新闻时间", default=now)
    news_source = models.CharField(verbose_name="新闻来源", max_length=50, blank=True)
    news_abstract = models.CharField(verbose_name="新闻摘要", max_length=500, blank=True)
    news_url = models.URLField(verbose_name="新闻链接", null=True, blank=True)
    news_content = models.TextField(verbose_name="新闻内容")
    monitorkeys = models.ForeignKey(MonitorKeys, verbose_name="监控关键词", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name="用户组", on_delete=models.CASCADE, default=1)
    create_time = models.DateTimeField(verbose_name="新闻创建时间", auto_now_add=True)

    def __str__(self):
        return self.news_title

    class Meta:
        db_table = "crawler_news"
        verbose_name = "爬虫数据"
        verbose_name_plural = "爬虫数据"


class MonitorNews(models.Model):
    news_title = models.CharField(verbose_name="新闻标题", max_length=200, db_index=True)
    news_url = models.URLField(verbose_name="新闻链接", null=True, blank=True)
    news_time = models.DateTimeField(verbose_name="新闻时间", auto_now_add=True)
    news_source = models.CharField(verbose_name="新闻来源", max_length=50, blank=True)
    news_content = models.TextField(verbose_name="新闻内容")
    news_positive = models.BooleanField(verbose_name="正面新闻")
    news_abstract = models.CharField(verbose_name="新闻摘要", max_length=500, blank=True)
    monitorkeys = models.ForeignKey(MonitorKeys, verbose_name="监控关键词", on_delete=models.CASCADE)

    def __str__(self):
        return self.news_title

    class Meta:
        db_table = "monitor_news"
        verbose_name = "新闻"
        verbose_name_plural = "新闻"


def get_uploads_path(instance, filename):
    cur_date = time.strftime("%Y-%m-%d").split("-")
    base_path = "pic/{0}/{1}/{2}".format(cur_date[0], cur_date[1], cur_date[2])
    extention = filename.split(".")[-1]
    if instance.pk:
        filename = '{0}.{1}'.format(instance.pk, extention)
    else:
        filename = '{0}.{1}'.format(uuid4().hex, extention)
    return os.path.join(base_path, filename)


class ReleaseNews(models.Model):
    release_title = models.CharField(verbose_name="新闻标题", max_length=200, db_index=True)
    release_path = models.ImageField(verbose_name="新闻图片", upload_to=get_uploads_path)
    release_type = models.PositiveSmallIntegerField(verbose_name="新闻类型", choices=Release_News_CHOICES, default=1)
    release_media = models.CharField(verbose_name="新闻介质", choices=MEDIA_CHOICES, max_length=10, default='Audio')

    def __str__(self):
        return self.release_title

    class Meta:
        db_table = "release_news"
        verbose_name = "新闻(完整版)"
        verbose_name_plural = "新闻(完整版)"
