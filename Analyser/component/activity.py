from Analyser.logger import logging
from Analyser.exception import AnalyserException
from Analyser.constant import *
import sys


class activity:
    def __init__(self, selected_user, df):
        try:
            logging.info(f"{'>>'*20} Activity Log Started {'<<'*20} ")
            self.selected_user = selected_user
            self.df = df

        except Exception as e:
            raise AnalyserException(e,sys)


    def weekly_activity(self):
        try:

            logging.info(f"********** Detecting Weekly Activity ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]
            else:
                df = self.df
            
            logging.info("Data Loaded.")

            logging.info(f"********** Weekly Activity Found ********** ")

            return df[DAY_NAME_HEADER_KEY].value_counts()

        except Exception as e:
            raise AnalyserException(e,sys)

    def monthly_activity(self):
        try:

            logging.info(f"********** Detecting Monthly Activity ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]

            df = self.df
            
            logging.info("Data Loaded.")

            logging.info(f"********** Monthly Activity Found ********** ")

            return df[MONTH_HEADER_KEY].value_counts()

        except Exception as e:
            raise AnalyserException(e,sys)


    def activity_heatmap(self):
        try:

            logging.info(f"********** Creating Activity Heatmap ********** ")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]

            df = self.df
            
            logging.info("Data Loaded.")

            details = df.pivot_table(
                index=DAY_NAME_HEADER_KEY, 
                columns=PERIOD_HEADER_KEY, 
                values=MESSAGE_COLUMN_HEADER_KEY, 
                aggfunc=AGGREGATION_FUNCTION_KEY).fillna(0)

            logging.info(f"********** Heatmap Created ********** ")

            return details

        except Exception as e:
            raise AnalyserException(e,sys)