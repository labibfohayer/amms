from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoticeListView.as_view()),
    path('create/', views.NoticeCreateView.as_view()),
    path('<int:pk>/', views.NoticeDetailView.as_view()),
    path('<int:pk>/broadcast/', views.NoticeWhatsAppBroadcastView.as_view()),
]
