from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .choices import CategoryType
from channels import Group
from random import randint
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


class GameUser(models.Model):

    name = models.CharField(max_length=25)
    reply_channel = models.CharField(max_length=50)
    creator = models.BooleanField()

    def __str__(self):
        return self.name


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(GameUser, blank=True)
    capacity = models.IntegerField()
    rounds = models.IntegerField()
    time = models.IntegerField()
    started = models.BooleanField()
    code = models.IntegerField()


    @classmethod
    def create(cls):
        room = cls(code=randint(1, 9999))  # could be really unlucky and get a dupe code but oh well
        return room

    def __str__(self):
        return f"{self.title} - Code: {self.code} - Users: {len(self.users.all())}/{self.capacity}"

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
