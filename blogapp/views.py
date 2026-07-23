from django.shortcuts import render
from .models import Article

# Create your views here.
def home(request):
    articles = Article.subject.all()
    return render(request, 'blogapp/home.html', {'articles' : articles})