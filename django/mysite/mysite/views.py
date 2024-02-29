from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import recommend_places

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

@csrf_exempt
def recommend_view(request):
    print(f'request : {request}')
    user_input = request.GET.get('input')
    print(f'user_input : {user_input}')
    if user_input:
        output_text = recommend_places(user_input)
        return JsonResponse({'output': output_text})
    else:
        return JsonResponse({'error': 'No input provided.'})
