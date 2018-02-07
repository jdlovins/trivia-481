from django.db import models
from .choices import CategoryType
from channels import Group
import json

# Create your models here.


class Answer(models.Model):
    content = models.CharField(default='', blank=False, max_length=150)
    correct = models.BooleanField(default=False)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)


class Question(models.Model):
    content = models.TextField(default='', blank=False, max_length=150)
    category = models.CharField(max_length=20, choices=CategoryType.choices)

    def __str__(self):
        return self.content


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group(f"room-{self.id}")

    def send_message(self, message):
        """
        Called to send a message to the room on behalf of a user.
        """
        #final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        # self.websocket_group.send(
        #     {"text": json.dumps(final_msg)}
        # )
        pass
