from rest_framework import serializers
from .models import Poll, Question, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'password']

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
        
        question_instances = [
            Question(title=question_data['title'], choices=question_data['choices']) 
            for question_data in questions_data
        ]
        
        Question.objects.bulk_create(question_instances)

        poll.questions.add(*question_instances)

        return poll

class PollUpdateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'questions', 'is_open']

    def update(self, instance, validated_data):
        if 'creater' in validated_data:
            raise serializers.ValidationError({'creater': 'The creater field cannot be updated.'})

        questions_data = validated_data.pop('questions', None)

        instance.title = validated_data.get('title', instance.title)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.save()

        if questions_data is not None:
            instance.questions.clear()

            question_instances = [
                Question(title=question_data['title'], choices=question_data['choices'])
                for question_data in questions_data
            ]

            Question.objects.bulk_create(question_instances)

            instance.questions.add(*question_instances)

        return instance
