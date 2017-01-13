import scrapy
x = 6081001
class SpidyQuotesViewStateSpider(scrapy.Spider):
    name = 'mbbs'
    start_urls = ['http://online.kanpuruniversity.org/Reg_SubjectUpdate/Result/MBBSNewResult2016.aspx']*17
    download_delay = 1.5
    
    def parse(self, response):
        yield scrapy.FormRequest(
                'http://online.kanpuruniversity.org/Reg_SubjectUpdate/Result/MBBSNewResult2016.aspx',
                formdata={
                'ddlcourse': '1',
				'__EVENTTARGET':'ddlcourse',
                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
				'__VIEWSTATEGENERATOR':response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first()
                },
                callback=self.parse_sem,dont_filter=True
        )

    def parse_sem(self, response):
        global x
        
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'ddlsem': '1oct','txtrollno' : str(x)},
            callback=self.parse_results,dont_filter=True
            )
        x = x + 1
        
    def parse_results(self, response):
        #print response
        return {
				
                'Roll No': response.css('span#lblRollNo ::text').extract_first(),
                'Name': response.css('span#lblName ::text').extract_first(),
				'Anatomy' : response.css('span#gridmark2_ctl02_lbltotalmar ::text').extract_first()
                'Marks' : response.css('span#lbltotal ::text').extract_first()
            }
