from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.another_user = User.objects.create(username='Другой пользователь')
        cls.another_client = Client()
        cls.another_client.force_login(cls.another_user)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        clients_results = (
            (self.author_client, True),
            (self.another_client, False),
        )
        for parametrized_client, expected_result in clients_results:
            with self.subTest(user=parametrized_client):
                url = reverse('notes:list')
                response = parametrized_client.get(url)
                assert ((self.note in response.context['object_list'])
                        is expected_result)

    def test_pages_contain_form(self):
        urls_args = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls_args:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
