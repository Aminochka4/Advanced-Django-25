from django.urls import path
from .views import contact_view, share_cv_email, success_view

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success'),
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email')
]
