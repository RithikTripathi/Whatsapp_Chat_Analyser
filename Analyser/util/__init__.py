import os

from Analyser.logger import logging
from Analyser.exception import AnalyserException
from Analyser.constant import *
import re # for regex
import pandas as pd
import sys





class preprocess:
    
        def __init__(self, data):
            try:
                logging.info(f"{'>>'*20} Data Preprocessing Started. {'<<'*20} ")
                self.data = data

            except Exception as e:
                raise AnalyserException(e,sys)

        def preprocessor(self):
            try:
                
                pattern = PATTERN
                # to catch the regex expression of messages
                
                messages = re.split(pattern, self.data)[1:]
                dates = re.findall(pattern, self.data)

                df = pd.DataFrame({USER_MESSAGE_COLUMN_HEADER_KEY: messages, MESSAGE_DATE_COLUMN_HEADER_KEY: dates})
                logging.info("Dataframe Obtained.")

                # convert message_date type
                df[MESSAGE_DATE_COLUMN_HEADER_KEY] = pd.to_datetime(df[MESSAGE_DATE_COLUMN_HEADER_KEY], format='%d/%m/%y, %I:%M %p - ')

                df.rename(columns={MESSAGE_DATE_COLUMN_HEADER_KEY: MESSAGE_DATE_COLUMN_HEADER_KEY_NEW}, inplace=True)

                # separatinng user and message
                users = []
                messages = []

                for message in df[USER_MESSAGE_COLUMN_HEADER_KEY]:
                    record = re.split('([\w\W]+?):\s', message)
                    if record[1:]:  # user name:
                        users.append(record[1])
                        messages.append(record[2])
                    else:
                        users.append('Group Notification')
                        messages.append(record[0])

                logging.info("Re Framing DataFrame")

                df[USER_COLUMN_HEADER_KEY] = users
                df[MESSAGE_COLUMN_HEADER_KEY] = messages
                df.drop(columns=[USER_MESSAGE_COLUMN_HEADER_KEY], inplace=True)

                df[YEAR_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.year
                df[MONTH_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.month_name()
                df[DAY_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.day
                df[HOUR_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.hour
                df[MINUTE_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.minute
                df[DATE_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.date
                df[MONTH_NUM_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.month
                df[DAY_NAME_HEADER_KEY] = df[MESSAGE_DATE_COLUMN_HEADER_KEY_NEW].dt.day_name()

                period = []
                for hour in df[[DAY_NAME_HEADER_KEY, HOUR_HEADER_KEY]][HOUR_HEADER_KEY]:
                    if hour == 23:
                        period.append(str(hour) + "-" + str('00'))
                    elif hour == 0:
                        period.append(str('00') + "-" + str(hour + 1))
                    else:
                        period.append(str(hour) + "-" + str(hour + 1))

                df[PERIOD_HEADER_KEY] = period

                logging.info(f"{'>>'*20} Data Preprocessing Completed. {'<<'*20} ")
                
                return df

            except Exception as e:
                    raise AnalyserException(e,sys)

