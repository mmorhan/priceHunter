from time import sleep
from telegram.ext import updater, Updater
import BotConfig
import CalculateRSI
import CalculateVolume
from datetime import datetime


class Subject:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(Subject, self).__new__(self)
        return self._instance

    def __init__(self):
        self.observers = set()

    def attach(self, observer):

        if observer not in self.observers:
            print(f'{observer} attached to {self} observable')
            self.observers.add(observer)

    def detach(self, observer):
        try:
            self.observers.remove(observer)
            print(f'{observer} detached to {self} observable')
        except Exception:
            print("Object Not Registered")
            pass

    def update(self, message):
        for observer in self.observers:
            observer.update(message)


class Observer:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))


class RSISubject(Subject):

    def __init__(self):
        super().__init__()

    def calculateRSI(self):
        result = CalculateRSI.check()
        now = datetime.now()
        currenttime = now.strftime("%H:%M:%S")
        for i in result:
            if (i[2] == -1):
                # sell pressure
                message = f"""
                🔔 Binance Futures Market
                 {i[0]} Oversold RSI:{i[1]:.2g}
                 5-Minutes-Chart
                 Time:{currenttime}
                """

                Subject.update(self, message)
            elif (i[2] == 1):
                # buy pressure
                message =f"""
                🔔 Binance Futures Market
                 {i[0]} Overbought RSI:{i[1]:.2g}
                 5-Minutes-Chart
                 Time:{currenttime}
                """
                Subject.update(self, message)


class VolumeSubject(Subject):
    def calculateVolume(self):
        result = CalculateVolume.check()
        for i in result:
            result = CalculateRSI.check()
            now = datetime.now()
            currenttime = now.strftime("%H:%M:%S")
            message = f'{i[0]} Volume spike! Current Volume:{i[1]}, average Volume: {i[2]}'
            message = f"""
            📢 Binance Futures Market
            Volume Spike
            {i[0]} VoluRSI:{i[1]}
            5-Minutes-Chart
            Time:{currenttime}
            """
            Subject.update(self, message)


class Observer_Telegram(Observer):
    def __init__(self, name):
        Observer.__init__(self, name)

    def update(self, message):
        # name is telegram chat id just send a telegram message to chat id
        # you know chat id just send a message that s all
        updater = Updater(BotConfig.API_KEY, use_context=True)
        updater.bot.send_message(self.name, text=message)


def main_design():
    print("Program Started")

    Rsibot = RSISubject()
    Volumebot = VolumeSubject()

    i = 0
    while (True):
        i = i + 1
        Rsibot.calculateRSI()
        Volumebot.calculateVolume()
        print(f'{i}. run')
        sleep(120)
