from rest_framework import serializers
from .models import Poll, Question, User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'choices']

class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    creater = serializers.EmailField()

    class Meta:
        model = Poll
        fields = ['id', 'title', 'creater', 'questions', 'is_open']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        creater_email = validated_data.pop('creater')

        user, created = User.objects.get_or_create(email=creater_email)
        
        poll = Poll.objects.create(creater=user, **validated_data)
        
        for question_data in questions_data:
            Question.objects.create(**question_data)
        
        return poll