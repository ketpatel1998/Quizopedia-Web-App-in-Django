from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.loginPage),
    path('Quiz/', views.startQuiz),
    path('QuizHistory/', views.QuizHistory),
    path('logout/', views.logout)
]