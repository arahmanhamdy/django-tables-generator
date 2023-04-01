from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Table
from .serializers import TableSerializer, generate_serializer_class


class TableCreateView(generics.CreateAPIView):
    serializer_class = TableSerializer

    def perform_create(self, serializer):
        serializer.save()
        serializer.migrate()


class TableUpdateView(generics.UpdateAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()

    def perform_update(self, serializer):
        serializer.alter_table()
        serializer.save()


class RowListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        model = self._get_model()
        return generate_serializer_class(model)

    def get_queryset(self):
        model = self._get_model()
        return model.objects.all()

    def _get_model(self):
        table_uuid = self.kwargs.get("table_uuid")
        table = get_object_or_404(Table, pk=table_uuid)
        return table.to_django_model()
