from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse
from django.urls import reverse

from .models import User, Question, Quizz, Option, Userquizzdetails, \
                    Leaderboard


def login(request):
    return HttpResponse("Hey you are doing good!")


def dashboard(request):
    return render(request, 'quizzapp/dashboard.html')


def quizz_questions(request, quizz_id):
    quizz = Quizz.objects.get(id=quizz_id)
    quizz_questions = quizz.relatedq.all()
    return render(request, 'quizzapp/dashboard.html', {'quizz1_q_set': quizz_questions})


def save_answer(request):
    quen_id = request.GET.get('question_id', None)
    opt_id = request.GET.get('option_id', None)
    question = Question.objects.get(pk=quen_id)
    selected_option = Option.objects.get(pk=opt_id)
    user = User.objects.get(pk=1)

    quizz_detail, created = Userquizzdetails.objects.get_or_create(
        user=user,
        question_no=question,
    )

    user_score, new_obj = Leaderboard.objects.get_or_create(
        user=user,
    )
    data = {
        'already_answered': False,
    }
    if created:
        quizz_detail.selected_answer = selected_option
        if selected_option == question.correct_option:
            user_score.score += question.marks
            user_score.save()
        quizz_detail.save()
    else:
        data['already_answered'] = True,
        data['error_message'] = "You have already answered this question"
    return JsonResponse(data)
