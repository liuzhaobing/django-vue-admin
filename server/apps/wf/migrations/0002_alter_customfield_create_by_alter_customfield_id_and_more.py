# Generated by Django 4.2.8 on 2024-05-20 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0004_alter_historicaldict_options_alter_dict_id_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wf", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customfield",
            name="create_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_create_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
        migrations.AlterField(
            model_name="customfield",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="customfield",
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
        migrations.AlterField(
            model_name="state",
            name="create_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_create_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
        migrations.AlterField(
            model_name="state",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="state",
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
        migrations.AlterField(
            model_name="ticket",
            name="belong_dept",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_belong_dept",
                to="system.organization",
                verbose_name="所属部门",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="create_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_create_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
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
        migrations.AlterField(
            model_name="ticketflow",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="transition",
            name="create_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_create_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
        migrations.AlterField(
            model_name="transition",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="transition",
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
        migrations.AlterField(
            model_name="workflow",
            name="create_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_create_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
        migrations.AlterField(
            model_name="workflow",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="workflow",
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
