from django.db import models

# Create your models here.
class UserCredential(models.Model):
    userFirstName = models.CharField(max_length=20, default=None)
    userLastName = models.CharField(max_length=20, default=None)
    userEmail = models.CharField(max_length=40, default=None, primary_key=True)
    userPhone = models.CharField(max_length=11, default=None)
    userPassword= models.CharField(max_length=20, default=None)
    created = models.DateTimeField(auto_now=True)

class QuestionAnswers(models.Model):
    questionId = models.AutoField(primary_key=True)
    questionDescription = models.CharField(max_length=200, default="")
    option1 = models.CharField(max_length=200, default="")
    option2 = models.CharField(max_length=200, default="")
    option3 = models.CharField(max_length=200, default="")
    option4 = models.CharField(max_length=200, default="")
    correctAnswer = models.CharField(max_length=10, default="")

class UserAttemptHistory(models.Model):
    attemptId = models.AutoField(primary_key=True)
    userEmail = models.CharField(max_length=40, default=None)
    userAttendedQuestions = models.CharField(max_length=20, default=None)
    userGainedGrades = models.FloatField(max_length=10, default=0)
    dateOnWhichAttempted = models.DateTimeField(auto_now=True)