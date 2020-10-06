import pandas as pd
from os import environ
from sqlalchemy import create_engine
import logging
import traceback
from calculations.Forecast import ForecastSignup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def split_date(date_time_stamp):
    """ Given a time stamp return a Series with the year month and day components
    :param date_time_stamp: pandas time stamp
    :return: Series of the year month and day components of the pandas timestamp
    """
    assert (type(date_time_stamp) is pd.Timestamp), "A timestamp was not provided"
    return pd.Series({'year': date_time_stamp.year, 'month': date_time_stamp.month, 'day': date_time_stamp.day})


def update_user_counts():
    # Create the Connection to the Postgres Database
    alchemy_engine = create_engine('postgresql+psycopg2://%s:%s@%s/postgres' % (environ['POSTGRES_USER'],
                                                                                environ['POSTGRES_PASSWORD'],
                                                                                environ['POSTGRES_HOST']),
                                   pool_recycle=3600)
    postgres_connection = alchemy_engine.connect()

    # Query the db to get data
    user_df = pd.read_sql_query('select user_id, last_four, visit_date from "users"', con=postgres_connection)

    # Restructure ids to one id for uniqueness
    user_df['id'] = user_df[['user_id', 'last_four']].apply(lambda x: str(x[0]) + " " + str(x[1]), axis=1)

    # Use the Forecast class to get cumulative mean
    user_aggregate = user_df[['id', 'visit_date']].forecast.expanding_mean.reset_index()

    # Split dates in to there year month and day components and concatenate them to the dataframe as columns
    daily_user_counts = pd.concat([user_aggregate, user_aggregate['visit_date'].apply(split_date)], axis=1)

    table_name = "daily_user_counts"
    logger.info("Attempting to create table %s", table_name)

    # Create Table in Postgres DB
    results = daily_user_counts[['year', 'month', 'day', 'observed', 'count']].to_sql(table_name,
                                                                                      postgres_connection,
                                                                                      if_exists='replace')

    logger.info("Results: %s", results)
    postgres_connection.close()

    logger.info("Connection to DB Closed")


if __name__ == '__main__':
    try:
        update_user_counts()
    except:
        logger.error(traceback.format_exc())