import csv
import os
from pathlib import Path

from entities import Fields, Product, Result
import main


def create_csv(csv_name, titles):
    if Path(csv_name + '.csv').is_file():
        return Result(False, 'Dosya zaten mevcut')

    with open(csv_name + '.csv', 'a', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(titles)
        return Result(True, 'Dosya başarıyla Oluşturuldu')


def delete_csv(csv_name):
    with Path(csv_name + '.csv') as f:
        if f.is_file():
            os.remove(f)
            return Result(True, 'Başarıyla silindi')
        else:
            return Result(False, 'Dosya bulunamadı')


def find_csv(csv_name):
    with Path(csv_name + '.csv') as f:
        if f.is_file():
            return Result(True, 'Dosya mevcut')
        else:
            return Result(False, 'Dosya bulunamadı')


def append_to_csv(csv_name, data):
    with open(csv_name + '.csv', 'a+', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
