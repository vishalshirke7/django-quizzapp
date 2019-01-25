from .models import User, Quizz


def add_variable_to_context(request):
    quizzes = Quizz.objects.all()
    if 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        return {'logged_in': True, 'user': user,
                'quizzes': quizzes}
    return {'logged_in': False,
            'quizzes': quizzes}
