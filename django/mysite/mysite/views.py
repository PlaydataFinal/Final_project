from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import recommend_places, get_answer
from kakaoapi.models import tour_kakao

from django.db.models import Count

def home(request): 
    return render(request, 'main.html')

def index(request):
    tour_even = tour_kakao.objects.all().annotate(like_count=Count('like')).order_by('-like_count').distinct()[:10:2]
    tour_odd = tour_kakao.objects.all().annotate(like_count=Count('like')).order_by('-like_count').distinct()[1:10:2]
    content = {
        'content' : dict(zip(tour_even, tour_odd))
    }
    return  render(request, 'index.html', content)

def main(request):
    return render(request, 'main.html')

@csrf_exempt
def recommend_view(request):
    user_input = request.GET.get('input')
    if user_input:
        output_text = recommend_places(user_input)
        return JsonResponse({'output': output_text}, json_dumps_params={'ensure_ascii': False}, status=200)
    else:
        return JsonResponse({'error': 'No input provided.'})
    
def chatbot(request):
    return render(request, "simple_chat.html")
    
@csrf_exempt
def chatbot_solve(request):
    user_input = request.POST.get('input')
    if user_input:
        output_text = get_answer(user_input)
        data = {
            'user_input' : user_input,
            'output_text' : output_text
        }
        return JsonResponse(data)
    else:
        return JsonResponse('Error')
