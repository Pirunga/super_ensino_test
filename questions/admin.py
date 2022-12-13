from django.contrib import admin
from questions.models import Questions, User


admin.site.register(User)
admin.site.register(Questions)
