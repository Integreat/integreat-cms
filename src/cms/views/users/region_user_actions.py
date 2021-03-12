"""
This module contains view actions for region user objects.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from ...decorators import region_permission_required
from ...models import Region

logger = logging.getLogger(__name__)


@require_POST
@login_required
@region_permission_required
@permission_required("cms.manage_region_users", raise_exception=True)
# pylint: disable=unused-argument
def delete_region_user(request, region_slug, user_id):
    """
    This view deletes a region user

    :param request: The current request
    :type request: ~django.http.HttpResponse

    :param region_slug: The slug of the current region
    :type region_slug: str

    :param user_id: The id of the user which should be deleted
    :type user_id: int

    :return: A redirection to region user list
    :rtype: ~django.http.HttpResponseRedirect
    """

    region = Region.get_current_region(request)
    user = get_object_or_404(region.users, id=user_id)
    if user.profile.regions.count() == 1:
        user.delete()
        logger.info('User "%s" deleted user "%s"', request.user, user)
        messages.success(request, _("User {} was successfully deleted.").format(user))
    else:
        user.profile.regions.remove(region)
        user.profile.save()
        logger.info(
            'User "%s" removed user "%s" from region "%s"', request.user, user, region
        )
        messages.success(
            request,
            _("User {} was successfully removed from this region.").format(user),
        )

    return redirect("region_users", region_slug=region.slug)
