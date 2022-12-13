from django.urls import path
from questions.views import QuestionsView, UserMarkView, UserView


urlpatterns = [
    path('', QuestionsView.as_view()),
    path('<int:question_id>/', QuestionsView.as_view()),
    path('user-mark/', UserMarkView.as_view()),
    path('user/<int:pk>', UserView.as_view()),
]