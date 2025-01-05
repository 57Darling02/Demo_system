# import pandas as pd
import Api as api
from ResourcePool import resource_pool
# 泄露这段密钥可能导致服务器受到攻击
Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGFpbXMiOnsiYXBwbmFtZSI6IkppYW5nIn19.85lmabJ-T1Rx7WAZm9257zUYDCx4ktK6sVamZRaG5G4"

def fetch_monitor_info():
    try:
        resp = api.get_monitor_data(Token)
        if resp["code"] == 200:
            return resp["data"]
        else:
            print(f"Failed to fetch monitor info. {resp['data']}")
            return None
    except Exception as e:
        print(f"Error fetching monitor info: {e}")
    return None

def generate_alerts_and_suggestions(data):
    # 定义阈值
    thresholds = {
        "rainfall": 50,  # mm
        "air_temperature": 35,  # °C
        "humidity": [30, 85],  # %
        "wind_speed": 30,  # m/s
        "air_pressure": {
            "low": 1000,
            "normal": [1000, 1015],
            "high": 1015
        },
        "wind_direction": None  # 无具体阈值，通常无需预警
    }

    alerts = []

    for _, row in data.iterrows():
        monitor_id = row["monitor_id"]
        collect_time = row["collect_time"]
        warnings = []
        suggestions = []

        # 遍历各个字段的值
        #降雨量
        # 降雨量
        rainfall = row['rainfall']
        if rainfall >= 250:
            warnings.append("特大暴雨预警")
            suggestions.append("立即撤离危险区域，确保人身安全。不要在暴雨期间涉水行车或步行，警惕触电和暗流。")
        elif rainfall >= 100:
            warnings.append("大暴雨预警")
            suggestions.append("避免一切户外活动，及时转移到安全区域。注意当地政府发布的紧急避险通知。")
        elif rainfall >= 50:
            warnings.append("暴雨预警")
            suggestions.append("避免进入山区、河道或低洼易涝地区。检查房屋排水系统，提前储备必要物资。")
        elif rainfall >= 25:
            warnings.append("大雨预警")
            suggestions.append("避免低洼地段停留，检查排水设施是否通畅。驾车时注意积水，减少不必要的外出。")
        elif rainfall >= 10:
            warnings.append("中雨预警")
            suggestions.append("携带雨具，驾驶时注意路面湿滑。农业需注意防止部分作物因雨量过大受损。")


        # 气温等级划分
        temp = row['air_temperature']
        if temp <= -10:
            warnings.append("寒潮预警")
            suggestions.append("注意防寒保暖，避免长时间户外活动。")
            suggestions.append("检查取暖设备安全，预防火灾或一氧化碳中毒。")
            suggestions.append("农业、供暖等行业需做好防冻措施。")
        elif -10 < temp <= 0:
            warnings.append("低温预警")
            suggestions.append("注意穿戴厚实衣物，保护耳部、手部等暴露部位。")
            suggestions.append("小心路面结冰，避免摔伤。")
        elif 0 < temp <= 25:
            pass  # 适宜温度，无需特别建议
        elif 25 < temp <= 35:
            warnings.append("高温")
            suggestions.append("多喝水，避免长时间暴晒。")
            suggestions.append("注意老人、儿童和体弱者的健康状况。")
        elif temp > 35:
            warnings.append("极端高温")
            suggestions.append("避免中午时段外出，减少剧烈运动。")
            suggestions.append("保持通风，注意补水，可以适量饮用淡盐水。")
            suggestions.append("高温下作业的人员需加强防护，遵循用工安全规定。")

        #湿度
        humidity = row['humidity']
        if humidity <= thresholds['humidity'][0]:
            warnings.append("干燥预警")
            suggestions.append("湿度过低，火灾风险提高，严禁野外用火，防止火灾，注意补充水分，保护皮肤和呼吸道。")
        elif humidity >= thresholds['humidity'][1]:
            warnings.append("高湿度预警")
            suggestions.append("湿度过高，常伴随降水或持续闷热天气。注意防潮防霉，保持室内通风。")

        #风速
        if row["wind_speed"] > thresholds["wind_speed"]:
            warnings.append("【严重预警】风速极高，可能导致建筑物损坏或树木倒伏。")
            suggestions.append("风速过高，可能引发大风灾害，封锁门窗，请注意防范。")
        elif row["wind_speed"] > 10:
            warnings.append("强风预警")
            suggestions.append("当前风速较高，请注意户外活动安全。")
        elif row["wind_speed"] > 17:
            warnings.append("大风预警")
            suggestions.append("当前风速较高，避免出门，室内加固。")

        #气压
        air_pressure = row["air_pressure"]
        if air_pressure < thresholds["air_pressure"]["low"]:
            warnings.append("低气压预警")
            suggestions.append("当前为低气压区，多为阴天、雨天或风暴天气，可能伴随强风和降水，请关注天气预报，减少户外活动。如有台风或低压扰动，需做好防护措施。")
        elif air_pressure > thresholds["air_pressure"]["high"]:
            warnings.append("高气压预警")
            suggestions.append("当前为高气压区，天气晴朗，云量少，气温昼夜差较大，空气较干燥。注意保湿，预防干燥引发的不适，夜晚气温较低，需注意保暖。")


        alerts.append({
            "collect_time": collect_time,
            "monitor_id": monitor_id,
            "warnings": warnings,
            "suggestions": suggestions
        })

    return alerts
def main():
    # 获取最新数据
    inputdata = resource_pool.get_realtime_data()
    # 生成预警和建议
    alerts_and_suggestions = generate_alerts_and_suggestions(inputdata)

    # 输出结果
    print(alerts_and_suggestions)

if __name__ == "__main__":
    main()
