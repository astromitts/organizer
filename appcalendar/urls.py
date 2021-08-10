from django.urls import path
from appcalendar.api import views as api_views


urlpatterns = [
    path('api/dashboard/event/', api_views.EventApi.as_view(), name='event_api'),
    path('api/dashboard/event/<str:event_pk>/', api_views.EventApi.as_view(), name='event_api'),
    path('api/dashboard/goal/', api_views.GoalApi.as_view(), name='dashboard_api'),
    path('api/dashboard/goal/<str:goal_pk>/', api_views.GoalApi.as_view(), name='dashboard_goal_api'),
    path('api/dashboard/goal/<str:goal_pk>/tasks/', api_views.TaskApi.as_view(), name='dashboard_goal_task_api'),
    path('api/dashboard/', api_views.DashboardApi.as_view(), name='dashboard_api'),
]
