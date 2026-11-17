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


@require_POST
def create_lead(request):
    form = LeadForm(request.POST)

    if form.data.get("website"):  # bot filled the honeypot: pretend everything is fine
        return _back(request)

    last = request.session.get("last_lead_ts", 0)
    if time.time() - last < MIN_SECONDS_BETWEEN_LEADS:
        messages.error(request, "Заявка уже отправлена. Подождите немного перед следующей.")
        return _back(request)

    if not form.is_valid():
        errors = " ".join(error for errs in form.errors.values() for error in errs)
        messages.error(request, f"Заявка не отправлена. {errors}")
        return _back(request)

    lead = form.save(commit=False)
    product = Product.objects.filter(pk=request.POST.get("product_id")).first()
    if product:
        lead.product = product
        lead.product_title = product.title
    lead.save()

    request.session["last_lead_ts"] = time.time()
    messages.success(request, "Спасибо! Заявка принята, менеджер свяжется с вами.")
    return _back(request)
