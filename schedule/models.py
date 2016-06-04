# __author__ = 'jakey'

from django.db import models
from django.contrib.auth.models import User, Group


class MonitorKeys(models.Model):
    author = models.ForeignKey(User, verbose_name="操作人员", on_delete=models.CASCADE, default=1)
    group = models.ForeignKey(Group, verbose_name="用户组", on_delete=models.CASCADE, default=1)
    keys_name = models.CharField(verbose_name="关键词名称", max_length=50)
    timestamp = models.DateTimeField(verbose_name="开始监控时间", auto_now_add=True)

    def __str__(self):
        return self.keys_name

    class Meta:
        db_table = "monitor_key"
        verbose_name = "关键词"
        verbose_name_plural = "关键词"
        get_latest_by = "timestamp"


class SchedulePlan(models.Model):
    push_interval_time = models.PositiveSmallIntegerField(verbose_name="调用间隔小时")
    group = models.ForeignKey(Group, verbose_name="用户组", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.push_interval_time)

    class Meta:
        db_table = "schedule_plan"
        verbose_name = "调度计划"
        verbose_name_plural = "调度计划"
