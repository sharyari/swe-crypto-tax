from datetime import datetime, timedelta
import os.path

EUROSEK_FILE = "EURSEK.csv"


def read_csv(filename):
    with open(filename, "r") as fp:
        fp.readline()  # skip first line, dc about colunmns
        for line in fp.readlines():
            date, _dc, sek = line.strip().split(",")
            yield (datetime.strptime(date, "%Y-%m-%d"), float(sek))

def get_exchange_csv(fr, to):
    # Returns the filename of the exchange rate file and a boolean
    # indicator (from SEK->EUR we can infer the values for EUR->SEK)
    if os.path.isfile(fr+to+'.csv'):
        return (fr + to + ".csv", False)
    elif os.path.isfile(to + fr + '.csv'):
        return (to + fr + ".csv", True)
    else:
        print("No exchange rate informations between {} and {}".format(fr, to))

# Class which converts from one fiat currency to another
class ExchangeRate():
    def __init__(self, den_from, den_to, t_fr=None, t_to=None):
        filename, inverted = get_exchange_csv(den_from, den_to) 

        self.rates = {}
        rates = list(read_csv(filename))

        # If nothing specified, start from first data available
        if not t_fr:
            t_fr = rates[0][0]
        # If nothing specified, try to read until todays date
        if not t_to:
            t_to = datetime.now()
        # used for iteration
        delta = timedelta(days=1)

        rates = dict(rates)

        # We iterate over available data by date in chronological order. If no data is available,
        # we assume the same value as the last date for which data existed. This happens for holidays
        last_known_value = -1
        while t_fr <= t_to:
            v = rates.get(t_fr, last_known_value)
            last_known_value = v
            self.rates[t_fr] = v
            t_fr = t_fr + delta

        if inverted:
            for k, v in self.rates.items():
                self.rates[k] = 1/v

    def convert(self, dt, euro):
        dt_day = datetime(dt.year, dt.month, dt.day)
        rate = self.rates.get(dt_day)
        return float(euro)*rate

if __name__ == '__main__':
    rates = ExchangeRate('EUR', 'SEK')
    print(rates.rates)
    dt = datetime.now()
    dt_day = datetime(dt.year, dt.month, dt.day)
    print(dt_day-timedelta(days=1))
    print(rates.rates.get(dt_day-timedelta(days=1)))
