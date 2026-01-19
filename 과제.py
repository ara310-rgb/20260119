import pandas as pd
# data = pd.read_csv("raw_trade_data.csv", encoding="utf-8")
data = pd.read_csv("raw_trade_data.csv", encoding="cp949")

# 과제 1: [실무형] 특정 품목의 수출입 현황 보고서 준비하기
# 시나리오: 여러분은 '반도체(HS코드 85)' 관련 무역 분석가입니다.
# 상사가 "최근 미국과 베트남의 반도체 수출 현황을 정리해달라"고 요청했습니다.

# 수행 단계:
# 전체 데이터에서 **HS코드 앞 2자리가 '85'**인 데이터만 추출하세요.
print("n -------- 과제 1 시작 반도체 수출 보고서 작성 --------")
# print(data.info())   # HS 코드가 숫자임을 확인 가능
cond_hs=data["hs_code"].astype(str).str.startswith("85")


# 그중 **국가명이 '미국' 혹은 '베트남'**인 데이터만 필터링하세요.
doble=data[["국가명"]]
country=doble[doble["국가명"].isin(['미국','베트남'])]


# 수출금액이 없는(0인) 데이터는 분석에서 제외하세요.
result_1=data["수출금액"] > 0

# 결과 데이터의 상위 10개를 출력하고, semiconductor_report.csv로 저장하세요.
step1=data[cond_hs]
step2=data[country]
step3=data[result_1]

print("상위 10개 데이터 확인")
print(step3.head(10))

step3.to_csv("raw_trade_data.csv",index=False)






