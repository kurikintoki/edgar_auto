import re
import time

import pandas as pd
import numpy as np

import requests
from urllib.error import HTTPError



http_headers = {#"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                "User-Agent": "karakuriuzumaki@gmail.com",
                #"Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"}


"""
See https://www.sec.gov/developer
"Current guidelines limit each user to a total of no more than 10 requests per second,
regardless of the number of machines used to submit requests."
"""
def _sleep_timer():
    time.sleep(1)


def _get_values(urls_series, name_list):
    d = {}
    # url is for pl, bs or cf for each year
    for year, url in urls_series.iteritems():
        # url is nan in cace fiscal_year is older than 2010
        if url and url is not np.nan:
            # print(url, type(url))
            if re.match(r'.*\.htm', url):
                # if year not in d:
                #     d[year] = self._get_values_from_html(url, settings)
                # else:
                #     d[year].update(self._get_values_from_html(url, settings))
                df = _fetch_table(url)
                d[year] = _get_values_from_table(df, name_list)
                if d[year] is '0':
                    print("The value is '0', see", url)
                    print(*name_list, sep='\n')
                #sleep_timer()
            elif re.match(r'.*\.xml', url):
                # self._set_data_from_xml(fiscal_year, index, keywords, balance_sheets_url)
                pass
            else:
                raise Exception('No .html or .xml file')

    return d


# def _get_value(url, name_list):
#     if url and url is not np.nan:
#         # print(url, type(url))
#         if re.match(r'.*\.htm', url):
#             df = _fetch_table(url)
#             return _get_values_from_table(df, name_list)
#             #sleep_timer()
#         elif re.match(r'.*\.xml', url):
#             # self._set_data_from_xml(fiscal_year, index, keywords, balance_sheets_url)
#             pass
#         else:
#             raise Exception('No .html or .xml file')


def _fetch_table(url):
    try:
        # See at https://stackoverflow.com/questions/43590153/http-error-403-forbidden-when-reading-html
        r = requests.get(url, headers=http_headers)
        #_sleep_timer()
        df = pd.read_html(r.text)[0]
    except Exception:
        print(url)
        raise
    # except HTTPError as e:
    #     print(url)
    #     raise

    return df


# Settings financial statements
def _get_values_from_table(df, name_list):
    for name in name_list:
        try:
            value = df.loc[df.iloc[:, 0] == name].iloc[:, 1].values[0]
            # print(value)
            # print(df.loc[df.iloc[:, 0] == name])
            # Cannot use math.isnan() because it takes only float values. Use is np.nan instead.
            # Try the next column (third column) if the second column is empty.
            if value is np.nan:
                value = df.loc[df.iloc[:, 0] == name].iloc[:, 2].values[0]
            # Try the next name if value is still nan
            if value is np.nan:
                continue
            #return value.translate(value.maketrans({'$': '', ' ': '', ',': ''}))
            return _format_number(value)
        # except AttributeError:
        #     # Go to the next keyword if value is still nan.
        #     if value is np.nan:
        #         print("value is still nan, replacing to '0'")
        #         print("There is no name in ", name_list)
        #         # print(url)
        #         # print(statement_name)
        #         # print(value)
        #         # d[statement_name] = '0'
        #         # break
        #         return '0'
        #     else:
        #         raise
        except IndexError:
            # Go to the next keyword
            continue

    return '0'


def _get_attr_list(obj_dict, parent_class):
    l = []
    for _, value in obj_dict.items():
        if isinstance(value, parent_class):
            l.append(value)

    return l


# def _statements(obj_dict, parent_class):
#     #raise NotImplementedError
#     l = []
#     #print(d)
#     for key, value in obj_dict.items():
#         #print(value.__class__)
#         #print(value.__class__.__bases__)
#         #print('children: ', id(value.__class__.__bases__))
#         #print('parent: ', id(parent_class))
#         if isinstance(value, parent_class):
#         #if issubclass(value.__class__, parent_class):
#             l.append(value)
#
#     return l

def _format_number(value):
    num = value.translate(value.maketrans({'$': '', ' ': '', ',': ''}))
    # If the number has
    if '(' and ')' in num:
        return '-{}'.format(re.findall(r'\d+', num)[0])

    return num
