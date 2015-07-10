from django.test import TestCase
from .models import Team, Member, Invitation
from django.contrib.auth.models import User


class TeamTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('super', 'super@mail.com', '123456')
        self.u = []
        for i in range(5):
            tmp_name = 'u%d' % (i)
            tmp_mail = 'u%d@email.com' % i
            self.u.append(User.objects.create_user(tmp_name, tmp_mail, '123456'))
        self.t1 = Team.objects.create(creator=self.u[0], name=u'team1', )
        self.m1 = Member.objects.create(team=self.t1, user = self.u[1],
                                        role = Member.Role.MEMBER, status = Member.Status.AUTO_JOINED)

    def test_invitations(self):
        inv = self.m1.invite(self.u[2], 'hello u2')
        self.assertEqual(self.m1.sent_invitations.count(), 1)
        self.assertEqual(self.u[2].received_invitations.count(),1)

    def test_get_member(self):
        self.assertEqual(self.t1.get_member(self.m1.user_id), self.m1)