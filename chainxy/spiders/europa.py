# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from lxml import etree

from lxml import html

import time

import pdb

import csv


class Europa(scrapy.Spider):

	name = 'europa'

	domain = 'http://ec.europa.eu'

	history = []

	cn_code_list = []

	output = []

	def __init__(self):

		try:

			file_path = 'cn_codes.csv'

			with open(file_path, 'rb') as csvfile:

				spamreader = csv.reader(csvfile)

				for row in spamreader:

					code = row[0].split(';')[0]

					if len(code) >= 8:

						self.cn_code_list.append(code)
				
		except Exception as e:

			print(e)

	
	def start_requests(self):

		for cn_code in self.cn_code_list:

			url = "http://ec.europa.eu/taxation_customs/dds2/ecics/chemicalsubstance_list.jsp?Lang=en&offset=0&CnCode="+cn_code+"&LangNm=en&sortOrder=1"

			yield scrapy.Request(url, callback=self.parse_detail, meta={'cn_code' : cn_code}) 


	def parse_detail(self, response):

		row_list = response.xpath('//table[@id="tblData"]//tr[contains(@class, "tdOddRow")]')

		if len(row_list) > 0:

			for row in row_list:

				data = self.validate(row.xpath('.//td[3]//text()').extract_first())

				item = ChainItem()

				item['CN_Code'] = response.meta['cn_code']

				item['CUS'] = self.validate(row.xpath('.//td[1]//text()').extract_first())

				item['CAS_Number'] = self.validate(row.xpath('.//td[3]//text()').extract_first())

				item['EC_Number'] = self.validate(row.xpath('.//td[4]//text()').extract_first())

				item['UN_Number'] = self.validate(row.xpath('.//td[5]//text()').extract_first())

				item['Nomen'] = self.validate(row.xpath('.//td[6]//text()').extract_first())

				item['Name'] = self.validate(row.xpath('.//td[7]//text()').extract_first())

				if item not in self.history:

					self.history.append(item)

					yield item

			pagenation_list = response.xpath('//div[@id="navigation"]//td')

			for pagenation in pagenation_list:

				text = ''.join(pagenation.xpath('.//text()').extract())

				if 'next' in text.lower():

					link = pagenation.xpath('.//a/@href').extract_first()

					next_number = link.split('offset=')[1].split('&Inchi')[0]

					link = response.url.split('offset=')[0] + 'offset=' + next_number + '&CnCode' + response.url.split('&CnCode')[1]

					yield scrapy.Request(link, callback=self.parse_detail)


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

		tmp = []

		for item in items:

			if self.validate(item) != '':

				tmp.append(self.validate(item))

		return tmp