print("\n -------- 과제 2 시작 데이터 클렌징 및 정규화")
data = pd.read_csv("raw_trade_data.csv", encoding="cp949")

# 1. 평균 HS코드 별 중량의 평균을 계산
hs_mean=data.groupby("hs")["중량"].mean()
