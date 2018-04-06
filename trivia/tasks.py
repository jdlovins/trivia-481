from triviagame.celery import app
from trivia.models import Room, Question, Answer, SubmittedAnswer
from trivia.events import UpdateProgressEvent, GameCountdownEvent, GameStartedEvent, QuestionInfoEvent, UpdatePlayerList
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
        time.sleep(2)

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
        users_count = len(room.users.all())
        rounds = 0

        while rounds <= room.rounds:

            while True:

                if len(used_questions) == question_count:
                    print("Ran out of questions... killing game")
                    return

                question_id = random.randint(1, question_count)
                if question_id not in used_questions:
                    question = Question.objects.get(pk=question_id)
                    if question is not None:
                        used_questions.append(question_id)
                        break

            print(f"We are going to send {question.id} to {room.id}")
            # send out message

            room.send_message(QuestionInfoEvent(question.content, question.id, question.category,
                                                [answer.to_dict() for answer in question.answer_set.all()]).to_json)

            while room.meta_info.users_answered != 1: #users_count:
                print(f"We have {room.meta_info.users_answered} locked in right now.")
                print("Waiting for all the users to lock in before proceeding to the next round!")
                time.sleep(1)
                room.refresh_from_db()

            # reset the users answered for the next round
            room.meta_info.users_answered = 0
            room.meta_info.save()

            for ans in room.submitted_answers.all():
                if ans.answer.correct:
                    points = (users_count - ans.rank + 1) * 5
                    print(f"We should award {ans.user.name} {points} points")
                    ans.user.points += points
                    ans.user.save()

            # update user ranks
            room.send_message(UpdatePlayerList([x.to_dict() for x in room.users.all()]).to_json)

            rounds += 1
            print("Incremeneted rounds")


