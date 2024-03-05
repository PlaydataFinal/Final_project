# ocr_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap

def index(request):
    return render(request, 'ocr_app/process_image.html')

def process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # 이미지를 서버에 저장
        uploaded_image = request.FILES['image']
        image_path = default_storage.save('uploaded_image.jpg', uploaded_image)

        # PaddleOCR 초기화
        ocr = PaddleOCR(lang="korean")

        # 이미지 처리 및 OCR 수행
        img = Image.open(image_path)
        result = ocr.ocr(img, cls=False)
        x_values_list = [result[0][i][1][0] for i in range(len(result[0]))]
        combined_string = ' '.join(x_values_list)

        # HuggingFace 및 ChatGoogleGenerativeAI 초기화
        model_name = "jhgan/ko-sbert-nli"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True}
        hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        template = """Answer the question as based only on the following context:
        {context}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        gemini = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

        # Runnable Map 구성
        chain = RunnableMap({
            "context": lambda x: x['combined_string'],
            "question": lambda x: x['question']
        }) | prompt | gemini

        # 질문 정의
        question = "여기 가게 이름이 뭐야? 가격은 얼마야? 날짜는 언제야? 표로 만들어줘."

        # Runnable Map 실행
        response_content = chain.invoke({'combined_string': combined_string, 'question': question}).content

        # 결과를 HTML 페이지로 렌더링
        return render(request, 'process_image.html', {'result': response_content})

    return render(request, 'process_image.html', {'result': None})
