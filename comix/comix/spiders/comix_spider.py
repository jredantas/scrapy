#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:45:03 2017

@author: 09959295800
"""

from scrapy import Spider
from scrapy.selector import Selector
from comix.items import ComixItem
from datetime import datetime, date
#from babel.dates import format_date, format_datetime, format_time, parse_date
#import locale

#locale.setlocale(locale.LC_ALL, 'pt_BR')
def to_week(s):
    days_of_week = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado']
    return days_of_week.index(s)+1

def to_month(s):
    months = ['Janeiro',
              'Fevereiro',
              'Março',
              'Abril',
              'Maio',
              'Junho',
              'Julho',
              'Agosto',
              'Setembro',
              'Outubro',
              'Novembro',
              'Dezembro']
    return [i for i, j in enumerate(months,1) if j == s][0]
    

class ComixSpider(Spider):
    name = 'comix'
    allowed_domains = ['www.comix.com.br']
    start_urls = ['http://www.comix.com.br/products_new.php']
    for i in range(25):
        start_urls.append('http://www.comix.com.br/products_new.php?page='+str(i))
        
    def parse(self, response):
        questions = Selector(response).xpath('//td[@class="main"]')
        
        #print(self.locale)
        
        for question in questions:
            
            #print(datetime.strftime(datetime.now(),"%A %d %B, %Y"))
            #break
            
            price = question.xpath('span[@class="preco"]/text()')
            if price:
                item = ComixItem()
                
                """
                Ordem de busca dos campos preco:
                    1- span[@class="preco"]
                    2- span[@class="preco"]/s
                """
                item['price'] = price.extract()[0].split('$')[-1].strip() 
                if price.extract()[0].strip() == '':
                    item['price'] = question.xpath('span[@class="preco"]/s/text()').extract()[0].split('$')[-1].strip()

                item['title'] = 'None' 
                title = question.xpath('a/b/u/text()')
                if title:
                    item['title'] = title.extract()[0]
            
                item['url'] = question.xpath('a/@href').extract()[0].split('&')[0]
                
                item['editor'] = 'None' 
                editor = question.xpath('text()')
                if editor:
                    item['editor'] = editor.extract()[1].split(':')[-1].strip()
            
                item['issue_date'] = 'None' 
                issue_date = question.xpath('text()')
                if issue_date:
                    #issue_date = parse_date(editor.extract()[0].split(':')[-1].strip(), locale='pt_BR')
                    #issue_date = datetime.strptime(editor.extract()[0].split(':')[-1].strip().title(), "%A %d %B, %Y")
                    issue_date = editor.extract()[0].split(':')[-1].strip().title()
                    item['test'] = issue_date #editor.extract()[0].split(':')[-1].strip()
                    #week = to_week(issue_date.split(' ')[0])
                    day = int(issue_date.split(' ')[1])
                    month = int(to_month(issue_date.split(' ')[2].split(',')[0]))
                    year = int(issue_date.split(' ')[-1])
                    item['issue_date'] = date(year, month, day) 

                yield item 
