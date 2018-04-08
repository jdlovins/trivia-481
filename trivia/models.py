from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from .choices import CategoryType, ButtonType, RoomStatus
from channels import Group
from random import randint
import json

# Create your models here.


class Answer(models.Model):
    content = models.CharField(default='', blank=False, max_length=150)
    correct = models.BooleanField(default=False)
    button = models.CharField(max_length=1, choices=ButtonType.choices, default=ButtonType.A)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def to_dict(self):
        return {"answer": self.content, "button": self.button, "pk": self.id}


class Question(models.Model):
    content = models.TextField(default='', blank=False, max_length=150)
    category = models.CharField(max_length=20, choices=CategoryType.choices)

    def __str__(self):
        return self.content


class SubmittedAnswer(models.Model):
    user = models.ForeignKey("GameUser", on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    rank = models.IntegerField()


class GameUser(models.Model):

    name = models.CharField(max_length=25)
    reply_channel = models.CharField(max_length=50)
    creator = models.BooleanField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name, "creator": self.creator, "points": self.points}


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(GameUser, blank=True)
    # meta = models.ForeignKey('RoomMeta', on_delete=models.CASCADE)
    capacity = models.IntegerField()
    rounds = models.IntegerField()
    time = models.IntegerField()
    status = models.CharField(max_length=15, choices=RoomStatus.choices, default=RoomStatus.NONE)
    code = models.IntegerField()

    submitted_answers = models.ManyToManyField(SubmittedAnswer, blank=True)

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
        self.websocket_group.send(message)


class RoomMeta(models.Model):
    users_answered = models.IntegerField()
    owner_room = models.OneToOneField(Room, related_name='meta_info', on_delete=models.CASCADE, null=True)


def pre_delete_room(sender, instance, **kwargs):
    for user in instance.users.all():
        user.delete()


pre_delete.connect(pre_delete_room, sender=Room)