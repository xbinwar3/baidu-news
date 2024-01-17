import scrapy

from baidu01.items import Baidu01Item

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["news.baidu.com"]
    start_urls = ["https://news.baidu.com"]

    def parse(self, response):
        print("-------------------------------------------------")
        alist = response.xpath('//*[@id="pane-news"]//a')
       # alist = response.text

        for i in alist:
            name  = i.xpath('./text()').extract_first()
            url = i.xpath('./@href').extract_first()
            if name :
                print("---")
            else:
                name = i.xpath('./b/text()').extract_first()
  
            news = Baidu01Item(name=name,url=url)
            yield news
            print(name)
            print(url)
        print("-------------------------------------------------")








