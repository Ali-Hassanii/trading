import finnhub
from matplotlib import pyplot as plt
from calendar import timegm
from os import uname, system

# set clear command (to cleaning screen)
if uname()[0] == 'Windows':
    clear = 'cls'
else:
    clear = 'clear'


class ConnectFinnhub:
    def __init__(self, _token):
        self.token = _token
        self.client = finnhub.Client(api_key=self.token)
        self.chart_data = None

        self.start_pint = None
        self.end_point = None
        self.resolution = None
        self.symbol = None

    def input_date(self):
        while True:
            _date = list(input('>>>').strip().split(' '))
            try:
                assert len(_date) == 6
                _date = [int(i) for i in _date]  # convert each number into int
                _date = tuple(_date)  # time object is better to be as tuple instead of list
                _date_sec = timegm(_date)
                del _date
                print('[i] %info% : date have been set')
                return _date_sec
            except ValueError:
                print(
                    '[Error] Converting error\n'
                    'could not convert input numbers into int\n'
                    'try again..\n'

                )
            except AssertionError:
                print(
                    '[Error] number of input is out of range\n'
                    'You should enter 5 number [year mouth day hour minute second]\n'
                    'Try again..\n'
                )

    def set_date_range(self):
        system(clear)
        print(
            'Enter interval initial value:\n'
            '[i] Split date by space (as [year mouth data hour minute second])\n',
            end=''
        )
        self.start_pint = self.input_date()

        print(
            'Enter interval end value:\n',
            end=''
        )
        self.end_point = self.input_date()

    def fetch_data(self):
        system(clear)
        print(
            'Select data resolution:\n'
            '\t_1_> 1\n'
            '\t_2_> 5\n'
            '\t_3_> 15\n'
            '\t_4_> 30\n'
            '\t_5_> 60\n'
            '\t_6_> Day\n'
            '\t_7_> Weak\n'
            '\t_8_> Mouth\n'
        )

        # validation input
        while True:
            resolution = input('>>>').strip()
            try:
                self.resolution = int(resolution)
                assert 0 < self.resolution < 9
                del resolution
                self.resolution = [1, 5, 15, 30, 60, 'D', 'W', 'M'][self.resolution - 1]
                print('[i] %info% : resolution have been set')
                break
            except ValueError:
                print(
                    '[Error] wrong input\n'
                    'please enter valid number\n'
                    'try again..\n'
                )
            except AssertionError:
                print(
                    '[Error] input is out of range\n'
                    'enter number between 0 and 9\n'
                    'try again..\n'
                )

        print('Enter stock symbol:')
        while True:
            self.symbol = input('>>>').strip().upper()
            with open('stocks.txt', 'r') as file:
                _stocks = file.read()
                if self.symbol in _stocks:
                    print('[i] %info% : symbol have been set')
                    break
                else:
                    print(
                        '[Error] stock name not found\n'
                        'please enter valid stock symbol\n'
                        'try again..\n'
                    )
        while True:
            try:
                self.chart_data = self.client.stock_candles(
                    symbol=self.symbol,
                    resolution=self.resolution,
                    _from=self.start_pint,
                    to=self.end_point
                )
                print('[i] %info% : data have been downloaded')
                return self.chart_data
            except finnhub.exceptions.FinnhubAPIException:
                print(
                    '[Error] invalid API key\n'
                    'please reenter your api key:\n'
                    'try again..\n'
                )
                self.token = input('>>>').strip()
                self.client = finnhub.Client(self.token)


class Visualize:
    def __init__(self, _chart_data):

        self.extracted_data = []  # final data goes there

        _open = _chart_data['o']
        _close = _chart_data['c']
        _high = _chart_data['h']
        _low = _chart_data['l']
        if len(_open) == len(_close) and len(_open) == len(_high) and len(_open) == len(_low):
            print('[i] %info% :', len(_open), 'objects have been found')
        for i in range(len(_open)):
            self.extracted_data.append([_open[i], _close[i], _high[i], _low[i]])
        del _open, _close, _high, _low

    def candles(self):
        for index in range(len(self.extracted_data)):
            _item = self.extracted_data[index]
            plt.bar(index, height=_item[2] - _item[1], bottom=_item[1], width=0.1, color='green')  # max
            plt.bar(index, height=_item[1] - _item[3], bottom=_item[3], width=0.1, color='red')  # min
            if _item[0] > _item[1]:
                plt.bar(index, height=_item[0] - _item[1], bottom=_item[1], color='red')
            elif _item[0] < _item[1]:
                plt.bar(index, _item[1] - _item[0], bottom=_item[0], color='green')


if __name__ == '__main__':
    print(
        'What is your token?\n'
        '[!] Don\'t have token? Sign in into https://finnhub.io to get one!\n'
        '>>>',
        end=''
    )
    token = input().strip()

    api = ConnectFinnhub(token)
    api.set_date_range()
    chart_data = api.fetch_data()

    chart = Visualize(_chart_data=chart_data)
    chart.candles()
    plt.title(api.symbol)
    plt.show()
