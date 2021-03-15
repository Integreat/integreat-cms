from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Role(models.Model):
    """
    Meta information about the default Django auth group model
    """

    group = models.OneToOneField(
        Group,
        unique=True,
        on_delete=models.CASCADE,
        related_name="role",
        verbose_name=_("Django auth group"),
    )
    staff_role = models.BooleanField(
        default=False,
        verbose_name=_("staff role"),
        help_text=_("Whether or not this role is designed for staff members"),
    )

    @property
    def name(self):
        """
        The role inherits its name from the Django auth group

        :return: The name of the role
        :rtype: str
        """
        return self.group.name

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Role object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the role
        :rtype: str
        """
        return self.name

    def __repr__(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<Role: Role object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the role
        :rtype: str
        """
        return f"<Role (id: {self.id}, name: {self.name}{', staff role' if self.staff_role else ''})>"

    class Meta:
        #: The verbose name of the model
        verbose_name = _("role")
        #: The plural verbose name of the model
        verbose_name_plural = _("roles")
        #: The default permissions for this model
        default_permissions = ()
