from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
from django.db.models import Count
from mazeData.models import Users, highScores, userData
from django.contrib.auth import authenticate, login
from .forms import Register
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import  IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from decimal import *
import math


#decided not to use the home page so ignore
def homePage(request):
	template = loader.get_template('MazeHTML5/index.html')
	return render(request, 'MazeHTML5/index.html')

#decided not to use the home page so ignore
def cookie(request):

	template = loader.get_template('mazeData/home.html')
	return render(request,'mazeData/home.html')

#for when a user registers
def registerResponse(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            
            try:
                user = Users.objects.get(userName =username)
                if(user is not None):
                    return HttpResponse("username already exists")
                else:
                    newUser = Users.objects.create_user(userName = username,  password = password)
                    return HttpResponse("registered")
            except:
                newUser = Users.objects.create_user(userName = username,  password = password)
                return HttpResponse("registered")
                

#for when a user logs in 
def loginResponse(request):
    context = {}
    
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            passW = request.POST['password']
            userN = request.POST['username']
            s = ""
            user = authenticate(request,userName=userN, password=passW)
            if user is not None:
                login(request,user)
                context['userMessage']  = "User: " + user.userName + " signed in"
                t = Token.objects.get(user=Users.objects.get(userName = userN))
                if(t is not None):
                    t.delete()

                t = Token.objects.create(user=Users.objects.get(userName = userN))
                t.save()
                return HttpResponse(t.key)
            else:
                #return render(request, 'mazeData/home.html', context)
                return HttpResponse("username or password incorrect")
                
            return HttpResponse("")


#sent to server from game when game is complete
#server sends back top 10 scores as well as some 
#data about the user's performance
@permission_classes([IsAuthenticated])
def scoreResponse(request):
    if request.method == 'POST':
        userN = request.POST['username']
        score = request.POST['time']
        
        try:
            highscore = highScores.objects.get(userName = userN)
            overallScore = userData.objects.get(userName = userN)
            if(highscore is not None):
                if(float(score) < float(highscore.time)):
                    highscore.time = float(score)
                    highscore.save()
            else:
                newHighScore = highScores(userName = userN, time = float(score))
                newHighScore.save() 
            if(overallScore is not None):
                prevTime = str(float(overallScore.prevTime))
                overallScore.prevTime = score
                overallScore.numberTries = str(int(overallScore.numberTries) + 1)
                overallScore.averageTime = str(float(overallScore.averageTime) * (float(overallScore.numberTries)-1)/float(overallScore.numberTries) + (float(score) * 1/float(overallScore.numberTries)))
                overallScore.save()
                s = leaderboard()
                s += roundString(prevTime) + '\n' + overallScore.numberTries + '\n' + roundString(overallScore.averageTime) + '\n' + roundString(highscore.time)
                return HttpResponse(s)
            else:
                newOverall = userData(userName = userN, prevTime = score, numberTries = 1, averageTime = score)
                newOverall.save()
                s = leaderboard()
                s += "N/A" + '\n' + "1" + '\n' + roundString(score) + '\n' + roundString(score) 
                return HttpResponse(s)
        except:
            newHighScore = highScores(userName = userN, time = float(score))
            newHighScore.save() 
            newOverall = userData(userName = userN, prevTime = score, numberTries = 1, averageTime = score)
            newOverall.save()
            s = leaderboard()
            s += "N/A" + '\n' + "1" + '\n' + roundString(score)  + '\n' + roundString(score) 
            return HttpResponse(s)
    return HttpResponse("High score updated")

#returns the top 10 times and users
def leaderboard():
    topScores = highScores.objects.order_by('time')[:10]
    leaderboard = []
    for i in range(0,10):
        if(i < len(topScores)):
            if(topScores[i] is not None):
                leaderboard.append([topScores[i].userName, roundString(topScores[i].time)])
        else:
            leaderboard.append(["N/A", "N/A"])
    s = ""
    for i in range(0,10):
        s += leaderboard[i][0]
        s += '\n'
        s += leaderboard[i][1]
        s += '\n'
    return s

#returns a string of an integer from a string of a float
def roundString(s):
    return str(int(round_half_up(float(s), 0)))

#regular mathematical rounding
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier