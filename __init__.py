# B63Xvi5l2Ky90cBhEu8U2PDwAcy39AuUosX6OOfJ
# https://www.rescuetime.com/anapi/data?key=B63Xvi5l2Ky90cBhEu8U2PDwAcy39AuUosX6OOfJ&restrict_kind=efficiency&resolution_time=day&restrict_begin=2019-02-22&restrict_end=2019-02-22&format=json&perspective=interval
# https://realpython.com/python-json/

# @TODO what is the "standard" way to do Python header commenting?
# Is this a docstrings thing?


from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
import requests
from datetime import datetime, timedelta
import json

__author__ = "kathyreid"

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
        rescuetime_intent = (
            IntentBuilder("RescuetimeIntent").require("rescuetime").build()
        )
        self.register_intent(rescuetime_intent, self.handle_rescuetime)

        """Set initial variables for the Rescuetime API"""
        self.rescuetime_API_URL_daily_summary = (
            "https://www.rescuetime.com/anapi/daily_summary_feed"
        )

        # these are not currently implemented, but are listed here for future expansion - see https://www.rescuetime.com/anapi/setup/documentation
        # self.rescuetime_API_URL_analytic_data = 'https://www.rescuetime.com/anapi/data'
        # self.rescuetime_API_URL_alerts_feed = 'https://www.rescuetime.com/anapi/alerts_feed'
        # self.rescuetime_API_URL_highlights_feed = 'https://www.rescuetime.com/anapi/highlights_feed'

        self.rescuetime_API_URL_daily_summary = "https://www.rescuetime.com/anapi/data"
        self.rescuetime_API_resolution_time = "day"
        self.rescuetime_API_restrict_kind = "overview"
        self.rescuetime_API_date_restrict_begin = datetime.now().isoformat()
        self.rescuetime_API_date_restrict_end = datetime.strftime(
            datetime.now() - timedelta(1), "%Y-%m-%d"
        )
        self.rescuetime_API_format = "json"
        self.rescuetime_API_perspective = "overview"

        """Check to see if the apikey has been entered in Settings"""
        if not self.settings.get("rescuetime_apikey"):
            LOGGER.error("rescuetime_apikey is not set on home.mycroft.ai")
            self.speak_dialog("ErrorAPIkeyNotSet")
        else:
            self.rescuetime_API_key = self.settings.get("rescuetime_apikey")

        """@TODO For code review - does this function need  a return() value at all? """

    @intent_file_handler("rescuetime.intent")
    def handle_rescuetime(self, message):
        productivity_pulse = self._get_productivity_pulse()
        # LOGGER.info(productivity_pulse)

    # Private methods
    def _get_productivity_pulse(self):
        """Return the current productivity pulse using percent"""
        # This function uses the defaults, we don't have to override any of the self.* values

        # @TODO is there a better data structure to handle these strings?
        # Should this be handled as some kind of object, or Dict?
        # Rather than individual variables?
        # How are null or empty values handled in an object or Dict?
        API_request_string = self._get_API_request_string(
            self.rescuetime_API_URL_daily_summary,
            self.rescuetime_API_key,
            self.rescuetime_API_resolution_time,
            self.rescuetime_API_restrict_kind,
            self.rescuetime_API_date_restrict_begin,
            self.rescuetime_API_date_restrict_end,
            self.rescuetime_API_format,
            self.rescuetime_API_perspective,
        )

        # the Python interpreter isn't converting all the values in
        # API_request_string
        LOGGER.info(self.rescuetime_API_URL_daily_summary)
        LOGGER.info(self.rescuetime_API_key)
        LOGGER.info(self.rescuetime_API_resolution_time)
        LOGGER.info(self.rescuetime_API_restrict_kind)
        LOGGER.info(self.rescuetime_API_date_restrict_begin)
        LOGGER.info(self.rescuetime_API_date_restrict_end)
        LOGGER.info(self.rescuetime_API_format)
        LOGGER.info(self.rescuetime_API_perspective)

        LOGGER.info("request string is: ", API_request_string)

        r = requests.get(API_request_string)
        # check that the status code that is returned is 200 OK
        # @TODO need to use a try ... catch ... throw construct here to check for a 200 code,
        # and exit with a failure if the return code is not 200 OK

        LOGGER.info(r)
        LOGGER.info(r.json())

    def _get_API_request_string(
        self,
        API_url,
        API_key,
        API_resolution_time,
        API_restrict_kind,
        API_dt_begin,
        API_dt_end,
        API_format,
        API_perspective,
    ):
        """Return a URL that can be used to make a GET request on the Rescuetime API"""

        LOGGER.info(API_url)
        LOGGER.info(API_key)
        LOGGER.info(API_resolution_time)
        LOGGER.info(API_restrict_kind)
        LOGGER.info(API_dt_begin)
        LOGGER.info(API_dt_end)
        LOGGER.info(API_format)
        LOGGER.info(API_perspective)

        APIstring = (
            API_url
            + "?"
            + "key="
            + API_key
            + "&"
            + "restrict_kind="
            + API_restrict_kind
            + "&"
            + "resolution_time="
            + API_resolution_time
            + "&"
            + "restrict_begin="
            + API_dt_begin
            + "&"
            + "restrict_end="
            + API_dt_end
            + "&"
            + "format="
            + API_format
            + "&"
            + "perspective="
            + API_perspective
        )

        LOGGER.info(APIstring)

        # APIstring = 'https://www.rescuetime.com/anapi/data?key=B63Xvi5l2Ky90cBhEu8U2PDwAcy39AuUosX6OOfJ&restrict_kind=efficiency&resolution_time=hour&restrict_begin=2019-03-03&restrict_end=2019-02-03&format=json&perspective=overview'

        return APIstring


def create_skill():
    return Rescuetime()
