from django.db import models


class User(models.Model):
    username = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Quizz(models.Model):
    quizz_name = models.CharField(max_length=200)


class Option(models.Model):
    option_text = models.CharField(max_length=500, unique=True)


class Question(models.Model):
    quizzno = models.ForeignKey(Quizz, related_name="relatedq",
                                on_delete=models.CASCADE)
    question_text = models.TextField()
    options = models.ManyToManyField(Option)
    marks = models.IntegerField(default=1)
    correct_option = models.ForeignKey(Option, related_name="correct",
                                       on_delete=models.CASCADE)


class Userquizzdetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_no = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Option, on_delete=models.CASCADE, null=True)


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


