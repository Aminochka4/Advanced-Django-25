from django.urls import path
from .views import export_csv, export_pdf, generate_report

urlpatterns = [
    path('export/csv/', export_csv, name='export_csv'),
    path('export/pdf/', export_pdf, name='export_pdf'),
    path("report/", generate_report, name="generate_report"),
]
