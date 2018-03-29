from triviagame.celery import app


@app.task
def test_task():
    print("hello!")


@app.task
def start_game_countdown(room_id):
    print("We got the room id: " + room_id)