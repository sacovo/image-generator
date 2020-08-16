from django.urls import path
from images import views

urlpatterns = [
    path('<int:pk>/', views.template_detail_view, name="template_detail"),
    path('<int:pk>/render/', views.generate_image, name="generate_image"),
    path('', views.template_list_view, name="template_list"),
]
