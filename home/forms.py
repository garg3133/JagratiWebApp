from django import forms
from .models import Section


class SectionAdminForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["section_id", "name", "is_parent_section", "parent_section"]

    def clean(self):
        cleaned_data = self.cleaned_data
        parent_section = cleaned_data.get("parent_section")
        is_parent_section = cleaned_data.get("is_parent_section")
        if parent_section and is_parent_section:
            raise forms.ValidationError(
                "A section cannot be a parent section and a child section at the same time. Only two level of parent-child relationship is allowed."
            )
        return cleaned_data
