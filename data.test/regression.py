import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 목데이터 생성
def generate_mock_data(start_date, end_date, freq='ME'):
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    values = np.random.randint(100, 1000, size=len(date_range))
    data = pd.DataFrame({'timestamp': date_range, 'value': values})
    return data

# 목데이터 생성
mock_data = generate_mock_data('2020-01-01', '2024-12-31')

print(mock_data)