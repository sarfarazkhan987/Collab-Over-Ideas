import datetime
import time

from collaboverideas.models import User, Teams, FileInfo, File


def file_upload_details(file, file_name, file_type, userid, teamid):
    t = time.time()
    st = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    user = User.objects.get(id=userid)
    team = Teams.objects.get(id=teamid)
    artifact = File(uploaded_file=file, file_name=file_name, file_type=file_type, upload_time=st)
    artifact.save()
    query = FileInfo(file=artifact, user=user, team=team)
    query.save()
    id = artifact.id
    return id


def get_file_list(userid, teamid):
    files = FileInfo.objects.get(teamid=teamid)
    file_id_list = []
    for file in files:
        file_id_list.append(file.id)
    file_list = dict()
    for fid in file_id_list:
        file = File.objects.filter(id=fid)
        # file_list.update(file.id:file.file_name)


def get_file_details(teamid):
    fileInfos = FileInfo.objects.filter(team=teamid).order_by('-file__upload_time')
    files_list = []
    for file_info in fileInfos:
        files_dict = dict()
        file = File.objects.get(id=file_info.file_id)
        files_dict['file_id'] = file.id
        files_dict['filename'] = file.file_name
        user = User.objects.get(id=file_info.user_id)
        files_dict['firstname'] = user.firstname
        files_list.append(files_dict)

    return files_list


def get_filename(fileid):
    complete_file = File.objects.get(id=fileid)
    # fid=complete_file.uploaded_file
    filename = complete_file.file_name
    return filename


def get_file(fileid):
    complete_file = File.objects.get(id=fileid)
    content = complete_file.uploaded_file
    return content


def delete_file(fileid):
    if File.objects.filter(id=fileid).exists():
        file = File.objects.get(id=fileid)
        file.delete()
        return 1
    return 0
