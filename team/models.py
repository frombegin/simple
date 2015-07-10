#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

import os, uuid


def avatar_upload(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = "%s%s" % (uuid.uuid4().hex, ext)
    return os.path.join(settings.TEAM_AVATAR_PATH, filename)


class TeamManager(models.Manager):
    def create_team(self, user, **kwargs):
        return self.create(**kwargs)


class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    private = models.BooleanField(default=False)

    objects = TeamManager()

    def get_absolute_url(self):
        return reverse(settings.TEAM_URL_DETAIL_NAME, args=[self.pk])

    def get_member(self, user_id):
        return Member.objects.filter(team=self).get(user_id=user_id)

    def __unicode__(self):
        return self.name


class Member(models.Model):
    class Role:
        MEMBER, MANAGER, OWNER = range(3)
        CHOICES = (
            (MEMBER, 'member'),
            (MANAGER, 'manager'),
            (OWNER, 'owner'),
        )

    class Status:
        APPLIED, INVITED, REJECTED, ACCEPTED, AUTO_JOINED = range(5)
        CHOICES = (
            (APPLIED, 'appled'),
            (INVITED, 'invited'),
            (REJECTED, 'rejected'),
            (ACCEPTED, 'accepted'),
            (AUTO_JOINED, 'auto_joined'),
        )

    team = models.ForeignKey(Team, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.IntegerField(default=Role.MEMBER, choices=Role.CHOICES)
    status = models.IntegerField(default=Status.APPLIED, choices=Status.CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def invite(self, user, text):
        return Invitation.objects.create(member=self, invitee=user, text=text)

    def __unicode__(self):
        return u'%s of team_%d' % (self.user.username, self.team_id)

    class Meta:
        unique_together = (
            ('team', 'user',),
        )


class Invitation(models.Model):
    member = models.ForeignKey(Member, related_name='sent_invitations')
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_invitations')
    text = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'invitee',)


class Activity(models.Model):
    team = models.ForeignKey(Team)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    text = models.CharField(max_length=128, )
    uri = models.URLField()

    def __unicode__(self):
        return u'%s (%s)' % (self.text, self.uri)
