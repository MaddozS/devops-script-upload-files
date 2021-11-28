import os
import pymysql
import csv
from datetime import datetime

import logging

from upload_gdrive import Upload_GDrive
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
# A function that get the data from the database, creates a file and returns the names of the files
def get_data():
    conn = pymysql.connect(host='localhost', user='maddozs', password='DevOps2021@', db='uady_sicei')
    sql_tables = "SHOW TABLES;"
    tables_name = None
    with conn.cursor() as cur:
        cur.execute(sql_tables)
        result = cur.fetchall()
        tables_name = [table[0] for table in result]

    sql_query = "SELECT * FROM {};"
    new_files_name = []
    for table in tables_name:
        with conn.cursor() as cur:
            cur.execute(sql_query.format(table))
            rows = cur.fetchall()
            headers = [col[0] for col in cur.description] # get headers

            # check if folder 'tables' exists
            if not os.path.exists('tables'):
                os.makedirs('tables')

            # get the current timestamp
            timestamp  =  datetime.now()

            # create a csv file for each table
            with open( f'tables/{table}_{timestamp}.csv', 'w', newline='') as csvfile:
                new_files_name.append(f'tables/{table}_{timestamp}.csv')
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)

            # data.append(result)
    return new_files_name

# a function that uploads a directory to Google Drive
def upload_to_drive(files_name):
    # upload the files to Google Drive
    GDrive = Upload_GDrive()
    for file_name in files_name:
        GDrive.upload_file(os.path.abspath(file_name), file_name)

# main 
if __name__ == "__main__":
    files_name = get_data()
    upload_to_drive(files_name)
    print('Done!')