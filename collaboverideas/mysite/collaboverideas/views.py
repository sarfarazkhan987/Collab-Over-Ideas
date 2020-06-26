import json

from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.gzip import gzip_page

from .Interfaces import UserManagement, TeamManagement, ChatManagement, \
    TaskManagement, CodeSnippetsManagement, File_upload, MeetingManagement
from .forms.FileUploadForm import FileUploadForm
from .forms.LoginForm import LoginForm
from .forms.SignupForm import SignupForm
from .forms.UpdateUserForm import UpdateUserForm


@gzip_page
def index(request):
    if request.session.get('username') is not None:
        return redirect('teams')
    context = {}
    template = loader.get_template('collaboverideas/index.html')
    return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            # login(request, user)
            if UserManagement.check_user(username=username, password=raw_password):
                request.session['username'] = username
                request.session['userid'] = UserManagement.get_user_id(username)
                return redirect('teams')
            else:
                messages.add_message(request, messages.INFO, 'Invalid Username or Password')
                return redirect("index")


def signup(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            firstname = form.cleaned_data['firstname']
            raw_password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # login(request, user)
            UserManagement.add_user(firstname=firstname, password=raw_password, email=email, username=username)
            request.session['username'] = username

            return redirect("index")


def sign_out(request):
    request.session.flush()
    return redirect('index')


def validate_username(request):
    username = request.GET.get('username', None)
    data = {}
    if username is None:
        data['is_taken'] = True
        data['error_message'] = 'Username cannot be empty'
        return JsonResponse(data)

    data['is_taken'] = UserManagement.check_username(username)

    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists'
    return JsonResponse(data)


def load_chat(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())

    if request.GET.get('type') == 'private':
        lst = ChatManagement.load_private_messages(request.session.get('userid'),
                                                   request.session.get('teamid'))

    else:

        lst = ChatManagement.load_group_messages(request.session.get('userid'),
                                                 request.session.get('teamid'))
    rs = json.dumps(lst)

    return HttpResponse(rs, content_type='application/json')


def send_chat(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.GET.get('type') == 'private':
        lst = {'status': ChatManagement.send_private_message(message_body=request.GET.get('message_body'),
                                                             sender_id=request.session.get('userid'),
                                                             recipient_id=request.GET.get('recipient'),
                                                             team_id=request.session.get('teamid'))}

    else:
        lst = {'status': ChatManagement.send_group_message(message_body=request.GET.get('message_body'),
                                                           sender_id=request.session.get('userid'),
                                                           team_id=request.session.get('teamid'))}
    rs = json.dumps(lst)

    return HttpResponse(rs, content_type='application/json')


def check_new_messages(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    # lst = [{'userid': '62', 'count': 3}, ]
    lst_group = ChatManagement.load_new_group_messages(request.session.get('userid'), request.session.get('teamid'))
    lst_private = ChatManagement.load_new_private_messages(request.session.get('userid'), request.session.get('teamid'))
    lst = (lst_private, lst_group)
    rs = json.dumps(lst)

    return HttpResponse(rs, content_type='application/json')


def add_members(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.POST.get('members') == '' or request.POST.get('members') == []:
        return HttpResponse('no members')
        members = []
    else:
        members = eval(request.POST.get('members'))

    if request.POST.get('emails') == '' or request.POST.get('emails') == []:
        emails = []
    else:
        emails = eval(request.POST.get('emails'))

    added = TeamManagement.add_team(team_name=request.POST.get('teamnameName'),
                                    username=request.session.get('username'),
                                    members=members,
                                    invites=emails)

    request.session['teamid'] = added
    return redirect('dashboard')


@gzip_page
def teams(request):
    if request.session.get('username') is None:
        return redirect('index')
    user = request.session.get('username')

    request.session['userid'] = UserManagement.get_user_id(user)
    if request.GET.get('teamid') is not None and TeamManagement.check_team_id(user_id=request.session.get('userid'),
                                                                              team_id=request.GET.get('teamid')):
        request.session['teamid'] = request.GET.get('teamid')
        return redirect('dashboard')

    usernames = TeamManagement.get_users(user)

    context = {
        'invites': TeamManagement.get_invites(user),
        'teams': TeamManagement.get_teams(user),
        'usernames': usernames,
        'user': request.session.get('username'),
    }
    template = loader.get_template('collaboverideas/teams.html')
    return HttpResponse(template.render(context, request))


def join_team(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.GET.get('action') == 'reject_team':
        data = {'rejected': TeamManagement.delete_invite(request.GET.get('team_id'), request.session.get('username')), }

    else:
        status = TeamManagement.join_team(request.GET.get('team_id'), request.session.get('username'))
        data = {'accepted': status}
    return JsonResponse(data)


def dashboard(request):
    if request.session.get('username') is None:
        return redirect('index')
    return redirect('mini_tasks')


@gzip_page
def mini_tasks(request):
    if request.session.get('username') is None:
        return redirect('index')
    context = get_dashboard_context(request)
    context['tasks1'] = TaskManagement.get_tasks(request.session.get('teamid'), 1)
    context['tasks2'] = TaskManagement.get_tasks(request.session.get('teamid'), 2)
    context['tasks3'] = TaskManagement.get_tasks(request.session.get('teamid'), 3)
    context['task_users'] = TaskManagement.get_users(request.session.get('teamid'))
    context['task_labels'] = TaskManagement.get_labels(request.session.get('teamid'))
    template = loader.get_template('collaboverideas/mini_tasks.html')
    return HttpResponse(template.render(context, request))


@gzip_page
def mini_calendar(request):
    if request.session.get('username') is None:
        return redirect('index')
    context = get_dashboard_context(request)
    context['cal_users'] = TeamManagement.get_team_members(request.session.get('username'),
                                                           request.session.get('teamid'))
    template = loader.get_template('collaboverideas/mini_calendar.html')
    return HttpResponse(template.render(context, request))


def manage_meetings(request):
    data = {}
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.GET.get('action') == 'get_meetings':
        meetings = MeetingManagement.get_meetings(team_id=request.session.get('teamid'),
                                                  user_id=request.session.get('userid'))
        data['meetings'] = meetings
    elif request.GET.get('action') == 'add_subject':
        id = MeetingManagement.add_meeting_subject(team_id=request.session.get('teamid'),
                                                   subject=request.GET.get('subject'),
                                                   scheduler_id=request.session.get('userid'),
                                                   meeting_date=request.GET.get('meeting_date'))
        data['id'] = id
    elif request.GET.get('action') == 'add_meeting':
        edited = MeetingManagement.edit_meeting(meeting_id=request.GET.get('meeting_id'), note=request.GET.get('note'),
                                                location=request.GET.get('location'),
                                                start_time=request.GET.get('start_time'),
                                                end_time=request.GET.get('end_time'),
                                                invitee_ids=eval(request.GET.get('invitee_ids')))
        data['edited'] = edited
    elif request.GET.get('action') == 'get_meeting':
        meetings = MeetingManagement.get_meeting(meeting_id=request.GET.get('meeting_id'),
                                                 user_id=request.session.get('userid'))
        data['meeting'] = meetings
    elif request.GET.get('action') == 'delete_meeting':
        meetings = MeetingManagement.delete_meeting(meeting_id=request.GET.get('meeting_id'))
        data['deleted'] = meetings
    elif request.GET.get('action') == 'edit_meeting':
        edited = MeetingManagement.edit_meeting(subject=request.GET.get('subject'),
                                                meeting_id=request.GET.get('meeting_id'),
                                                note=request.GET.get('note'),
                                                location=request.GET.get('location'),
                                                start_time=request.GET.get('start_time'),
                                                end_time=request.GET.get('end_time'),
                                                invitee_ids=eval(request.GET.get('invitee_ids')))
        data['edited'] = edited
    return JsonResponse(data)


@gzip_page
def mini_codes(request):
    if request.session.get('username') is None:
        return redirect('index')
    if request.POST.get('code-name') is not None:
        if request.POST.get('code-id-edit') is not None and request.POST.get('code-id-edit') != '':
            CodeSnippetsManagement.edit_snippet(code_id=request.POST.get('code-id-edit'),
                                                file_name=request.POST.get('code-name'),
                                                language=request.POST.get('editing-lang'),
                                                code=request.POST.get('code-content'),
                                                )
        else:
            CodeSnippetsManagement.add_snippet(file_name=request.POST.get('code-name'),
                                               language=request.POST.get('editing-lang'),
                                               code=request.POST.get('code-content'),
                                               team_id=request.session.get('teamid'),
                                               user_id=request.session.get('userid'))
    context = get_dashboard_context(request)
    context['codes'] = CodeSnippetsManagement.get_snippets(request.session.get('teamid'))
    template = loader.get_template('collaboverideas/mini_codes.html')
    return HttpResponse(template.render(context, request))


def manage_tasks(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.GET.get('action') == 'reassign':
        TaskManagement.reassign_task(task_id=request.GET.get('task_id'), new_list_id=request.GET.get('list_id'))
        data = {'task': request.GET.get('task_id'),
                'list': request.GET.get('list_id')
                }
    elif request.GET.get('action') == 'delete':
        TaskManagement.delete_task(request.GET.get('task_id'))
        data = {'deleted': request.GET.get('task_id')}
    elif request.GET.get('action') == 'add_label':
        data = {'added': TaskManagement.add_label(request.session.get('teamid'), request.GET.get('name'))}
    elif request.GET.get('action') == 'add_task':
        added = TaskManagement.add_task(list_id=request.GET.get('list_id'),
                                        team_id=request.session.get('teamid'),
                                        task_name=request.GET.get('task_name'),
                                        task_description=request.GET.get('task_description'),
                                        due_date=request.GET.get('due_date'),
                                        user_ids=eval(request.GET.get('user_ids')),
                                        label_ids=eval(request.GET.get('label_ids')))
        data = {'added': added}

    elif request.GET.get('action') == 'get_task':
        data = {'task': TaskManagement.get_task(task_id=request.GET.get('task_id'),
                                                team_id=request.session.get('teamid'))}
    elif request.GET.get('action') == 'edit_task':
        edited = TaskManagement.edit_task(task_id=request.GET.get('task_id'),
                                          team_id=request.session.get('teamid'),
                                          task_name=request.GET.get('task_name'),
                                          task_description=request.GET.get('task_description'),
                                          due_date=request.GET.get('due_date'),
                                          user_ids=eval(request.GET.get('user_ids')),
                                          label_ids=eval(request.GET.get('label_ids')))
        data = {'edited': edited}
    else:
        data = {}

    return JsonResponse(data)


def view_code(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    members = request.GET.getlist('membersName')
    code_id = request.GET.get('code_id')
    code_dict = CodeSnippetsManagement.get_snippet(code_id)

    data = {'code': code_dict.get('code'),
            'language': code_dict.get('language'),
            'author': code_dict.get('firstname'),
            'name': code_dict.get('file_name'),
            }

    return JsonResponse(data)


def delete_code(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.GET.get('codeid') is not None:
        CodeSnippetsManagement.delete_snippet(request.GET.get('codeid'))
        return JsonResponse({'deleted': True})


# not a view
def get_dashboard_context(request):
    user = request.session.get('username')
    request.session['members_dict'] = TeamManagement.get_team_members(user, request.session.get('teamid'))

    context = {'userid': request.session.get('userid'), 'username': user,
               'user': UserManagement.get_user(user).get('firstname'), 'teamid': request.session.get('teamid'),
               'members': request.session.get('members_dict'),
               'init_private': ChatManagement.load_private_messages(current_user_id=request.session.get('userid'),
                                                                    team_id=request.session.get('teamid')),
               'init_group': ChatManagement.load_group_messages(request.session.get('userid'),
                                                                request.session.get('teamid')),
               'teams': TeamManagement.get_teams(user),
               'team_name': TeamManagement.get_team_name(request.session.get('teamid')),
               'team_id': int(request.session.get('teamid')),
               }

    return context


@gzip_page
def edit_profile(request):
    if request.session.get('username') is None:
        return redirect('index')
    user = request.session.get('username')
    # to show existing data in the form
    first_name = UserManagement.get_user(user).get('firstname')
    last_name = UserManagement.get_user(user).get('lastname')

    dob = UserManagement.get_user(user).get('dob')

    email_id = UserManagement.get_user(user).get('email')
    country_id = UserManagement.get_user(user).get('country_id')
    country_name = UserManagement.get_country_name(country_id)
    pwd = UserManagement.get_user(user).get('password')
    uname = UserManagement.get_user(user).get('username')
    context = get_dashboard_context(request)
    context['first_name'] = first_name
    context['last_name'] = last_name
    context['email_id'] = email_id
    context['dob'] = dob
    context['pwd'] = ''
    context['country_name'] = country_name
    context['uname'] = uname

    template = loader.get_template('collaboverideas/edit_profile.html')
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        # to insert the data in the database
        if form.is_valid():
            uname = request.session.get('username')
            firstname = form.cleaned_data['firstname']
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']
            lastname = form.cleaned_data['lastname']
            password = form.cleaned_data['password']
            country = form.cleaned_data['country']
            UserManagement.update_user(uname, firstname=firstname, lastname=lastname, email=email, dob=dob,
                                       password=password, country=country)
            return redirect('edit_profile')

    return HttpResponse(template.render(context, request))


@gzip_page
def file_upload(request):
    if request.session.get('username') is None:
        return redirect('index')
    context = get_dashboard_context(request)
    template = loader.get_template('collaboverideas/file_upload.html')
    teamid = request.session.get('teamid')
    files_list = File_upload.get_file_details(teamid)
    context['files_list'] = files_list
    form = FileUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        uploaded_file = request.FILES['files[]'].read()
        file_name = request.POST.get('fileName')
        file_type = request.POST.get('fileType')
        userid = request.session.get('userid')
        File_upload.file_upload_details(uploaded_file, file_name, file_type, userid, teamid)
        list = File_upload.get_file_details(teamid)
        return redirect('file_upload')
    return HttpResponse(template.render(context, request))


def file_download(request):
    id = request.GET.get('fileid')
    if id is not None:
        fname = File_upload.get_filename(id)
        file = File_upload.get_file(id)
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment; filename=' + fname
        return response
    else:
        return redirect('file_upload')


def file_delete(request):
    if request.session.get('username') is None:
        return JsonResponse(dict())
    if request.GET.get('fid') is not None:
        File_upload.delete_file(request.GET.get('fid'))
        return JsonResponse({'deleted': True})
