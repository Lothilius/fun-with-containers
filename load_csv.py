import pandas as pd
from os import environ
import logging
from sqlalchemy import create_engine
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def load_csv():
    # Create the Connection to the Postgres Database
    alchemy_engine = create_engine('postgresql+psycopg2://%s:%s@%s/postgres' % (environ['POSTGRES_USER'],
                                                                                       environ['POSTGRES_PASSWORD'],
                                                                                       environ['POSTGRES_HOST']),
                                   pool_recycle=3600)
    postgres_connection = alchemy_engine.connect()
    table_name = "users"

    # Load User file in to a Dataframe
    users_df = pd.read_csv(environ['CSV_FILE'])

    # Split id column in to components
    users_df = pd.concat([users_df,
                          users_df['id'].apply(lambda x: pd.Series({'user_id': int(x.split(' ')[0]),
                                                                    'last_four': int(x.split(' ')[1])}))], axis=1)

    # Set User Id and last four as index
    users_df.set_index(['user_id', 'last_four'], inplace=True)
    # Set type for date column
    users_df['visit_date'] = pd.to_datetime(arg=users_df['visit_date'])


    users_df[['first_name', 'last_name', 'age', 'gender', 'visit_date']].to_sql(table_name,
                                                                                postgres_connection,
                                                                                if_exists='replace')

    logger.info("Table %s created successfully.", table_name)
    postgres_connection.close()
    logger.info("Connection to DB Closed")



if __name__ == '__main__':
    try:
        load_csv()
    except:
        logger.error(traceback.format_exc())