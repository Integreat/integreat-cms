"""Views related to the statistics module"""
from datetime import date, timedelta

# pylint: disable=redefined-builtin
from requests.exceptions import ConnectionError, InvalidURL

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from .matomo_api_manager import MatomoApiManager
from ...decorators import region_permission_required
from ...models import Region


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class AnalyticsView(TemplateView):
    """
    View for the statistics overview.
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "statistics/statistics_overview.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "statistics"}

    # pylint: disable=too-many-locals
    def get(self, request, *args, **kwargs):
        """
        Render statistics of access numbers tracked by Matomo

        :param request: The current request
        :type request: ~django.http.HttpResponse

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        region_slug = kwargs.get("region_slug")
        region = Region.get_current_region(request)
        start_date = request.GET.get(
            "start_date", str(date.today() - timedelta(days=30))
        )
        end_date = request.GET.get("end_date", str(date.today()))
        if (start_date == "") or (end_date == "") or (start_date > end_date):
            messages.error(request, _("Please enter a correct start and end date"))
            return redirect("statistics", region_slug=region_slug)

        languages = [
            ["de", "Deutsch", "#7e1e9c"],
            ["en", "Englisch", "#15b01a"],
            ["ar", "Arabisch", "#0343df"],
            ["en", "Englisch", "#0343df"],
            ["es", "Spanisch", "#ff81c0"],
            ["fr", "Französisch", "#653700"],
            ["ar", "Arabisch", "#e50000"],
            ["fa", "Farsi", "#00ffff"],
            ["am", "Amharisch", "#029386"],
            ["ru", "Russisch", "#f97306"],
            ["tr", "Türkisch", "#96f97b"],
            ["ro", "Rumänisch", "#c20078"],
            ["ku", "Kurdisch", "#ffff14"],
            ["ti", "Tigrinya", "#75bbfd"],
            ["sr", "Serbisch", "#929591"],
            ["per", "Persisch", "#89fe05"],
            ["bg", "Bulgarisch", "#bf77f6"],
            ["so", "Somali", "#9a0eea"],
            ["pl", "Polnisch", "#033500"],
            ["de-si", "Einfaches Deutsch", "#06c2ac"],
            ["hr", "Kroatisch", "#06c2ac"],
            ["it", "Italienisch", "#c79fef"],
            ["hu", "Ungarisch", "#00035b"],
            ["el", "Griechisch", "#d1b26f"],
        ]

        api_man = MatomoApiManager(
            matomo_url=region.matomo_url,
            matomo_api_key=region.matomo_token,
        )
        response_dates = []
        response_hits = []

        # Match active languages with

        matomo_id = api_man.get_matomo_id_by_user()
        for lang in languages:
            try:
                api_hits = api_man.get_visitors_per_timerange(
                    date_string=start_date + "," + end_date,
                    matomo_id=matomo_id,
                    period=request.GET.get("peri", "day"),
                    lang=lang[0],
                )
                temp_hits = []
            except ConnectionError:
                messages.error(
                    request, _("Connection to Matomo could not be established")
                )
                return redirect("dashboard", region_slug=region_slug)
            except InvalidURL:
                messages.error(
                    request,
                    _(
                        "The url you have entered is invalid. Please check the corresponding settings."
                    ),
                )
                return redirect("dashboard", region_slug=region_slug)
            except TypeError:
                messages.error(
                    request,
                    _(
                        "There was an error during the establishment of a connection. Please check the region and the entered key."
                    ),
                )
                return redirect("dashboard", region_slug=region_slug)
            for single_day in api_hits:
                temp_hits.append(single_day[1])
            response_hits.append([lang[1], lang[2], temp_hits])
        for single_day in api_hits:
            response_dates.append(single_day[0])

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "dates": response_dates,
                "hits": response_hits,
            },
        )


@login_required
def get_total_views_ajax(request):
    """[summary]

    Args:
        request ([type]): [description]
        region_slug ([type]): [description]
    """

    region = Region.get_current_region(request)

    api_manager = MatomoApiManager(region.matomo_url, region.matomo_api_key)
    matomo_id = api_manager.get_matomo_id_by_user()

    start_date = str(date.today() - timedelta(days=14))
    end_date = str(date.today())
    date_range = start_date + "," + end_date

    total_views = api_manager.get_total_hits(matomo_id, date_range)

    return render(
        request,
        "statistics/_statisics_widget.html",
        {
            "total_views": total_views,
            "dates": date_range,
        },
        status=201,  # HTTP 201 Created
    )
