from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('quote/', views.quote, name='quote'),
    path('author/', views.author, name='author'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>', views.detail_author, name='detail_author'),
    path('delete_author/<int:author_id>/', views.delete_author, name='delete_author'),
]