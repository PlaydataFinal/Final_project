from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import recommend_places, get_answer
from kakaoapi.models import tour_kakao

from pymongo import MongoClient
import pandas as pd
from django.db.models import Count

def home(request): 
    return render(request, 'main.html')

def predict(request): 
    return render(request, 'predict.html')

# def result(request):
#     import numpy as np
#     import pickle

# def index(request):
#     return  render(request, 'index.html')

def index(request):
    tour = tour_kakao.objects.all().annotate(like_count=Count('like')).order_by('-like_count').distinct()[:10]
    content = {"tour" : tour}
    return  render(request, 'index.html', content)

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
        print(output_text)
        return JsonResponse({'output': output_text}, json_dumps_params={'ensure_ascii': False}, status=200)
    else:
        return JsonResponse({'error': 'No input provided.'})

@csrf_exempt
def test(request):
    return render(request, 'recommend.html')
    
@csrf_exempt
def chatbot_solve(request):
    print(f'request : {request}')
    # user_input = request.GET.get('input')
    user_input = request.POST.get('input')
    if user_input:
        # output_text = recommend_places(user_input)
        output_text = get_answer(user_input)
        print(f'output_text : ' + output_text)
        data = {
            'user_input' : user_input,
            'output_text' : output_text
        }
        # return render(request, 'recommend_result.html', data)
        return JsonResponse(data)
    else:
        # return redirect('test')
        return JsonResponse('Error')
    
    
# def get_data_from_mongodb(host, username, password, db_name, collection_name):
#     # MongoDB 연결
#     client = MongoClient(host, username=username, password=password)
#     db = client[db_name]

#     # 데이터 가져오기
#     collection = db[collection_name]
#     data = collection.find()

#     # 데이터프레임으로 변환
#     df = pd.DataFrame(list(data))

#     return df

# MongoDB에서 데이터 가져오기
# df = get_data_from_mongodb('mongodb+srv://admin:admin123@atlascluster.rlgup9y.mongodb.net/jejutext', 
#                         'admin', 'admin123', 'jejutext', 'df')

def chatbot(request):
    return render(request, "simple_chat.html")

def tour_detail(request, tour_id):
    tour_list = tour_kakao.objects.get(id=tour_id)
    tour_all = tour_kakao.objects.all()
    content = {"tour" : tour_list, "tour_all" : tour_all}
    return render(request, "tour_detail.html", content)

