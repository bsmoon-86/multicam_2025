import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import os

# 1. 데이터 로드
# data 폴더 내의 parkinsons.csv 파일을 읽어옵니다.
data_path = os.path.join('data', 'parkinsons.csv')

try:
    df = pd.read_csv(data_path)
    
    # 2. 전처리
    # 'status' 컬럼은 파킨슨병 여부(1: 환자, 0: 정상)를 나타내는 타겟 데이터입니다.
    # 'name' 컬럼은 단순 식별자이므로 특징 데이터에서 제외합니다.
    X = df.drop(['status', 'name'], axis=1)
    y = df['status']

    # 3. 데이터셋 분할 (학습용 80%, 테스트용 20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 4. Pipeline 구성
    # 스케일러와 분류기를 하나로 묶습니다.
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(random_state=42))
    ])

    # 5. GridSearchCV를 위한 파라미터 그리드 설정
    # 파이프라인 내의 인자에 접근할 때는 '단계명__파라미터명' 형식을 사용합니다.
    param_grid = {
        'rf__n_estimators': [50, 100, 200],
        'rf__max_depth': [None, 10, 20],
        'rf__min_samples_split': [2, 5, 10]
    }

    # 6. 교차 검증 및 그리드 서치 수행
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid_search = GridSearchCV(pipeline, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
    
    print("최적의 파라미터를 찾는 중입니다... (시간이 소요될 수 있습니다)")
    grid_search.fit(X_train, y_train)

    # 7. 최적의 모델 평가
    print(f"최적 파라미터: {grid_search.best_params_}")
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    print(f"\n최종 모델 정확도: {accuracy_score(y_test, y_pred):.4f}")
    print("\n상세 분류 보고서:\n", classification_report(y_test, y_pred))
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {data_path}. 파일명이나 경로가 정확한지 확인해 주세요.")