from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Article, Comment

# Create your views here.
def home(request):
    articles = Article.objects.all()
    return render(request, 'blogapp/home.html', {'articles' : articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    my_comments = request.session.get('my_comments', [])

    context = {
        'article' : article,
        'my_comments' : my_comments,
    }

    return render(request, 'blogapp/article_detail.html', context)

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
    
    if request.method == 'POST':
        name = request.POST.get('name')
        body = request.POST.get('body')
        
        if name and body:
            comment = Comment.objects.create(article=article, name=name, body=body)

            my_comments = request.session.get('my_comments', [])
            my_comments.append(comment.id)
            request.session['my_comments'] = my_comments
            request.session.modified = True
            
            article.refresh_from_db()

    my_comments = request.session.get('my_comments', [])
    context = {
        'article': article,
        'my_comments': my_comments
    }
    return render(request, 'blogapp/comments_partial.html', context)


def delete_comment(request, comment_id):
    my_comments = request.session.get('my_comments', [])

    if comment_id in my_comments:
        comment = get_object_or_404(Comment, id=comment_id)
        article = comment.article

        comment.delete()

        my_comments.remove(comment_id)
        request.session['my_comments'] = my_comments

        context = {
            'article' : article,
            'my_comments' : my_comments,
        }

        return render(request, 'blogapp/comments_partial.html', context)
    return HttpResponseForbidden("You Cannot Delete This Comment!")


def edit_comment(request, comment_id):
    my_comments = request.session.get('my_comments', [])

    if comment_id not in my_comments:
        return HttpResponseForbidden("You Cannot Edit This Comment!")

    comment = get_object_or_404(Comment, id=comment_id)

    if request.method=='POST':
        new_body = request.POST.get('body')
        if new_body:
            comment.body = new_body
            comment.save()

        context = {'comment': comment, 'my_comments': my_comments}
        return render(request, 'blogapp/single_comment_partial.html', context)

    return render(request, 'blogapp/comment_edit_partial.html', {'comment': comment})