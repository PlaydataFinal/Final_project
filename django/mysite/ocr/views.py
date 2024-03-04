# Create your views here.
# ocr/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ocr1 import preprocess_image, loaded_model, label_encoder
import base64


# Create your views here.
def index(request):
    return render(request, 'ocr/ocr.html')

def predict(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file')
        contents = image_file.read()
        image_base64 = base64.b64encode(contents).decode("utf-8")
        input_image = preprocess_image(base64.b64decode(image_base64))
        predictions = loaded_model.predict(input_image)
        predicted_label_encoded = np.argmax(predictions, axis=1)
        predicted_labels = label_encoder.inverse_transform([predicted_label_encoded])[0]
        image_url = "/static/uploaded_image.jpg"
        return render(request, "ocr/ocr.html", {"result": predicted_labels, "image_url": image_url})
    return JsonResponse({"error": "Invalid request method"})