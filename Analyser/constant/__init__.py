import os

from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


ROOT_DIR = os.getcwd()

# stats related variable
OVERALL_ANALYSIS_KEY = "Overall Analysis"
DF_USER_KEY = "user"
DF_MESSAGE_KEY = "message"

# preprocessing related variables
PATTERN = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s+\wm\s-\s'
USER_MESSAGE_COLUMN_HEADER_KEY = "user_message"
MESSAGE_DATE_COLUMN_HEADER_KEY = "message_date"
MESSAGE_DATE_COLUMN_HEADER_KEY_NEW = "date"

USER_COLUMN_HEADER_KEY = "user"
MESSAGE_COLUMN_HEADER_KEY = "message"

YEAR_HEADER_KEY = "year"
MONTH_HEADER_KEY = "month"
DAY_HEADER_KEY = "day"
HOUR_HEADER_KEY = "hour"
MINUTE_HEADER_KEY = "minute"
DATE_HEADER_KEY = "Date"
MONTH_NUM_HEADER_KEY = "month_num"
DAY_NAME_HEADER_KEY = "day_name"
PERIOD_HEADER_KEY = "period"

# most common words related variables
STOP_WORD_FILE_NAME_KEY = "stop_hinglish.txt"

# app related variables
FETCH_RESULTS_KEY = "Fetch Results"

# timeline related variables
TIME_KEY = 'time'

# activity related function
AGGREGATION_FUNCTION_KEY = 'count'

