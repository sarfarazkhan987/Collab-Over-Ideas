from django.contrib import admin

from .models import Country
from .models import Teams
# Register your models here.
from .models import User
from .models import Tasks, Labels, Snippets

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Teams)
admin.site.register(Tasks)
admin.site.register(Labels)
admin.site.register(Snippets)