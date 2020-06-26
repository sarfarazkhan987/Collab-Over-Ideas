import logging

from django.db.models import Q

from collaboverideas.models import User, Teams, Tasks, Labels


def add_label(team_id, label_name):
    logger = logging.getLogger('interface')
    try:
        tm = Teams.objects.get(id=team_id)
        criteria1 = Q(team=tm)
        criteria2 = Q(label_name__iexact=label_name)
        if Labels.objects.filter(criteria1 & criteria2).exists():
            return 0
        else:
            label = Labels(label_name=label_name, team=tm)
            label.save()
            return label.id

    except Exception as e:
        logger.debug('interface.task_management.add_label', exc_info=e)


def add_task(list_id, team_id, task_name, task_description, due_date, user_ids, label_ids):
    logger = logging.getLogger('interface')
    try:
        tm = Teams.objects.get(id=team_id)
        task = Tasks(task_name=task_name, task_description=task_description, due_date=due_date, list_id=list_id,
                     team=tm)
        task.save()
        if user_ids != '':
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                task.user.add(user)
            task.save()

        if label_ids != '':
            for label_id in label_ids:
                label = Labels.objects.get(id=label_id)
                task.label.add(label)
            task.save()
        return task.id

    except Exception as e:
        logger.debug('interface.task_management.add_task', exc_info=e)


def get_labels(team_id):
    logger = logging.getLogger('interface')
    try:
        labels = Labels.objects.filter(team=team_id).order_by(
            'label_name')  # fetch all the labels from the labels table
        labels_list = []

        for label in labels:
            labels_dict = dict()
            labels_dict['label_id'] = label.id
            labels_dict[
                'label_name'] = label.label_name  # populate all the labels with its corresponding ids into dictionary as key value pair.
            labels_list.append(labels_dict)
        return labels_list

    except Exception as e:
        logger.debug('interface.task_management.get_labels', exc_info=e)


def get_users(team_id):
    logger = logging.getLogger('interface')
    try:
        users = User.objects.filter(teams__id=team_id)
        users_list = []
        for user in users:
            users_dict = dict()
            users_dict['user_id'] = user.id
            users_dict['firstname'] = user.firstname
            users_list.append(users_dict)
        return users_list

    except Exception as e:
        logger.debug('interface.task_management.get_users', exc_info=e)


def get_tasks(team_id, list_id):
    logger = logging.getLogger('interface')
    try:
        criteria1 = Q(team=team_id)
        criteria2 = Q(list_id=list_id)
        tasks = Tasks.objects.filter(criteria1 & criteria2).order_by('-due_date')

        tasks_list = []
        for task in tasks:
            task_dict = dict()

            task_dict.update({'task_id': task.id})
            task_dict.update({'task_name': task.task_name})
            task_dict.update({'task_description': task.task_description})
            task_dict.update({'due_date': task.due_date})

            users = User.objects.filter(tasks__id=task.id)
            members_list = []
            for member in users:
                members_list.append(member.firstname)
            task_dict.update({'users': members_list})

            labels = Labels.objects.filter(tasks__id=task.id)
            labels_list = []
            if labels is not None:
                for label in labels:
                    labels_list.append(label.label_name)
            task_dict.update({'labels': labels_list})

            tasks_list.append(task_dict)
        return tasks_list

    except Exception as e:
        logger.debug('interface.task_management.get_tasks', exc_info=e)


def reassign_task(task_id, new_list_id):
    logger = logging.getLogger('interface')
    try:
        task = Tasks.objects.get(id=task_id)
        task.list_id = new_list_id
        task.save()
        return 1

    except Exception as e:
        logger.debug('interface.task_management.reassign_task', exc_info=e)


def delete_task(task_id):
    logger = logging.getLogger('interface')
    try:
        task = Tasks.objects.get(id=task_id)
        task.delete()
        return 1

    except Exception as e:
        logger.debug('interface.task_management.delete_task', exc_info=e)


def edit_task(team_id, task_id, task_name, task_description, due_date, user_ids, label_ids):
    logger = logging.getLogger('interface')
    try:
        team = Teams.objects.get(id=team_id)
        task = Tasks.objects.get(id=task_id)

        user_list = []
        if user_ids != '':
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                user_list.append(user)
            task.user.set(user_list)
            task.save()
        else:
            task.user.clear()

        labels_list = []
        if label_ids != '':
            for label_id in label_ids:
                label = Labels.objects.get(id=label_id)
                labels_list.append(label)
            task.label.set(labels_list)
            task.save()
        else:
            task.label.clear()

        task.task_name = task_name
        task.due_date = due_date
        task.task_description = task_description
        task.save()
        return 1

    except Exception as e:
        logger.debug('interface.task_management.edit_task', exc_info=e)


def get_task(task_id, team_id):
    logger = logging.getLogger('interface')
    try:
        task = Tasks.objects.get(id=task_id)
        task_dict = dict()
        task_dict['task_id'] = task.id
        task_dict['task_name'] = task.task_name
        task_dict['task_description'] = task.task_description
        task_dict['due_date'] = task.due_date

        assigned_users = User.objects.filter(tasks__id=task.id)
        assigned_user_ids = []
        for assigned_user in assigned_users:
            assigned_user_ids.append(assigned_user.id)
        users = get_users(team_id)

        users_list = []
        for user in users:
            user_dict = dict()
            user_dict['user_id'] = user['user_id']
            user_dict['firstname'] = user['firstname']
            if user['user_id'] in assigned_user_ids:
                user_dict['user_flag'] = 1
            else:
                user_dict['user_flag'] = 0
            users_list.append(user_dict)
        task_dict['users_list'] = users_list

        assigned_labels = Labels.objects.filter(tasks__id=task.id)
        assigned_label_ids = []
        for assigned_label in assigned_labels:
            assigned_label_ids.append(assigned_label.id)
        labels = get_labels(team_id)
        labels_list = []
        for label in labels:
            label_dict = dict()
            label_dict['label_id'] = label['label_id']
            label_dict['label_name'] = label['label_name']
            if label['label_id'] in assigned_label_ids:
                label_dict['label_flag'] = 1
            else:
                label_dict['label_flag'] = 0
            labels_list.append(label_dict)
        task_dict['labels_list'] = labels_list

        return task_dict

    except Exception as e:
        logger.debug('interface.task_management.get_task', exc_info=e)
