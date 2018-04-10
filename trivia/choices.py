from djchoices import DjangoChoices, ChoiceItem


class CategoryType(DjangoChoices):
    sports = ChoiceItem("Sports")
    school = ChoiceItem("School")
    history = ChoiceItem("History")
    dank_memes = ChoiceItem("Dank Memes")
    blumisms = ChoiceItem("Blumisms")
    computers = ChoiceItem("Computers")
    cars = ChoiceItem("Cars")
    famous_people = ChoiceItem("Famous People")
    sciences = ChoiceItem("Sciences")
    entertainment = ChoiceItem("Entertainment")
    arts = ChoiceItem("Arts")


class ButtonType(DjangoChoices):
    A = ChoiceItem()
    B = ChoiceItem()
    C = ChoiceItem()
    D = ChoiceItem()


class RoomStatus(DjangoChoices):
    PRE_GAME = ChoiceItem()
    STARTED = ChoiceItem()
    NONE = ChoiceItem()