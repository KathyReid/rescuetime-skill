# B63Xvi5l2Ky90cBhEu8U2PDwAcy39AuUosX6OOfJ
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
import requests

__author__ = 'kathyreid'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


class Rescuetime(MycroftSkill):
    # The constructor of the Skill, which calls MycroftSkill's constructor
    def __init__(self):
        MycroftSkill.__init__(self)

    # This method loads the files needed for the Skill's functioning, and
    # creates and registers each intent that the Skill uses
    def initialize(self):
        rescuetime_intent = IntentBuilder("RescuetimeIntent").\
            require("rescuetime").build()
        self.register_intent(rescuetime_intent, self.handle_rescuetime)

        """Check to see if the apikey has been entered in Settings"""
        if not self.settings.get('rescuetime_apikey'):
            LOGGER.error('rescuetime_apikey is not set on home.mycroft.ai')
            self.speak_dialog('ErrorAPIkeyNotSet')

    @intent_file_handler('rescuetime.intent')
    def handle_rescuetime(self, message):
        LOGGER.info(self.settings['rescuetime_apikey'])
        #productivity_pulse = #self._get_productivity_pulse(self.settings['rescuetime_apikey'])
        #LOGGER.info(productivity_pulse)

    # Private methods
    def _get_productivity_pulse(self):
        """Return the current productivity pulse using percent"""
        LOGGER.info(apikey)
        APIstring = self._get_API_request_string()
        r = requests.get('https://www.rescuetime.com/anapi/daily_summary_feed', auth=('', apikey))
        # check that the status code that is returned is 200 OK
        LOGGER.info(r)

    #def _get_API_request_string(self, apikey)

def create_skill():
    return Rescuetime()
