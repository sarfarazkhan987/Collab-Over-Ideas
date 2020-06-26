import logging

from django.db.models import Q

from collaboverideas.models import User, Meetings


def add_meeting_subject(team_id, subject, meeting_date, scheduler_id):
    logger = logging.getLogger('interface')
    try:
        meeting = Meetings(subject=subject, meeting_date=meeting_date, scheduler_id=scheduler_id, team_id=team_id)
        meeting.save()
        return meeting.id
    except Exception as e:
        logger.debug('interface.meeting_management.add_meeting', exc_info=e)


def edit_meeting(meeting_id, note, location, start_time, end_time, invitee_ids, subject=None):
    logger = logging.getLogger('interface')
    try:
        meeting = Meetings.objects.get(id=meeting_id)
        if subject is not None:
            meeting.subject = subject
            meeting.save()

        invitees_list = []
        if invitee_ids:
            for invitee_id in invitee_ids:
                invitee = User.objects.get(id=invitee_id)
                invitees_list.append(invitee)
            meeting.invitees.set(invitees_list)
            meeting.save()

        meeting.note = note
        meeting.location = location
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.save()
        return meeting.id
    except Exception as e:
        logger.debug('interface.meeting_management.get_meetings', exc_info=e)


def get_meetings(team_id, user_id):
    logger = logging.getLogger('interface')
    try:
        criteria1 = Q(team_id=team_id)
        user = User.objects.get(id=user_id)
        meetings = Meetings.objects.filter(criteria1)
        meetings_list = []
        for meeting in meetings:
            invitees = User.objects.filter(meetings__id=meeting.id)
            if user in invitees or user == meeting.scheduler:
                meeting_dict = dict()
                meeting_dict['meeting_id'] = meeting.id
                meeting_dict['subject'] = meeting.subject
                meeting_dict['meeting_date'] = meeting.meeting_date
                meetings_list.append(meeting_dict)
        return meetings_list

    except Exception as e:
        logger.debug('interface.meeting_management.get_meetings', exc_info=e)


def get_meeting(meeting_id, user_id):
    logger = logging.getLogger('interface')
    try:
        if Meetings.objects.filter(id=meeting_id).exists():
            meeting_dict = dict()
            meeting = Meetings.objects.get(id=meeting_id)
            meeting_dict['meeting_id'] = meeting.id
            meeting_dict['subject'] = meeting.subject
            meeting_dict['note'] = meeting.note
            meeting_dict['location'] = meeting.location
            meeting_dict['meeting_date'] = meeting.meeting_date
            meeting_dict['start_time'] = meeting.start_time
            meeting_dict['end_time'] = meeting.end_time
            users = User.objects.filter(teams__id=meeting.team.id)
            invitees_list = []
            invitees = User.objects.filter(meetings__id=meeting_id)
            if meeting.scheduler.id == user_id:
                meeting_dict['scheduler_name'] = 'You'
                for user in users:
                    if user.id == user_id:
                        continue
                    invitee_dict = {'user_id': user.id, 'firstname': user.firstname}
                    if user in invitees:
                        invitee_dict['user_flag'] = 1
                    else:
                        invitee_dict['user_flag'] = 0
                    invitees_list.append(invitee_dict)
            else:
                if meeting.scheduler.lastname:
                    meeting_dict['scheduler_name'] = meeting.scheduler.firstname + " " + meeting.scheduler.lastname
                else:
                    meeting_dict['scheduler_name'] = meeting.scheduler.firstname
                for user in users:
                    if user.id == meeting.scheduler.id:
                        continue
                    invitee_dict = {'user_id': user.id}
                    if user.id == user_id:
                        invitee_dict['firstname'] = 'You'
                    else:
                        invitee_dict['firstname'] = user.firstname
                    if user in invitees:
                        invitee_dict['user_flag'] = 1
                    else:
                        invitee_dict['user_flag'] = 0
                    invitees_list.append(invitee_dict)
            meeting_dict['invitees'] = invitees_list
            return meeting_dict
        return 0
    except Exception as e:
        logger.debug('interface.meeting_management.get_meeting', exc_info=e)


def delete_meeting(meeting_id):
    logger = logging.getLogger('interface')
    try:
        if Meetings.objects.filter(id=meeting_id).exists():
            meeting = Meetings.objects.get(id=meeting_id)
            meeting.delete()
        return 0
    except Exception as e:
        logger.debug('interface.meeting_management.delete_meeting', exc_info=e)
