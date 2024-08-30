from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('process-customer-audio/', views.process_customer_audio, name='process_customer_audio'),
    path('process-agent-audio/', views.process_agent_audio, name='process_agent_audio'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)