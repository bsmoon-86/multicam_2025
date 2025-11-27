import pandas as pd

file_path = 'test/서울시 휴게음식점 인허가 정보.csv'

print("Attempting to read with cp949...")
try:
    df = pd.read_csv(file_path, encoding='cp949')
    print("Success with cp949")
except Exception as e:
    print(f"Failed with cp949: {e}")

print("\nAttempting to read with cp949 and errors='replace' using file handle...")
try:
    with open(file_path, 'r', encoding='cp949', errors='replace') as f:
        df = pd.read_csv(f)
    print("Success with cp949 and errors='replace'")
    print(df.head())
except Exception as e:
    print(f"Failed with cp949 and errors='replace': {e}")

print("\nAttempting to read with euc-kr...")
try:
    df = pd.read_csv(file_path, encoding='euc-kr')
    print("Success with euc-kr")
except Exception as e:
    print(f"Failed with euc-kr: {e}")
