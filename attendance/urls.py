from django.urls import path
from . import views

urlpatterns = [
    path('', views.farmer_list, name='farmer_list'),
    path('create/', views.farmer_create, name='farmer_create'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('api/farmers/', views.farmer_list_api, name='farmer_list_api'),
    path('<int:farmer_id>/', views.farmer_detail, name='farmer_detail'),
    path('<int:farmer_id>/update/', views.farmer_update, name='farmer_update'),
    path('<int:farmer_id>/delete/', views.farmer_delete, name='farmer_delete'),
]