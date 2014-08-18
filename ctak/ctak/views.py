from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

def success(request):
    return render(request, 'home/success.html')
