import time

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.catalog.models import Product

from .forms import LeadForm

MIN_SECONDS_BETWEEN_LEADS = 20


def _back(request):
    target = request.POST.get("next", "")
    if target and url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(target)
    return redirect(reverse("core:home"))


def _remember_form(request, form, extra_error=""):
    """Keep values and messages so the product page can reopen the modal."""
    errors = {
        field: [item["message"] for item in items]
        for field, items in form.errors.get_json_data().items()
    }
    if extra_error:
        errors.setdefault("nonfield", []).append(extra_error)
    request.session["lead_form_state"] = {
        "errors": errors,
        "values": {
            "name": request.POST.get("name", ""),
            "phone": request.POST.get("phone", ""),
            "wants_installment": request.POST.get("wants_installment") == "1",
        },
    }


@require_POST
def create_lead(request):
    form = LeadForm(request.POST)

    if form.data.get("website"):  # bot filled the honeypot: pretend everything is fine
        return _back(request)

    if not form.is_valid():
        _remember_form(request, form)
        messages.error(request, "Заявка не отправлена. Проверьте выделенные поля.")
        return _back(request)

    last = request.session.get("last_lead_ts", 0)
    if time.time() - last < MIN_SECONDS_BETWEEN_LEADS:
        _remember_form(
            request, form,
            "Заявка уже отправлена. Подождите немного перед следующей.",
        )
        return _back(request)

    lead = form.save(commit=False)
    product_id = request.POST.get("product_id", "")
    if product_id.isdigit():
        product = Product.objects.published().filter(pk=product_id).first()
        if product:
            lead.product = product
            lead.product_title = product.title
    lead.save()

    request.session["last_lead_ts"] = time.time()
    request.session.pop("lead_form_state", None)
    messages.success(request, "Спасибо! Заявка принята, менеджер свяжется с вами.")
    return _back(request)
