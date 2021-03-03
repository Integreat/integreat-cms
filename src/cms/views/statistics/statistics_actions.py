"""
This module contains view actions related to pages.
"""
import logging

from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import JsonResponse

from .matomo_api_manager import MatomoApiManager
from ...models import Region

logger = logging.getLogger(__name__)


@login_required
def get_total_views_ajax(request, region_slug):
    """
    Aggregates the total API hits of the last 14 days and renders a Widget for the Dashboard.

    Args:
        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param region_slug: The slug of the current region
        :type region_slug: str

        :return: A rendered version for the Dashboard.
        :rtype: ~django.http.HttpResponseRedirect
    """

    region = Region.get_current_region(request)

    api_manager = MatomoApiManager(region.matomo_url, region.matomo_token)
    matomo_id = api_manager.get_matomo_id_by_user()

    start_date = str(date.today() - timedelta(days=14))
    end_date = str(date.today())
    date_range = start_date + "," + end_date

    total_views = api_manager.get_total_hits(matomo_id, date_range)

    return JsonResponse(total_views)


def prepare_export_csv_ajax(languages, hits, dates):
    """
    Method to create CSV String from the API hits
    :param languages: The list languages which should be evaluated
    :type languages: list
    :param hits: The list of response hits
    :type hits: list
    :param dates: The list of response dates
    :type dates: list
    :return: The raw csv string of the results
    :rtype: str
    """
    csv_row = "date"
    csv_raw = ""
    for l_value in languages:
        csv_row += "," + l_value[1]
    csv_raw += csv_row + ";"
    for date_index, _ in enumerate(dates):
        csv_row = ""
        csv_row += str(dates[date_index]) + ","
        for idy in range(0, len(languages)):
            csv_row += str(hits[idy][2][date_index])
            if idy < (len(languages) - 1):
                csv_row += ","
        csv_row += ";"
        csv_raw += str(csv_row)
    return csv_raw
