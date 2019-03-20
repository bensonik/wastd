# -*- coding: utf-8 -*-
"""Conservation forms."""

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django_select2.forms import ModelSelect2Widget  # ModelSelect2MultipleWidget
from leaflet.forms.widgets import LeafletWidget

from conservation import models as cons_models
from conservation import widgets as cons_widgets
from taxonomy import widgets as tax_widgets
from shared.admin import LEAFLET_SETTINGS
from shared.forms import DateInput  # DateTimeInput


class ConservationActionForm(forms.ModelForm):
    """Common form for ConservationAction."""

    def __init__(self, *args, **kwargs):
        """Customise form layout."""
        super(ConservationActionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Relations',
                'taxa',
                'communities',
                'document',
                'target_area',
                'occurrence_area_code',
            ),
            Fieldset(
                'Task',
                'category',
                'instructions',
            ),
            Fieldset(
                'Implementation',
                'implementation_notes',
                'completion_date',
                'expenditure',
                # 'attachments'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        """Class options."""

        model = cons_models.ConservationAction
        fields = (
            "taxa",
            "communities",
            "document",
            "occurrence_area_code",
            "target_area",
            "category",
            "instructions",
            "implementation_notes",
            "completion_date",
            "expenditure",
            # "attachments"
        )
        widgets = {
            'taxa': tax_widgets.TaxonMultipleWidget(),
            'communities': tax_widgets.CommunityMultipleWidget(),
            'document': cons_widgets.DocumentWidget(),
            'target_area': LeafletWidget(attrs=LEAFLET_SETTINGS),
            'category': cons_widgets.ConservationActionCategoryWidget(),
            'completion_date': DateInput(),
        }


class ConservationActivityForm(forms.ModelForm):
    """Common form for ConservationActivity."""

    def __init__(self, *args, **kwargs):
        """Customise form layout."""
        super(ConservationActivityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Task',
                'conservation_action',
            ),
            Fieldset(
                'Implementation',
                'implementation_notes',
                'completion_date',
                'expenditure',
                # 'attachments'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        """Class options."""

        model = cons_models.ConservationActivity
        fields = (
            "conservation_action",
            "implementation_notes",
            "completion_date",
            "expenditure",
            # "attachments"
        )
        widgets = {
            'conservation_action': cons_widgets.ConservationActionWidget(),
            'completion_date': DateInput(),
        }
