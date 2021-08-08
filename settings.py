import json

from pathlib import Path

from traitlets import Int, List, Dict, Unicode
from traitlets.config import Application
from traitlets.config.configurable import Configurable
from traitlets.config.loader import PyFileConfigLoader



# for URLs
class URLSettings:
    @property
    def base(self):
        return 'Base'

    @property
    def filing_summary(self):
        return 'Filing summary'

    @property
    def filing(self):
        return 'Filing'



class FinancialStatementsSettings:
    def __init__(self):
        self.bs_settings = BalanceSheetsSettings()
        self.pl_settings = StatementsOfIncomeSettings()
        self.cf_settings = StatementsOfCashFlowsSettings()

    @property
    def settings(self):
        return [self.pl_settings, self.bs_settings, self.cf_settings]
        #return [self.bs_settings, self.pl_settings, self.cf_settings]



"""
name: Balance sheets, Statements of income, Statements of cash cash_flows
statement: Revenues, Total stockholders' equity, Net cash provided by operating_activeties, etc...
"""
class SettingsBase:
    @property
    def name(self):
        raise NotImplementedError

    @property
    def shortnames(self):
        raise NotImplementedError

    @property
    def other_names(self):
        return NotImplementedError

    def statements(self):
        raise NotImplementedError



# bs
class BalanceSheetsSettings(SettingsBase):
    @property
    def name(self):
        return 'Balance Sheets'


    @property
    def shortnames(self):
        return ['balance sheet',
                'balance sheets']


    def statements(self):
        return [TotalStockholdersEquitySettings(),
                TotalLiabilitiesAndStockholdersEquitySettings()]



class TotalStockholdersEquitySettings(SettingsBase):
    @property
    def name(self):
        return "Total stockholders' equity"


    @property
    def other_names(self):
        return ["Total stockholders' equity",
                "Total stockholders’ equity",
                "Total shareholders' equity",
                "Total shareholders’ equity",
                "Total shareholders' (deficit) equity",
                "Total shareholders’ (deficit) equity",
                "Total shareholders' equity (deficit)",
                "Total shareholders’ equity (deficit)",
                'Total equity',
                "Total shareowners' equity"]



class TotalLiabilitiesAndStockholdersEquitySettings(SettingsBase):
    @property
    def name(self):
        return "Total liabilities and stockholders' equity"


    @property
    def other_names(self):
        return ["Total liabilities and stockholders' equity",
                "Total liabilities and stockholders’ equity",
                "Total liabilities and shareholders' equity",
                "Total liabilities and shareholders’ equity",
                "Total liabilities, noncontrolling interest and shareholders' (deficit) equity",
                "Total liabilities, noncontrolling interest and shareholders’ (deficit) equity",
                "Total liabilities, redeemable noncontrolling interest and shareholders' equity",
                "Total liabilities, redeemable noncontrolling interest and shareholders’ equity",
                "Total liabilities, redeemable noncontrolling interest and shareholders' equity (deficit)",
                "Total liabilities, redeemable noncontrolling interest and shareholders’ equity (deficit)",
                'Total liabilities and equity',
                "Total liabilities, redeemable noncontrolling interest, and shareowners' equity",
                "Total liabilities and shareowners' equity",
                "Total liabilities, temporary equity and stockholders’ equity",
                "Total liabilities, temporary equity and stockholders' equity",
                "TOTAL LIABILITIES AND SHAREHOLDERS' EQUITY",
                "TOTAL LIABILITIES AND SHAREHOLDERS’ EQUITY"]



# pl
class StatementsOfIncomeSettings(SettingsBase):
    @property
    def name(self):
        return 'Statements of income'


    @property
    def shortnames(self):
        return ['statements of income',
                'income statements',
                'statement of operations',
                'statements of operations',
                'statements of earnings',
                'statement of income']


    def statements(self):
        return [RevenueSettings(),
                IncomeFromOperationsSettings(),
                NetIncomeSettings()]



class RevenueSettings(SettingsBase):
    @property
    def name(self):
        return 'Revenue'


    @property
    def other_names(self):
        return ['Revenue',
                'Revenues',
                'Net Sales',
                'Net sales',
                'Total net sales',
                'Total revenue',
                'Total revenues',
                'Net revenues']



class IncomeFromOperationsSettings(SettingsBase):
    @property
    def name(self):
        return 'Income from Operations'


    @property
    def other_names(self):
        return ['Income from operations',
                'Income (loss) from operations',
                'Operating income',
                'Operating income (loss)',
                'Net income attributable to Honeywell',
                'Loss from operations',
                'Income before income taxes',
                'Operating loss']



class NetIncomeSettings(SettingsBase):
    @property
    def name(self):
        return 'Net income'


    @property
    def other_names(self):
        return ['Net income',
                'Net income (loss)',
                'Net loss',
                'Net loss attributable to common stockholders',
                'Net income (loss) attributable to salesforce.com',
                'NET INCOME']



# cf
class StatementsOfCashFlowsSettings(SettingsBase):
    @property
    def name(self):
        return 'Statements of cash flows'


    @property
    def shortnames(self):
        return ['statement of cash flows',
                'statements of cash flows',
                'cash flows statements']



class NetCashProvidedByOperatingActivetiesSettings(SettingsBase):
    @property
    def name(self):
        return 'Net cash provided by operating activities'


    @property
    def other_names(self):
        return ['Net cash provided by operating activities',
                'Net cash from operations',
                'Net cash provided by (used in) operating activities',
                'Net cash used in operating activities',
                'Net cash (used in) provided by operating activities',
                'Net cash provided by (used for) operating activities',
                'Cash provided (used) by operations',
                'Cash provided by operations',
                'Cash generated by operating activities']



# Settings for KPI
class OperatingMarginSettings(SettingsBase):
    @property
    def name(self):
        return 'Operating margin'


class ROESettings(SettingsBase):
    @property
    def name(self):
        return 'ROE'


class ShareholdersEquityRatioSettings(SettingsBase):
    @property
    def name(self):
        return "Shareholders' equity ratio"
