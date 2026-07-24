from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Comment

# Create your views here.
def home(request):
    articles = Article.objects.all()
    return render(request, 'blogapp/home.html', {'articles' : articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'blogapp/article_detail.html', {'article': article})

def like_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        liked_articles = request.session.get('liked_articles', [])

        if article.slug in liked_articles:
            if article.likes > 0:
                article.likes -= 1
            liked_articles.remove(article.slug)
            button_text = "Like"
        else:
            article.likes += 1
            liked_articles.append(article.slug)
            button_text = "Liked ❤️"

        request.session['liked_articles'] = liked_articles
        request.session.modified = True
        article.save()


        context = f"""
        <span>Likes: {article.likes}</span>
        <button hx-post="/article/{article.slug}/like/" hx-target="#like-section">{button_text}</button>
        """
        return HttpResponse(context)


def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method=="POST":
        name = request.POST.get('name')
        body = request.POST.get('body')

        Comment.objects.create(article=article, name=name, body=body)

        return render(request, 'blogapp/comments_partial.html', {'article': article})