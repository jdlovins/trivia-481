from triviagame.celery import app
from trivia.models import Room, Question, Answer, SubmittedAnswer
from trivia.events import *
from trivia.utils import ordinal
from trivia.choices import RoomStatus
import time
import random


@app.task
def test_task():
    print("hello!")


@app.task
def start_game_countdown(room_id):
    print(f"Task got called! {room_id}")
    room = Room.objects.get(pk=room_id)

    if room is not None:
        time.sleep(1)

        room.send_message(GameCountdownEvent().to_json)

        for x in range(10, 0, -1):
            room.send_message(UpdateProgressEvent(x).to_json)
            time.sleep(1)

        start_game.delay(room_id)


@app.task
def start_game(room_id):
    room = Room.objects.get(pk=room_id)
    used_questions = []

    if room is not None:
        room.send_message(GameStartedEvent().to_json)
        question_count = len(Question.objects.all())
        question_pks = [x.id for x in Question.objects.all()]
        users_count = len(room.users.all())
        rounds = 1

        room.status = RoomStatus.STARTED
        room.save()

        while rounds <= room.rounds:

            while True:

                if len(used_questions) == question_count:
                    print("Ran out of questions... killing game")
                    room.send_message(UpdateStatusMessageEvent("We ran out of questions!").to_json)
                    room.send_message(UpdateProgressEvent(0).to_json)
                    return

                question_id = question_pks[random.randint(0, len(question_pks) - 1)]

                if question_id not in used_questions:
                    question = Question.objects.get(pk=question_id)
                    if question is not None:
                        used_questions.append(question_id)
                        break

            room.send_message(UpdateProgressMaxEvent(5).to_json)
            room.send_message(UpdateStatusMessageEvent("Waiting for next round....").to_json)
            room.send_message(RoundOverEvent().to_json)

            for x in range(5, -1, -1):
                print(f"[ROUND_NEXT] Sending Progress {x}")
                room.send_message(UpdateProgressEvent(x).to_json)
                time.sleep(1)

            print(f"We are going to send {question.id} to {room.id}")
            # send out message
            room.send_message(UpdateProgressMaxEvent(10).to_json)

            room.send_message(UpdateStatusMessageEvent("Round in progress... Answer quickly!").to_json)
            room.send_message(QuestionInfoEvent(question.content, question.id, question.category,
                                                [answer.to_dict() for answer in question.answer_set.all()]).to_json)

            for x in range(room.time, -1, -1):
                room.send_message(UpdateProgressEvent(x).to_json)
                print(f"[ROUND_COUNDOWN] Sending progress {x}")

                if room.meta_info.users_answered == users_count or x == 0:
                    room.send_message(RoundOverEvent().to_json)
                    print("Sending round over event")
                    break

                time.sleep(1)
                room.refresh_from_db()

            # reset the users answered for the next round
            room.meta_info.users_answered = 0
            room.meta_info.save()

            correct_message = ""
            amount_correct = 1
            for ans in room.submitted_answers.all():
                if ans.answer.correct:
                    points = (users_count - ans.rank + 1) * 5
                    correct_message += f"{ans.user.name} answered question {rounds + 1} " \
                                       f"correctly {ordinal(amount_correct)} and was awarded {points} points! \n"
                    amount_correct += 1
                    ans.user.points += points
                    ans.user.save()

            # clear out all the submitted answers
            room.submitted_answers.all().delete()

            room.send_message(UpdateLogEvent(correct_message).to_json)

            # update user ranks
            room.send_message(UpdatePlayerListEvent([x.to_dict() for x in room.users.all()]).to_json)

            rounds += 1

    #  send game over stuff here!

    room.send_message(UpdateStatusMessageEvent("Game over!").to_json)
    room.send_message(UpdateProgressEvent(0).to_json)
