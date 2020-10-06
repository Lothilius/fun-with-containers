import pandas as pd
import logging
import traceback
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

@pd.api.extensions.register_dataframe_accessor("forecast")
class ForecastSignup:
    def __init__(self, pandas_obj):
        """
        :param pandas_obj:
        """
        self.validate(pandas_obj)
        self.obj = pandas_obj
        self.datetime_column = self.obj.select_dtypes(include=[np.datetime64]).columns.to_list()[0]


    @staticmethod
    def validate(obj):
        """ Verify object passed has a data column
        :param obj: Pandas Dataframe object
        :return: an error if no datetime column present
        """
        if obj.select_dtypes(include=[np.datetime64]).empty:
            raise Exception("No datetime column found in Dataframe provided")

    @property
    def summary(self):
        summary = self.obj.groupby(by=[self.datetime_column]).count()
        return summary


    @property
    def expanding_mean(self):
        """
        :return:
        """
        self.summary['observed'] = self.summary.iloc[:, 0].expanding(min_periods=2).mean()
        shifted_df = self.summary.shift(1, freq="D")
        final_df = pd.concat([self.summary, shifted_df], axis=1, sort=False)
        return final_df
