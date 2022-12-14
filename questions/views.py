from django.shortcuts import render
from math import trunc
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView
)
from questions.models import Questions, User, UserMark
from questions.serializer import (
    QuestionsSerializer,
    UserMarkSerializer,
    UserPerfomaceSerializer
)


class QuestionsView(ListAPIView, RetrieveAPIView):
    """
    List and Retrive questions. 
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        if question_id := self.request.parser_context.get('kwargs').get('question_id'):
            queryset = [self.queryset.filter(id=question_id).first()]

        user = get_object_or_404(User, pk=self.request.headers.get('user-id'))

        for question in queryset:
            if user_mark := UserMark.objects.filter(question=question, user=user).first():
                question.user_mark_id = UserMarkSerializer(user_mark).data

        return queryset


class UserMarkView(CreateAPIView):
    """
    Create user's answer to the question.
    """
    queryset = UserMark.objects.all()
    serializer_class = UserMarkSerializer

    def create(self, request, *args, **kwargs):
        question_id = request.data.get('question')
        user_id = request.headers.get('user-id')
        question = get_object_or_404(Questions, pk=question_id)
        user = get_object_or_404(User, pk=user_id)
        
        if UserMark.objects.filter(question=question, user=user):
            return Response(
                {'message': 'You Already have answered this question'},
                HTTP_409_CONFLICT
            )

        self.verify_user_answer(
            question.correct_alternative,
            user,
            request.data.get('user_mark')
        )

        user_mark = UserMark.objects.create(
            question=question,
            user=user,
            user_mark=request.data.get('user_mark')
        )

        serializer = UserMarkSerializer(user_mark)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            HTTP_201_CREATED,
            headers
        )

    @staticmethod
    def verify_user_answer(correct_alternative, user, user_answer):
        """
        Verifies if the user's answer is correct or not
        and updates the information in database.
        :param str user_answer: User's answer to verify.
        :param str user: User that answered.
        :param str correct_alternative: Alternative with correct answer.
        """
        if user_answer == correct_alternative:
            user.correct_answers += 1

        else:
            user.wrong_answers += 1
        
        user.save()


class UserView(RetrieveAPIView):
    """
    Gets user's perfomace information.
    """
    queryset = User.objects.all()
    serializer_class = UserPerfomaceSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        user = get_object_or_404(User, pk=self.request.headers.get('user-id'))

        if questions_length := Questions.objects.all().count():
            perfomace_index = trunc(user.correct_answers / questions_length)
            user.perfomace_index = str(100 * perfomace_index) + '%'
            user.save()
        
        return queryset
