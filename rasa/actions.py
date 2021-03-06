# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
#
#
# This is a simple example for a custom action which utters "Hello World!"
from jikanpy import Jikan
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted

from datetime import datetime

NUMBER_OF_SEARCH_RESULT = 1
ANIME_GENRES = {
    'action': 1,
    'adventure': 2,
    'comedy': 4,
    'mystery': 7,
    'drama': 8,
    'fantasy': 10,
    'horror': 14,
    'romance': 22,
    'school': 23,
    'space': 29,
    'psychological': 40,
    'thriller': 41,
    'seinen': 42,
    'josei': 43
}


class GenreForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "genre_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["genre", "num_anime"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "genre": [self.from_entity(entity="genre", intent="request_genre"),
                      self.from_entity(entity="genre", intent=["inform", "request_genre"])],

            "num_anime": [self.from_entity(entity="num_anime", intent=["inform"]),
                          self.from_entity(entity="CARDINAL")],

        }

    def submit(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        genre = tracker.get_slot(key="genre")
        num_anime = tracker.get_slot(key="num_anime")
        genre = genre.lower()

        # error checking for genre
        if genre not in ANIME_GENRES:
            dispatcher.utter_message(text="Error, could not find the genre anime. Please try again")
            return [SlotSet("genre", None), SlotSet("num_anime", None)]  # reset the form

        # error checking for num_anime
        try:
            num_anime = int(num_anime)
        except ValueError:
            dispatcher.utter_message(text="Error, please enter the number of anime as a digit. Please try again")
            return [SlotSet("num_anime", None)]  # reset the form

        dispatcher.utter_message(text="Displaying the most popular " + str(num_anime) + " anime for " + genre + " anime")

        genre_num = ANIME_GENRES[genre]
        jikan = Jikan()
        top_anime = jikan.genre(type='anime', genre_id=genre_num)
        result = top_anime['anime'][:num_anime]

        for anime in result:

            image = {
                "type": "image",
                "payload": {
                    "src": anime['image_url'],
                    "width": 200,
                    "height": 300
                }
            }

            dispatcher.utter_message(text=anime['title'], attachment=image)
            dispatcher.utter_message(text="Read more about it here: " + anime['url'])

        return [SlotSet("genre", None),SlotSet("num_anime", None)]  # reset the form

class ActionAiringToday(Action):

    def name(self) -> Text:
        return "action_airing_today"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jikan = Jikan()
        today_date = datetime.today().strftime('%A').lower()
        dispatcher.utter_message(text="Here are some anime that are airing today")
        today_anime = jikan.schedule(day=today_date)[today_date][:3]

        for anime in today_anime:

            image = {
                "type": "image",
                "payload": {
                    "src": anime['image_url'],
                    "width": 200,
                    "height": 300
                }
            }

            dispatcher.utter_message(text=anime['title'], attachment=image)
            dispatcher.utter_message(text="Read more about it here: " + anime['url'])

        return []

class ActionGetStarted(Action):

    def name(self) -> Text:
        return "action_get_started"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        control = {
            "type": "control",
            "payload": {
                 "fullscreen": True,
            }
        }

        dispatcher.utter_message(attachment=control)
        dispatcher.utter_message(text="Howdy, welcome to Austin's Anime Bot! Look to the left for the types of questions you can ask me!")

        return []


class ActionTopAnime(Action):

    def name(self) -> Text:
        return "action_top_anime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jikan = Jikan()
        top_anime = jikan.top(type='anime')
        animes = top_anime['top'][:5]

        dispatcher.utter_message(text="Displaying the top 5 anime")

        for anime in animes:
            image = {
                "type": "image",
                "payload": {
                    "src": anime['image_url'],
                    "width": 200,
                    "height": 300
                }
            }

            dispatcher.utter_message(text=anime['title'], attachment=image)
            dispatcher.utter_message(text="Score: " + str(anime['score']))
            dispatcher.utter_message(text="Read more about it here: " + anime['url'])

        return []


class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Returning the top 1 results...")
        user_input = tracker.current_state()['latest_message']['text']
        output = self.search(user_input)
        for i in output:

            image = {
                "type": "image",
                "payload": {
                    "src": i['image_url'],
                    "width": 200,
                    "height": 300
                }
            }

            video = {
                "type": "video",
                "payload": {
                    "src": i['trailer_url']
                }
            }

            dispatcher.utter_message(text=i['title'], attachment=image)
            dispatcher.utter_message(text="Here's a trailer!")
            dispatcher.utter_message(attachment=video)

            '''

            play_youtube_video_snippet = """
                    <div>
                    <iframe width="420" height="315"
            src=%s style="position:fixed; left:400px; bottom:100px;">
            </iframe>
                    </div>
                    """ %(video_url)
            control = {
                "type": "control",
                "payload": {
                    "insert_html": play_youtube_video_snippet

                }

            }'''
            dispatcher.utter_message(text="Read more about it here: " + i['url'])

        return []

    def search(self, user_input):
        jikan = Jikan()
        output = []
        user_input = user_input.split(' ', 1)[1]
        search = jikan.search('anime', user_input)
        animes = search['results'][:NUMBER_OF_SEARCH_RESULT]  # get first NUMBER_OF_SEARCH_RESULT results

        for anime in animes:
            anime_output = {}
            mal_id = anime['mal_id']
            current_anime = jikan.anime(mal_id)

            anime_output['title'] = current_anime['title']
            anime_output['url'] = current_anime['url']
            anime_output['image_url'] = current_anime['image_url']
            anime_output['trailer_url'] = current_anime['trailer_url']

            output.append(anime_output)

        return output

