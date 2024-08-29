from django import forms
from .models import tour_comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = tour_comment
        fields = ['comment']
        labels = {
            'comment': '답변내용',
        }