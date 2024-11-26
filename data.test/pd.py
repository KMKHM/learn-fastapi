import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 목데이터 생성
def generate_mock_data(start_date, end_date, freq='ME'):
    """시계열 목데이터 생성"""
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    values = np.random.randint(100, 1000, size=len(date_range))
    data = pd.DataFrame({'timestamp': date_range, 'value': values})
    return data

# 목데이터 생성 (월별 데이터)
mock_data = generate_mock_data('2020-01-01', '2024-12-31')

# 데이터 확인
print(mock_data.head())

# 데이터 시각화
plt.figure(figsize=(12, 6))
plt.plot(mock_data['timestamp'], mock_data['value'], label='Monthly Value', marker='o')
plt.title('Simulated Monthly Time Series Data')
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.grid()
plt.legend()
plt.show()
