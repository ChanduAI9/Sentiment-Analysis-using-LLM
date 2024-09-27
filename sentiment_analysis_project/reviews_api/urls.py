from django.urls import path
from .views import FileUploadView, index

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('', index, name='index'),
]
