from django.contrib import admin
from trivia.models import Question, Answer, GameUser, Room, RoomMeta, SubmittedAnswer

# Register your models here.


class AnswerInline(admin.StackedInline):
    model = Answer


class RoomMetaInLine(admin.StackedInline):
    model = RoomMeta

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]


class RoomAdmin(admin.ModelAdmin):
    inlines = [
        RoomMetaInLine
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(GameUser)
admin.site.register(Room, RoomAdmin)
admin.site.register(SubmittedAnswer)