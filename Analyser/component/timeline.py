from Analyser.logger import logging
from Analyser.exception import AnalyserException
from Analyser.constant import *
import sys


class timeline:
    def __init__(self, selected_user, df):
        try:
            logging.info(f"{'>>'*20} Timeline Log Started {'<<'*20} ")
            self.selected_user = selected_user
            self.df = df

        except Exception as e:
            raise AnalyserException(e,sys)


    def monthly_timleine(self):
        try:

            logging.info(f"********** Creating Monthly Timeline ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]
            else:
                df = self.df
            logging.info("Data Loaded.")
            
            timeline = df.groupby([YEAR_HEADER_KEY, MONTH_NUM_HEADER_KEY, MONTH_HEADER_KEY]).count()[MESSAGE_COLUMN_HEADER_KEY].reset_index()

            time = []
            for i in range(timeline.shape[0]):
                time.append(timeline[MONTH_HEADER_KEY][i] + " - " + str(timeline[YEAR_HEADER_KEY][i]))

            timeline[TIME_KEY] = time

            logging.info(f"********** Monthly Timeline Created ********** ")

            return timeline

        except Exception as e:
            raise AnalyserException(e,sys)


    def daily_timleine(self):
        try:

            logging.info(f"********** Creating Daily Timeline ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]

            df = self.df
            logging.info("Data Loaded.")
            
            d_timeline = df.groupby(DATE_HEADER_KEY).count()[MESSAGE_COLUMN_HEADER_KEY].reset_index()
    

            logging.info(f"********** Daily Timeline Created ********** ")

            return d_timeline

        except Exception as e:
            raise AnalyserException(e,sys)