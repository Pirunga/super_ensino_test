from django.http import response
from django.test import TestCase
from rest_framework.test import APIClient
from questions.models import Questions, User, UserMark
from questions.views import QuestionsView

class TestView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        admin_user_data = {
            'email':'kirito@sao.com',
            'username':'kirito',
            'password':'sao',
            'is_superuser': True,
            'is_staff': True,
        }

        self.base_url = '/question/'

        self.viewer_user = User.objects.create_superuser(**admin_user_data)

        self.user_headers = {'HTTP_user-id': '1'}
        self.wrong_user_headers = {'HTTP_user-id': '2'}

        self.question_created_data = [{
            'id': 1,
            'question': 'Qual é o maior medo de um cachorro?',
            'alternative_a': 'Um furaCÃO',
            'alternative_b': 'Do carteiro não aparecer',
            'alternative_c': 'De não conhecer o caramelo',
            'alternative_d': 'Um aspirador',
            'correct_alternative': 'A',
            'created_by': {
                'email': 'kirito@sao.com',
                'first_name': '',
                'last_name': '',
                'username': 'kirito'
            }
        }]

        self.question_data = {
            'id': 1,
            'question': 'Qual é o maior medo de um cachorro?',
            'alternative_a': 'Um furaCÃO',
            'alternative_b': 'Do carteiro não aparecer',
            'alternative_c': 'De não conhecer o caramelo',
            'alternative_d': 'Um aspirador',
            'correct_alternative': 'A'
        }

        self.user_mark_data = {
            'question': 1,
            'user_mark': 'B'
        }

        self.user_mark_viewer = {
            'user': self.viewer_user
        }

        self.user_perfomace_data = {
            'correct_answers': 0,
            'wrong_answers': 0,
            'perfomace_index': '0%'
        }

        self.user_mark_output_data = {'id': 1}

        self.not_found = {'detail': 'Not found.'}

    def test_get_question_success(self):
        """
        Test get question success.
        """
        response = self.client.get(self.base_url, **self.user_headers)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data, [])

    def test_get_question_fail(self):
        """
        Test get question with invalid user.
        """
        response = self.client.get(self.base_url, **self.wrong_user_headers)
        self.assertEqual(response.status_code, 404)

        response_data = response.json()
        self.assertEqual(response_data, {'detail': 'Not found.'})

    def test_retrieve_question_success(self):
        """
        Test retrieve question success.
        """
        self.question_data.update({'created_by': self.viewer_user})
        question = Questions.objects.create(**self.question_data)

        response = self.client.get(self.base_url + '1/', **self.user_headers)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data, self.question_created_data)

    def test_retrieve_question_fail(self):
        """
        Test retrieve question with invalid user.
        """
        response = self.client.get(self.base_url + '1/', **self.wrong_user_headers)
        self.assertEqual(response.status_code, 404)

        response_data = response.json()
        self.assertEqual(response_data, self.not_found)

    def test_user_mark_success(self):
        """
        Test user answer creation success. 
        """
        self.question_data.update({'created_by': self.viewer_user})
        question = Questions.objects.create(**self.question_data)

        response = self.client.post(
            self.base_url + 'user-mark/',
            self.user_mark_data,
            **self.user_headers
        )
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data, self.user_mark_output_data)

    def test_user_mark_fail(self):
        """
        Test user answer creation fail. 
        """
        response = self.client.post(
            self.base_url + 'user-mark/',
            self.user_mark_data,
            **self.user_headers
        )
        self.assertEqual(response.status_code, 404)

        response_data = response.json()
        self.assertEqual(response_data, self.not_found)

    def test_get_user_perfomace_success(self):
        """
        Test get user perfomace informations success.
        """
        response = self.client.get(self.base_url + 'user/1', **self.user_headers)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data, self.user_perfomace_data)

    def test_get_user_perfomace_fail(self):
        """
        Test get user perfomace informations fail. 
        """
        response = self.client.get(
            self.base_url + 'user/2',
            **self.wrong_user_headers
        )
        self.assertEqual(response.status_code, 404)

        response_data = response.json()
        self.assertEqual(response_data, self.not_found)
