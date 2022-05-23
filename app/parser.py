# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import time
import random

headers = {'User-Agent': 'Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41', 'Accept-Encoding': 'identity'}


# список 'User-Agent' для того, чтоб обойти блокировку rpn.gov.ru по количеству запросов
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/4.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
'Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.1.112 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.111 YaBrowser/21.2.1.108 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.2.108 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 YaBrowser/21.2.4.165 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 YaBrowser/20.11.3.183 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/[WEBKIT_VERSION] (KHTML, like Gecko, Mediapartners-Google) Chrome/[CHROME_VERSION] Safari/[WEBKIT_VERSION]',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
]

page = 15
id = []
company_info = {}
fkko_info = {}
start_time = datetime.now()

# поиск последней страницы в пагинации
response_pag = requests.get('https://rpn.gov.ru/licences/?page=page-1', headers=headers)
soup_pag = BeautifulSoup(response_pag.text,'lxml')

for pagin in soup_pag.find_all(class_='paginationBox__numbers'):
	pagination_end = pagin.find_all(class_='paginationBox__number')[-1].get_text(strip=True)


# начало цикла и работа парсера
while int(page) < int(pagination_end):
	# замена headers случайным значением из списка user_agent_list
	if page % 300 == 0:
		user_agent = random.choice(user_agent_list)
		headers = {'User-Agent': user_agent, 'Accept-Encoding': 'identity'}
		time.sleep(1)


	response = requests.get('https://rpn.gov.ru/licences/?page=page-' + str(page), headers=headers)
	soup = BeautifulSoup(response.text,'lxml')
	for info in soup.find_all('a', class_='sectionRegistry__resultTableRow'):
		id_company = info.get('href')[10:-1]
		# id.append(id_company.strip())

		date_status = info.find_all(class_='sectionRegistry__resultTableContent')[1].get_text(' ', strip=True)
		d_s = date_status.split()

		if d_s[1] in "Действуюшая":
			print("действуйющая")

			company_info['id'] = id_company.strip()
			company_info['№ лицензии'] = info.find_all(class_='sectionRegistry__resultTableContent _medium')[0].get_text(strip=True)
			company_info['Дата выдачи'] = d_s[0]
			company_info['Статус'] = d_s[1]
			company_info['Выдана'] = info.find_all(class_='sectionRegistry__resultTableContent')[2].get_text(' ', strip=True)
			company_info['Приказ о прекращении / переоформлении'] = info.find_all(class_='sectionRegistry__resultTableContent')[3].get_text(strip=True)
			adress_lic = info.find(class_='_address').get_text("@", strip=True)
			company_info['Лицензиат'] = adress_lic.split("@")[0]

			try:
				company_info['Адрес места нахождения'] = adress_lic.split("@")[1]
			except:
				company_info['Адрес места нахождения'] = None

			company_info['ИНН'] = info.find('div', class_='_inn').get_text(strip=True)

			class_dangerous = info.find(class_='_view').get_text("@", strip=True)
			company_info['Вид работ'] = class_dangerous.split("@")[0]
			try:
				company_info['Класс опасности отхода'] = class_dangerous.split("@")[1]
			except:
				company_info['Класс опасности отхода'] = None

			# Парсер Кодов ФККО
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
					headers_fkko = {
						'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
						'Accept-Encoding': 'identity'}

					if page_fkko % 50 == 0:
						user_agent = random.choice(user_agent_list)
						headers_fkko = {'User-Agent': user_agent, 'Accept-Encoding': 'identity'}
						print(f'User_agent = {headers_fkko}')
						print(f'page_fkko делиться на 50 = {page_fkko} из {pagination_end_fkko}')
						time.sleep(1)
					try:
						response_fkko_info = requests.get(
							'https://rpn.gov.ru/licences/fkko.php?id=' + (new_url_fkko_page) + '&pagen=page-' + str(
								page_fkko),
							headers=headers_fkko)
					except:
						print("Let me sleep for 5 minut")
						print("ZZzzzz...")
						time.sleep(300)
						continue

					soup_fkko_info = BeautifulSoup(response_fkko_info.text, 'lxml')

					# удалили заголовок таблицы
					try:
						soup_fkko_info.find(class_='_head').decompose()
					except:
						continue

					# заполняем новую таблицу с информацией про коды ФККО
					for info_fkko in soup_fkko_info.find_all(class_='registryCard__itemTableRow'):

						# общие данные info_all_fkko
						info_all_fkko = info_fkko.get_text("@", strip=True)

						fkko_info['id компании'] =  company_info['id']
						fkko_info['id страницы ФККО'] = new_url_fkko_page
						fkko_info['Лицензиат'] = adress_lic.split("@")[0]
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
						with open('fkko_info220522.csv', 'a', newline='', encoding="utf-8") as file:
							writer = csv.writer(file)
							writer.writerow([fkko_info])
					page_fkko += 1
		else:
			pass

		try:
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

			with open('all_info220522.csv', 'a', newline='', encoding="utf-8") as file:
				writer = csv.writer(file)
				writer.writerow([company_info])
		except:
			pass

	page += 1


print(datetime.now() - start_time)


