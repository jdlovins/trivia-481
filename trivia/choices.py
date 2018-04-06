from djchoices import DjangoChoices, ChoiceItem


class CategoryType(DjangoChoices):
    sports = ChoiceItem("Sports")
    school = ChoiceItem("School")


class ButtonType(DjangoChoices):
    A = ChoiceItem()
    B = ChoiceItem()
    C = ChoiceItem()
    D = ChoiceItem()