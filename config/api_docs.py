import json

from django.shortcuts import render
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.renderers import OpenApiJsonRenderer


def _get_schema_json():
    generator = SchemaGenerator()
    schema = generator.get_schema(request=None, public=True)
    renderer = OpenApiJsonRenderer()
    json_bytes = renderer.render(schema, renderer_context={})
    return json_bytes.decode("utf-8")


def swagger_view(request):
    return render(request, "api/swagger.html", {"schema_json": _get_schema_json()})


def redoc_view(request):
    return render(request, "api/redoc.html", {"schema_json": _get_schema_json()})
