from django.shortcuts import render, redirect
from .models import Question, Answer, Room
import json
import datetime


# Create your views here.


def index(request):
    # Example of adding objects to database
    # answer = Answer.objects.create(main="Red")
    # answer.save()
    # question = Question.objects.create(content="What is the color of an apple?", ans=answer)
    # question.save()
    # return render(request, 'index.html', {'question': question, 'answer': answer})
    return render(request, 'index.html')


def broadcast(request):
    rooms = Room.objects.all()

    '''
     self.websocket_group.send(
        #     {"text": json.dumps(final_msg)}
        # )
        '''

    for r in rooms:
        r.websocket_group.send(
            {
                "text": json.dumps({
                    "type": "BROADCAST",
                    "content": "Broadcast sent! (" + str(datetime.datetime.now().time()) + ")"
                })
            }
        )

    return render(request, 'broadcast.html')
