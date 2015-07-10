# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import team.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=128)),
                ('uri', models.URLField()),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitee', models.ForeignKey(related_name='received_invitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(default=0, choices=[(0, b'member'), (1, b'manager'), (2, b'owner')])),
                ('status', models.IntegerField(default=0, choices=[(0, b'appled'), (1, b'invited'), (2, b'rejected'), (3, b'accepted'), (4, b'auto_joined')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(upload_to=team.models.avatar_upload, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(related_name='created_teams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(related_name='members', to='team.Team'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitation',
            name='member',
            field=models.ForeignKey(related_name='sent_invitations', to='team.Member'),
        ),
        migrations.AddField(
            model_name='activity',
            name='team',
            field=models.ForeignKey(to='team.Team'),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('member', 'invitee')]),
        ),
    ]
