from unittest import TestCase

from publisher.forms import EditorCreationForm


class FormTests(TestCase):
    def editor_creation_form_with_all_rows_valid(self):

        editor_form = {

            "username": "FlyingVince",
            "password1": "MrCarter123_",
            "password2": "MrCarter123_",
            "first_name": "Vince",
            "last_name": "Carter",
            "years_of_experience": 20,
        }

        form = EditorCreationForm(data=editor_form)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, editor_form)
