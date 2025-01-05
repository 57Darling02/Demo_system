# import requests
# import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import Api as api
import pandas as pd
import atexit
@atexit.register
def on_exit():
    resource_pool.scheduler.shutdown()
    print("Scheduler has been shut down.")
class ResourcePool:
    # 类变量，存储唯一的实例
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            # 创建新的实例
            instance = super().__new__(cls)
            # 初始化实例
            instance.Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGFpbXMiOnsiYXBwbmFtZSI6IkppYW5nIn19.85lmabJ-T1Rx7WAZm9257zUYDCx4ktK6sVamZRaG5G4"
            instance.update_interval = 1.5  # 更新间隔，单位：秒
            instance.MaxDataId = 0
            instance.resources = {}
            instance.scheduler = BackgroundScheduler()
            instance.start_scheduler()
            instance.update_timestamp = datetime.datetime.now()
            cls._instance = instance
        return cls._instance

    def get_update_timestamp(self):
        return self.update_timestamp


    def ifNewdata(self):
        try:
            resp = api.getMaxDataId(self.Token)
            if resp["code"] == 200:
                if resp["data"] != self.MaxDataId:
                    self.MaxDataId = resp["data"]
                    return True
        except Exception as e:
            print(e)
        return False


    def fetch_monitor_data(self):
        if self.ifNewdata():
            try:
                resp = api.get_monitor_data(self.Token)
                if resp["code"] == 200:
                    return resp["data"]
                else:
                    print(f"Failed to fetch form data.{resp['data']}")
                    return None
            except Exception as e:
                print(f"Error fetching form data: {e}")
        return None

    def fetch_monitor_info(self):
        try:
            resp = api.get_monitor_list(self.Token)
            if resp["code"] == 200:
                return resp["data"]
            else:
                print(f"Failed to fetch monitor info.{resp['data']}")
                return None
        except Exception as e:
            print(f"Error fetching monitor info: {e}")
        return None

    def update_resource_pool(self):
        try:
            self.update_timestamp = datetime.datetime.now()
            print(f"{self.update_timestamp} : Updating resource pool...")
            detected_data = self.fetch_monitor_data()
            monitor_info = self.fetch_monitor_info()
            if detected_data:
                self.resources["form_data"] = detected_data
            if monitor_info:
                self.resources["monitor_info"] = monitor_info
        except InterruptedError:
            print("Cleaning up...")
            self.scheduler.shutdown()

    def start_scheduler(self):
        self.update_resource_pool()
        self.scheduler.add_job(self.update_resource_pool, 'interval', seconds=self.update_interval,max_instances=3,replace_existing=True)
        self.scheduler.start()

    def get_detected_data(self):
        df = pd.DataFrame(self.resources.get("form_data"))
        df["collect_time"]=pd.to_datetime(df['collect_time'],format='%Y-%m-%d %H:%M:%S')
        df["upload_time"]=pd.to_datetime(df['upload_time'],format='%Y-%m-%d %H:%M:%S')
        df["collect_time"] = df["collect_time"].dt.tz_localize('Asia/Shanghai')
        df["upload_time"] = df["upload_time"].dt.tz_localize('Asia/Shanghai')
        return df
    def get_monitor_info(self):
        df = pd.DataFrame(self.resources.get("monitor_info"))
        return df


    def get_realtime_data(self):
        # 获取最新的监测数据
        data = self.get_detected_data()
        data = data.sort_values(by='collect_time')
        data = data.drop_duplicates(subset=['monitor_id'], keep='last')
        return data



resource_pool = ResourcePool()




if __name__ == "__main__":
    # 仅在作为脚本直接运行时测试资源池
    resource_pool = ResourcePool()
    while True:
        a = resource_pool.get_realtime_data()
        import time
        time.sleep(10)