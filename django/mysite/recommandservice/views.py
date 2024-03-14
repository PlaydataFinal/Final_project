from django.shortcuts import render

# Create your views here.

import pandas as pd
import os 
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def index(request):
    return render(request, 'recommandservice/recommandservice.html')


df = pd.read_csv('./vector_csv4.csv')

# 이미지 벡터를 배열로 변환
all_vectors = np.array(df['Image Vector'].apply(lambda x: np.array(eval(x))).tolist())

# 모든 이미지 간의 코사인 유사도 계산
similarities_all = cosine_similarity(all_vectors)

# 유사도를 데이터프레임에 저장
similarities_df = pd.DataFrame(similarities_all, index=df['Image Name'], columns=df['Image Name'])

# 'nan.jpg' 관련 데이터 삭제(이상한거 들어있어서 삭제)
similarities_df = similarities_df.drop('nan.jpg', axis=0)  # 행 삭제
similarities_df = similarities_df.drop('nan.jpg', axis=1)  # 열 삭제


import random

def select_destinations(similarities_df, num=2, max_attempts=100):
    selected_destinations = []
    attempts = 0
    while len(selected_destinations) < num and attempts < max_attempts:
        dest1, dest2 = random.sample(similarities_df['Image Name'].tolist(), 2)
        
        # 유사도가 0.15 이하인 관광지를 선택할 때까지 반복
        while True:
            similarity = similarities_df[(similarities_df['Image Name'] == dest1) & (similarities_df['Image Name'] == dest2)].iloc[:, 1:].values.flatten()
            if similarity.size == 0 or similarity[0] <= 0.15:
                break
            dest1, dest2 = random.sample(similarities_df['Image Name'].tolist(), 2)
        
        selected_destinations.append((dest1, dest2))
        attempts += 1
    return selected_destinations

def find_similar_destinations(selected_destinations, similarities_df, top_n=1):
    similar_destinations = {}
    for dest1, dest2 in selected_destinations:
        similar_destinations[(dest1, dest2)] = []
        for dest in [dest1, dest2]:
            similarity_row = similarities_df[similarities_df['Image Name'] == dest].iloc[:, 1:].values.flatten()
            similar_indices = np.argsort(similarity_row)[::-1][1:top_n+1]  # 제외하고 가장 유사한 인덱스 선택
            similar_destinations[(dest1, dest2)].extend([(similarities_df.iloc[i]['Image Name'], similarity_row[i]) for i in similar_indices])
    return similar_destinations

# 랜덤한 관광지 3개 선택 후 유사한 관광지 찾기
selected_destinations = select_destinations(similarities_df, num=3)
similar_destinations = find_similar_destinations(selected_destinations, similarities_df)

# 선택한 관광지와 가장 유사한 관광지 출력
for dest1, dest2 in selected_destinations:
    print("랜덤한 관광지 두 개를 선택하세요:")
    print("1.", dest1)
    print("2.", dest2)
    user_choice = input("선택하세요 (1 또는 2): ")
    chosen_dest = dest1 if user_choice == '1' else dest2
    print(f"선택한 관광지: {chosen_dest}")
    
    similar_list = similar_destinations[(dest1, dest2)]
    for i, (similar_dest, similarity) in enumerate(similar_list, start=1):
        print(f"{i}번째로 유사한 관광지: {similar_dest}, Similarity: {similarity:.4f}")
    print()

# 최종 추천: 선택한 관광지의 첫 번째로 유사한 관광지들
print("최종 추천:")
for chosen_dest1, chosen_dest2 in selected_destinations:
    similar_list1 = similar_destinations[(chosen_dest1, chosen_dest2)]
    first_similar_dest1, first_similarity1 = similar_list1[0]
    first_similar_dest2, first_similarity2 = similar_list1[1]
    print(f"{chosen_dest1}의 최종 추천: {first_similar_dest1}, Similarity: {first_similarity1:.4f}")
    print(f"{chosen_dest2}의 최종 추천: {first_similar_dest2}, Similarity: {first_similarity2:.4f}")



