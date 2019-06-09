from pyquery import PyQuery as pq
from lxml import etree
import urllib

feed_page_url = "http://empregos.alternativa.co.jp/"
# pq(url="http://google.com", headers={'user-agent': 'pyquery'}, {'q': 'foo'}, method='post', verify=True)
dquery = pq(feed_page_url)

# print(dquery)

home_jobs_items_xpath = "gr__empregos_alternativa_co_jp body div.gridContainer.clearfix div.empregos_contents div.section_contents_jobs_home div.detail_job_box"

# home_jobs = dquery(home_jobs_items_xpath)
home_jobs = dquery("body").find("div.section_contents_jobs_home div.detail_job_box")

# print(type(home_jobs))

clean_jobs = []

for job in home_jobs:
    
    # breakpoint()
    try:
    
        # easy to work
        job = pq(job)

        job_page_url = feed_page_url + job.find('.title_box_blue_text a').attr("href")
        
        job_page_query = pq(job_page_url)

        # company_logo_url = feed_page_url + job_page_query(".img_corp2 img").attr('src')

        job_page_articles = job_page_query("article")

        job_salary = pq(pq(job_page_articles[0]).find('.job_text')[0]).text()

        job_description = '\n'.join(pq(job_text_item).text() for job_text_item in pq(job_page_articles[1]).find('.job_text'))

        job_time = '\n'.join(pq(job_text_item).text() for job_text_item in pq(job_page_articles[2]).find('.job_text'))

        job_advantages = '\n'.join(pq(job_text_item).text() for job_text_item in pq(job_page_articles[3]).find('.job_text'))
        
        job_requirements = '\n'.join(pq(job_text_item).text() for job_text_item in pq(job_page_articles[4]).find('.job_text'))

        job_local = pq(pq(job_page_articles[5]).find('.job_text')[0]).text()

        job_contact = '\n'.join(pq(job_text_item).text() for job_text_item in pq(job_page_articles[6]).find('.job_text'))

        clean_jobs.append({
            'title': job.find('.title_box_blue_text a').text(),
            'url': job_page_url, # job.find('.title_box_blue_text a').attr("href"),
            # 'local': job.find('.job_detail_empregos_text').text().split('|')[0],
            'local_2': job_local,
            'salary': job_salary,
            'description': job_description,
            'time': job_time,
            'advantages': job_advantages,
            'requirements': job_requirements,
            'contact': job_contact
        })

    except Exception as e:
        
        # if something wrong print and contine
        print(e)

    # exit()

from pprint import pprint
# print(clean_jobs)

pprint(clean_jobs)

print('Total founds: ', len(clean_jobs))
