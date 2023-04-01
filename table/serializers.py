from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework import serializers
from .models import Table, Field


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("title", "data_type")


class TableSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, required=True)

    class Meta:
        model = Table
        fields = ("id", "fields")

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        table = super().create(validated_data)
        for field_data in fields_data:
            Field.objects.create(table=table, **field_data)
        return table

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields')
        table = super().update(instance, validated_data)
        table.fields.all().delete()
        for field_data in fields_data:
            Field.objects.create(table=table, **field_data)
        return table

    def migrate(self):
        self.instance.migrate()

    def alter_table(self):
        updated_fields_data = self.validated_data["fields"]
        try:
            self.instance.alter(updated_fields_data)
        except IntegrityError:
            raise ValidationError({"error": "you can't alter this table as it is not empty"})


def generate_serializer_class(model_cls):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_cls
            fields = '__all__'

    return GenericSerializer
