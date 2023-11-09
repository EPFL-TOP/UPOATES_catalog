from . import views
from django.urls import path


urlpatterns = [
 
    path('analyses/', views.AnalysisListView.as_view(), name='analyses'),
    path('analysis/<int:pk>', views.AnalysisDetailView.as_view(), name='analysis-detail'),

]