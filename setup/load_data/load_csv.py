import pandas as pd
from os import environ
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import traceback
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def connect_to_db():
    alchemy_engine = create_engine('postgresql+psycopg2://%s:%s@%s/postgres' % (environ['POSTGRES_USER'],
                                                                                       environ['POSTGRES_PASSWORD'],
                                                                                       environ['POSTGRES_HOST']),
                                   pool_recycle=3600)

    return alchemy_engine.connect()


def load_csv(table_name="users"):
    """ Load a CSV file in to a predefined postgres DB by creating a table with the name provided. Postgres and csv
    are predefined in environment variable.
    :param table_name: string of the table name to be created
    :return: None
    """
    # Create the Connection to the Postgres Database
    try:
        postgres_connection = connect_to_db()
    except OperationalError:
        logger.warning("DB not available. Trying again in 5 seconds")
        time.sleep(5)
        postgres_connection = connect_to_db()

    # Load User file in to a Dataframe
    users_df = pd.read_csv(environ['CSV_FILE'])

    # Split id column in to components
    users_df = pd.concat([users_df,
                          users_df['id'].apply(lambda x: pd.Series({'user_id': int(x.split(' ')[0]),
                                                                    'last_four': x.split(' ')[1]}))], axis=1)

    # Set User Id and last four as index
    users_df.set_index(['user_id', 'last_four'], inplace=True)

    # Set type for date column
    users_df['visit_date'] = pd.to_datetime(arg=users_df['visit_date'])

    logger.info("Attempting to create table %s", table_name)
    # Create Table in Postgres DB
    results = users_df[['first_name', 'last_name', 'age', 'gender', 'visit_date']].to_sql(table_name,
                                                                                postgres_connection,
                                                                                if_exists='replace')

    logger.info("Results: %s", results)
    postgres_connection.close()



    logger.info("Connection to DB Closed")


if __name__ == '__main__':
    try:
        load_csv()
    except:
        logger.error(traceback.format_exc())