#mysite/utils.py
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

#df = pd.read_csv('./tour_index_vectorized_list.csv')

def recommend_places(df,user_input):
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
 # 일반 유사도 계산
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity([embedding], [x]).squeeze())
    
    # 유사도가 가장 높은 상위 40개의 장소 선택
    top_40_similar = df.nlargest(40, 'similarity')
    
    # 태그 유사도 계산
    top_40_similar['tag_similarity'] = top_40_similar['tag_embedding'].apply(lambda x: cosine_similarity([embedding], [x]).squeeze())

    # 태그 유사도가 가장 높은 상위 10개의 장소 선택 
    top_10_tag_similar = top_40_similar.nlargest(10, 'tag_similarity')

    # 조회수가 높은 상위 3개의 장소 선택
    top_3_hits = top_10_tag_similar.nlargest(3, 'Hits')

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

def get_answer(user_input, text_data):
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
    {context} Please answer in Korean and only use the information provided in the data. Summarize the contents of the data and respond accordingly.
    When you answer a question, start with "I'll answer the question" and answer it. If the number of items is not specified, answer with 3 items. 
    If the number of items is specified, respond accordingly. Include as many elements from the data columns as possible in your response.
    Please answer in written language. When you answer the 'detail_box_elements' element, please answer it with 'information'
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
        
        
    # 챗봇이 답변 생성
    result = chain.invoke({'text_data': text_data, 'question': user_input})
        
    return result.content

# # MongoDB에서 데이터 가져오기
df1 = get_data_from_mongodb('mongodb+srv://joowan119:admin123@atlascluster.gq7ssmg.mongodb.net/jejutext',
                            'joowan119', 'admin123', 'jejutext', 'df')

df2 = get_data_from_mongodb('mongodb+srv://joowan119:admin123@atlascluster.gq7ssmg.mongodb.net/jejutext',
                            'joowan119', 'admin123', 'jejutext', 'food_df')

df3 = get_data_from_mongodb('mongodb+srv://joowan119:admin123@atlascluster.gq7ssmg.mongodb.net/jejutext',
                            'joowan119', 'admin123', 'jejutext', 'sleep_df')

def get_selected_df(selected_number):
    if selected_number == 1:
        return df1
    elif selected_number == 2:
        return df2
    elif selected_number == 3:
        return df3
    else:
        raise ValueError("Invalid selected number.")
    