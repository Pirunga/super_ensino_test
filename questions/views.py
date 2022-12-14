from django.shortcuts import render
from math import trunc
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
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
            queryset = [get_object_or_404(self.queryset, pk=question_id)]

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
        
        if UserMark.objects.filter(question=question, user=user).first():
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
    
    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        obj = get_object_or_404(queryset, pk=self.request.headers.get('user-id'))

        if questions_length := Questions.objects.all().count():
            perfomace_index = trunc(obj.correct_answers / questions_length)
            obj.perfomace_index = str(100 * perfomace_index) + '%'
            obj.save()

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
