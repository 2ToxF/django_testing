from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.another_user = User.objects.create(username='Другой пользователь')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        clients_results = (
            (self.author, True),
            (self.another_user, False),
        )
        for client, expected_result in clients_results:
            self.client.force_login(client)
            with self.subTest(client=client):
                url = reverse('notes:list')
                response = self.client.get(url)
                assert ((self.note in response.context['object_list'])
                        is expected_result)

    def test_pages_contain_form(self):
        self.client.force_login(self.author)
        urls_args = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls_args:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
