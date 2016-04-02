from django.conf.urls import url
from schedule_cab import views as schedule_cab_views

schedules = schedule_cab_views.SchedulesListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    url(r'^$', schedules, name='schedules-list'),
    url(r'^products/$', schedule_cab_views.uber_products),
]
