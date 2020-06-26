import datetime
import time

from django.db.models import Q

from collaboverideas.models import User, Message, MessageReference


def send_private_message(message_body, sender_id, recipient_id, team_id):
    t = time.time()
    st = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    message = Message(message_body=message_body, timestamp=st, team_id=team_id)
    message.save()
    message_reference = MessageReference(message=message, sender_id=sender_id, recipient_id=recipient_id)
    message_reference.save()
    return True


def send_group_message(message_body, sender_id, team_id):
    sender = User.objects.get(id=sender_id)
    t = time.time()
    st = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    message = Message(message_body=message_body, timestamp=st, team_id=team_id, group_flag=1)
    message.save()
    recipients = User.objects.filter(teams__id=team_id)
    # print(recipients)
    for recipient in recipients:
        if recipient != sender:
            message_reference = MessageReference(message=message, sender_id=sender_id, recipient=recipient)
            message_reference.save()
    return True


def load_private_messages(current_user_id, team_id):
    criteria1 = Q(sender_id=current_user_id)
    criteria2 = Q(recipient_id=current_user_id)
    criteria3 = Q(team_id=team_id) & Q(group_flag=0)

    messages = Message.objects.filter(criteria3).order_by('timestamp')
    messages_list = []
    for message in messages:
        criteria4 = Q(message=message)
        criteria5 = Q(message=message) & Q(read_status_flag=1)
        if MessageReference.objects.filter((criteria4 & criteria1) | (criteria2 & criteria5)).exists():
            mr = MessageReference.objects.get(message=message)
            message_dict = dict()
            message_dict.update({'message_body': message.message_body})
            message_dict.update({'sender_id': mr.sender.id})
            message_dict.update({'recipient_id': mr.recipient.id})
            if mr.sender.id == current_user_id:
                message_dict['opposite_user_id'] = mr.recipient.id
            else:
                message_dict['opposite_user_id'] = mr.sender.id
            # message_dict.update({'timestamp' : message.timestamp})   #TODO
            messages_list.append(message_dict)
    return messages_list


def load_group_messages(current_user_id, team_id):
    criteria1 = Q(team_id=team_id) & Q(group_flag=1)
    messages = Message.objects.filter(criteria1).order_by('timestamp')
    messages_list = []
    for message in messages:
        message_dict = dict()
        criteria2 = Q(message=message)
        criteria3 = Q(sender_id=current_user_id)
        criteria4 = Q(recipient_id=current_user_id) & Q(read_status_flag=1)
        if MessageReference.objects.filter(criteria2 & (criteria3 | criteria4)).exists():
            mr = MessageReference.objects.filter(criteria2 & (criteria3 | criteria4))[0]
            message_dict.update({'message_body': message.message_body})
            message_dict.update({'sender_id': mr.sender.id})
            message_dict.update({'firstname': mr.sender.firstname})
            # message_dict.update({'timestamp' : message.timestamp})   #TODO
            messages_list.append(message_dict)

    return messages_list


def load_new_private_messages(current_user_id, team_id):
    criteria1 = Q(team_id=team_id) & Q(group_flag=0)
    users = User.objects.filter(teams__id=team_id)
    messages = Message.objects.filter(criteria1).order_by('timestamp')
    messages_list = []
    for user in users:
        if user.id != current_user_id:
            mess_list = []
            for message in messages:
                criteria3 = Q(message=message)
                criteria2 = Q(sender=user) & Q(recipient_id=current_user_id) & Q(read_status_flag=0)
                if MessageReference.objects.filter(criteria2 & criteria3).exists():
                    mr = MessageReference.objects.get(criteria2 & criteria3)
                    mr.read_status_flag = 1
                    mr.save()
                    mess_list.append(message.message_body)
            if mess_list != []:
                message_dict = dict()
                message_dict['sender'] = user.id
                message_dict['messages'] = mess_list
                messages_list.append(message_dict)
    return messages_list


def load_new_group_messages(current_user_id, team_id):
    criteria1 = Q(team_id=team_id) & Q(group_flag=1)
    criteria2 = Q(recipient_id=current_user_id) & Q(read_status_flag=0)
    messages = Message.objects.filter(criteria1).order_by('timestamp')
    messages_list = []
    for message in messages:
        criteria3 = Q(message=message)
        if MessageReference.objects.filter(criteria2 & criteria3).exists():
            mr = MessageReference.objects.get(criteria2 & criteria3)
            message_dict = dict()
            message_dict['sender_id'] = mr.sender.id
            message_dict['message_body'] = message.message_body
            message_dict['firstname'] = mr.sender.firstname
            mr.read_status_flag = 1
            mr.save()
            messages_list.append(message_dict)
    return messages_list
