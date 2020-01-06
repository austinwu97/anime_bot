## happy path
* greet
  - action_hello_world
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## search 
* search 
  - action_search
  
## get_started
* get_started
  - utter_get_started
 
## top_anime
* top_anime
  - action_top_anime

## airing_today
* airing_today
  - action_airing_today
  
## faq
* ask_faq
  - respond_ask_faq
 
## genre path 
* request_genre
  - genre_form
  - form{"name": "genre_form"}
  - form{"name": null}