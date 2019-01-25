from django.urls import path

from . import views

app_name = 'quizzapp'

urlpatterns = [
    # path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quizz/<int:quizz_id>', views.quizz_questions, name='quizz_questions'),
    path('save_answer/', views.save_answer, name='save_answer'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]