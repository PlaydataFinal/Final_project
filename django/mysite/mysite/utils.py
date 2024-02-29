from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pymongo import MongoClient
import ast

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

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
                           'admin', 'admin123', 'jejutext', 'text')




def recommend_places(user_input):
    model_name = "jhgan/ko-sbert-nli"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')

    # 사용자 입력 문장 임베딩
    embedding = encoder.encode(user_input)
    print(df.columns)
# 데이터프레임의 각 임베딩과 사용자 입력 문장 임베딩 간의 코사인 유사도 계산
    df['similarity'] = df['vector'].map(lambda x: cosine_similarity([embedding], [ast.literal_eval(x)]).squeeze())

    # 유사도가 가장 높은 5개의 장소를 선택
    answer = df.nlargest(5, 'similarity')
    names = answer.sort_values('similarity', ascending=False)[14].tolist()[:5]
    result = df[df[14].isin(names)].set_index(14).loc[names].reset_index()

    # 추천 장소 이름 출력
    recommended_names = ", ".join(result[14])
    output_text = f"추천하는 관광지는 {recommended_names}입니다.\n"

    # 각 장소에 대한 정보 출력
    for _, row in result.iterrows():
        text = f"\n{row[14]}에 대한 정보입니다:\n"
        text += f"주소는 {row[3]}에 있습니다.\n"
        text += f"전화번호는 {row[4]}입니다.\n"
        text += f"상세 정보는 {row[11]}\n"
        text += "-" * 50 + "\n"
        output_text += text

    return output_text