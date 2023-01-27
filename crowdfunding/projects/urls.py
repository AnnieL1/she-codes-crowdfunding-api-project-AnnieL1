from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from . import views 

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('pledges/<int:pk>/', views.PledgeDetail.as_view()),
    path('stretch_goals/', views.StretchGoalsList.as_view()),
    path('stretch_goals/<int:pk>', views.StretchGoalsDetail.as_view()),
    # path('pledges/delete/<int:pk>/', views.DeletePledge.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)