from django.shortcuts import render
from rest_framework import generics
from .models import tour_kakao, tour_comment
from .serializers import TourKakaoSerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from django.http import HttpResponse

from django.http import HttpResponseNotAllowed
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from common.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, 'kakaoapi/kakao.html')# kakaoapi/views.py
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 15  # 한 페이지당 아이템 수
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class TourKakaoList(generics.ListAPIView):
    serializer_class = TourKakaoSerializer
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return tour_kakao.objects.filter(Name__icontains=keyword)
    
def tour_detail(request, tour_id):
    tour_list = tour_kakao.objects.get(id=tour_id)
    tour = {"tour" : tour_list}
    return render(request, "tour_detail.html", tour)

def comment_create(request, tour_id):
    tour = get_object_or_404(tour_kakao, pk=tour_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.tour = tour
            comment.author = request.user
            comment.save()
            return redirect('kakaoapi:tour_detail', tour_id=tour.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'tour': tour, 'form': form}
    return render(request, 'tour_detail.html', context)

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(tour_comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('kakaoapi:tour_detail', tour_id=comment.tour.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
        return redirect('kakaoapi:tour_detail', tour_id=comment.tour.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'kakaoapi/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(tour_comment, pk=comment_id)
    print(f'comment_id : {comment_id}\ncomment : {comment.comment}')
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('kakaoapi:tour_detail', tour_id=comment.tour.id)