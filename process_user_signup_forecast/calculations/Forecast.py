import pandas as pd
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

@pd.api.extensions.register_dataframe_accessor("forecast")
class ForecastSignup:
    def __init__(self, pandas_obj):
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
    def count_summary(self):
        summary = self.obj.groupby(by=[self.datetime_column]).count()
        summary.rename(columns={'id': 'count'}, inplace=True)
        return summary


    @property
    def expanding_mean(self):
        """ Use summary propery of the dataframe to create cumulative mean column shifted forward a day. The cumulative
        is the expected users to sign up for the day based on all the previous days.
        :return: dataframe of the summarized with the count and the cumulative mean column
        """
        shifted_df = self.count_summary.iloc[:, 0].expanding(min_periods=2).mean()
        shifted_df = shifted_df.shift(1, freq="D")
        shifted_df.rename('observed', inplace=True)
        count_mean_df = pd.concat([self.count_summary, shifted_df], axis=1, sort=False)
        return count_mean_df
