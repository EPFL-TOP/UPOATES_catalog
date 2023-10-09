from . import views
from django.urls import path


urlpatterns = [
 
    path('experiments/', views.ExperimentListView.as_view(), name='experiments'),
    path('experiment/<int:pk>', views.ExperimentDetailView.as_view(), name='experiment-detail'),

]