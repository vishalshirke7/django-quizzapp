from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from .models import User, Question, Quizz, Option, Userquizzdetails, \
                    Leaderboard
from quizzproject import settings
from .decorators import myuser_login_required


# def login(request):
#     """
#     Base function to login a user using google
#     :return:
#     """
#     if 'user_id' in request.session.keys():
#         print("WHy the hell session is not persisting between two tabs")
#         return HttpResponseRedirect(reverse('quizzapp:dashboard'))
#     google = OAuth2Session(
#         settings.CLIENT_ID,
#         redirect_uri=settings.REDIRECT_URI,
#         scope=settings.SCOPE)
#     auth_url, state = google.authorization_url(
#         settings.AUTH_URI, access_type="offline")
#     request.session['oauth_state'] = state
#     return HttpResponseRedirect(auth_url)
#     # return render(request, 'quizzapp/login.html', {'auth_url': auth_url})

#
# def callback(request):
#     """
#     Callback method for gmail login. Whenever a user enter credentials for his/her
#     gmail account, the page is redirected using this method for obtaining a access token
#     for making requests to gmail API
#     """
#     if 'user_id' in request.session.keys():
#         return HttpResponseRedirect(reverse('quizzapp:dashboard'))
#     if 'error' in request.args:
#         if request.args.get('error') == 'access_denied':
#             return 'You denied access.'
#         return 'Error encountered.'
#     if 'code' not in request.args and 'state' not in request.args:
#         return HttpResponseRedirect(reverse('quizzapp:login'))
#     else:
#         google = OAuth2Session(settings.CLIENT_ID, state=request.args['state'],
#                                redirect_uri=settings.REDIRECT_URI)
#         try:
#             token = google.fetch_token(
#                 settings.TOKEN_URI,
#                 client_secret=settings.CLIENT_SECRET,
#                 authorization_response=request.url)
#         except HTTPError:
#             return 'HTTPError occurred.'
#         google = OAuth2Session(settings.CLIENT_ID, token=token)
#         resp = google.get(settings.USER_INFO)
#         # print(resp)
#         if resp.status_code == 200:
#             user_data = resp.json()
#             email = user_data['email']
#             user = User.objects.filter(email=email).first()
#             if user is None:
#                 user = User()
#                 user.email = email
#             user.name = user_data['name']
#             # print(token)
#             # store = file.Storage('/tokens/'+user.email+'.txt')
#             # store.put(token)
#             user.tokens = json.dumps(token)
#             # db.session.add(user)
#             # db.session.commit()
#             request.session['user_id'] = user.id
#             return HttpResponseRedirect(reverse('quizzapp:dashboard'))
#         return 'Could not fetch your information.'


def dashboard(request):
    return render(request, 'quizzapp/dashboard.html')


def quizz_questions(request, quizz_id):
    quizz = Quizz.objects.get(id=quizz_id)
    quizz_questions = quizz.relatedq.all()
    user = User.objects.get(pk=1)
    que_list = Userquizzdetails.objects.filter(user=user)
    attempted = []
    if que_list.exists():
        attempted = [question.selected_answer.id for question in que_list]
        print(attempted)
    return render(request, 'quizzapp/dashboard.html', {'quizz_q_set': quizz_questions,
                                                       'attempted': attempted
                                                       })


def save_answer(request):
    quen_id = request.GET.get('question_id', None)
    opt_id = request.GET.get('option_id', None)
    question = Question.objects.get(pk=quen_id)
    selected_option = Option.objects.get(pk=opt_id)
    user = User.objects.get(pk=1)
    quizz_detail, created = Userquizzdetails.objects.get_or_create(user=user,
                                                                   question_no=question)
    user_score, new_obj = Leaderboard.objects.get_or_create(user=user)
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


def leaderboard(request):
    lead_b = Leaderboard.objects.order_by('-score')
    context = {'leaderboard': lead_b}
    return render(request, 'quizzapp/leaderboard.html',
                  context)

