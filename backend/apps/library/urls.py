from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('books', views.BookViewSet)
router.register('issues', views.BookIssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
