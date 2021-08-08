import re
import time
import json

import requests
from urllib.error import HTTPError

from bs4 import BeautifulSoup

import pandas as pd
#import math
import numpy as np

from settings import *



"""
See https://www.sec.gov/developer
"Current guidelines limit each user to a total of no more than 10 requests per second,
regardless of the number of machines used to submit requests."
"""
def sleep_timer():
    time.sleep(1)

#http_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}
http_headers = {#"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                "User-Agent": "karakuriuzumaki@gmail.com",
                #"Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"}

class EdgarURL:
    def __init__(self,
                 cik,
                 #financial_statements_settings,
                 fiscal_year='all',
                 filing_type='10-K'):

        self.cik = cik
        self.year = fiscal_year
        self.filing_type = filing_type

        self.url_settings = URLSettings()
        self.fs_settings = FinancialStatementsSettings()

        """
        _get_rss_soup() should be excuted before _get_filing_type_tags()
        because it is called by _get_filing_type_tags()
        """
        self._rss_soup = self._get_rss_soup()
        self._filing_type_tags = self._get_filing_type_tags()

        self._urls_dict = {}


    def _get_rss_soup(self):
        base_rss_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type={}%25&dateb=&owner=include&start=0&count=&output=atom&CIK={}'
        rss_url = base_rss_url.format(self.filing_type, self.cik)
        rss_page = requests.get(rss_url, headers=http_headers)
        sleep_timer()

        #if rss_page.headers['Content-Type'] != 'application/atom+xml':
        content_type = rss_page.headers['Content-Type']
        if content_type != 'application/atom+xml' and content_type != 'text/html':
            #print(rss_url)
            raise ValueError('The content is not xml formatted.',
                             rss_page.headers['Content-Type'],
                             rss_url)

        return BeautifulSoup(rss_page.content, "lxml")


    def _get_filing_type_tags(self):
        """
        Retrieve all fiscal years soup tags by filing-type from the RSS page
        """
        return self._rss_soup.find_all("filing-type", string=self.filing_type)


    def _get_base_urls(self):
        """
        Retrieve filing urls for all years from the rss feed and set them into
        a dictionary.

        filing_url:
        filing_summary_url:
        base_url:
        """
        d = {}
        filing_summary_xml_filename = 'FilingSummary.xml'
        # One loop for each fiscal year
        for filing_type_tag in self._filing_type_tags:
            # Retrieve the filing url of each fiscal year from a filing-href tag
            filing_url = filing_type_tag.parent.find('filing-href').get_text()
            # Retrieve the fiscal year from a filing-date tag
            fiscal_year = re.findall(r'^\d{4}', filing_type_tag.parent.find('filing-date').get_text())[0]
            #filing_date = filing_type_tag.parent.find('filing-date').get_text()
            # Set urls into the url dataframe
            base_url = filing_url.rsplit('/', maxsplit=1)[0]
            filing_summary_url = base_url + '/' + filing_summary_xml_filename

            d[fiscal_year] = {self.url_settings.base: base_url,
                              self.url_settings.filing_summary: filing_summary_url,
                              self.url_settings.filing: filing_url}

        return d


    #def _financial_statements(self, fs_settings):
    def _get_fs_urls(self):
        d = {}
        for fiscal_year, urls in self._get_base_urls().items():
            filing_summary_xml_page = requests.get(urls[self.url_settings.filing_summary],
                                                   headers=http_headers)
            sleep_timer()

            try:
                filing_summary_xml_page.raise_for_status()
            except Exception:
                # Ignore if 404
                if filing_summary_xml_page.status_code == requests.codes.not_found:
                    """
                    Make urls of the year empty if filing_summary_xml_page is not found
                    then go to the next fiscal_year.
                    """
                    print('The HTTP code 404 occurs. Please check the year and url: ',
                          fiscal_year,
                          urls[self.url_settings.filing_summary])
                    d[fiscal_year] = {}
                    continue
                else:
                    raise
                # if filing_summary_xml_page.status_code != requests.codes.not_found:
                #     raise
            else:
                filing_summary_xml_soup = BeautifulSoup(filing_summary_xml_page.content, "lxml")

            #print(fiscal_year, id(filing_summary_xml_soup))
            di = {}
            for fs_settings in self.fs_settings.settings:
                for shortname in fs_settings.shortnames:
                    #print(shortname)
                    #print(fiscal_year, filing_summary_xml_soup)
                    shortname_tag = filing_summary_xml_soup.find("shortname",
                                                                 string=re.compile(shortname, re.IGNORECASE))
                    if shortname_tag:
                        #print(fiscal_year, id(shortname_tag))
                        filename = shortname_tag.parent.find(["htmlfilename", "xmlfilename"]).get_text()
                        financial_statements_url = urls[self.url_settings.base] + '/' + filename
                        di[fs_settings.name] = financial_statements_url
                    else:
                        continue

            d[fiscal_year] = di

        return d


    def to_dict(self):
        if not self._urls_dict:
            d = {}
            base_d = self._get_base_urls()
            fs_d = self._get_fs_urls()
            for k, v in base_d.items():
                # k is year
                d[k] = {**v, **fs_d[k]}

            self._urls_dict = d

        return self._urls_dict


    def to_dataframe(self):
        if not self._urls_dict:
            self._urls_dict = self.to_dict()

        d = {}
        #for year, urls in self.to_dict().items():
        for year, urls in self._urls_dict.items():
            d[year] = list(urls.values())

        columns = [self.url_settings.base,
                   self.url_settings.filing_summary,
                   self.url_settings.filing,
                   self.fs_settings.pl_settings.name,
                   self.fs_settings.bs_settings.name,
                   self.fs_settings.cf_settings.name]

        try:
            return pd.DataFrame.from_dict(d, orient='index', columns=columns)
        except ValueError as e:
            print(e)
            print('Missing urls of bs, pl or cf')
            print('Columns: {}'.format(columns))
            print('URLs: ')
            print(*list(d.values()), sep='\n')
            raise


    def to_json(self):
        if not self._urls_dict:
            self._urls_dict = self.to_dict()

        return json.dumps(self._urls_dict)
