import numpy as np
import matplotlib.pyplot as plt

# 중심극한정리 시뮬레이션 함수
def central_limit_theorem_demo(sample_size=30, num_samples=1000000):
    """
    중심극한정리 시뮬레이션
    - sample_size: 각 샘플의 크기
    - num_samples: 샘플링 횟수
    """
    # 원래 분포 (균등분포에서 샘플링)
    population = np.random.uniform(low=0, high=10, size=100000)
    
    # 샘플 평균 저장 리스트
    sample_means = []

    # 여러 번 샘플링하여 평균 계산
    for _ in range(num_samples):
        sample = np.random.choice(population, size=sample_size, replace=False)
        sample_mean = np.mean(sample)
        sample_means.append(sample_mean)

    # 샘플 평균의 분포 시각화
    plt.figure(figsize=(12, 6))

    # 원래 분포 시각화
    plt.subplot(1, 2, 1)
    plt.hist(population, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title("Original Population Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    # 샘플 평균 분포 시각화
    plt.subplot(1, 2, 2)
    plt.hist(sample_means, bins=30, color='lightgreen', edgecolor='black', alpha=0.7)
    plt.title(f"Distribution of Sample Means (n={sample_size})")
    plt.xlabel("Sample Mean")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

# 실행
central_limit_theorem_demo(sample_size=30, num_samples=1000000)
