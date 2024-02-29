from django.shortcuts import render
from django.http import HttpResponse

<<<<<<< HEAD




=======
>>>>>>> 66526a717ce1445670311a4bb76384a50e3a18f0
def home(request): 
    return render(request, 'main.html')

def predict(request): 
    return render(request, 'predict.html')

# def result(request):
#     import numpy as np
#     import pickle

def index(request):
    return  render(request, 'index.html')

def index_view(request):
    return render(request, 'main.html')

def result(request):
    return render(request, 'result.html')

def main(request):
    return render(request, 'main.html')