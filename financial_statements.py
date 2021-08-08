import pandas as pd

from helpers import _get_attr_list
from settings import *
#from base import FinancialStatementsBase
from statement import *



"""
FinancialStatementsBase is a parent class for each financial statements class
such as
- StatementsOfIncome (P/L)
- BalanceSheets (B/S)
- StatementsOfCashFlows (in C/F)

This base class have to be in the same module as children classes
to make isinstance() in statements() method work.

See details in
- https://stackoverflow.com/questions/50478661/python-isinstance-not-working-as-id-expect
- https://stackoverflow.com/questions/10582774/python-why-can-isinstance-return-false-when-it-should-return-true

"""
class FinancialStatementsBase:
    # def __init__(self,
    #              urls_df=None,
    #              edgar_urls=None):
    #     self.urls_df = urls_df
    #     self.edgar_urls = edgar_urls


    # @property
    # def settings(self):
    #     return self.settings


    @property
    def name(self):
        return self.settings.name


    @property
    def shortnames(self):
        return self.settings.shortnames


    # def statements(self):
    #     #raise NotImplementedError
    #     d = self.__dict__
    #     l = []
    #     #print(d)
    #     for key, value in d.items():
    #         #print(value.__class__.__bases__)
    #         if issubclass(value.__class__, StatementBase):
    #             l.append(value)
    #
    #     return l
    def statements(self):
        return _get_attr_list(self.__dict__, StatementBase)


    def to_dataframe(self, urls_df):
        l = []
        for statement in self.statements():
            l.append(statement.to_dataframe(urls_df[self.name]))

        return pd.concat(l)


# pl
class StatementsOfIncome(FinancialStatementsBase):
    def __init__(self):
        self.settings = StatementsOfIncomeSettings()
        self.revenue = Revenue()
        self.income_from_operations = IncomeFromOperations()
        self.net_income = NetIncome()

    # @property
    # def settings(self):
    #     return StatementsOfIncomeSettings()
    #
    # def statements(self):
    #     return [Revenue(),
    #             IncomeFromOperations()]

    def operating_margin(self):
        return OperatingMargin()


    # def statements(self):
    #     #raise NotImplementedError
    #     d = self.__dict__
    #     l = []
    #     for key, value in d.items():
    #         if issubclass(value.__class__, StatementBase):
    #             l.append(value)
    #
    #     return l
    # def statements(self):
    #     return _statements(self.__dict__, StatementBase)



# bs
class BalanceSheets(FinancialStatementsBase):
    def __init__(self):
        self.settings = BalanceSheetsSettings()
        self.total_stockholders_equity = TotalStockholdersEquity()
        self.total_liabilities_and_stockholders_equity = TotalLiabilitiesAndStockholdersEquity()


    # def settings(self):
    #     return BalanceSheetsSettings()


    # @property
    # def total_stockholders_equity(self):
    #     #return TotalStockholdersEquity()
    #     return self.total_stockholders_equity
    #
    #
    # @property
    # def total_liabilities_and_stockholders_equity(self):
    #     #return TotalLiabilitiesAndStockholdersEquity()
    #     return self.total_liabilities_and_stockholders_equity


    # def statements(self):
    #     return [TotalStockholdersEquity(),
    #             TotalLiabilitiesAndStockholdersEquity()]
    # def statements(self):
    #     return _statements(self.__dict__, StatementBase)



# cf
class StatementsOfCashFlows(FinancialStatementsBase):
    def __init__(self):
        self.settings = StatementsOfCashFlowsSettings()
        self.net_cash_provided_by_operating_activities = NetCashProvidedByOperatingActiveties()


    # @property
    # def settings(self):
    #     return StatementsOfCashFlowsSettings()
    #
    #
    # def statements(self):
    #     return [NetCashProvidedByOperatingActiveties()]
    # def statements(self):
    #     return _statements(self.__dict__, StatementBase)
