from django.contrib import admin

from . models import User, Question, Quizz,\
    Option, Userquizzdetails, Leaderboard
from .models import User


admin.site.register(User)
admin.site.register(Question)
admin.site.register(Quizz)
admin.site.register(Option)
admin.site.register(Userquizzdetails)
admin.site.register(Leaderboard)
