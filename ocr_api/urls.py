from django.urls import path
from ocr_api.views import Ocr,OcrDetail

urlpatterns = [
    path('', Ocr.as_view()),
    path('<str:report_id>', OcrDetail.as_view())
]