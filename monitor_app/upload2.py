import time
from datetime import datetime
from random import randrange
import requests
base_url = "http://127.0.0.1:8686/monitor/"
# 这本文件不需要修改，请直接import这个包并调用upload_data函数上传数据
class Monitor:
    def __init__(self, id, password,base_url):
        self.id = id
        self.password = password
        self.base_url = base_url
        self.token = self.login()
    def upload_data(self, collect_time=None, wind_direction=None, wind_speed=None, humidity=None, rainfall=None, air_temperature=None, air_pressure=None, scene_type=None):
        url = self.base_url+"uploadData"
        headers = {"Authorization": f"{self.token}"}
        payload = {
            "collect_time": collect_time,
            "wind_direction": wind_direction,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "rainfall": rainfall,
            "air_temperature": air_temperature,
            "air_pressure": air_pressure,
            "scene_type": scene_type,
        }
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        if data['code'] == 200:
            print("上传成功")
        elif data['code'] == 401:
            self.token = self.login()
        else:
            print(f"error: {data}")
    def login(self):
        url = self.base_url + "login"
        # 填上注册的id和密码，之后传数据的时候每个数据会对应上检测器的id
        payload = {"monitor_id": self.id, "password": self.password}
        response = requests.post(url, data=payload)
        data = response.json()
        if data['code'] == 200:
            print(f"登录成功,id:{self.id}")
            return data['data']
        else:
            print(f"登录失败: {data}")
            time.sleep(3)
            return None

# 下面是示例，每隔一秒上传一次数据，请在其他地方导入这个包并使用upload_data函数上传数据
if __name__ == "__main__":
    try:
        monitor = Monitor(2,"114514",base_url)
        for i in range(1000):
            time.sleep(1)
            # 模拟每一秒钟获取到数据并上传
            # 这里是获取的数据
            Wind_direction = randrange(1, 360)
            Wind_speed = i*randrange(1, 10)
            Humidity = 50+randrange(1, 10)
            Rainfall = 50-randrange(1, 10)
            Air_temperature = 20 +randrange(1, 10)
            Air_pressure = 12+randrange(1, 10)*1.5
            Scene_type = "测试数据"
            Collect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 将数据上传
            monitor.upload_data(collect_time = Collect_time, wind_direction = Wind_direction, wind_speed = Wind_speed,
                        humidity = Humidity, rainfall = Rainfall, air_temperature = Air_temperature, air_pressure = Air_pressure,
                        scene_type = Scene_type)
    except Exception as e:
        print(f"error: {e}")

