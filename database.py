import pandas as pd
import pymysql
from sqlalchemy import create_engine

CONNECTION_STRING = 'mysql+pymysql://ppxTimeAdmin:gtRYiVqRds8Pstk@db-ppx-timetracker.cualg22alycu.eu-west-2.rds.amazonaws.com:3306'
USER_NAME = 'test_person'

class db_connection:
    def __init__(self):
        """ init with useful paths and variables that are needed in the class scope """
        self.engine = create_engine(CONNECTION_STRING)
        self.path_to_clean_logs =  r"log_files/log_files_cleaned/clean_logs.csv"
        self.clean_logs = pd.DataFrame({'activity':[],'BeginDatetime':[],'EndDatetime':[]})
        self.path_to_activity = "activity.json"
        self.table_name = USER_NAME

    def set_up_user(self):
        sql_query = f"""   
        CREATE TABLE {USER_NAME}_activity_history (
    activity varchar(255),
    startdatetime varchar(255),
    endatetime varchar(255),
   ....
    );
        """
        with self.engine.connect() as bridge_connected:
            bridge_connected.execute(sql_query)
        
    def push_local_to_db(self):
        """ sends local data to database, will replace all data in the database currently """
        self.clean_logs = pd.read_csv(self.path_to_clean_logs)

        with self.engine as bridge:
            self.clean_logs.to_sql(con=bridge.connect(),name=f"{USER_NAME}_activity_history",index=False)
    def read_db(self):
        database_logs = pd.DataFrame()
        with self.engine.connect() as bridge_connected:
            sql_query = f"""
            SELECT * FROM {USER_NAME}_activity_history
            """
            database_logs = pd.read_sql(con=bridge_connected)
        
