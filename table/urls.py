from django.urls import path

from .views import TableCreateView, TableUpdateView, RowListCreateView

urlpatterns = [
    path('', TableCreateView.as_view()),
    path('<uuid:pk>', TableUpdateView.as_view()),
    path('<uuid:table_uuid>/row', RowListCreateView.as_view()),
    path('<uuid:table_uuid>/rows', RowListCreateView.as_view()),
]
