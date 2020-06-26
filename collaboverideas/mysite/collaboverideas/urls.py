from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/load_chat/$', views.load_chat, name='load_chat'),
    url(r'^ajax/send_chat/$', views.send_chat, name='send_chat'),
    url(r'^ajax/check_new_messages/$', views.check_new_messages, name='check_new_messages'),
    url(r'^ajax/add_members/$', views.add_members, name='add_members'),
    url(r'^ajax/view_code/$', views.view_code, name='view_code'),
    url(r'^ajax/delete_code/$', views.delete_code, name='delete_code'),
    url(r'^ajax/manage_tasks/$', views.manage_tasks, name='manage_tasks'),
    url(r'^ajax/manage_meetings/$', views.manage_meetings, name='manage_meetings'),

    url(r'^ajax/join_team/$', views.join_team, name='join_team'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/tasks/$', views.mini_tasks, name='mini_tasks'),
    url(r'^dashboard/codes/$', views.mini_codes, name='mini_codes'),
    url(r'^dashboard/calendar/$', views.mini_calendar, name='mini_calendar'),

    url(r'^dashboard/signout/$', views.sign_out, name='sign_out'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^teams/$', views.teams, name='teams'),
    url(r'^dashboard/file_upload/$', views.file_upload, name='file_upload'),

    url(r'^dashboard/file_download/$', views.file_download, name='file_download'),
    url(r'^dashboard/file_delete/$', views.file_delete, name='file_delete'),
    url(r'^dashboard/edit_profile/$', views.edit_profile, name='edit_profile'),
]
