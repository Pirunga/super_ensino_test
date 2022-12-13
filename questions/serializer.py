from rest_framework import serializers
from questions.models import Questions, User, UserMark


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'username',
        ]


class UserMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMark
        fields = ['id']
class QuestionsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    user_mark_id = UserMarkSerializer(required=False)

    class Meta:
        model = Questions
        fields = [
            'id',
            'question',
            'alternative_a',
            'alternative_b',
            'alternative_c',
            'alternative_d',
            'correct_alternative',
            'created_by',
            'user_mark_id',
        ]


class UserPerfomaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'correct_answers',
            'wrong_answers',
            'perfomace_index',
        ]
