from django.test import TestCase
from questions.models import Questions, User, UserMark


class QuestionsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.question = Questions.objects.create(
            question='O que é a vida?',
            alternative_a='Uma maravilha',
            alternative_b='Uma coisa',
            alternative_c='Algo inexplicável',
            alternative_d='Eu vou lá saber?',
            correct_alternative='A',
            created_by=User.objects.create(
                email='kirito@sao.com',
                username='kirito',
                password='sao'
            )
        )

    def test_information_fields(self) -> None:
        self.assertIsInstance(self.question.question, str)
        self.assertIsInstance(self.question.alternative_a, str)
        self.assertIsInstance(self.question.alternative_b, str)
        self.assertIsInstance(self.question.alternative_c, str)
        self.assertIsInstance(self.question.alternative_d, str)
        self.assertIsInstance(self.question.correct_alternative, str)


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
                email='kirito@sao.com',
                username='kirito',
                password='sao'
        )

    def test_information_fields(self) -> None:
        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.emal, str)
        self.assertIsInstance(self.user.password, str)


class UserMarkModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_mark = UserMark.objects.create(
            user_mark='A',
            user=User.objects.create(
                email='kirito@sao.com',
                username='kirito',
                password='sao'
            ),
            question=Questions.objects.create(
                question='O que é a vida?',
                alternative_a='Uma maravilha',
                alternative_b='Uma coisa',
                alternative_c='Algo inexplicável',
                alternative_d='Eu vou lá saber?',
                correct_alternative='A',
                created_by=User.objects.create(
                    email='kirito@sao.com',
                    username='kirito',
                    password='sao'
                )
            )
        )

    def test_information_fields(self) -> None:
        self.assertIsInstance(self.user_mark.user_mark, str)