from Analyser.logger import logging
from Analyser.exception import AnalyserException
from Analyser.constant import *
from collections import Counter
import sys
import pandas as pd


class commonWords:
    def __init__(self, selected_user, df):
        try:
            logging.info(f"{'>>'*20} Common Words Log Started {'<<'*20} ")
            self.selected_user = selected_user
            self.df = df

        except Exception as e:
            raise AnalyserException(e,sys)


    def most_common_words(self):
        try:

            logging.info(f"********** Searching Most Common Words ********** ")

            stopWFile = open(STOP_WORD_FILE_NAME_KEY,'r')
            stopWords = stopWFile.read()

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]
            else:
                df = self.df
            logging.info("Data Loaded.")

            temp = df[df[USER_COLUMN_HEADER_KEY] != 'Group Notification']
            temp = temp[temp[MESSAGE_COLUMN_HEADER_KEY] != "<Media omitted>\n"]

            words = []
            for message in temp[MESSAGE_COLUMN_HEADER_KEY]:
                for word in message.lower().split():
                    if word not in stopWords:
                        words.append(word)

            most_common_df =  pd.DataFrame(Counter(words).most_common(20))

            logging.info(f"********** Most Common Words Found ********** ")

            return most_common_df

        except Exception as e:
            raise AnalyserException(e,sys)