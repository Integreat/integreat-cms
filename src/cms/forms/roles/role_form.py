from ...models import Role
from ..placeholder_model_form import PlaceholderModelForm


class RoleForm(PlaceholderModelForm):
    """
    Form for creating and modifying user role objects
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        #: The model of this :class:`django.forms.ModelForm`
        model = Role
        #: The fields of the model which should be handled by this form
        fields = ["staff_role"]
