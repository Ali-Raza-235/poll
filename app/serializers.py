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
            question = Question.objects.create(**question_data)
            poll.questions.add(question)
        
        return poll
    
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        creater_email = validated_data.get('creater', instance.creater.email)

        if creater_email != instance.creater.email:
            user, created = User.objects.get_or_create(email=creater_email)
            instance.creater = user

        instance.title = validated_data.get('title', instance.title)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.save()

        if questions_data is not None:
     
            for question_data in questions_data:
                question = Question.objects.create(**question_data)
                instance.questions.add(question)

        return instance
