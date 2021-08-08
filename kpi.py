import pandas as pd

from helpers import _get_values
from settings import *
from statement import *



"""
KPIBase is a parent class for each financial KPI class such as
- OperatingMargin (Operating margin)
- ROE (ROE)
- ShareholdersEquityRatio (Shareholder's equity ratio) .
"""
class KPIBase:
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
        raise NotImplementedError


    def to_dataframe(self, values_df):
        return self.values(values_df)



class OperatingMargin(KPIBase):
    def __init__(self):
        self.revenue = Revenue()
        self.income_from_operations = IncomeFromOperations()


    @property
    def settings(self):
        return OperatingMarginSettings()


    def values(self, values_df):
        revenue = pd.to_numeric(values_df.loc[self.revenue.name])
        income_from_operations = pd.to_numeric(values_df.loc[self.income_from_operations.name])

        return ((income_from_operations / revenue) * 100).round(2)



class ROE(KPIBase):
    # Net income / ((Total stockholder's equity + Total stockholder's equity of last year) / 2)
    def __init__(self):
        self.net_income = NetIncome()
        self.total_stockholders_equity = TotalStockholdersEquity()


    @property
    def settings(self):
        return ROESettings()


    def values(self, values_df):
        net_income = pd.to_numeric(values_df.loc[self.net_income.name])
        total_stockholders_equity = pd.to_numeric(values_df.loc[self.total_stockholders_equity.name])

        shifted_total_stockholders_equity = total_stockholders_equity.shift(periods=-1)
        average_total_stockholders_equity = (total_stockholders_equity + shifted_total_stockholders_equity) / 2

        return ((net_income / average_total_stockholders_equity) * 100).round(2)



class ShareholdersEquityRatio(KPIBase):
    def __init__(self):
        self.total_stockholders_equity = TotalStockholdersEquity()
        self.total_liabilities_and_stockholders_equity = TotalLiabilitiesAndStockholdersEquity()


    @property
    def settings(self):
        return ShareholdersEquityRatioSettings()


    def values(self, values_df):
        total_stockholders_equity = pd.to_numeric(values_df.loc[self.total_stockholders_equity.name])
        total_liabilities_and_stockholders_equity = pd.to_numeric(values_df.loc[self.total_liabilities_and_stockholders_equity.name])

        return ((total_stockholders_equity / total_liabilities_and_stockholders_equity) * 100).round(2)
