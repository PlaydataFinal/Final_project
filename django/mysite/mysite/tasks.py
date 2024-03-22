# # tasks.py

# from django.utils.deprecation import MiddlewareMixin
# from celery import Celery
# from kakaoapi.models import tour_kakao
# from django.db.models import Count

# app = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq//')

# class CeleryMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # 사용자 요청이 들어올 때마다 Celery에 비동기 작업을 요청합니다.
#         process_index.delay(request.GET.get('data'))

# @app.task
# def process_index(data):
#     tour_even = tour_kakao.objects.all().annotate(like_count=Count('like')).order_by('-like_count').distinct()[:10:2]
#     tour_odd = tour_kakao.objects.all().annotate(like_count=Count('like')).order_by('-like_count').distinct()[1:10:2]
#     content = {
#         'content' : dict(zip(tour_even, tour_odd))
#     }
#     return content
