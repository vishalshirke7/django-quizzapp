from .models import User, Quizz


def add_variable_to_context(request):
    # if 'user_id' in request.session:
    #     userid = request.session['user_id']
    #     user = User.objects.get(pk=userid)
    quizzes = Quizz.objects.all()
    return {
            # 'logged_in': True,
            # 'user': user,
        'quizzes': quizzes
    }
