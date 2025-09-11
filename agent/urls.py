from django.urls import path
from . import views

urlpatterns = [
    path('agents/', views.AgentProfileListCreateAPIView.as_view(), name='agent_list_create'),
    path('agents/<int:pk>/', views.AgentProfileDetailAPIView.as_view(), name='agent_detail'),
]