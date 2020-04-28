#!/usr/bin/env python3
import pandas
import sys
import io


def read_me(path_or_file):
    return pandas.read_csv(
        path_or_file,
        encoding='cp1251',
        sep=';',
        skiprows=2,
        parse_dates=['Date'],
        dayfirst=True,
        decimal=',').dropna()


def read_cs(path_or_file):
    '''
    a[a['Transaction time'] > pd.to_datetime('2020-04-06')].groupby(
        'Transaction time')['Amount in operation currency'].agg('sum').median()
    '''
    frame = pandas.read_csv(
        path_or_file,
        encoding='cp1251',
        sep=';',
        skiprows=2,
        parse_dates=['Transaction time'],
        dayfirst=True)
    frame = frame[(frame['Operation type'] != 'Получение средств') &
                  (frame['Operation status'] == 'Завершено успешно')]
    return frame


def read_cs2(path_or_file):
    def amount(x):
        return float(x.replace(' BYN', ''))

    frame = pandas.read_excel(
            path_or_file,
            skiprows=6,
            skipfooter=1,
            usecols=[0, 2, 4, 6, 7],
            converters={3: amount},
            parse_dates=['Date'],
            dayfirst=True,
            names=('Date', 'Details', 'MMC', 'Amount', 'Status'),
    ).dropna()
    frame = frame[(frame['Status'] == 'Completed successfully') &
                  (frame['Amount'] < 0)]
    frame.Date = frame.Date.dt.date
    return frame


def read_vpsk(path_or_file):
    # TODO: modify the copy.
    frame = pandas.read_csv(
        path_or_file,
        encoding='cp1251',
        sep=';',
        skiprows=2,
        parse_dates=['Transaction time'],
        dayfirst=True)
    frame = frame[(frame['Operation type'] != 'Получение средств') &
                  (frame['Operation status'] == 'Завершено успешно')]
    frame['Transaction time'] = frame['Transaction time'].dt.date
    return frame


if __name__ == '__main__':
    read_me(io.TextIOWrapper(sys.stdin.buffer, encoding='cp1251')).to_csv(
            sys.stdout, index=False)
