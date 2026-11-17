from rest_framework import serializers

from .models import Lead


class LeadCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Lead
        fields = ["name", "phone", "wants_installment", "comment", "product_id"]

    def validate_phone(self, value):
        import re

        digits = re.sub(r"\D", "", value.strip())
        if not 9 <= len(digits) <= 15:
            raise serializers.ValidationError("Введите номер телефона, например +996 555 123 456.")
        return value.strip()

    def create(self, validated_data):
        from apps.catalog.models import Product

        product_id = validated_data.pop("product_id", None)
        lead = Lead(**validated_data)
        if product_id:
            product = Product.objects.filter(pk=product_id).first()
            if product:
                lead.product = product
                lead.product_title = product.title
        lead.save()
        return lead
