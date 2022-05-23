# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import time
import random

# Парсер Кодов ФККО
id_company = 3560875
headers = {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00', 'Accept-Encoding': 'identity'}


response_code_fkko = requests.get('https://rpn.gov.ru/licences/' + str(id_company) + '/', headers=headers)
soup_code_fkko = BeautifulSoup(response_code_fkko.text, 'lxml')

# Парсер подробной страницы с кодами ФККО
locations_info = {}
fkko_info = {}

# Переходим на страницу с подробным описанием о компании
for id_code_fkko in soup_code_fkko.find_all(class_='registryCard__itemHead'):

	# добавляем id страницы с подробным описанием кодов фкко
	url_fkko_page = id_code_fkko.attrs['data-id']

	# поиск Места осуществления
	locations = id_code_fkko.find(class_='registryCard__itemTitle').get_text(strip=True)

	# записываем в словарь данные по id и месту осуществления
	locations_info[url_fkko_page] = locations


# функция парсера данных ФККО
def parser_fkko(pagination_end_fkko):
	page_fkko = 1
	# цикл проходит по всем страницам пагинации
	while int(page_fkko) <= int(pagination_end_fkko):
		response_fkko_info = requests.get(
			'https://rpn.gov.ru/licences/fkko.php?id=' + (new_url_fkko_page) + '&pagen=page-' + str(page_fkko), headers=headers)
		soup_fkko_info = BeautifulSoup(response_fkko_info.text, 'lxml')

		# удалили заголовок таблицы
		soup_fkko_info.find(class_='_head').decompose()

		# заполняем новую таблицу с информацией про коды ФККО
		for info_fkko in soup_fkko_info.find_all(class_='registryCard__itemTableRow'):

			# общие данные info_all_fkko
			info_all_fkko = info_fkko.get_text("@", strip=True)

			fkko_info['id компании'] = new_url_fkko_page
			fkko_info['Места осуществления'] = value_locations.strip()
			fkko_info['Код'] = info_all_fkko.split("@")[0].replace(" ", "")

			# ставим None, если данные парсера пустые
			try:
				fkko_info['Наименование'] = info_all_fkko.split("@")[1]
			except:
				fkko_info['Наименование'] = None

			try:
				fkko_info['Класс опасности'] = info_all_fkko.split("@")[2]
			except:
				fkko_info['Класс опасности'] = None

			try:
				fkko_info['Вид деятельности'] = info_all_fkko.split("@")[3]
			except:
				fkko_info['Вид деятельности'] = None

			# записываем полученные данные в файл  fkko_info.csv
			with open('fkko_info.csv', 'a', newline='', encoding="utf-8") as file:
				writer = csv.writer(file)
				writer.writerow([fkko_info])

		page_fkko += 1


# Переходим на страницу с подробным описанием о компании
for new_url_fkko_page, value_locations in locations_info.items():

	# поиск последней пагинации
	response_fkko_info_pag = requests.get(
		'https://rpn.gov.ru/licences/fkko.php?id=' + (new_url_fkko_page), headers=headers)
	soup_fkko_info_pag = BeautifulSoup(response_fkko_info_pag.text, 'lxml')
	for pagin_fkko in soup_fkko_info_pag.find_all(class_='paginationBox__numbers'):
		pagination_end_fkko = pagin_fkko.find_all(class_='paginationBox__number')[-1].get_text(strip=True)

	# запуск функции парсера
	parser_fkko(pagination_end_fkko)

