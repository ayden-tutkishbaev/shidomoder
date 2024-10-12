from aiogram.fsm.state import State, StatesGroup


class Sending(StatesGroup):
    message = State()


class EngStoryCreation(StatesGroup):
    title = State()
    text = State()


class RusStoryCreation(StatesGroup):
    title = State()
    text = State()


class BugReport(StatesGroup):
    message = State()


class AnswerMessage(StatesGroup):
    to = State()
    message = State()


class GenerateAIResponse(StatesGroup):
    text = State()


class AlterHowToAdd(StatesGroup):
    text = State()


class AlterCommandsList(StatesGroup):
    text = State()


class AlterAboutDev(StatesGroup):
    text = State()


class AlterAdditionToAGroup(StatesGroup):
    text = State()


class AlterWM(StatesGroup):
    text = State()


class AlterAPPhoto(StatesGroup):
    text = State()