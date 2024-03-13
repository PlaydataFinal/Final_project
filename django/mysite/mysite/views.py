from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import recommend_places, get_answer, get_data_from_mongodb
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
    
# @csrf_exempt
# def chatbot_solve(request):
#     print(f'request : {request}')
#     # user_input = request.GET.get('input')
#     user_input = request.POST.get('input')
#     if user_input:
#         # output_text = recommend_places(user_input)
#         output_text = get_answer(user_input)
#         print(f'output_text : ' + output_text)
#         data = {
#             'user_input' : user_input,
#             'output_text' : output_text
#         }
#         # return render(request, 'recommend_result.html', data)
#         return JsonResponse(data)
#     else:
#         # return redirect('test')
#         return JsonResponse('Error')
    
    # MongoDB에서 데이터 가져오기
df1 = get_data_from_mongodb('mongodb+srv://admin:admin123@atlascluster.rlgup9y.mongodb.net/jejutext',
                            'admin', 'admin123', 'jejutext', 'tour_df')

df2 = get_data_from_mongodb('mongodb+srv://admin:admin123@atlascluster.rlgup9y.mongodb.net/jejutext',
                            'admin', 'admin123', 'jejutext', 'food_df')

df3 = get_data_from_mongodb('mongodb+srv://admin:admin123@atlascluster.rlgup9y.mongodb.net/jejutext',
                            'admin', 'admin123', 'jejutext', 'sleep_df')

def get_selected_df(selected_number):
    if selected_number == 1:
        return df1
    elif selected_number == 2:
        return df2
    elif selected_number == 3:
        return df3
    else:
        raise ValueError("Invalid selected number.")
    



@csrf_exempt
def chatbot_solve(request):
    if request.method == 'POST':
        user_input = request.POST.get('input')
        selected_number = request.POST.get('selected_number')
        
        if selected_number is None:
            return JsonResponse({'error': 'Please select a number (1, 2, or 3).'}, status=400)

        selected_number = int(selected_number)
        
        try:
            selected_df = get_selected_df(selected_number)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        if user_input:
            text_data = recommend_places(selected_df, user_input)

            # 수정된 부분: get_answer 함수 호출 시 사용자의 질문 전달
            result = get_answer(user_input)
            
            return JsonResponse({'output': result}, json_dumps_params={'ensure_ascii': False}, status=200)
        else:
            return JsonResponse({'error': 'Invalid input. Please try again.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def chatbot(request):
    return render(request, "simple_chat.html")

def tour_detail(request, tour_id):
    tour_list = tour_kakao.objects.get(id=tour_id)
    tour_all = tour_kakao.objects.all()
    content = {"tour" : tour_list, "tour_all" : tour_all}
    return render(request, "tour_detail.html", content)

