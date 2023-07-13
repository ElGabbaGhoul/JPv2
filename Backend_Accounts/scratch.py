from datetime import datetime

def Trimmed_datetime():
    current_datetime = datetime.now()
    trimmed_datetime = current_datetime.replace(microsecond=0)
    return trimmed_datetime

Trimmed_datetime()