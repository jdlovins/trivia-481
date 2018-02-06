from django.shortcuts import render, redirect
from .models import Question, Answer

# Create your views here.


def index(request):
    # Example of adding objects to database
    # answer = Answer.objects.create(main="Red")
    # answer.save()
    # question = Question.objects.create(content="What is the color of an apple?", ans=answer)
    # question.save()
    # return render(request, 'index.html', {'question': question, 'answer': answer})
    return render(request, 'index.html')
