# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
#
#
# This is a simple example for a custom action which utters "Hello World!"
from jikanpy import Jikan
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from datetime import datetime

NUMBER_OF_SEARCH_RESULT = 1


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello Pooge!")

        return []

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
            dispatcher.utter_message(text=anime['title'])

        return []


class ActionTopAnime(Action):

    def name(self) -> Text:
        return "action_top_anime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jikan = Jikan()
        top_anime = jikan.top(type='anime')
        animes = top_anime['top'][:NUMBER_OF_SEARCH_RESULT]

        dispatcher.utter_message(text="Displaying the top " + str(NUMBER_OF_SEARCH_RESULT) + " anime")

        for anime in animes:
            image = {
                "type": "image",
                "payload": {
                    "src": anime['image_url']
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
        #dispatcher.utter_message(text=str(tracker.current_state()['latest_message']['text']))
        user_input = tracker.current_state()['latest_message']['text']
        output = self.search(user_input)
        for i in output:

            image = {
                "type": "image",
                "payload": {
                    "src": i['image_url']
                }
            }

            video = {
                "type": "video",
                "payload": {
                    "src": i['trailer_url']
                }
            }

            dispatcher.utter_message(text=i['title'], attachment=image)
            dispatcher.utter_message(attachment=video)
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
