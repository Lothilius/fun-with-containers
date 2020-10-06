import pandas as pd
from os import environ
from sqlalchemy import create_engine
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def split_date(date_time_stamp):
    assert (type(date_time_stamp) is pd.Timestamp), "A timestamp was not provided"
    return pd.Series({'year': date_time_stamp.year, 'month': date_time_stamp.month, 'day': date_time_stamp.day})


def update_user_counts():
    # Create the Connection to the Postgres Database
    alchemy_engine = create_engine('postgresql+psycopg2://%s:%s@%s/postgres' % (environ['POSTGRES_USER'],
                                                                                environ['POSTGRES_PASSWORD'],
                                                                                'localhost'), # environ['POSTGRES_HOST']),
                                   pool_recycle=3600)
    postgres_connection = alchemy_engine.connect()

    # Query the db to get data
    user_df = pd.read_sql_query('select user_id, last_four, visit_date from "users"', con=postgres_connection)

    # Restructure ids to one id for uniqueness
    user_df['id'] = user_df[['user_id', 'last_four']].apply(lambda x: str(x[0]) + " " + str(x[1]), axis=1)

    user_df[['id', 'visit_date']].forecast.expanding_mean #.reindex(inplace=True)
    user_df = pd.concat([user_df, user_df['visit_date'].apply(split_date)], axis=1)

    table_name = "daily_user_counts"
    logger.info("Attempting to create table %s", table_name)

    # Create Table in Postgres DB
    results = user_df[['year', 'month', 'day', 'observed', 'count']].to_sql(table_name,
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