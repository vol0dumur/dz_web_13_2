from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author

# Create your views here.
def main(request):
    quotes = Quote.objects.filter(user=request.user).all() if request.user.is_authenticated else Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


def authors(request):
    authors = Author.objects.all()
    return render(request, 'quoteapp/authors.html', {"authors": authors})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': QuoteForm()})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quoteapp:main')
    else:
        form = AuthorForm()

    return render(request, 'quoteapp/author.html', {'form': form})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoteapp/detail.html', {"quote": quote})


def detail_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/detail_author.html', {"author": author})


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='quoteapp:main')


@login_required
def delete_author(request, author_id):
    Author.objects.get(pk=author_id).delete()
    return redirect(to='quoteapp:main')