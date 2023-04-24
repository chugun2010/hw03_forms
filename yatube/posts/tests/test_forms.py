from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    def setUp(self):
        """
        Установка первоначальных данных в бд для тестирования
        """
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username="HasNoName")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        # Cоздаём пост с id 99 для второго задания
        self.group4 = Group.objects.create(title="Тестовая группа4",
                                           slug="test_group4")
        Post.objects.create(
            id=99,
            text="Второе задание по формам",
            group=self.group4,
            author=self.user
        )

    def test_post_create(self):
        """
        Проверка, что создаётся запись в бд при создании поста
        """
        self.authorized_client.post(
            reverse("posts:create"),
            {"text": "Test form first evere created"}
        )

        self.assertTrue(
            Post.objects.filter(
                text="Test form first evere created",
            ).exists()
        )

    def test_post_edit(self):
        """
        Проверка, что пост в базе обновляется
        """
        self.authorized_client.post(
            reverse("posts:edit", kwargs={"post_id": 99}),
            {"text": "Update post"}
        )

        self.assertTrue(
            Post.objects.filter(
                id=99,
                text="Update post",
            ).exists()
        )
