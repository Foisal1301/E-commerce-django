from django.urls import path
from . import views

urlpatterns = [
    path('latest_products/',views.LatestProductList.as_view()),
    path('product/search/',views.search),
    path('checkout/', views.checkout),
    path('get_username/', views.get_username),
    path('orders/', views.OrdersList.as_view()), 
    path('product/<slug:category_slug>/<slug:product_slug>/',views.ProductDetail.as_view()),
    path('product/<slug:category_slug>/',views.CategoryDetail.as_view()),
]
