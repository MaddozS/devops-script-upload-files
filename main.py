import os
import pymysql
import csv
from datetime import datetime
from upload_gdrive import Upload_GDrive
import logging
from config import CONFIG

# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
# A function that get the data from the database, creates a file and returns the names of the files
def get_data():
    logging.debug('get_data method called')

    conn = pymysql.connect(host=CONFIG["host"], user=CONFIG["user"], password=CONFIG["password"], db=CONFIG["database"], port=CONFIG["port"])
    sql_tables = "SHOW TABLES;"
    tables_name = None
    try:
        with conn.cursor() as cur:
            cur.execute(sql_tables)
            logging.debug('fetchall method called')
            result = cur.fetchall()
            tables_name = [table[0] for table in result]

        sql_query = "SELECT * FROM {};"
        new_files_name = []
        for table in tables_name:
            with conn.cursor() as cur:
                cur.execute(sql_query.format(table))
                rows = cur.fetchall()
                logging.debug('fetchall method called')
                headers = [col[0] for col in cur.description] # get headers

                # check if folder 'tables' exists
                logging.info('checking if folder tables exist...')
                if not os.path.exists('tables'):
                    os.makedirs('tables')

                # get the current timestamp
                timestamp  =  datetime.now()

                # create a csv file for each table
                with open( f'tables/{table}_{timestamp}.csv', 'w', newline='') as csvfile:
                    files_name = csvfile.name
                    logging.info(f'creating {files_name} file...')

                    new_files_name.append(files_name)

                    logging.info(f'Adding information to {files_name} file...')
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
                    writer.writerows(rows)

    except Exception as e:
        logging.exception("Error getting tables")

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
    # start logger
    logging.basicConfig(handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ], level=logging.DEBUG)

    logging.info('Script started: Uploading files to Google Drive...')
    files_name = get_data()
    upload_to_drive(files_name)
    logging.info('Script finished!')
