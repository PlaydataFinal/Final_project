from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pymongo import MongoClient
import ast, os

from sentence_transformers import SentenceTransformer

from langchain_community.embeddings import HuggingFaceEmbeddings
import random

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from sklearn.preprocessing import StandardScaler

from langchain_google_genai import ChatGoogleGenerativeAI


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

# def recommend_places(user_input):
#     model_name = "jhgan/ko-sbert-nli"
#     model_kwargs = {'device': 'cpu'}
#     encode_kwargs = {'normalize_embeddings': True}
#     hf = HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs=model_kwargs,
#         encode_kwargs=encode_kwargs
#     )

#     encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')

#     # 사용자 입력 문장 임베딩
#     embedding = encoder.encode(user_input)
# # 데이터프레임의 각 임베딩과 사용자 입력 문장 임베딩 간의 코사인 유사도 계산
#     df['similarity'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [ast.literal_eval(x)]).squeeze())

#     # 유사도가 가장 높은 5개의 장소를 선택
#     answer = df.nlargest(5, 'similarity')
#     # answer 까지는 얼추 맞음
    
#     #names 부터 수정 필요
#     names = answer.sort_values('similarity', ascending=False)['Name'].tolist()[:5]
#     result = df[df['Name'].isin(names)].set_index('Name').loc[names].reset_index()

#     # 추천 장소 이름 출력
# # 추천 장소 이름 출력
#     recommended_names = ", ".join(result['Name'])
#     output_text = f"추천하는 관광지는 {recommended_names}입니다.\n"

#     # 각 장소에 대한 정보 출력
#     for _, row in result.iterrows():
#         text = f"\n{row['Name']}에 대한 정보입니다:\n"
#         text += f"주소는 {row['Address']}에 있습니다.\n"
#         text += f"전화번호는 {row['Tel']}입니다.\n"
#         text += f"상세 정보는 {row['detail_box_elements']}\n"
#         text += "-" * 50 + "\n"
#         output_text += text

#     return output_text

def recommend_places(user_input):
    # 'Hits' 열을 숫자형으로 변환
    df['Hits'] = pd.to_numeric(df['Hits'], errors='coerce')

    # SentenceTransformer로 사용자 입력 문장 임베딩
    encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')
    embedding = encoder.encode(user_input)

    # 데이터프레임의 각 임베딩과 사용자 입력 문장 임베딩 간의 코사인 유사도 계산
    df['similarity'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [ast.literal_eval(x)]).squeeze())

    # 유사도가 가장 높은 상위 20개의 장소 선택
    top_20_similar = df.nlargest(20, 'similarity')

    # 방문 횟수가 높은 상위 3개의 장소 선택
    top_3_hits = top_20_similar.nlargest(3, 'Hits')

    # 선택된 장소들에 대한 정보 추출
    answer = top_3_hits[['Name', 'Address', 'detail_box_elements']]

    # 선택된 장소들을 문자열로 변환하여 반환
    text_list = []
    for index, row in answer.iterrows():
        text = ''
        for column in answer.columns:
            text += f'{column}은 {row[column]}이고, '

        # 마지막에 쉼표 제거
        text = text[:-2]

        text_list.append(text + '\n')

    # 리스트를 하나의 문자열로 변환
    text_data = ''.join(text_list)
    
    return text_data


def get_answer(user_input):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyAPWz4S7KJA0spMwfdwBBa6nA8XnsoeByw"
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    # Hugging Face Embeddings 설정
    model_name = "jhgan/ko-sbert-nli"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    # 질문 템플릿 설정
    template = """Answer the question as based only on the following context:
    {context} 한국어로 대답하고 자료 안에 있는 내용으로 대답해. 자료 안의 내용들을 최대한 포함해서 대답해.
    질문에 답변할 때는 질문을 언급하고 시작해. 친절하고 경어체로 대답해. 문맥 자연스럽게 대답해.

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # ChatGoogleGenerativeAI 모델 설정
    gemini = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    # Runnable Map 설정
    chain = RunnableMap({
        "context": lambda x: x['text_data'],  # Use text_data as context
        "question": lambda x: x['question']  # Use the provided question
    }) | prompt | gemini
    
    # 사용자의 질문에 대한 관련 장소 추천
    text_data = recommend_places(user_input)
    
    # 챗봇이 답변 생성
    result = chain.invoke({'text_data': text_data, 'question': user_input})
    
    return result.content