from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIView,ProductImageListCreateAPIView

#___________________________________________________________________________________________
urlpatterns = [
    path("", ProductListCreateAPIView.as_view(), name='product-list'),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name='product-detail'),
    path('product-images/', ProductImageListCreateAPIView.as_view(), name='product-image-list-create'),
]
