from ..placeholder_model_form import PlaceholderModelForm
from ...models import Document


class DocumentForm(PlaceholderModelForm):
    """
    Form for creating and modifying document objects
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        #: The model of this :class:`django.forms.ModelForm`
        model = Document
        fields = ()
