from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from publisher.models import Editor, Newspaper


class EditorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Editor
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "years_of_experience")


class EditorYearsOfExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ["years_of_experience"]

    def clean_years_of_experience(self):
        years = self.cleaned_data["years_of_experience"]

        if years > 50:
            raise forms.ValidationError("Years of experience cannot exceed 50 years.")

        return years


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Newspaper
        fields = "__all__"
