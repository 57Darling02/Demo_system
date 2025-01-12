# data_preprocessing.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import 开发片段_古


def preprocess_data(csv_path, time_step=10, pred_step=3, train_size=0.6, random_state=42):
    # 读取 CSV 文件，只选择必要的列
    df = pd.read_csv(csv_path,usecols=['monitor_id', 'collect_time', 'wind_speed', 'humidity', 'rainfall', 'air_temperature'])
    # 去除任何存在缺失值的行
    df = df.dropna(axis=0, how='any')

    # 将数据按 monitor_id 和 collect_time 进行排序（确保时间顺序）
    df['collect_time'] = pd.to_datetime(df['collect_time'])
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


if __name__ == "__main__":
    preprocess_data(csv_path='./example2.csv')