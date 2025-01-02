import pandas as pd
import Api as api
# 泄露这段密钥可能导致服务器受到攻击
Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGFpbXMiOnsiYXBwbmFtZSI6IkppYW5nIn19.85lmabJ-T1Rx7WAZm9257zUYDCx4ktK6sVamZRaG5G4"
def fetch_monitor_info():
    try:
        resp = api.get_monitor_data(Token)
        if resp["code"] == 200:
            return resp["data"]
        else:
            print(f"Failed to fetch monitor info.{resp['data']}")
            return None
    except Exception as e:
        print(f"Error fetching monitor info: {e}")
    return None
### timestamp全部改成collect_time用就行，不需要额外增加一列
def get_detected_data():
    df = pd.DataFrame(fetch_monitor_info())
    df["collect_time"] = pd.to_datetime(df['collect_time'], format='%Y-%m-%d %H:%M:%S')
    df["upload_time"] = pd.to_datetime(df['upload_time'], format='%Y-%m-%d %H:%M:%S')
    df["collect_time"] = df["collect_time"].dt.tz_localize('Asia/Shanghai')
    df["upload_time"] = df["upload_time"].dt.tz_localize('Asia/Shanghai')
    return df
def get_realtime_data():
    # 获取最新的监测数据
    data = get_detected_data()
    data = data.sort_values(by='collect_time')
    data = data.drop_duplicates(subset=['monitor_id'], keep='last')
    return data

inputdata = get_detected_data()
##### 你可以在这打断点看看inputdata具体是什么
"""
inputdata是一个pandas的DataFrame，他的每一行都是某个监测器的最新数据，因为我们目前只有一个监视器，因此只有一行数据，但是我们处理的时候要考虑到可能有多个监视器的情况
也就是说，处理每一条inputdata里的数据
然后，输出一个列表 列表包含多个字典，每个字典是一个监视器的预警和建议
有如下项目：
["rainfall", "air_temperature", "humidity", "wind_speed", "air_pressure","wind_direction"]
遍历项目值，得出相应建议，组成
超过阈值的项目名称放入warnings,
然后遍历所有的项目，根据值的大小，给出建议放入suggestions列表中
如果这个值超过阈值，则把这个项目放入warnings列表中。
我表格的某一行是这样的：
monitor_id = 1  collect_time = xxx  upload_time = xxx  rainfall = 10000  air_temperature = xxx  humidity =10000 wind_speed = xxx  air_pressure = xx  wind_direction = xxx
那么你的输出应该的一个字典如下：
output = [
{
"monitor_id": 1,
"warnings": ["wind_speed","humidity"],
"suggestions": ["大量降雨xxx。","气温较低。","湿度过高xxx。","风速较低。","气压正常。","风向正常。"]
},
{
"monitor_id": 2,
"warnings": [],
"suggestions": []
]



"""
print(get_realtime_data())