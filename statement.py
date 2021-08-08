import pandas as pd

from helpers import _get_values
from settings import *
#from base import StatementBase



"""
StatementBase is a parent class for each financial statement class
such as
- Revenue (in P/L)
- Total stockholders equity (in B/S)
- Net cash provided by operating activeties (in C/F) .
"""
class StatementBase:
    @property
    def settings(self):
        raise NotImplementedError


    @property
    def name(self):
        return self.settings.name


    @property
    def name_list(self):
        return self.settings.other_names


    def values(self, urls_series):
        return _get_values(urls_series, self.name_list)


    def years(self):
        return self._years


    def to_dict(self, urls_series):
        return self.values(urls_series)


    def to_json(self, urls_series):
        return json.dumps(self.to_dict(urls_series))


    def to_dataframe(self, urls_series):
        return pd.DataFrame(self.to_dict(urls_series), index=[self.name])



# bs
class TotalStockholdersEquity(StatementBase):
    def parent(self):
        return BalanceSheets()


    @property
    def settings(self):
        return TotalStockholdersEquitySettings()


class TotalLiabilitiesAndStockholdersEquity(StatementBase):
    @property
    def settings(self):
        return TotalLiabilitiesAndStockholdersEquitySettings()



# pl
class Revenue(StatementBase):
    @property
    def settings(self):
        return RevenueSettings()


class IncomeFromOperations(StatementBase):
    @property
    def settings(self):
        return IncomeFromOperationsSettings()


class NetIncome(StatementBase):
    @property
    def settings(self):
        return NetIncomeSettings()



# cf
class NetCashProvidedByOperatingActiveties(StatementBase):
    @property
    def settings(self):
        return NetCashProvidedByOperatingActivetiesSettings()
