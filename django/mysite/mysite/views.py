from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import recommend_places, get_answer, get_selected_df
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
    
def chatbot(request):
    return render(request, "simple_chat.html")


@csrf_exempt
def chatbot_solve(request):
    if request.method == 'POST':
        user_input = request.POST.get('input')
        selected_number = request.POST.get('selected_number')
        
        if selected_number is None:
            return JsonResponse({'error': 'Please select a number (1, 2, or 3).'}, status=400)

        selected_number = int(selected_number)
        
        try:
            selected_df = get_selected_df(selected_number)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        if user_input:
            text_data = recommend_places(selected_df, user_input)
            # 수정된 부분: get_answer 함수 호출 시 사용자의 질문 전달
            result = get_answer(user_input, text_data)
            
            return JsonResponse({'output': result}, json_dumps_params={'ensure_ascii': False}, status=200)
        else:
            return JsonResponse({'error': 'Invalid input. Please try again.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)