from Analyser.logger import logging
from Analyser.exception import AnalyserException
from Analyser.constant import *
from collections import Counter

import emoji
import sys
import pandas as pd
import streamlit as st



class emojii:
    def __init__(self, selected_user, df):
        try:
            logging.info(f"{'>>'*20} Emoji Log Started {'<<'*20} ")
            self.selected_user = selected_user
            self.df = df

        except Exception as e:
            raise AnalyserException(e,sys)


    def emoji_analysis(self):
        try:

            logging.info(f"********** Emoji Analysis Started ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]
            else:
                df = self.df
            logging.info("Data Loaded.")

            emojis = []
            for message in df[MESSAGE_COLUMN_HEADER_KEY]:
                emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
            emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

            logging.info(f"********** Emoji Analysis Completed. ********** ")

            return emoji_df

        except Exception as e:
            raise AnalyserException(e,sys)