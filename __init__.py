from mycroft import MycroftSkill, intent_file_handler


class Rescuetime(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('rescuetime.intent')
    def handle_rescuetime(self, message):
        self.speak_dialog('rescuetime')


def create_skill():
    return Rescuetime()

