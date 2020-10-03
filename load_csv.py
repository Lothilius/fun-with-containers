import pandas as pd
from os import environ
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def main():
    # Create the Connection to the Postgres Database
    alchemy_engine = create_engine('postgresql+psycopg2://%s:%s@127.0.0.1/postgres' % (environ['POSTGRES_USER'],
                                                                                       environ['POSTGRES_PASSWORD']),
                                   pool_recycle=3600)
    postgres_connection = alchemy_engine.connect()
    table_name = "users"

    # Load User file in to Dataframe
    users_df = pd.DataFrame('Generated_Data_modified.csv')

    # Split id column in to components
    users_df = pd.concat([users_df,
                          users_df['id'].apply(lambda x: pd.Series({'user_id': int(x.split(' ')[0]),
                                                                    'last_four': int(x.split(' ')[1])}))], axis=1)

    # Set User Id and last four as index
    users_df.set_index(['user_id', 'last_four'], inplace=True)

    try:
        users_df[['first_name', 'last_name', 'age', 'gender', 'visit_date']].to_sql(table_name,
                                                                                    postgres_connection,
                                                                                    if_exists='replace')
    except ValueError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    else:
        logger.info("Table %s created successfully.", table_name)
    finally:
        postgres_connection.close()


if __name__ == '__main__':
    main()
