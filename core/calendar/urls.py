
from django.urls import path
from core.calendar import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/day/<int:year>/<int:month>/<int:day>/', views.event_day, name='event_day'),
    path('events/week/<int:year>/<int:week>/', views.event_week, name='event_week'),
    path('events/month/<int:year>/<int:month>/', views.event_month, name='event_month'),
    path('events/year/<int:year>/', views.event_year, name='event_year'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/add/<int:year>/<int:month>/<int:day>/', views.event_add, name='event_add_with_date'),
    path('events/import/', views.event_import, name='event_import'),
    path('events/export/', views.event_export, name='event_export_all'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
    path('events/<int:id>/export/', views.event_export, name='event_export'),
    path('events/<int:id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:id>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:id>/move/<int:days>/<int:minutes>/', views.event_move, name='event_move'),
    path('events/<int:id>/resize/<int:days>/<int:minutes>/', views.event_resize, name='event_resize'),
    path('events/<int:id>/timeline/', views.event_detail, {'template_name': 'calendar/event_timeline.html'}, name='event_timeline'),
]
