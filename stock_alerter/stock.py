from datetime import timedelta
import bisect
import collections
from enum import Enum
from .timeseries import TimeSeries

class StockSignal(Enum):
     buy = 1
     neutral = 0
     sell = -1

class NotEnoughDataException(Exception):
     pass

class Stock:
    LONG_TERM_TIMESPAN = 10
    SHORT_TERM_TIMESPAN = 5

    def __init__(self, symbol):
        self.symbol = symbol
        self.history = TimeSeries()

    @property
    def price(self):
         try:
              return self.history[-1].value
         except IndexError:
              return None

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        self.history.update(timestamp, price)

    def is_increasing_trend(self):
        return self.history[-3].value < self.history[-2].value < self.history[-1].value

    def _is_crossover_below_to_above(self, prev_ma,
                                     prev_reference_ma,
                                     current_ma, current_reference_ma):
        return prev_ma < prev_reference_ma and current_ma > current_reference_ma

    def _value_on(self, end_date, timespan):
        moving_avg_series = self.history.get_closing_price_list(end_date, timespan)
        if len(moving_avg_series) < timespan:
            raise NotEnoughDataException("Not enough data to calculate moving average")
        price_list = [update.value for update in moving_avg_series]
        return sum(price_list)/timespan


    def get_crossover_signal(self, on_date):
        NUM_DAYS = self.LONG_TERM_TIMESPAN + 1

        closing_price_list = self.history.get_closing_price_list(on_date, NUM_DAYS)
        # Return NEUTRAL signal
        if len(closing_price_list) < NUM_DAYS:
            return StockSignal.neutral

        long_term_series = closing_price_list[-self.LONG_TERM_TIMESPAN:]
        prev_long_term_series = closing_price_list[-self.LONG_TERM_TIMESPAN-1:-1]
        short_term_series = closing_price_list[-self.SHORT_TERM_TIMESPAN:]
        prev_short_term_series = closing_price_list[-self.SHORT_TERM_TIMESPAN-1:-1]

        try:
            long_term_ma = self._value_on(on_date, self.LONG_TERM_TIMESPAN)
            prev_long_term_ma = self._value_on(on_date - timedelta(1), self.LONG_TERM_TIMESPAN)
            short_term_ma = self._value_on(on_date, self.SHORT_TERM_TIMESPAN)
            prev_short_term_ma = self._value_on(on_date - timedelta(1), self.SHORT_TERM_TIMESPAN)
        except NotEnoughDataException:
             pass

        # BUY signal
        if self._is_crossover_below_to_above(prev_short_term_ma,
                                             prev_long_term_ma,
                                             short_term_ma,
                                             long_term_ma):
                    return StockSignal.buy

        # BUY signal
        if self._is_crossover_below_to_above(prev_long_term_ma,
                                             prev_short_term_ma,
                                             long_term_ma,
                                             short_term_ma):
                    return StockSignal.sell

        # NEUTRAL signal
        return StockSignal.neutral
