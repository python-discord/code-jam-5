"""Import to use forms."""
from django import forms
from .models import List


class ListForm(forms.ModelForm):
    """Listing out."""

    class Meta:
        """Meta class."""

        model = List
        fields = ["item", "completed"]
