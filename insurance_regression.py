import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# ==========================================
# 1. 데이터 로드 및 전처리
# ==========================================
# 데이터 불러오기 (경로는 환경에 맞춰 수정하세요)
df = pd.read_csv('data/insurance.csv')

# 범주형 데이터 처리 (One-hot Encoding)
# sex, smoker, region 컬럼을 숫자로 변환합니다.
df_encoded = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

# 특징(X)과 타겟(y) 분리
X = df_encoded.drop('charges', axis=1)
y = df_encoded['charges']

# 학습 데이터와 테스트 데이터 분리 (8:2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 데이터 스케일링 (특징 값들의 범위를 맞춤)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# PyTorch 텐서로 변환
# 회귀 문제이므로 y값도 float32이며, (N, 1) 형태로 맞춰야 합니다.
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)

X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

# ==========================================
# 2. MLP 모델 정의
# ==========================================
input_size = X_train_tensor.shape[1] # 입력 피처 수

model = nn.Sequential(
    nn.Linear(input_size, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 1) # 마지막 출력은 1개 (예측 비용)
)

# 손실 함수 (MSE) 및 옵티마이저 (Adam)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# ==========================================
# 3. 모델 학습
# ==========================================
epochs = 200
print("보험료 예측 모델 학습을 시작합니다...")

for epoch in range(epochs):
    model.train()
    
    optimizer.zero_grad()
    predictions = model(X_train_tensor)
    loss = criterion(predictions, y_train_tensor)
    
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 50 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss(MSE): {loss.item():.4f}")

# ==========================================
# 4. 모델 평가
# ==========================================
model.eval()
with torch.no_grad():
    test_preds = model(X_test_tensor)
    test_loss = criterion(test_preds, y_test_tensor)
    
    # R2 Score 계산 (회귀 모델의 성능 지표)
    r2 = r2_score(y_test_tensor.numpy(), test_preds.numpy())
    
    print("-" * 30)
    print(f"테스트 손실(MSE): {test_loss.item():.4f}")
    print(f"결정계수 (R2 Score): {r2:.4f}") # 1에 가까울수록 정확함

print("예측 예시 (첫 번째 데이터):")
print(f"실제값: {y_test.values[0]:.2f} / 예측값: {test_preds[0].item():.2f}")