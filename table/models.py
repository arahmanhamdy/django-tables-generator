import uuid

from django.db import models, connection


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_django_model(self):
        return type(str(self), (models.Model,), {
            "__module__": self.__module__,
            **self.model_fields
        })

    def migrate(self):
        model = self.to_django_model()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)

    def alter(self, updated_fields_data):
        updated_fields = {field_data["title"]: Field.create_django_field_from(field_data)
                          for field_data in updated_fields_data}
        changes = self._get_schema_changes(updated_fields)
        self._migrate_changes(changes)

    def _migrate_changes(self, changes):
        model = self.to_django_model()
        with connection.schema_editor() as schema_editor:
            for added_field in changes["added"]:
                schema_editor.add_field(model, added_field)
            for removed_field in changes["removed"]:
                schema_editor.remove_field(model, removed_field)
            for old_field, new_field in changes["altered"]:
                schema_editor.alter_field(model, old_field, new_field)

    def _get_schema_changes(self, updated_fields):
        updated_fields_titles = updated_fields.keys()
        current_fields_titles = self.model_fields.keys()
        added_fields_titles = updated_fields_titles - current_fields_titles
        removed_fields_titles = current_fields_titles - updated_fields_titles
        remaining_fields_titles = current_fields_titles - removed_fields_titles
        return {
            "added": [updated_fields.get(title) for title in added_fields_titles],
            "removed": [self.model_fields.get(title) for title in removed_fields_titles],
            "altered": [(self.model_fields.get(title), updated_fields.get(title)) for title in remaining_fields_titles]
        }

    @property
    def model_fields(self):
        return {field.title: field.to_django_field() for field in self.fields.all()}

    def __str__(self):
        return f"table_{self.id}"


class Field(models.Model):
    title = models.CharField(max_length=250)
    data_type = models.CharField(max_length=7,
                                 choices=[("string", "string"), ("boolean", "boolean"), ("number", "number")])
    table = models.ForeignKey(Table, related_name="fields", on_delete=models.CASCADE)

    @classmethod
    def create_django_field_from(cls, field_data):
        field = cls(**field_data)
        return field.to_django_field()

    def to_django_field(self):
        field = None
        if self.data_type == "string":
            field = models.CharField(max_length=255, db_column=self.title)
        elif self.data_type == "number":
            field = models.FloatField(db_column=self.title)
        elif self.data_type == "boolean":
            field = models.BooleanField(db_column=self.title)
        if field:
            field.set_attributes_from_name(field.db_column)
            return field
