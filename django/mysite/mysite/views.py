from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import recommend_places, get_answer

from pymongo import MongoClient
import pandas as pd
import random

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
        print(output_text)
        return JsonResponse({'output': output_text}, json_dumps_params={'ensure_ascii': False}, status=200)
    else:
        return JsonResponse({'error': 'No input provided.'})

@csrf_exempt
def test(request):
    return render(request, 'recommend.html')
    
@csrf_exempt
def test2(request):
    user_input = request.GET.get('input')
    if user_input:
        # output_text = recommend_places(user_input)
        output_text = get_answer(user_input)
        data = {
            'user_input' : user_input,
            'output_text' : output_text
        }
        return render(request, 'recommend_result.html', data)
    else:
        return redirect('test')
    
    
def get_data_from_mongodb(host, username, password, db_name, collection_name):
    # MongoDB 연결
    client = MongoClient(host, username=username, password=password)
    db = client[db_name]

    # 데이터 가져오기
    collection = db[collection_name]
    data = collection.find()

    # 데이터프레임으로 변환
    df = pd.DataFrame(list(data))

    return df

# MongoDB에서 데이터 가져오기
df = get_data_from_mongodb('mongodb+srv://admin:admin123@atlascluster.rlgup9y.mongodb.net/jejutext', 
                        'admin', 'admin123', 'jejutext', 'df')

    
def test3(request):
    input_num = request.GET.get('input_num')
    print(f'input_num : {input_num}')
    if input_num == None:
        input_num = random.randrange(0, len(df) + 1)
    else:
        try:
            input_num = int(input_num)
        except:
            print('error')
            messages.warning(request, "숫자만 입력하세요")
            return redirect('test3')
    df['addr_id'] = 0
    for x in range(0, len(df)):
        df.loc[x, 'addr_id'] = x
    data = {
        'name' : df['Name'][input_num],
        'image_url' : df['Image URL'][input_num].replace('"', ''),
        'address' : df['Address'][input_num]
    }
    return render(request, 'test3.html', data)

def test4(request):
    return render(request, "simple_chat.html")