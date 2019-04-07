# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


x = 1
class GazetaDoPovoSpider(scrapy.Spider):
    
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []
    x = 1

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('../../frontier/gazetadopovo.json') as json_file:
                data = json.load(json_file)
                
        self.start_urls = list(data.values())


    def parse(self, response):

        for noticia in response.xpath("/html/body/div[2]/div[3]/section/section/div/section/article"):
              yield response.follow(noticia.xpath(".//a/@href").get(),callback=self.pagina_parse)

        yield scrapy.request(urlparse.urljoin('https://www.gazetadopovo.com.br/ultimas-noticias/?offset=', x),callback=self.parse)
        x = x+1

    def pagina_parse (self,response) :


        titulo = response.css('h1.col-8.c-left.c-title::text').get()
        if  titulo:

            autor = response.css(' div.container.hidden > section > article > div > header > div.col-8.c-left > div.c-credits.mobile-hide > ul > li.item-name > span::text').get()
            data = response.css('#section-republica > div.container.hidden > section > article > div > header > div.col-8.c-left > div.c-credits.mobile-hide > ul > li:nth-child(3)').get()
            secao = response.css('#section-republica > div.container.hidden > section > article > ul > li > a::text').get()

           
            
            
        else:
            titulo = response.css('h1.c-titulo::text').get()
            data = response.css('div.c-creditos time::text').get()
            autor = response.css('.c-autor > span::text').get()
            secao = response.css('.c-nome-editoria span::text').get()

                    
        texto ="".join(response.css('div.container.hidden > section > article > div > div.col-8.c-content > div.paywall-google>p::text').getall())

            


        yield {
            'titulo': titulo, 
             'autor': autor, 
             'data' : data, 
             'secao' : secao, 
             'texto': texto, 
             'url' : response.xpath("//link[@rel='canonical']/@href").get()
        }

