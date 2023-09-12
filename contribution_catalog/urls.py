from . import views
from django.urls import path


urlpatterns = [
 
    path('persons/', views.PersonListView.as_view(), name='persons'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),

    path('contributors/', views.ContributorListView.as_view(), name='contributors'),
    path('contributor/<int:pk>', views.ContributorDetailView.as_view(), name='contributor-detail'),

    path('affiliations/', views.AffiliationListView.as_view(), name='affiliations'),
    path('affiliation/<int:pk>', views.AffiliationDetailView.as_view(), name='affiliation-detail'),

    path('contributions/', views.ContributionListView.as_view(), name='contributions'),
    path('contribution/<int:pk>', views.ContributionDetailView.as_view(), name='contribution-detail'),

]