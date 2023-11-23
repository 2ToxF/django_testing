import pytest
from django.urls import reverse

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
