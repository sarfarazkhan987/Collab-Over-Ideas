import logging

from django.db.models import Q

from collaboverideas.models import User, Teams, UserInvites


def get_users(username):
    users_list = User.objects.exclude(username__iexact=username)
    users = []
    for user in users_list:
        users.append(user.username)
    return users


def add_team(team_name, username, members, invites):
    t = Teams(team_name=team_name)
    t.save()
    user = User.objects.get(username__iexact=username)
    t.user.add(user)
    if members:
        for member in members:
            mem = User.objects.get(username__iexact=member)
            t.user.add(mem)
        t.save()
    if invites:
        for invite in invites:
            user_invite = UserInvites(team_id=t.id, email_id=invite)
            user_invite.save()
    return t.id


def get_team(username):
    user = User.objects.get(username=username)
    if Teams.objects.filter(user=user).exists():
        return Teams.objects.filter(user=user).values('id')[0].get('id')  # TODO this is temporary.
    else:
        return 0


def get_teams(username):
    user = User.objects.get(username=username)
    teams = Teams.objects.filter(user=user).values('id', 'team_name')
    return teams


def check_team_id(user_id, team_id):
    if Teams.objects.filter(id=team_id).exists():
        team = Teams.objects.get(id=team_id)
        teams = Teams.objects.filter(user__id=user_id)
        return team in teams
    return False


def get_team_name(team_id):
    if Teams.objects.filter(id=team_id).exists():
        team = Teams.objects.get(id=team_id)
        return team.team_name


def get_team_members(username, team_id):
    users = User.objects.filter(teams__id=team_id)
    members_list = dict()
    for member in users:
        if member.username != username:
            members_list.update({member.id: member.firstname})
    return members_list


def delete_invite(team_id, username):
    logger = logging.getLogger('interface')
    try:
        if User.objects.filter(username__iexact=username).exists():
            user = User.objects.get(username__iexact=username)
            criteria = Q(email_id=user.email) & Q(team_id=team_id)
            if UserInvites.objects.filter(criteria).exists():
                invites = UserInvites.objects.filter(criteria)
                invites.delete()
                return 1
        return 0
    except Exception as e:
        logger.debug('interface.team_management.delete_invite', exc_info=e)


def get_invites(username):
    invites_list = []
    user = User.objects.get(username__iexact=username)
    criteria = Q(email_id=user.email) & Q(invite_flag=0)
    if UserInvites.objects.filter(criteria).exists():
        invites = UserInvites.objects.filter(criteria)
        for invite in invites:
            invite_dict = dict()
            invite_dict['team_id'] = invite.team.id
            invite_dict['team_name'] = invite.team.team_name
            invites_list.append(invite_dict)
    return invites_list


def join_team(team_id, username):
    if User.objects.filter(username__iexact=username).exists() and Teams.objects.filter(id=team_id).exists():
        user = User.objects.get(username__iexact=username)
        team = Teams.objects.get(id=team_id)
        team.user.add(user)
        team.save()
        criteria1 = Q(team_id=team_id) & Q(email_id=user.email)
        user_invite = UserInvites.objects.get(criteria1)
        user_invite.invite_flag = 1
        user_invite.save()
        return team.id
    return 0
