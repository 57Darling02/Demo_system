from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import pickle
from ResourcePool import resource_pool
# 定义长短期网络模型
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=1, dropout_rate=0.2):
        super(LSTMModel, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc1 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.dropout(out[:, -1, :])
        out = self.fc1(out)
        out = self.relu(out)
        return out

def preprocess_data(time_step=10, pred_step=3, train_size=0.6, random_state=42):
    # 读取 CSV 文件，只选择必要的列
    df = resource_pool.get_detected_data()
    # 去除任何存在缺失值的行
    df = df.dropna(axis=0, how='any')

    df = df.sort_values(by=['monitor_id', 'collect_time'])

    # 获取所有 monitor_id 和时间的唯一值
    monitor_ids = df['monitor_id'].unique()
    times = df['collect_time'].unique()

    # 初始化一个空列表用于存储最终数据
    dataset = []

    # 遍历每个 monitor_id
    for monitor in monitor_ids:
        monitor_data = df[df['monitor_id'] == monitor].sort_values(by='collect_time')
        features = monitor_data[['wind_speed', 'humidity', 'rainfall', 'air_temperature']].values

        # 将缺失的时间点补充为 NaN
        full_features = []
        for t in times:
            time_data = monitor_data[monitor_data['collect_time'] == t]
            if time_data.empty:
                full_features.append([np.nan] * 4)
            else:
                full_features.append(time_data[['wind_speed', 'humidity', 'rainfall', 'air_temperature']].values[0])

        dataset.append(full_features)

    # 转换为 NumPy 数组，形状为 (monitor, time, feature)
    dataset = np.array(dataset, dtype=float)
    print(f"Original dataset shape: {dataset.shape}")

    # 确认 dataset 是三维的
    if len(dataset.shape) != 3:
        print("Error: dataset is not 3-dimensional")
        exit()

    # 处理 NaNs，填充 NaN 使用每个特征的均值
    feature_means = np.nanmean(dataset, axis=(0, 1))
    print(f"Feature means for filling NaNs: {feature_means}")

    # 替换 NaN 为对应特征的均值
    inds = np.where(np.isnan(dataset))
    dataset[inds] = np.take(feature_means, inds[2])

    # 确保所有 NaN 都被替换
    if np.isnan(dataset).any():
        print("Warning: There are still NaN values in the dataset after filling.")
    else:
        print("All NaN values have been filled.")

    # 使用最近 10 个时刻的数据来预测未来 3 个时刻的 air_temperature
    samples_x = []
    samples_y = []

    for i in range(dataset.shape[1] - time_step - pred_step + 1):
        samples_x.append(dataset[:, i:i + time_step, [0, 1, 2]])  # 风速、湿度、降水量
        samples_y.append(dataset[:, i + time_step:i + time_step + pred_step, 3])  # air_temperature

    # 转换为 NumPy 数组并转置
    X = np.array(samples_x).transpose(0, 2, 1, 3)
    Y = np.array(samples_y).transpose(0, 2, 1)

    print(f"X shape after transposing: {X.shape}")
    print(f"Y shape after transposing: {Y.shape}")

    # 扁平化数据以适配模型输入
    samples_x = X.reshape(-1, time_step, 3)
    samples_y = Y.reshape(-1, pred_step)

    print(f"samples_x shape after reshaping: {samples_x.shape}")
    print(f"samples_y shape after reshaping: {samples_y.shape}")

    # 数据归一化：对特征 (samples_x) 进行归一化
    scaler = StandardScaler()
    samples_x_reshaped = samples_x.reshape(-1, 3)
    samples_x_scaled = scaler.fit_transform(samples_x_reshaped)
    samples_x_scaled = samples_x_scaled.reshape(-1, time_step, 3)

    print(f"samples_x_scaled shape after scaling: {samples_x_scaled.shape}")

    # 拆分数据集：训练集、验证集、测试集
    train_x, tmp_x, train_y, tmp_y = train_test_split(samples_x_scaled, samples_y, train_size=train_size,
                                                      random_state=random_state, shuffle=True)
    val_x, test_x, val_y, test_y = train_test_split(tmp_x, tmp_y, train_size=0.5, random_state=random_state,
                                                    shuffle=True)

    print(f"train_x shape: {train_x.shape}, train_y shape: {train_y.shape}")
    print(f"val_x shape: {val_x.shape}, val_y shape: {val_y.shape}")
    print(f"test_x shape: {test_x.shape}, test_y shape: {test_y.shape}")

    # 保存处理后的数据和 scaler
    np.save('train_x.npy', train_x)
    np.save('train_y.npy', train_y)
    np.save('val_x.npy', val_x)
    np.save('val_y.npy', val_y)
    np.save('test_x.npy', test_x)
    np.save('test_y.npy', test_y)

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print("Data preprocessing completed and files saved.")











# ---------------------------- 数据准备部分 ----------------------------





def prepare_latest_data(scaler, time_step=10, monitor_id=None,p_type='wind_speed'):
    """
    准备最新的时间步数据用于预测
    参数:
    -----
    api_data: 从 API 获取的原始数据
    scaler: 训练时使用的 StandardScaler
    time_step: 输入时间步长
    pred_step: 预测时间步长
    monitor_id: 指定的 monitor_id，如果为 None，则选择第一个
    返回:
    -----
    latest_features_tensor: 归一化后的输入特征张量
    """

    data = resource_pool.get_detected_data()
    # 确保包含必要的列
    required_columns = ['monitor_id', 'collect_time', 'wind_speed', 'humidity', 'rainfall', 'air_temperature']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Data does not contain all required columns: {required_columns}")

    # 确保数据按时间排序
    data = data.sort_values(by=['monitor_id', 'collect_time'])

    # 获取所有 monitor_id
    monitor_ids = data['monitor_id'].unique()

    if monitor_id is None:
        monitor_id = monitor_ids[0]  # 默认选择第一个 monitor_id

    print(f"Selected monitor_id for prediction: {monitor_id}")

    # 过滤指定 monitor_id 的数据
    monitor_data = data[data['monitor_id'] == monitor_id].sort_values(by='collect_time')

    # 筛选 air_temperature 小于 10 的行
    # monitor_data = monitor_data[monitor_data['air_temperature'] < 10]
    # print(f"Monitor data shape after filtering air_temperature < 10: {monitor_data.shape}")
    # if monitor_data.empty:
    #     raise ValueError(f"No data for monitor_id {monitor_id} after filtering  < 10.")

    # 提取特征列
    if p_type == 'wind_speed':
        features = monitor_data[['humidity', 'rainfall', 'air_temperature']].values  # 不包括 wind_speed 作为特征
        wind_speeds = monitor_data['wind_speed'].values
    else:
        features = monitor_data[['wind_speed', 'humidity', 'rainfall']].values
        air_temps = monitor_data['air_temperature'].values

    # 检查是否有足够的数据
    if len(features) < time_step:
        raise ValueError(f"Monitor ID {monitor_id} 的数据不足 {time_step} 个时间步。")

    # 取最新的 time_step 个特征
    latest_features = features[-time_step:]

    print(f"Latest features shape: {latest_features.shape}")
    print("Latest features:")
    print(latest_features)

    # 归一化
    latest_features_scaled = scaler.transform(latest_features)
    latest_features_scaled = latest_features_scaled.reshape(1, time_step, 3)

    # 转换为张量
    latest_features_tensor = torch.from_numpy(latest_features_scaled.astype(np.float32))

    return latest_features_tensor

# ---------------------------- 预测函数部分 ----------------------------

def predict(time_step=10, pred_step=3, monitor_id=None,p_type='wind_speed'):
    if p_type == 'wind_speed':
        try:
            with open('wind_scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Scaler file 'wind_scaler.pkl' not found.")
    elif p_type == 'air_temperature':
        try:
            with open('temp_scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Scaler file 'temp_scaler.pkl' not found.")

    # 获取所有检测到的数据
    latest_input = prepare_latest_data(scaler=scaler, time_step=time_step, monitor_id=monitor_id,p_type=p_type)
    # 加载训练好的模型
    hidden_size = 16
    input_size = 3
    output_size = pred_step  # 预测未来3个
    num_layers = 1
    dropout_rate = 0.2
    model = LSTMModel(input_size=input_size, hidden_size=hidden_size, output_size=output_size, num_layers=num_layers,
                      dropout_rate=dropout_rate)
    try:
        model.load_state_dict(torch.load('temp_model.pth', map_location=torch.device('cpu')))
    except FileNotFoundError:
        raise FileNotFoundError("Trained model file 'temp_model.pth' not found.")
    model.eval()

    # 进行预测
    with torch.no_grad():
        predicted = model(latest_input)  # 输出形状: (1, pred_step)
        predicted = predicted.numpy().flatten()

    predicted_list = predicted.tolist()
    rounded_list = []
    for num in predicted_list:
        # 使用 round 函数将 num 精确到两位小数
        rounded_num = round(num, 2)
        rounded_list.append(rounded_num)
    return rounded_list

# ---------------------------- 主函数部分 ----------------------------

def main():
    try:
        predicted_wind_speeds = predict(p_type='air_temperature')
        print(f"预测的未来 3 个 wind_speed 值: {predicted_wind_speeds}")
    except Exception as e:
        print(f"预测过程中发生错误: {e}")


if __name__ == "__main__":
    main()