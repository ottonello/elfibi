from datetime import date, datetime
from typing import List, Dict

import riak

client = riak.RiakClient()


# https://github.com/cvitter/Riak-TS-Python-Demo

def _get_datetime(the_date: date, time: str):
    parsed_time = datetime.strptime(time, "%H:%M:%S")
    return datetime(the_date.year, the_date.month, the_date.day, parsed_time.hour, parsed_time.minute,
                    parsed_time.second)


def add_heartrate_data(user_id: str, the_date: date, dataset: List[Dict]):
    rows = [[user_id, _get_datetime(the_date, datapoint["time"]), float(datapoint["value"])] for datapoint in dataset]
    print(rows)
    table_obj = client.table("HeartRate").new(rows)
    try:
        result = client.ts_put(table_obj)
        print("Record written: {}".format(result))
    except Exception as e:
        print("Error: {}".format(e))


def get_heartrate_data(user_id: str, the_date: date):
    start_date_str: str = the_date.strftime("%Y-%m-%d 00:00:00")
    end_date_str: str = the_date.strftime("%Y-%m-%d 23:59:59")
    query = f"""\
    SELECT *
    FROM
        HeartRate
    WHERE
        time > '{start_date_str}' and time < '{end_date_str}' and
        user_id = '{user_id}'
    ORDER BY time
    """

    data_set = client.ts_query("HeartRate", query)
    rowcount = len(data_set.rows)

    dataset = []
    for row in data_set.rows:
        timestamp = datetime.fromtimestamp(row[1]/1000)
        print(row[1], timestamp)
        new_row = {"time": timestamp.strftime("%H:%M:%S"), "value": row[2]}
        dataset.append(new_row)
    return dataset
