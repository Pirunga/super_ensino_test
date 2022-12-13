from django.db.models import (
    CharField,
    FloatField,
    ForeignKey,
    IntegerField,
    Model,
    TextField
)
from django.contrib.auth.models import AbstractUser, User
from django.db.models.deletion import CASCADE


ALTERNATIVES = [
    ('A', 'a'),
    ('B', 'b'),
    ('C', 'c'),
    ('D', 'd'),
]


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
    
    correct_answers = IntegerField(default=0)
    wrong_answers = IntegerField(default=0)
    perfomace_index = CharField(max_length=4, default='0%')


class Questions(Model):
    created_by = ForeignKey(User, on_delete=CASCADE)
 
    question = TextField()
    alternative_a = CharField(max_length=255, null=False)
    alternative_b = CharField(max_length=255, null=False)
    alternative_c = CharField(max_length=255, null=False)
    alternative_d = CharField(max_length=255, null=False)
    correct_alternative = CharField(
        max_length=1,
        null=False,
        choices=ALTERNATIVES
    )


class UserMark(Model):
    question = ForeignKey(Questions, on_delete=CASCADE)

    user = ForeignKey(User, on_delete=CASCADE)

    user_mark = CharField(
        max_length=1,
        null=False,
        choices=ALTERNATIVES
    )