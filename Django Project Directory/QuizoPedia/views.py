from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserCredential, QuestionAnswers, UserAttemptHistory
import random

# Create your views here.
def loginPage(request):
    if request.session.get('userEmail') == None:
        if request.method == 'POST':
            # print(request.POST)
            print("Hello")
            if request.POST.get('typeOfForm') == 'signup':
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                password = request.POST.get('password')
                if UserCredential.objects.filter(userEmail=email):
                    request.session['IsValidEmailLogin'] = False
                    request.session['IsValidEmailSignup'] = True
                    return render(request, 'signup.html')
                else:
                    request.session['IsValidEmailSignup'] = False
                    newUser = UserCredential(userFirstName=firstname, userLastName=lastname, userEmail=email, userPhone=phone, userPassword=password)
                    newUser.save()
                    request.session['validUser'] = True
                    request.session['userEmail'] = email
                    request.session['userFirstName'] = firstname
                    request.session['userLastName'] = lastname
                    # return HttpResponse("In Signup Thank you : ")
                    return redirect('/QuizoPedia/QuizHistory')
            else:
                email = request.POST.get('email')
                password = request.POST.get('password')
                if UserCredential.objects.filter(userEmail=email, userPassword=password):
                    userData = UserCredential.objects.filter(userEmail=email, userPassword=password).values()
                    # print(userData)
                    request.session['IsValidEmailLogin'] = False
                    request.session['validUser'] = True
                    request.session['userEmail'] = userData[0]['userEmail']
                    request.session['userFirstName'] = userData[0]['userFirstName']
                    request.session['userLastName'] = userData[0]['userLastName']
                    # print(userData[0]['userId'])
                    # return HttpResponse("User Found")
                    print('Session Setup Done')
                    return redirect('/QuizoPedia/QuizHistory')
                else:
                    request.session['IsValidEmailSignup'] = False
                    request.session['IsValidEmailLogin'] = True
                    return render(request, 'signup.html')
        else:
            return render(request, 'signup.html')
    else:
        return redirect('/QuizoPedia/QuizHistory')
    
def startQuiz(request):
    if request.session.get('userEmail') != None:
        if request.method == 'POST':
            questionIds = []
            selectedAnswers = {}
            for i in range(1,6):
                questionIds.append(request.POST.get('questionId'+str(i)))
                selectedAnswers[request.POST.get('questionId' + str(i))] = request.POST.get('answer' + str(i))
                # for j in range(1,5):
                #     if 'option'+str(j)+str(i) in request.POST:
                #         selectedAnswers[request.POST.get('questionId'+str(i))] = 'option'+str(j)
            # print(questionIds)
            allQuestion = QuestionAnswers.objects.all().values()
            correctAnswers = 0
            for question in allQuestion:
                if str(question['questionId']) in questionIds:
                    if question['correctAnswer'] == selectedAnswers[str(question['questionId'])]:
                        correctAnswers=correctAnswers+1

            # print(correctAnswers)
            # print(allQuestion)
            # print(selectedAnswers)
            userEmail = request.session.get('userEmail')
            userAttendedQuestions = ','.join(questionIds)
            userGainedGrades = correctAnswers
            quizAttempt = UserAttemptHistory(userEmail=userEmail, userAttendedQuestions=userAttendedQuestions, userGainedGrades = userGainedGrades)
            quizAttempt.save()
            message = "Please Try Again!"
            if correctAnswers * 100 / 5 == 100.0:
                message = "You are a genius!"
            elif correctAnswers * 100 / 5 == 80.0:
                message = "Excellent work!"
            elif correctAnswers * 100 / 5 == 60.0:
                message = "Good Job!"

            return render(request, 'QuizResult.html', { 'message' : message })
        else:
            allQuestions = QuestionAnswers.objects.values_list('questionId','questionDescription','option1','option2','option3','option4')
            # print(allQuestions)
            selectedQuestionIndexSet = set();
            while len(selectedQuestionIndexSet) != 5:
                selectedQuestionIndexSet.add(random.randint(0, len(allQuestions)-1))
            # print(selectedQuestionIndexSet)
            # for i in range()
            selectedQuestionsList = []
            i = 1
            for index in selectedQuestionIndexSet:
                # selectedQuestionsList[index[0]] = index
                ques = list(allQuestions[index])
                ques.append(i)
                selectedQuestionsList.append(ques)
                i=i+1
            # print(selectedQuestionsList)
            return render(request, 'Quiz.html', {'questions':selectedQuestionsList})
    else:
        return redirect('/QuizoPedia/signup')

def QuizHistory(request):
    if request.session.get('userEmail') != None:
        allPastQuizAttempts = UserAttemptHistory.objects.filter(userEmail=request.session.get('userEmail')).order_by('-dateOnWhichAttempted').values()

        i = 1
        totalScore = 0
        maximumScore = 0
        minimumScore = 5
        for quiz in allPastQuizAttempts:
            quiz['indexOfAttempt'] = i
            quiz['percentageScore'] = quiz['userGainedGrades'] * 100 / 5
            i = i+1
            totalScore = totalScore + quiz['userGainedGrades']
            if quiz['userGainedGrades'] > maximumScore:
                maximumScore = quiz['userGainedGrades']
            if quiz['userGainedGrades'] < minimumScore:
                minimumScore = quiz['userGainedGrades']
        # print(allPastQuizAttempts)
        if len(allPastQuizAttempts) == 0:
            maximumScore = 0
            minimumScore = 0
        averageScore = 0
        if len(allPastQuizAttempts) > 0:
            averageScore = round(totalScore / len(allPastQuizAttempts),2)
        return render(request, 'quizHistory.html', {'quizHistory': allPastQuizAttempts, 'averageScore': str(averageScore), 'MaximumScore': str(maximumScore), 'MinimumScore': str(minimumScore)})
    else:
        # return render(request, 'signup.html')
        return redirect('/QuizoPedia/signup')
def logout(request):
    # request.session['userEmail'] = ""
    request.session.clear()
    # return render(request, 'signup.html')
    return redirect('/QuizoPedia/signup')
