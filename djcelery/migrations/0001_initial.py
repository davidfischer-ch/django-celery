# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import djcelery.picklefield


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrontabSchedule',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('minute', models.CharField(max_length=64, default='*', verbose_name='minute')),
                ('hour', models.CharField(max_length=64, default='*', verbose_name='hour')),
                ('day_of_week', models.CharField(max_length=64, default='*', verbose_name='day of week')),
                ('day_of_month', models.CharField(max_length=64, default='*', verbose_name='day of month')),
                ('month_of_year', models.CharField(max_length=64, default='*', verbose_name='month of year')),
            ],
            options={
                'ordering': ['month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute'],
                'verbose_name': 'crontab',
                'verbose_name_plural': 'crontabs',
            },
        ),
        migrations.CreateModel(
            name='IntervalSchedule',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('every', models.IntegerField(verbose_name='every')),
                ('period', models.CharField(choices=[('days', 'Days'), ('hours', 'Hours'), ('minutes', 'Minutes'), ('seconds', 'Seconds'), ('microseconds', 'Microseconds')], max_length=24, verbose_name='period')),
            ],
            options={
                'ordering': ['period', 'every'],
                'verbose_name': 'interval',
                'verbose_name_plural': 'intervals',
            },
        ),
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, help_text='Useful description', verbose_name='name', unique=True)),
                ('task', models.CharField(max_length=200, verbose_name='task name')),
                ('args', models.TextField(help_text='JSON encoded positional arguments', default='[]', blank=True, verbose_name='Arguments')),
                ('kwargs', models.TextField(help_text='JSON encoded keyword arguments', default='{}', blank=True, verbose_name='Keyword arguments')),
                ('queue', models.CharField(null=True, help_text='Queue defined in CELERY_QUEUES', blank=True, max_length=200, default=None, verbose_name='queue')),
                ('exchange', models.CharField(blank=True, max_length=200, default=None, null=True, verbose_name='exchange')),
                ('routing_key', models.CharField(blank=True, max_length=200, default=None, null=True, verbose_name='routing key')),
                ('expires', models.DateTimeField(null=True, blank=True, verbose_name='expires')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('last_run_at', models.DateTimeField(null=True, editable=False, blank=True)),
                ('total_run_count', models.PositiveIntegerField(default=0, editable=False)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('crontab', models.ForeignKey(null=True, help_text='Use one of interval/crontab', to='djcelery.CrontabSchedule', blank=True, verbose_name='crontab')),
                ('interval', models.ForeignKey(null=True, to='djcelery.IntervalSchedule', blank=True, verbose_name='interval')),
            ],
            options={
                'verbose_name': 'periodic task',
                'verbose_name_plural': 'periodic tasks',
            },
        ),
        migrations.CreateModel(
            name='PeriodicTasks',
            fields=[
                ('ident', models.SmallIntegerField(serialize=False, default=1, primary_key=True, unique=True)),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskMeta',
            fields=[
                ('task_id', models.UUIDField(serialize=False, primary_key=True, editable=False, max_length=32, default=uuid.uuid4, verbose_name='task id')),
                ('status', models.CharField(choices=[('FAILURE', 'FAILURE'), ('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('RETRY', 'RETRY'), ('REVOKED', 'REVOKED'), ('STARTED', 'STARTED'), ('SUCCESS', 'SUCCESS')], max_length=50, default='PENDING', verbose_name='state')),
                ('result', djcelery.picklefield.PickledObjectField(null=True, default=None, editable=False)),
                ('date_done', models.DateTimeField(auto_now=True, verbose_name='done at')),
                ('traceback', models.TextField(null=True, blank=True, verbose_name='traceback')),
                ('hidden', models.BooleanField(default=False, db_index=True, editable=False)),
                ('meta', djcelery.picklefield.PickledObjectField(null=True, default=None, editable=False)),
            ],
            options={
                'db_table': 'celery_taskmeta',
                'verbose_name': 'task state',
                'verbose_name_plural': 'task states',
            },
        ),
        migrations.CreateModel(
            name='TaskSetMeta',
            fields=[
                ('taskset_id', models.UUIDField(serialize=False, primary_key=True, editable=False, max_length=32, default=uuid.uuid4, verbose_name='group id')),
                ('result', djcelery.picklefield.PickledObjectField(editable=False)),
                ('date_done', models.DateTimeField(auto_now=True, verbose_name='created at')),
                ('hidden', models.BooleanField(default=False, db_index=True, editable=False)),
            ],
            options={
                'db_table': 'celery_tasksetmeta',
                'verbose_name': 'saved group result',
                'verbose_name_plural': 'saved group results',
            },
        ),
        migrations.CreateModel(
            name='TaskState',
            fields=[
                ('state', models.CharField(max_length=64, db_index=True, verbose_name='state')),
                ('task_id', models.UUIDField(serialize=False, primary_key=True, editable=False, max_length=32, default=uuid.uuid4, verbose_name='UUID')),
                ('name', models.CharField(max_length=200, db_index=True, null=True, verbose_name='name')),
                ('tstamp', models.DateTimeField(db_index=True, verbose_name='event received at')),
                ('args', models.TextField(null=True, verbose_name='Arguments')),
                ('kwargs', models.TextField(null=True, verbose_name='Keyword arguments')),
                ('eta', models.DateTimeField(null=True, verbose_name='ETA')),
                ('expires', models.DateTimeField(null=True, verbose_name='expires')),
                ('result', models.TextField(null=True, verbose_name='result')),
                ('traceback', models.TextField(null=True, verbose_name='traceback')),
                ('runtime', models.FloatField(null=True, help_text='in seconds if task succeeded', verbose_name='execution time')),
                ('retries', models.IntegerField(default=0, verbose_name='number of retries')),
                ('hidden', models.BooleanField(default=False, db_index=True, editable=False)),
            ],
            options={
                'get_latest_by': 'tstamp',
                'ordering': ['-tstamp'],
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
        ),
        migrations.CreateModel(
            name='WorkerState',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('hostname', models.CharField(max_length=255, verbose_name='hostname', unique=True)),
                ('last_heartbeat', models.DateTimeField(null=True, db_index=True, verbose_name='last heartbeat')),
            ],
            options={
                'get_latest_by': 'last_heartbeat',
                'ordering': ['-last_heartbeat'],
                'verbose_name': 'worker',
                'verbose_name_plural': 'workers',
            },
        ),
        migrations.AddField(
            model_name='taskstate',
            name='worker',
            field=models.ForeignKey(null=True, to='djcelery.WorkerState', verbose_name='worker'),
        ),
    ]
