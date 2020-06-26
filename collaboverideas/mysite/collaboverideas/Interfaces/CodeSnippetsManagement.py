import datetime
import logging
import time

from collaboverideas.models import User, Teams, Snippets


def add_snippet(file_name, language, code, team_id, user_id):
    # logger = logging.getLogger('interface')
    # try:
    team = Teams.objects.get(id=team_id)
    user = User.objects.get(id=user_id)
    decoded_code = code.encode()
    t = time.time()
    st = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    code = Snippets(file_name=file_name, language=language, timestamp=st, code=decoded_code, team=team,
                    user=user)
    code.save()
    return 1

    # except Exception as e:
    #     logger.debug('interface.code_snippets_management.add_snippet', exc_info=e)


def get_snippets(team_id):
    team = Teams.objects.get(id=team_id)
    snippets = Snippets.objects.filter(team=team).order_by('-timestamp')
    snippets_list = []
    for snippet in snippets:
        snippet_dict = dict()
        snippet_dict.update({'code_id': snippet.id})
        snippet_dict.update({'file_name': snippet.file_name})
        snippet_dict.update({'time': snippet.timestamp})

        snippet_dict['language'] = snippet.language
        if snippet.user.lastname != '':
            snippet_dict['name'] = snippet.user.firstname + ' ' + snippet.user.lastname
        else:
            snippet_dict['name'] = snippet.user.firstname
        snippets_list.append(snippet_dict)

    return snippets_list


def get_snippet(code_id):
    snippet = Snippets.objects.get(id=code_id)
    snippet_dict = dict()
    snippet_dict.update({'file_name': snippet.file_name})
    snippet_dict.update({'language': snippet.language})
    code = snippet.code.decode()
    snippet_dict.update({'code': code})
    snippet_dict.update({'firstname': snippet.user.firstname})

    return snippet_dict


def delete_snippet(code_id):
    logger = logging.getLogger('interface')
    try:
        snippet = Snippets.objects.get(id=code_id)
        snippet.delete()
        return 1

    except Exception as e:
        logger.debug('interface.code_snippets_management.add_snippet', exc_info=e)


def edit_snippet(code_id, file_name, language, code):
    logger = logging.getLogger('interface')
    try:
        decoded_code = code.encode()
        t = time.time()
        st = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
        snippet = Snippets.objects.filter(id=code_id).update(file_name=file_name, language=language, timestamp=st,
                                                             code=decoded_code)
        return 1

    except Exception as e:
        logger.debug('interface.code_snippets_management.edit_snippet', exc_info=e)
