# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommsAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('audience', models.ForeignKey(to='core.Audience', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_desc', models.CharField(max_length=140)),
                ('full_desc', models.CharField(max_length=3000)),
                ('bh_number', models.CharField(max_length=255, null=True, blank=True)),
                ('value_of_award', models.IntegerField(default=0)),
                ('value_awarded_to_ncl', models.IntegerField(default=0, null=True, blank=True)),
                ('project_start_date', models.DateField()),
                ('duration', models.IntegerField(default=0)),
                ('external', models.CharField(max_length=255, blank=True)),
                ('created_on', models.DateField(null=True)),
                ('admin_checked', models.BooleanField(default=False)),
                ('level', models.CharField(max_length=3, choices=[(b'N/A', b'N/A'), (b'UG', b'Undergraduate'), (b'PGT', b'Postgraduate Taught'), (b'PGR', b'Postgraduate Research'), (b'ST', b'Staff')])),
                ('flag', models.BooleanField(default=False)),
                ('audiences', models.ManyToManyField(to='core.Audience', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalAudience',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical audience',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalCommsAudit',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('audience', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Audience', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('sent', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Communication', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical comms audit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalCommunication',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('short_desc', models.CharField(max_length=140)),
                ('full_desc', models.CharField(max_length=3000)),
                ('bh_number', models.CharField(max_length=255, null=True, blank=True)),
                ('value_of_award', models.IntegerField(default=0)),
                ('value_awarded_to_ncl', models.IntegerField(default=0, null=True, blank=True)),
                ('project_start_date', models.DateField()),
                ('duration', models.IntegerField(default=0)),
                ('external', models.CharField(max_length=255, blank=True)),
                ('created_on', models.DateField(null=True)),
                ('admin_checked', models.BooleanField(default=False)),
                ('level', models.CharField(max_length=3, choices=[(b'N/A', b'N/A'), (b'UG', b'Undergraduate'), (b'PGT', b'Postgraduate Taught'), (b'PGR', b'Postgraduate Research'), (b'ST', b'Staff')])),
                ('flag', models.BooleanField(default=False)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical communication',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalNotes',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('created_on', models.DateField(null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical notes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalSources',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical sources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalTags',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalUserProfile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('username', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=35)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('user_type', models.CharField(max_length=1, choices=[(b'1', b'Staff'), (b'2', b'Student')])),
                ('email', models.EmailField(max_length=75)),
                ('smart_card', models.CharField(max_length=255)),
                ('login_count', models.IntegerField()),
                ('last_login', models.DateField(editable=False, blank=True)),
                ('unit', models.CharField(max_length=255)),
                ('known_as', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical user profile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=23)),
                ('audit', models.ForeignKey(to='core.CommsAudit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('created_on', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=35)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('user_type', models.CharField(max_length=1, choices=[(b'1', b'Staff'), (b'2', b'Student')])),
                ('email', models.EmailField(max_length=75)),
                ('smart_card', models.CharField(max_length=255)),
                ('login_count', models.IntegerField()),
                ('last_login', models.DateField(auto_now=True)),
                ('unit', models.CharField(max_length=255)),
                ('known_as', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='notes',
            name='created_by',
            field=models.ForeignKey(blank=True, to='core.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalnotes',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalnotes',
            name='history_user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalcommunication',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalcommunication',
            name='history_user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalcommunication',
            name='source',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Sources', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalcommsaudit',
            name='sent_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='communication',
            name='created_by',
            field=models.ForeignKey(to='core.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='communication',
            name='individuals',
            field=models.ManyToManyField(related_name='communication_individuals', null=True, to='core.UserProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='communication',
            name='notes',
            field=models.ManyToManyField(related_name='communication_notes', null=True, to='core.Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='communication',
            name='source',
            field=models.ForeignKey(to='core.Sources', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='communication',
            name='tags',
            field=models.ManyToManyField(related_name='communication_tags', null=True, to='core.Tags', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commsaudit',
            name='sent',
            field=models.ForeignKey(to='core.Communication', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commsaudit',
            name='sent_by',
            field=models.ForeignKey(blank=True, to='core.UserProfile', null=True),
            preserve_default=True,
        ),
    ]
