__author__ = "Jonathan Carlton"
from django import forms
from functools import partial
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, PrependedAppendedText, InlineCheckboxes

DateInput = partial(forms.DateInput, {
    'class': 'datepicker'
})


class CommunicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommunicationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_errors = True
        # TODO Add image field
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Key Information',
                    'short_desc',
                    'full_desc',
                    'project_start_date',
                    'duration',
                    'bh_number',
                    InlineCheckboxes('level'),
                    HTML(
                        """
                        <a class="btn btn-primary pull-right" id="key-btn" roles="button">Next</a>
                        """
                    )
                ),
                Tab(
                    'Values',
                    PrependedAppendedText('value_of_award', '&pound;', '.00'),
                    PrependedAppendedText('value_awarded_to_ncl', '&pound;', '.00'),
                    HTML(
                        """
                        <a class="btn btn-primary pull-right" id="value-btn" roles="button">Next</a>
                        """
                    )
                ),
                Tab(
                    'Involved',
                    'external',
                    'individuals',
                    HTML(
                        """
                        <a class="btn btn-primary pull-right" id="involved-btn" role="button">Next</a>
                        """
                    )
                ),
                Tab(
                    'Additional',
                    'source',
                    'tags',
                    # 'notes',
                    ButtonHolder(
                        Submit('submit_comm', 'Submit', css_class='btn btn-primary', css_id='jq-growl-notice'),
                        # HTML(
                        #     """
                        #     <a class="btn btn-primary" id="audit-btn" role="button" data-toggle='modal'
                        #     data-target='#modal-audit'>Audit</a>
                        #     """
                        # )
                    )
                )
            ),
        )
        self.fields['bh_number'].label = "BH Number"
        self.fields['short_desc'].label = "Short Description"
        self.fields['full_desc'].label = "Full Description"
        self.fields['value_of_award'].label = "Value of the Award"
        self.fields['value_awarded_to_ncl'].label = "Value Awarded to Newcastle University"
        self.fields['duration'].label = "Duration &#40;No. of Weeks&#41;"

    class Meta:
        model = Communication
        exclude = [
            'created_by', 'admin_checked', 'created_on', 'notes'
        ]
        widgets = {
            'full_desc': forms.Textarea(attrs={
                'cols': 6,
                'rows': 6
            }),
            'audiences': forms.CheckboxSelectMultiple(),
            'project_start_date': DateInput(),
        }


class AudienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AudienceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Audience',  # Form Legend
                'name',
                'description'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = Audience
        exclude = []
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 6,
                'rows': 6
            })
        }


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'User Profile',  # Form legend
                'user',
                'username',
                'title',
                'first_name',
                'last_name',
                'known_as',
                'user_type',
                'email',
                'smart_card',
                'unit',
                'role'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = UserProfile
        exclude = []


class SourcesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SourcesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Source',  # Form legend
                'name',
                'description'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = Sources
        exclude = []
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 6,
                'rows': 6
            })
        }


class CommsAuditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommsAuditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',  # Form legend
                'audience',
                'from_date',
                'to_date'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-danger')
            )
        )

    class Meta:
        model = CommsAudit
        exclude = ['sent']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
            # 'audience': forms.CheckboxSelectMultiple()
        }


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Tags',  # Form legend
                'name'
            ),
            ButtonHolder(
                Submit('submit_tag', 'Submit', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = Tags
        exclude = []


class NotesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Notes',
                'title',
                'content'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = Notes
        exclude = ['created_on', 'created_by']
        widgets = {
            'content': forms.Textarea(attrs={
                'cols': 6,
                'rows': 6
            })
        }


class NewsletterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields['audit'].label = "Audited Communication to add to Newsletter"
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Add to Newsletter',
                'audit'
            ),
            ButtonHolder(
                Submit('submit', 'Add', css_class="btn btn-primary")
            )
        )

    class Meta:
        model = Newsletter
        exclude = ['link']
