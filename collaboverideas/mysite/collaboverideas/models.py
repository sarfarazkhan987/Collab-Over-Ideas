from django.db import models


# Create your models here.

class Country(models.Model):
    def __str__(self):
        return self.country_name

    # country_id = models.PositiveIntegerField(primary_key=True)
    country_name = models.CharField(max_length=20)


class User(models.Model):
    def __str__(self):
        return self.username

    # user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=1000, blank=False, null=False)
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(max_length=35, blank=False, null=False)
    country = models.ForeignKey('Country', models.SET_NULL, blank=True, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)


class Teams(models.Model):
    # team_id = models.PositiveIntegerField(primary_key=True)
    team_name = models.CharField(max_length=20, null=False, blank=False)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.team_name


class Workspace(models.Model):
    # workspace_id = models.PositiveIntegerField(primary_key=True)
    workspace_name = models.CharField(max_length=20, null=False, blank=False)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.workspace_name


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    message_body = models.CharField(max_length=500)
    group_flag = models.BooleanField(default=0)
    team = models.ForeignKey('Teams', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message_body


class MessageReference(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    sender = models.ForeignKey('User', blank=True, on_delete=models.CASCADE)
    recipient = models.ForeignKey('User', blank=True, related_name='recipients', on_delete=models.CASCADE)
    read_status_flag = models.BooleanField(default=0)

    def __str__(self):
        return str(self.teams) + ':' + str(self.sender) + ':' + str(self.recipient) + ':' + str(self.message)


class Labels(models.Model):  # Creating table named labels
    label_name = models.CharField(max_length=50, blank=True)
    team = models.ForeignKey('Teams', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.label_name


class Tasks(models.Model):  # Creating table named tasks
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=1000)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    list_id = models.PositiveSmallIntegerField(default=1, blank=True)
    team = models.ForeignKey('Teams', blank=True, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    label = models.ManyToManyField(Labels)

    def __str__(self):
        return self.task_name


class Snippets(models.Model):
    file_name = models.CharField(max_length=30)
    language = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    code = models.BinaryField()
    team = models.ForeignKey('Teams', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey('User', blank=True, on_delete=models.CASCADE)


class File(models.Model):
    file_name = models.CharField(max_length=500, blank=False, null=True)
    file_type = models.CharField(max_length=50)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    uploaded_file = models.BinaryField(null=True)

    # file_path = models.FilePathField(null=True)
    def __str__(self):
        return self.file_name


class FileInfo(models.Model):
    file = models.OneToOneField('File', on_delete=models.CASCADE)
    user = models.ForeignKey('User', models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey('Teams', models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.file.file_name


class UserInvites(models.Model):
    team = models.ForeignKey('Teams', blank=True, on_delete=models.CASCADE)
    email_id = models.EmailField(max_length=100, blank=False, null=False)
    invite_flag = models.BooleanField(default=0)
    passcode = models.CharField(max_length=100)


class Meetings(models.Model):
    subject = models.CharField(max_length=50)
    note = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    meeting_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    scheduler = models.ForeignKey('User', blank=True, related_name='scheduler', on_delete=models.CASCADE)
    invitees = models.ManyToManyField(User)
    team = models.ForeignKey('Teams', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject
