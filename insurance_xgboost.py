import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import os

# 1. 데이터 로드
data_path = os.path.join('data', 'insurance.csv')
df = pd.read_csv(data_path)

# 2. 범주형 데이터 전처리 (Pandas get_dummies 사용)
# sex, smoker, region 컬럼을 원-핫 인코딩합니다.
df_encoded = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

# 3. 특징(X)과 타겟(y) 분리
X = df_encoded.drop('charges', axis=1)
y = df_encoded['charges']

# 4. 전체 파이프라인 구성 (스케일링 + XGBoost)
# get_dummies로 수치화된 전체 특징값들을 StandardScaler로 표준화합니다.
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('xgb', XGBRegressor(random_state=42))
])

# 5. GridSearchCV를 위한 하이퍼파라미터 설정
# 파이프라인 내 XGBoost 인자에 접근하기 위해 'xgb__' 접두사를 사용합니다.
param_grid = {
    'xgb__n_estimators': [100, 200, 300],
    'xgb__max_depth': [3, 4, 5],
    'xgb__learning_rate': [0.01, 0.05, 0.1],
    'xgb__subsample': [0.8, 0.9,1.0]
}

# 6. 교차 검증(KFold) 및 학습
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5-Fold 교차 검증 설정
kf = KFold(n_splits=5, shuffle=True, random_state=42)

grid_search = GridSearchCV(pipeline, param_grid, cv=kf, scoring='r2', n_jobs=-1, verbose=1)

print("최적의 파라미터를 탐색하며 모델을 학습 중입니다...")
grid_search.fit(X_train, y_train)

# 7. 결과 확인 및 평가
print(f"최적 하이퍼파라미터: {grid_search.best_params_}")

best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\n[모델 평가 결과]")
print(f"R2 Score (결정계수): {r2_score(y_test, y_pred):.4f}")
print(f"RMSE (평균 제곱근 오차): {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")