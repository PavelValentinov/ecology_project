# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import time
import random

# ������ ����� ����
id_company = 3560875
headers = {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00', 'Accept-Encoding': 'identity'}


response_code_fkko = requests.get('https://rpn.gov.ru/licences/' + str(id_company) + '/', headers=headers)
soup_code_fkko = BeautifulSoup(response_code_fkko.text, 'lxml')

# ������ ��������� �������� � ������ ����
locations_info = {}
fkko_info = {}

# ��������� �� �������� � ��������� ��������� � ��������
for id_code_fkko in soup_code_fkko.find_all(class_='registryCard__itemHead'):

	# ��������� id �������� � ��������� ��������� ����� ����
	url_fkko_page = id_code_fkko.attrs['data-id']

	# ����� ����� �������������
	locations = id_code_fkko.find(class_='registryCard__itemTitle').get_text(strip=True)

	# ���������� � ������� ������ �� id � ����� �������������
	locations_info[url_fkko_page] = locations


# ������� ������� ������ ����
def parser_fkko(pagination_end_fkko):
	page_fkko = 1
	# ���� �������� �� ���� ��������� ���������
	while int(page_fkko) <= int(pagination_end_fkko):
		response_fkko_info = requests.get(
			'https://rpn.gov.ru/licences/fkko.php?id=' + (new_url_fkko_page) + '&pagen=page-' + str(page_fkko), headers=headers)
		soup_fkko_info = BeautifulSoup(response_fkko_info.text, 'lxml')

		# ������� ��������� �������
		soup_fkko_info.find(class_='_head').decompose()

		# ��������� ����� ������� � ����������� ��� ���� ����
		for info_fkko in soup_fkko_info.find_all(class_='registryCard__itemTableRow'):

			# ����� ������ info_all_fkko
			info_all_fkko = info_fkko.get_text("@", strip=True)

			fkko_info['id ��������'] = new_url_fkko_page
			fkko_info['����� �������������'] = value_locations.strip()
			fkko_info['���'] = info_all_fkko.split("@")[0].replace(" ", "")

			# ������ None, ���� ������ ������� ������
			try:
				fkko_info['������������'] = info_all_fkko.split("@")[1]
			except:
				fkko_info['������������'] = None

			try:
				fkko_info['����� ���������'] = info_all_fkko.split("@")[2]
			except:
				fkko_info['����� ���������'] = None

			try:
				fkko_info['��� ������������'] = info_all_fkko.split("@")[3]
			except:
				fkko_info['��� ������������'] = None

			# ���������� ���������� ������ � ����  fkko_info.csv
			with open('fkko_info.csv', 'a', newline='', encoding="utf-8") as file:
				writer = csv.writer(file)
				writer.writerow([fkko_info])

		page_fkko += 1


# ��������� �� �������� � ��������� ��������� � ��������
for new_url_fkko_page, value_locations in locations_info.items():

	# ����� ��������� ���������
	response_fkko_info_pag = requests.get(
		'https://rpn.gov.ru/licences/fkko.php?id=' + (new_url_fkko_page), headers=headers)
	soup_fkko_info_pag = BeautifulSoup(response_fkko_info_pag.text, 'lxml')
	for pagin_fkko in soup_fkko_info_pag.find_all(class_='paginationBox__numbers'):
		pagination_end_fkko = pagin_fkko.find_all(class_='paginationBox__number')[-1].get_text(strip=True)

	# ������ ������� �������
	parser_fkko(pagination_end_fkko)

