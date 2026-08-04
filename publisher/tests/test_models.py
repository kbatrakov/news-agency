from django.test import TestCase
from django.contrib.auth import get_user_model
from publisher.models import Topic, Newspaper


class ModelTests(TestCase):
    def setUp(self):
        self.editor = get_user_model().objects.create_user(
            username="VladTs",
            password="Tsepesh_123haha",
            first_name="Vlad",
            last_name="Tsepesh",
            years_of_experience=2
        )

        self.topic = Topic.objects.create(name="Sports")

        self.newspaper = Newspaper.objects.create(
            title="WePlayinBasketball",
            content="Basketball lovers are welcomed!",
            published_date="2026-07-27",
            topic=self.topic,
        )

        self.newspaper.publishers.add(self.editor)

    def test_editor_str(self):
        self.assertEqual(str(self.editor), f"Editor: "
                                           f"{self.editor.first_name} "
                                           f"{self.editor.last_name} "
                                           f"({self.editor.username})")

    def test_topic_str(self):
        self.assertEqual(str(self.topic), f"Topic of the publication: "
                                          f"{self.topic.name}")

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), (f"Title: "
                                               f"{self.newspaper.title}"
                                               f"Topic: "
                                               f"{self.newspaper.topic}"
                                               f"Published by: "
                                               f"{self.newspaper.publishers}"))

    def test_editor_create(self):
        username = "VanHelsing"
        password = "VanVanHels_777"
        years_of_experience = 2

        new_editor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(new_editor.username, username)
        self.assertTrue(new_editor.check_password(password))
        self.assertEqual(new_editor.years_of_experience, years_of_experience)
