#!/usr/bin/env python

from traceback import print_tb
from unittest import skip, skipIf
from urllib import request
from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://www.coches.com/'


def getHtml(url):
    r = requests.get(url)
    return r.text


def formatBrand(str):
    return str.replace(' ', '-').lower() + '.htm'

## Getting brands to further search
def getBrands():
    html_text = getHtml(URL + 'km0')
    soup = BeautifulSoup(html_text, 'lxml')
    brand_search = soup.find_all('a', class_='marca')
    brands = [brand.text for brand in brand_search]
    return brands

def batchStrRemove(str, remove_list):
    for remove in remove_list:
        str = str.replace(remove, '')
    return str

## Formatting car to be shown in the front and remove duplicate info
def formatCarRow(car, brand):
    row = batchStrRemove(car.text, ['/t', '\n\n', brand, ' km', ' cv'])
    row = row.split('\n')[3:]
    if (len(row) < 7 or len(row[1]) == 0):
        return []
    row[1] = batchStrRemove(row[1], ['Diesel', 'Gasolina', 'Híbrido'])
    row[1] = row[1].replace('  ', ' ')
    row.insert(1, brand)
    row.append(car.find('img')['src'])
    return [s.strip() for s in row]

## Get all cars from a brand
def getCars(brand='wolkswagen', car_type='km0'):
    if car_type not in ['km0', 'coches-segunda-mano'] or brand not in getBrands():
        return []
    soup = BeautifulSoup(getHtml(URL + car_type + '/' + formatBrand(brand)), 'lxml')
    car_search = soup.find_all('div', class_='pill')
    cars = []
    for car in car_search:
        row = formatCarRow(car, brand)
        if row != []:
            cars.append(row)
    return cars

if __name__ == '__main__':

    cars = []
    brands = getBrands()
    brands_to_URL = []

    ## Getting all cars from all brands
    for brand in brands:
        cars += getCars(brand, 'km0')

    ## Saving km0 cars
    df = pd.DataFrame(cars, columns=['Precio', 'Marca', 'Modelo', 'Motor', 'Potencia', 'Km', 'Ciudad', 'Año', 'Image'])
    df.to_csv('cars-km0.csv')

    for brand in brands:
        cars += getCars(brand, 'coches-segunda-mano')

    ## Saving second-hand cars
    df = pd.DataFrame(cars, columns=['Precio', 'Marca', 'Modelo', 'Motor', 'Potencia', 'Km', 'Ciudad', 'Año', 'Image'])
    df.to_csv('cars-segunda-mano.csv')

