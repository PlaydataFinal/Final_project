# ezocr/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import EzocrResult
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from django.template.defaultfilters import safe
from langchain.schema.runnable import RunnableMap
import easyocr
import cv2
import imutils
from imutils.perspective import four_point_transform
from PIL import Image
from django.conf import settings
import os
from django.http import HttpResponse
import json

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
# Hugging Face Embeddings 설정
model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Chat Prompt Template
template = """Answer the question as based only on the following context:
{context} 여기서 너가 생각하기에 가격인 것 같은 부분, 가게이름인 것 같은 부분, 날짜 및 시간인 부분을 알려줘.

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# ChatGoogleGenerativeAI model
gemini = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

def preprocess_receipt(image_path):
    image = cv2.imread(image_path)
    transformed_image = find_contour_and_transform(image)
    return transformed_image

def find_contour_and_transform(image):
    ratio = image.shape[0] / 500.0
    org_image = image.copy()
    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 0, 40)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt is None:
        return org_image
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    transform_image = four_point_transform(org_image, screenCnt.reshape(4, 2) * ratio)
    return transform_image

def enhance_contrast(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return enhanced

def ezocr(request):
    if request.method == 'POST':
        image = request.FILES['image']
        image_path = f"/home/ubuntu/Final_project/django/mysite/static/images/{image.name}"
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        preprocessed_image = preprocess_receipt(image_path)
        enhance_preprocessed_image = enhance_contrast(preprocessed_image)

        reader = easyocr.Reader(['ko'])
        results = reader.readtext(enhance_preprocessed_image)
        x_values_list = [results[i][1] for i in range(len(results))]
        combined_string = ' '.join(x_values_list)

        chain = RunnableMap({
            "context": lambda x: x['combined_string'],
            "question": lambda x: x['question']
        }) | prompt | gemini

        answer = chain.invoke({'combined_string': combined_string, 'question': "여기 가게 이름이 뭐야? 가격은 얼마야? 날짜는 언제야? 표로 만들어줘."}).content

        EzocrResult.objects.create(context=combined_string, question="여기 가게 이름이 뭐야? 가격은 얼마야? 날짜는 언제야? 표로 만들어줘.", answer=answer)

        response_data = {'answer': answer}
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type='application/json')

    return render(request, 'ezocr/ezocr.html')
