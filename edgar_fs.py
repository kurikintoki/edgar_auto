import pandas as pd

from helpers import _get_attr_list
from edgar_url import EdgarURL
#from base import FinancialStatementsBase
from financial_statements import *
from kpi import *


class EdgarFS:
    def __init__(self, cik):
        self.cik = cik
        self.edgar_url = EdgarURL(cik)
        self.urls_df = None

        self.pl = StatementsOfIncome()
        self.bs = BalanceSheets()
        self.cf = StatementsOfCashFlows()

        self.operating_margin = OperatingMargin()
        self.roe = ROE()
        self.shareholders_equity_ratio = ShareholdersEquityRatio()
        # self.shareholders_equity_ratio = ShareholdersEquityRatio()


    def _urls_df(self):
        if self.urls_df is not None:
            return self.urls_df

        self.urls_df = self.edgar_url.to_dataframe()
        return self.urls_df


    # def statements(self):
    #     #raise NotImplementedError
    #     d = self.__dict__
    #     l = []
    #     for key, value in d.items():
    #         if isinstance(value, FinancialStatementsBase):
    #         #if issubclass(value.__class__, FinancialStatementsBase):
    #             l.append(value)
    #
    #     return l
    def statements(self):
        return _get_attr_list(self.__dict__, FinancialStatementsBase)


    def kpis(self):
        return _get_attr_list(self.__dict__, KPIBase)


    def to_dataframe(self):
        l = []
        for statements in self.statements():
            l.append(statements.to_dataframe(self._urls_df()))

        df = pd.concat(l)

        for kpi in self.kpis():
            df.loc[kpi.name] = kpi.to_dataframe(df)

        return df
