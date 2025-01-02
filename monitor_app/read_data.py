import serial
import time
import crcmod
from datetime import datetime

# 新增的传感器命令
wind_speed_cmd = 'C8 03 00 00 00 01'  # 读取风速数据的命令
rainfall_cmd = 'C9 03 00 00 00 02'  # 读取降雨量数据的命令
temperature_cmd = '66 03 00 00 00 01'  # 读取温度数据的命令
pressure_cmd = '66 03 00 02 00 01'  # 读取气压数据的命令
humidity_cmd = '66 03 00 01 00 01'  # 读取湿度数据的命令
wind_direction_cmd = 'C8 03 00 01 00 01'  # 读取风向数据的命令


def calculate_crc16(data):
    """
    计算 CRC16 校验码，低字节在前，高字节在后
    :param data: 要计算 CRC 的字节数据
    :return: 低字节在前，高字节在后的 CRC16 校验码（字节类型）
    """
    crc16 = crcmod.predefined.mkCrcFun('modbus')
    crc_value = crc16(data)
    crc_bytes = crc_value.to_bytes(2, byteorder='little')
    return crc_bytes


def send_and_receive_hex_data(port, baudrate, hex_data):
    """
    此函数用于向指定串口发送十六进制数据，并接收响应
    :param port: 串口名称，如 'COM1' 或 '/dev/ttyUSB0'
    :param baudrate: 波特率，如 9600, 115200 等
    :param hex_data: 要发送的十六进制数据，以字符串形式表示，如 'C8 03 00 00 00 01'
    """
    ser = None
    try:
        # 打开串口
        ser = serial.Serial(port, baudrate, timeout=1, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                            parity=serial.PARITY_NONE)
        # 将十六进制字符串转换为字节数据
        data_to_send = bytes.fromhex(hex_data)
        # 计算 CRC16 校验码
        crc = calculate_crc16(data_to_send)
        # 追加 CRC16 校验码
        data_to_send += crc
        # 发送数据
        ser.write(data_to_send)
        # 等待一段时间，确保设备有足够的时间响应
        time.sleep(0.1)
        # 读取响应
        response = ser.read(ser.in_waiting)
        # 关闭串口
        if ser.is_open:
            ser.close()
        return response
    except Exception as e:
        # 关闭串口
        if ser and ser.is_open:
            ser.close()
        print(f"An error occurred: {e}")
        return None


def parse_weather_data(response):
    """
    解析气象传感器的响应数据
    :param response: 从传感器接收到的字节数据，不包括 CRC 部分
    :return: 解析得到的值
    """
    if len(response) >= 5:
        address = response[0]
        function_code = response[1]
        data_length = response[2]
        data_bytes = response[3:3 + data_length]
        # 检查数据长度是否正确
        if data_length == len(data_bytes):
            value = (data_bytes[0] * 256 + data_bytes[1])
            return value / 100  # 根据协议解析值
        else:
            print("数据长度不匹配")
    else:
        print("响应数据过短")


# 循环发送和接收数据的主函数

def read_data(port='COM8', baudrate=9600):
    start_time = datetime.now()  # 记录发送时间
    # 获取风速数据
    wind_response = send_and_receive_hex_data(port, baudrate, wind_speed_cmd)
    wind_speed = parse_weather_data(wind_response) if wind_response else None

    # 获取降雨量数据
    rainfall_response = send_and_receive_hex_data(port, baudrate, rainfall_cmd)
    rainfall = parse_weather_data(rainfall_response) if rainfall_response else None

    # 获取温度数据
    temperature_response = send_and_receive_hex_data(port, baudrate, temperature_cmd)
    temperature = parse_weather_data(temperature_response) if temperature_response else None

    # 获取气压数据
    pressure_response = send_and_receive_hex_data(port, baudrate, pressure_cmd)
    pressure = parse_weather_data(pressure_response) if pressure_response else None

    # 获取湿度数据
    humidity_response = send_and_receive_hex_data(port, baudrate, humidity_cmd)
    humidity = parse_weather_data(humidity_response) if humidity_response else None

    # 获取风向数据
    wind_direction_response = send_and_receive_hex_data(port, baudrate, wind_direction_cmd)
    wind_direction = parse_weather_data(wind_direction_response) if wind_direction_response else None

    end_time = datetime.now()  # 记录回传时间
    elapsed_time = (end_time - start_time).total_seconds()
    local_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

    # 打印数据
    print(f"风速: {wind_speed} m/s, 降雨量: {rainfall} mm, 温度: {temperature} °C")
    print(f"气压: {pressure} hPa, 湿度: {humidity} %, 风向: {wind_direction}°")
    print(f"数据回传时间: {elapsed_time} 秒, 本地时间: {local_time}")

    return wind_speed, rainfall, temperature, pressure, humidity, wind_direction, local_time
