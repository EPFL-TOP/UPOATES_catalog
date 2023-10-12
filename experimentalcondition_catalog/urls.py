from . import views
from django.urls import path


urlpatterns = [
    path('experimentalconditions/', views.ExperimentalConditionListView.as_view(), name='experimentalconditions'),
    path('experimentalcondition/<int:pk>', views.ExperimentaConditionDetailView.as_view(), name='experimentalcondition-detail'),
]

