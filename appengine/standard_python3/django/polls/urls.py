from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('products', views.products, name="products"),
    path('payment', views.payment, name="payment"),
    path('thanks', views.thanks, name="thanks"),
    path('product/<str:pid>', views.product, name="product"),
    path('basket', views.basket, name="basket"),
    path('searchResults', views.searchResults, name="searchResults"),
]
