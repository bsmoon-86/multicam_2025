import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# ==========================================
# 1. 데이터 준비 및 텐서 변환
# ==========================================
# 데이터 불러오기 및 분리
df = pd.read_csv('data/parkinsons.csv')
X = df.drop(['name', 'status'], axis=1)
y = df['status']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 스케일링
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


print(X_train_scaled.shape)
print(X_test_scaled.shape)



# [핵심 변경점] DataLoader나 Dataset 객체를 만들지 않고 텐서만 준비합니다.
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)

X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

# [변경 포인트 2] 모델의 최종 출력 개수를 2개(정상 0, 파킨슨 1)로 변경
model = nn.Sequential(
    nn.Linear(22, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 2)  # <--- 원래 1이었던 것을 2로 변경!
)

# [변경 포인트 3] 손실 함수와 옵티마이저 변경
criterion = nn.CrossEntropyLoss() # <--- CrossEntropy로 변경
optimizer = optim.Adam(model.parameters(), lr=0.01, ) # <--- SGD로 변경 (관성 0.9 추가)

# ... (학습 코드는 기존과 100% 동일하게 유지) ...
print("모델 학습을 시작합니다...")

# 데이터를 쪼개지 않으므로, 에폭(반복 횟수)을 조금 더 늘려주는 것이 좋습니다.
epochs = 150 

for epoch in range(epochs):
    model.train()
    
    # [핵심 변경점] for batch in DataLoader: 형태의 반복문이 사라졌습니다!
    # 전체 훈련 데이터(X_train_tensor)를 한 번에 모델에 집어넣습니다.
    
    optimizer.zero_grad()                       # 1) 기울기 초기화
    predictions = model(X_train_tensor)         # 2) 전체 데이터로 예측
    loss = criterion(predictions, y_train_tensor) # 3) 전체 오차 계산
    loss.backward()                             # 4) 역전파
    optimizer.step()                            # 5) 가중치 업데이트
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
# [변경 포인트 4] 예측 시 Max(Argmax) 사용
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_tensor) # 모델이 (데이터 수, 2) 형태의 점수를 뱉어냄
    
    # torch.max는 (최댓값, 최댓값의 인덱스) 두 가지를 반환합니다.
    # 우리가 필요한 건 인덱스(0번이 컸냐, 1번이 컸냐)이므로 두 번째 값만 가져옵니다.
    _, predicted_classes = torch.max(test_outputs, dim=1) 
    
    accuracy = accuracy_score(y_test_tensor.numpy(), predicted_classes.numpy())
    print(f"SGD & CrossEntropy : {accuracy * 100}%")