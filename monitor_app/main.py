import time
from read_data import read_data
import upload
import configparser


def main():
    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()
    # 读取 config.ini 文件
    config.read("config.ini", encoding='utf-8')

    # 获取配置信息
    interval = config.get('Device', 'interval')
    port = config.get('Device', 'port')  # 例如：'COM8'
    baudrate = config.get('Device', 'baudrate')  # 例如：'9600'
    baudrate = int(baudrate)
    monitor_id = config.get('Monitor', 'id')  # 例如：'1'
    monitor_id = int(monitor_id)
    password = config.get('Monitor', 'password')  # 登录服务器的密码
    base_url = config.get('Monitor', 'base_url')  # 服务器的基础 URL
    interval = int(interval)
    monitor = None
    for i in range(3):  # 尝试连接服务器三次
        try:
            monitor = upload.Monitor(monitor_id, password, base_url)  # 假设 Monitor 类有 token 作为登录凭证
            break
        except Exception as e:
            print(f"无法连接到服务器: {e}\n第{i + 1}次重试中...")
            time.sleep(3)

    if not monitor or not monitor.token:
        print("无法连接到服务器，请检查网络连接")
        return

    print("成功连接到服务器，开始采集数据...")

    while True:
        try:
            # 调用采集函数，读取所有传感器数据
            wind_speed, rainfall, temperature, pressure, humidity, wind_direction, local_time = read_data(port,
                                                                                                          baudrate)

            # 检查是否所有数据都成功采集
            if any(data is None for data in [wind_speed, rainfall, temperature, pressure, humidity, wind_direction]):
                print("无法获取部分数据，请检查传感器连接")
            else:
                print(
                    f"采集数据成功：风速={wind_speed}, 降雨量={rainfall}, 温度={temperature}, 气压={pressure}, 湿度={humidity}, 风向={wind_direction}")

                # 上传数据到服务器
                monitor.upload_data(
                    collect_time=local_time,
                    wind_speed=wind_speed,
                    rainfall=rainfall,
                    air_temperature=temperature,
                    air_pressure=pressure,
                    humidity=humidity,
                    wind_direction=wind_direction
                )

            time.sleep(interval)  # 设置采集间隔时间（秒）
        except KeyboardInterrupt:  # 捕捉 Ctrl+C 终止程序
            print("程序终止")
            break
        except Exception as e:  # 捕捉其他异常
            print(f"发生错误: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
