from django.shortcuts import render

# Create your views here.

import pandas as pd
import os 
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def index(request):
    return render(request, 'recommandservice/recommandservice.html')


