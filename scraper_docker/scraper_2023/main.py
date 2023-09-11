import datetime
from utils.api import Request, Response
from input.config import ZONES_FOLDER_ID, RUN_AT
from utils.google_sheet import GoogleSheet
from utils.utils import get_date_today
from utils.db import MySQLite
import time
import schedule
from pytz import timezone
from utils.logger import logger


def main():
    logger.info('Starting the script')
    my_sqlite = MySQLite()
    clients_list = my_sqlite.get_zones()
    for client in clients_list:
        logger.info(str(datetime.datetime.now()))
        payload_fresh_map = client['payload_fresh_map']
        client_name = client['client_name']
        logger.info(f'client_name : {client_name}')
        logger.info(f'payload_fresh_map : {payload_fresh_map}')
        r = Request(payload=payload_fresh_map)

        fresh_text = r.call_fresh()
        resp = Response(fresh_text)
        homes = resp.run()

        # Create a folder with client_name
        sh = GoogleSheet()
        folder_id = sh.get_or_create(client_name, ZONES_FOLDER_ID)

        sheet_name = client_name + '_' + get_date_today()
        sheet_id = sh.create_sheet(sheet_name, folder_id)

        df_homes = sh.convert_to_df(homes)

        sh.update_values(sheet_id, df_homes)

        time.sleep(3)
    logger.info('#'*100)
    logger.info('#'*100)


if __name__ == "__main__":
    # main()

    schedule.every().day.at(RUN_AT, timezone("Canada/Mountain")).do(main)
    schedule.every(10).seconds.do(main)
    logger.info(str(datetime.datetime.now()))
    while True:
        schedule.run_pending()
        time.sleep(1)

    while 1:
        n = schedule.idle_seconds()
        logger.info('Sleep: ' + time.strftime("%H:%M:%S", time.gmtime(n)))
        if n is None:
            # no more jobs
            logger.info('n is None')
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()
