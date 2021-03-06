from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...constants import frequency, weekdays, weeks


class RecurrenceRule(models.Model):
    """
    Data model representing the recurrence frequency and interval of an event
    """

    #: Manage choices in :mod:`cms.constants.frequency`
    frequency = models.CharField(
        max_length=7,
        choices=frequency.CHOICES,
        default=frequency.WEEKLY,
        verbose_name=_("frequency"),
        help_text=_("How often the event recurs"),
    )
    interval = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Repeat every ... time(s)"),
        help_text=_("The interval in which the event recurs."),
    )
    #: Manage choices in :mod:`cms.constants.weekdays`
    weekdays_for_weekly = ArrayField(
        models.IntegerField(choices=weekdays.CHOICES),
        blank=True,
        verbose_name=_("weekdays"),
        help_text=_(
            "If the frequency is weekly, this field determines on which days the event takes place"
        ),
    )
    #: Manage choices in :mod:`cms.constants.weekdays`
    weekday_for_monthly = models.IntegerField(
        choices=weekdays.CHOICES,
        null=True,
        blank=True,
        verbose_name=_("weekday"),
        help_text=_(
            "If the frequency is monthly, this field determines on which days the event takes place"
        ),
    )
    #: Manage choices in :mod:`cms.constants.weeks`
    week_for_monthly = models.IntegerField(
        choices=weeks.CHOICES,
        null=True,
        blank=True,
        verbose_name=_("week"),
        help_text=_(
            "If the frequency is monthly, this field determines on which week of the month the event takes place"
        ),
    )
    recurrence_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("recurrence end date"),
        help_text=_(
            "If the recurrence is not for an indefinite period, this field contains the end date"
        ),
    )

    class Meta:
        #: The verbose name of the model
        verbose_name = _("recurrence rule")
        #: The plural verbose name of the model
        verbose_name_plural = _("recurrence rules")
        #: The default permissions for this model
        default_permissions = ()
