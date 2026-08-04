from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from publisher.models import Topic, Newspaper


class PublicTopicTest(TestCase):

    def test_login_required(self):
        res = self.client.get(reverse("publisher:topic-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateTopicTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="some_test_user",
            password="Test_user123"
        )

        self.client.force_login(user)

    def test_retrieve_topics(self):
        Topic.objects.create(
            name="Healthcare"
        )

        response = self.client.get(reverse("publisher:topic-list"))
        self.assertEqual(response.status_code, 200)

        topics = Topic.objects.all()

        self.assertEqual(
            list(response.context["topic_list"]), list(topics)
        )

        self.assertTemplateUsed(response, "publisher/topic_list.html")


class PublicEditorTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("publisher:editor-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateEditorTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="Eduardo",
            password="Ed123456"
        )

        self.client.force_login(user)

    def test_create_editor(self):
        form_data = {
            "username": "LeBronnnieJames",
            "password1": "Lbj12345_king",
            "password2": "Lbj12345_king",
            "first_name": "Lebron",
            "last_name": "James",
            "years_of_experience": 20
        }

        self.client.post(reverse("publisher:editor-create"), data=form_data)

        editor = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(editor.first_name, form_data["first_name"])
        self.assertEqual(editor.last_name, form_data["last_name"])
        self.assertEqual(editor.years_of_experience, form_data["years_of_experience"])


class PublicNewspaperTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("publisher:newspaper-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="another_test_user",
            password="Test_user123"
        )
        self.client.force_login(user)

    def test_retrieve_newspapers_and_their_attributes(self):
        first_editor = get_user_model().objects.create_user(
            username="test_editor_1",
            password="Test_editor123"
        )

        second_editor = get_user_model().objects.create_user(
            username="test_editor_2",
            password="Test_editor_2_1234"
        )

        first_topic = Topic.objects.create(name="Economics")
        second_topic = Topic.objects.create(name="Politics")

        first_newspaper = Newspaper.objects.create(
            title="German financial observer",
            topic=first_topic,
            content="Germany recently has faced a huge economical downfall based on "
                    "variety of different factors.",
            published_date="2026-08-01"
        )

        first_newspaper.publishers.add(first_editor, second_editor)

        second_newspaper = Newspaper.objects.create(
            title="Regime",
            topic=second_topic,
            content="Last news & overviews of political states of "
                    "countries outside EU.",
            published_date="2026-08-01"
        )

        second_newspaper.publishers.add(first_editor)

        response = self.client.get(reverse("publisher:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        newspapers = Newspaper.objects.all()
        self.assertEqual(list(response.context["newspaper_list"]), list(newspapers))
        self.assertTemplateUsed("publisher/newspaper_list.html")
        self.assertEqual(first_newspaper.topic, first_topic)
        self.assertEqual(first_newspaper.publishers.count(), 2)
        self.assertEqual(second_newspaper.title, "Regime")
        self.assertEqual(second_newspaper.publishers.count(), 1)


class TopicSearchTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="Test_user123"
        )
        self.client.force_login(user)

        Topic.objects.create(
            name="Sports"
        )

        Topic.objects.create(
            name="Global climate change"
        )

        Topic.objects.create(
            name="Literature"
        )

    def test_search_returns_correct_query_by_topic_name(self):
        response = self.client.get(reverse("publisher:topic-list"),
                                   {"name": "Sport"})
        query = response.context["topic_list"]
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(query.first().name, "Sports")

    def test_search_case_insensitivity_by_topic_name(self):
        response = self.client.get(reverse("publisher:topic-list"),
                                   {"name": "gLoBAL"})
        query = response.context["topic_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(query.first().name, "Global climate change")


class NewspaperSearchTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="DwyaneWade3",
            password="Dwade3miami_"
        )
        self.client.force_login(user)

        editor_1 = get_user_model().objects.create_user(
            username="TimDUncan",
            password="TdSanAntonio123_"
        )

        editor_2 = get_user_model().objects.create_user(
            username="KevinGarnett",
            password="KGtimberwolf555_"
        )

        topic_1 = Topic.objects.create(name="Sports")
        topic_2 = Topic.objects.create(name="Nature")

        newspaper_1 = Newspaper.objects.create(
            title="Courtside",
            topic=topic_1,
            content="American basketball observer.",
            published_date="2026-08-02"
        )

        newspaper_2 = Newspaper.objects.create(
            title="Mother Earth",
            topic=topic_2,
            content="World we live in.",
            published_date="2026-08-02"
        )

        newspaper_1.publishers.add(editor_1, editor_2)
        newspaper_2.publishers.add(editor_1)

    def test_search_returns_correct_query_by_newspaper_title(self):
        response = self.client.get(reverse("publisher:newspaper-list"),
                                   {"title": "Mother"})
        query = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(query.first().title, "Mother Earth")

    def test_search_case_insensitivity_by_newspaper_title(self):
        response = self.client.get(reverse("publisher:newspaper-list"),
                                   {"title": "cOurtSIDE"})
        query = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.first().title, "Courtside")
        self.assertEqual(query.count(), 1)


class EditorSearchTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="BramStoker",
            password="BramBram12343_"
        )
        self.client.force_login(user)

        get_user_model().objects.create_user(
            username="JohnSnow",
            password="TheGreatWall1234_"
        )

        get_user_model().objects.create_user(
            username="Ned_Stark_wolf",
            password="Eddard123Starky_"
        )

        get_user_model().objects.create_user(
            username="JohnnyD",
            password="Depp12343J_"
        )

    def test_search_returns_correct_query_by_editor_username(self):
        response = self.client.get(reverse("publisher:editor-list"),
                                   {"username": "John"})
        query = response.context["editor_list"]

        self.assertEqual(query.count(), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.first().username, "JohnSnow")

    def test_search_case_insensitivity_by_editor_username(self):
        response = self.client.get(reverse("publisher:editor-list"),
                                   {"username": "stark"})
        query = response.context["editor_list"]
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.first().username, "Ned_Stark_wolf")
