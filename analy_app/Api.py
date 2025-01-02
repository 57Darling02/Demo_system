import requests

# 使用 json.loads 方法将 JSON 字符串解析为 Python 对象
# data = json.loads(json_str)

# 使用 json.dumps 方法将 Python 对象转换为 JSON 字符串
# json_str = json.dumps(data)
# base_url = "http://127.0.0.1:8686/"
base_url = "http://db.57d02.cn:8686/"

def login(username, password):
    url = base_url+"user/login"
    payload = {"username": username, "password": password}
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        print(f"Login: {data}")
        return data
    except Exception as e:
        print(e)
        return None

def user_register(username, password):
    url = base_url+"user/register"
    payload = {"username": username, "password": password}
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        print(f"userRegister: {data}")
        return data
    except Exception as e:
        print(e)
        return None

def monitor_register(username, password,token):
    headers = {"Authorization": f"{token}"}
    url = base_url+"monitor/register"
    payload = {"monitor_id": username, "password": password}
    try:
        response = requests.post(url,headers=headers, data=payload)
        data = response.json()
        print(f"monitorRegister: {data}")
        return data
    except Exception as e:
        print(e)
        return None

def get_monitor_list(token):
    url = base_url + "monitor/monitorList"
    headers = {"Authorization": f"{token}"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        print(e)
        return None

def get_monitor_data(token):
    url = base_url + "monitor/getAllData"
    header = {"Authorization": f"{token}"}
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        return data
    except Exception as e:
        print(e)
        return None

def getMaxDataId(token):
    url = base_url + "monitor/getMaxDataId"
    header = {"Authorization": f"{token}"}
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        return data
    except Exception as e:
        print(e)
    return None

# resp = login("zzh114","114514")
# if resp != None and resp["code"] == 200:
#     token = resp["data"]
#     # get_monitor_data(token)
#     getMaxDataId(token)