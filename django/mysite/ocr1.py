# ocr.py

from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from sklearn.preprocessing import LabelEncoder
import boto3
import joblib 




#S3 설정
aws_access_key_id = 'AKIA2UYLYPVJMZYQGZW2'
aws_secret_access_key = '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'
s3_bucket = 'jeju-bucket' 
s3_model_key = 'tour/ocr.h5'

# 모델 다운로드
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
model_path_local = 'ocr.h5'
s3.download_file(s3_bucket, s3_model_key, model_path_local)



# Load the trained OCR model
loaded_model = load_model(model_path_local)
#Load the label encoder
#저장된 라벨 인코더를 불러오기
label_encoder = joblib.load('label_encoder.joblib')



class Image(BaseModel):
    file: UploadFile

def preprocess_image(img):
    img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)
    return img

app = FastAPI()





@app.post("/predict")
async def predict(file: UploadFile):
    contents = await file.read()
    # Decode Base64
    image_base64 = base64.b64encode(contents).decode("utf-8")

    # Preprocess the image
    input_image = preprocess_image(base64.b64decode(image_base64))
    
    # Make predictions using the loaded model
    predictions = loaded_model.predict(input_image)
    
    # Assuming predictions is a list or array of results
    predicted_label_encoded = np.argmax(predictions, axis=1)
    #label_encoder = LabelEncoder()
    predicted_labels = label_encoder.inverse_transform([predicted_label_encoded])[0]

    return JSONResponse(content=predicted_labels)