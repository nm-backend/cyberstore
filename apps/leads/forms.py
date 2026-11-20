import re

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field.
    website = forms.CharField(required=False)
    consent = forms.BooleanField(
        required=True,
        error_messages={
            "required": "Подтвердите согласие на обработку персональных данных.",
        },
    )

    class Meta:
        model = Lead
        fields = ["name", "phone", "wants_installment", "comment"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"[+\d][\d\s()\-]{6,29}", phone):
            raise forms.ValidationError(
                "Введите номер телефона, например +996 555 123 456."
            )
        digits = re.sub(r"\D", "", phone)
        if not 9 <= len(digits) <= 15:
            raise forms.ValidationError("Введите номер телефона, например +996 555 123 456.")
        return phone

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Укажите имя — хотя бы 2 символа.")
        return name
