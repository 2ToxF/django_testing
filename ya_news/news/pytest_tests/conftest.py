from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture(autouse=True)
def db_autouse(db):
    pass


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def detail_url(news_id_for_args):
    return reverse('news:detail', args=news_id_for_args)


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def comment_id_for_args(comment):
    return (comment.id,)


# Fixtures only for test.content.py

@pytest.fixture
def many_news_list():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def create_two_comments(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()


# Fixtures only for test_logic.py

@pytest.fixture
def form_data():
    return {
        'text': 'Текст комментария'
    }


@pytest.fixture
def new_form_data():
    return {
        'text': 'Обновлённый комментарий'
    }


@pytest.fixture
def edit_url(comment_id_for_args):
    return reverse('news:edit', args=comment_id_for_args)


@pytest.fixture
def delete_url(comment_id_for_args):
    return reverse('news:delete', args=comment_id_for_args)


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'
