# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from csv_processor import dimension_columns
from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.forms import FormAction 
from rasa_sdk.executor import CollectingDispatcher
import logging
import pandas as pd

logger = logging.Logger("ActionServer")

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.debug("Here are all the slots")
        logger.debug(tracker.slots)
        dispatcher.utter_message(text="Hello World!")
        df = pd.read_csv('sample_dataset_chatbot.csv')
        agg = "mean"
        if tracker.get_slot("agg") is not None:
            agg = tracker.get_slot("agg")
        if tracker.get_slot("metric") is not None:
            metric  = tracker.get_slot("metric")
        elif tracker.get_slot("prev_metric") is not None:
            metric = tracker.get_slot("prev_metric")
        else:
            dispatcher.utter_message("No Metric mentioned in context. Can you tell me rephrase the sentance")
            return [AllSlotsReset()]
        for dim_col in dimension_columns:
            if tracker.get_slot(dim_col) is not None:
                dim = dim_col
                dim_val = tracker.get_slot(dim_col)
                answer= df[df[dim]==dim_val][metric].agg(agg)
                dispatcher.utter_message("Answer is {}".format(answer))
                break 
        return [AllSlotsReset()]

