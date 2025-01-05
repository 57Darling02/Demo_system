import Api as api
# 泄露这段密钥可能导致服务器受到攻击
Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGFpbXMiOnsiYXBwbmFtZSI6IkppYW5nIn19.85lmabJ-T1Rx7WAZm9257zUYDCx4ktK6sVamZRaG5G4"
# 获取所有检测到的数据
def get_all_data():
    try:
        resp = api.get_monitor_data(Token)
        if resp["code"] == 200:
            return resp["data"]
        else:
            print(f"Failed to fetch form data.{resp['data']}")
            return None
    except Exception as e:
        print(f"Error fetching form data: {e}")

# 可以处理成dataframe，如下：
import pandas as pd
#原始数据
org_data = get_all_data()
#转换成DataFrame
data = pd.DataFrame(org_data)
print()