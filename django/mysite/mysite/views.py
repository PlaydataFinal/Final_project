from django.shortcuts import render
from django.http import HttpResponse




from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
# # 데이터 로딩
df_place = pd.read_csv('C:\\travel\django\mysite\data\\tour_place.csv')
# # vectorizer와 tag_vectors를 전역 변수로 정의
# vectorizer_place = TfidfVectorizer()
# tag_vectors_place = vectorizer_place.fit_transform(df_place['tour_place_tag'])
# CSV 파일 불러오기
# df_food = pd.read_csv('./data/tour_food.csv')
# 데이터 프레임에서 tour_place_tag를 리스트로 추출
tags_list_place = df_place['tour_place_tag'].tolist()
# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
tag_vectors_place = vectorizer.fit_transform(tags_list_place)
# 코사인 유사도 계산
similarity_matrix_place = cosine_similarity(tag_vectors_place)
# 유사도 행렬을 데이터프레임으로 변환
similarity_df_place = pd.DataFrame(similarity_matrix_place, columns=df_place['tour_place'], index=df_place['tour_place'])
def find_similar_places(request):
    if request.method == 'POST':
        input_place = request.POST.get('input_place', '')
        similar_places = calculate_similarity(input_place)
        return render(request, 'result.html', {'input_place': input_place, 'similar_places': similar_places})
    else:
        return render(request, 'index.html')
def calculate_similarity(input_text):
    # 여기서 input_text와 유사도를 계산하는 코드를 삽입
    # input_vector = vectorizer_place.transform([input_text])
    # similarity_scores = cosine_similarity(input_vector, tag_vectors_place).flatten()
    # related_indices = similarity_scores.argsort()[:-4:-1]  # 상위 3개 결과
    # related_places = df_place.loc[related_indices, 'tour_place'].tolist()
    choice_place = input_text
    related_places = similarity_df_place[choice_place].sort_values(ascending=False)
    top_related_places = related_places.index[1:4]
    return top_related_places





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