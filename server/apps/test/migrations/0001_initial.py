# Generated by Django 4.2.8 on 2024-05-20 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("system", "0004_alter_historicaldict_options_alter_dict_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="名称"),
                ),
                (
                    "create_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_create_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建人",
                    ),
                ),
                (
                    "update_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_update_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="最后编辑人",
                    ),
                ),
            ],
            options={
                "verbose_name": "分组",
                "verbose_name_plural": "分组",
            },
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="名称"),
                ),
            ],
            options={
                "verbose_name": "执行日志",
                "verbose_name_plural": "执行日志",
            },
        ),
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="名称"),
                ),
                ("config", models.TextField(verbose_name="计划参数配置")),
                ("data_source", models.TextField(verbose_name="数据源")),
                (
                    "belong_dept",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_belong_dept",
                        to="system.organization",
                        verbose_name="所属部门",
                    ),
                ),
                (
                    "create_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_create_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建人",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test.group",
                        verbose_name="分组",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试计划",
                "verbose_name_plural": "测试计划",
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="状态名称")),
                (
                    "create_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_create_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建人",
                    ),
                ),
                (
                    "update_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_update_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="最后编辑人",
                    ),
                ),
            ],
            options={
                "verbose_name": "状态",
                "verbose_name_plural": "状态",
            },
        ),
        migrations.CreateModel(
            name="Type",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="类型名称"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="类型描述"),
                ),
                (
                    "create_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_create_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建人",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test.status",
                        verbose_name="类型状态",
                    ),
                ),
                (
                    "update_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_update_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="最后编辑人",
                    ),
                ),
            ],
            options={
                "verbose_name": "任务类型",
                "verbose_name_plural": "任务类型",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="名称")),
                (
                    "job_instance_id",
                    models.CharField(max_length=128, unique=True, verbose_name="任务ID"),
                ),
                (
                    "progress",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="执行进度"
                    ),
                ),
                (
                    "progress_percent",
                    models.IntegerField(default=0, verbose_name="进度百分比"),
                ),
                (
                    "metrics",
                    models.TextField(blank=True, null=True, verbose_name="评测指标"),
                ),
                (
                    "message",
                    models.TextField(blank=True, null=True, verbose_name="任务消息"),
                ),
                (
                    "case_file",
                    models.CharField(
                        blank=True, max_length=512, null=True, verbose_name="测试用例文件"
                    ),
                ),
                (
                    "result_file",
                    models.CharField(
                        blank=True, max_length=512, null=True, verbose_name="测试结果文件"
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="开始时间",
                        verbose_name="开始时间",
                    ),
                ),
                (
                    "end_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="结束时间",
                        verbose_name="结束时间",
                    ),
                ),
                (
                    "belong_dept",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_belong_dept",
                        to="system.organization",
                        verbose_name="所属部门",
                    ),
                ),
                (
                    "create_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_create_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建人",
                    ),
                ),
                (
                    "plan_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test.plan",
                        verbose_name="计划ID",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test.status",
                        verbose_name="任务状态",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test.type",
                        verbose_name="任务类型",
                    ),
                ),
                (
                    "update_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_update_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="最后编辑人",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试任务",
                "verbose_name_plural": "测试任务",
            },
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="创建时间",
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, help_text="修改时间", verbose_name="修改时间"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="删除标记", verbose_name="删除标记"
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="报告名称")),
                (
                    "data",
                    models.TextField(blank=True, null=True, verbose_name="测试报告数据"),
                ),
                (
                    "task_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test.task",
                        verbose_name="任务ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "测试报告",
                "verbose_name_plural": "测试报告",
            },
        ),
        migrations.AddField(
            model_name="plan",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="test.type",
                verbose_name="计划类型",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="update_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_update_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="最后编辑人",
            ),
        ),
    ]
