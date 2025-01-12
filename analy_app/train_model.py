# train_model.py

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import pickle


# 定义 LSTMModel 类
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


def set_loader(x, y, batch_size):
    tensor_x = torch.from_numpy(x.astype(np.float32))
    tensor_y = torch.from_numpy(y.astype(np.float32))
    loader = DataLoader(TensorDataset(tensor_x, tensor_y), batch_size=batch_size, shuffle=True)
    return loader


def lstm_train(model, epochs, train_loader, val_loader, learning_rate=0.01, plot_loss=False):
    loss_function = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    train_losses = []
    val_losses = []

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for x_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = loss_function(outputs, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * x_batch.size(0)

        train_loss /= len(train_loader.dataset)
        train_losses.append(train_loss)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                outputs = model(x)
                loss = loss_function(outputs, y)
                val_loss += loss.item() * x.size(0)
        val_loss /= len(val_loader.dataset)
        val_losses.append(val_loss)

        print(f'Epoch [{epoch + 1}/{epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

    if plot_loss:
        plt.figure(figsize=[8, 6])
        plt.plot(train_losses, 'b', label='Train Loss')
        plt.plot(val_losses, 'r', label='Val Loss')
        plt.legend()
        plt.title(f'Epochs: {epochs}  Learning Rate: {learning_rate}')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.grid(True)
        plt.show()

    return model


def main():
    # 加载预处理后的数据和 scaler
    train_x = np.load('train_x.npy')
    train_y = np.load('train_y.npy')
    val_x = np.load('val_x.npy')
    val_y = np.load('val_y.npy')

    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # 设置超参数
    hidden_size = 16
    input_size = 3
    output_size = 3
    batch_size = 16
    epochs = 500
    learning_rate = 0.001

    # 准备数据加载器
    train_loader = set_loader(train_x, train_y, batch_size)
    val_loader = set_loader(val_x, val_y, batch_size)

    print(f"Number of training batches: {len(train_loader)}")
    print(f"Number of validation batches: {len(val_loader)}")

    # 初始化模型
    model = LSTMModel(input_size=input_size, hidden_size=hidden_size, output_size=output_size, num_layers=1,
                      dropout_rate=0.2)

    # 训练模型
    model = lstm_train(model, epochs=epochs, train_loader=train_loader, val_loader=val_loader,
                       learning_rate=learning_rate, plot_loss=True)

    # 保存训练好的模型
    torch.save(model.state_dict(), 'trained_model.pth')
    print("Model training completed and saved as 'trained_model.pth'.")


if __name__ == "__main__":
    main()