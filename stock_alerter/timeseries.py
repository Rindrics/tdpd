import bisect
import collections
from datetime import timedelta


Update = collections.namedtuple("Update", ["timestamp", "value"])

class TimeSeries:
    def __init__(self):
        self.series = []

    def __getitem__(self, index):
        return self.series[index]

    def update(self, timestamp, value):
        bisect.insort_left(self.series, Update(timestamp, value))

    def get_closing_price_list(self, on_date, num_days, price_history):
        closing_price_list = []
        for i in range(num_days):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(price_history):
                if price_event.timestamp.date() > chk:
                    pass
                if price_event.timestamp.date() == chk:
                    closing_price_list.insert(0, price_event)
                    break
                if price_event.timestamp.date() < chk:
                    closing_price_list.insert(0, price_event)
                    break
        return closing_price_list
