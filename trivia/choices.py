from djchoices import DjangoChoices, ChoiceItem


class CategoryType(DjangoChoices):
    sports = ChoiceItem("Sports")
    school = ChoiceItem("School")