from Analyser.logger import logging
from Analyser.exception import AnalyserException
from Analyser.constant import *
import sys
from wordcloud import WordCloud

class worldCloud:
    def __init__(self, selected_user, df):
        try:
            logging.info(f"{'>>'*20} WorldCloud Log Started {'<<'*20} ")
            self.selected_user = selected_user
            self.df = df

        except Exception as e:
            raise AnalyserException(e,sys)


    def create_worldCloud(self):
        try:


            logging.info(f"********** WorldCloud Creation Started ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]
            else:
                df = self.df
            
            logging.info("Data Loaded.")

            wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
            df_wordcloud = wc.generate(df[DF_MESSAGE_KEY].str.cat(sep=" "))

            logging.info(f"********** WorldCloud Created ********** ")

            return df_wordcloud

        except Exception as e:
            raise AnalyserException(e,sys)