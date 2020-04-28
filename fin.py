#!/usr/bin/env python3
import pandas
import sys
import io


def read_alfabank(path_or_file):
    frame = pandas.read_csv(
        path_or_file,
        encoding='cp1251',
        sep=';',
        skiprows=2,
        header=0,
        names=(
            'Transaction',
            'Date',
            'Type',
            'Status',
            'Amount',
            'Currency',
            'City',
            'Country',
            'Details',
        ),
        parse_dates=['Date'],
        dayfirst=True,
        infer_datetime_format=True,
    )
    frame = frame[(frame.Type != 'Получение средств') &
                  (frame.Status == 'Завершено успешно')]
    return frame


def read_ideabank(path_or_file):
    def amount(x):
        return float(x.rstrip('BYN '))

    frame = pandas.read_excel(
            path_or_file,
            skiprows=6,
            skipfooter=1,
            usecols=(0, 2, 4, 6, 7),
            converters={3: amount},
            parse_dates=['Date'],
            dayfirst=True,
            names=('Date', 'Details', 'MMC', 'Amount', 'Status'),
    ).dropna()
    frame = frame[(frame['Status'] == 'Completed successfully') &
                  (frame['Amount'] < 0)]
    frame.Date = frame.Date.dt.date
    return frame


if __name__ == '__main__':
    read_alfabank(io.TextIOWrapper(
        sys.stdin.buffer, encoding='cp1251')).to_csv(
            sys.stdout, index=False)
