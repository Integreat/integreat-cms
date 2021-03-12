"""
This module contains view actions for offer objects.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ...decorators import region_permission_required
from ...models import Region, Offer, OfferTemplate


@require_POST
@login_required
@region_permission_required
@permission_required("cms.manage_offers", raise_exception=True)
def activate(request, region_slug, offer_template_slug):
    """
    This view activates an offer for a specific region by creating an :class:`~cms.models.offers.offer.Offer` object

    :param request: The current request
    :type request: ~django.http.HttpResponse

    :param region_slug: The slug of the current region
    :type region_slug: str

    :param offer_template_slug: The slug of the offer template which should be activated for this region
    :type offer_template_slug: str

    :return: A redirection to the media library
    :rtype: ~django.http.HttpResponseRedirect
    """
    region = Region.get_current_region(request)
    template = OfferTemplate.objects.get(slug=offer_template_slug)
    Offer.objects.create(region=region, template=template)
    messages.success(
        request,
        _('Offer "%(offer_name)s" was successfully activated')
        % {"offer_name": template.name},
    )
    return redirect(
        "offers",
        **{
            "region_slug": region_slug,
        }
    )


@require_POST
@login_required
@region_permission_required
@permission_required("cms.manage_offers", raise_exception=True)
def deactivate(request, region_slug, offer_template_slug):
    """
    This view deactivates an offer for a specific region by deleting the respective
    :class:`~cms.models.offers.offer.Offer` object

    :param request: The current request
    :type request: ~django.http.HttpResponse

    :param region_slug: The slug of the current region
    :type region_slug: str

    :param offer_template_slug: The slug of the offer template which should be deactivated for this region
    :type offer_template_slug: str

    :return: A redirection to the media library
    :rtype: ~django.http.HttpResponseRedirect
    """
    region = Region.get_current_region(request)
    template = OfferTemplate.objects.get(slug=offer_template_slug)
    offer = Offer.objects.filter(region=region, template=template).first()
    offer.delete()
    messages.success(
        request,
        _('Offer "%(offer_name)s" was successfully deactivated')
        % {"offer_name": template.name},
    )
    return redirect(
        "offers",
        **{
            "region_slug": region_slug,
        }
    )
