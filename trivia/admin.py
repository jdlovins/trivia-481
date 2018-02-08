from django.contrib import admin
from trivia.models import Question, Answer, GameUser, Room

# Register your models here.


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(GameUser)
admin.site.register(Room)
