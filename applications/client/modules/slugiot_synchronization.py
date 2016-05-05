from gluon import current;
from datetime import datetime;
import requests
from gluon import serializers;

class SlugIOTSynchronization():
    def some_function(self):
        db = current.db
        print "hello world"

    def synchronize_logs(self):
        synchronized_timestamp = datetime.utcnow()
        data = self.__get_log_data(synchronized_timestamp)
        url = server_url + "/synchronization/receive_logs"
        json_data = serializers.json(data)
        sync_response = requests.post(url=url, data=json_data)
        if (sync_response.status_code == 200):
            #success
            self.__set_last_synchronized("logs", synchronized_timestamp)
            return dict(success=True,timestamp=synchronized_timestamp)
        else:
            #failure
            error = sync_response.content
            return dict(
                    success=False,
                    timestamp=synchronized_timestamp,
                    error=error,
                    server_url=url,
                )

    """
    This function takes in a table_name (logs, outputs, etc) and returns the latest timestamp the data was synchronized

       :param p1: table_name
       :type p1: str
       :return: Timestamp of latest entry in a database table
       :rtype: datetime
    """

    def __get_last_synchronized(self, table_name):
        timestamp = db(db.synchronization_events.table_name == table_name).select(db.synchronization_events.time_stamp,
                                                                                  orderby="time_stamp DESC",
                                                                                  limitby=(0, 1))
        if (not timestamp):
            return datetime.fromtimestamp(0)
        return timestamp[0].time_stamp

    """
    This function takes in a table_name and timestamp and inserts in into the synchronization_events table

       :param p1: table_name
       :type p1: str
       :param p1: timestamp
       :type p1: str
    """

    def __set_last_synchronized( self, table_name, timestamp):
        db.synchronization_events.insert(table_name=table_name, time_stamp=timestamp)


