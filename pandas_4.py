import streamlit
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('WebAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import datetime
import PyQt5




"""데이터 불러오기"""
# try = iferror

try :
    """실적 데이터 가져오기 trade_performance.csv
    마스터 데이터 국가코드 국가명 country_master.csv"""
    df_perf = pd.read_csv("./trade_performance.csv", encoding="cp949")
    df_master = pd.read_csv("./country_master.csv", encoding="cp949")

except FileNotFoundError : 
    print("❌ CSV파일이 없습니다. 경로를 다시 확인해주세요.")
    exit()

# print(df_perf)
# print(df_master)



"""1. 데이터 통합 (Merge), 엑셀의 vlookup과 같음"""
df = pd.merge(df_perf, df_master, on="ctry_code", how="left")
# on => 어떤 데이터를 가져올건데?
# how => df_perf, df_master 중에 왼쪽에 기준을 두겠다
# print(df)



"""2. 대륙별 성과 분석 총 수출액 수입 합계 (Aggregation)"""
continent_states = df.groupby("continent")[["export_val","import_val"]].sum()
# -> 각각 그룹을 만들고, 각각의 합계를 구함, 엑셀의 부분합과 같음!
print(continent_states)



"""무역수지 계산 수출-수입 (Groupby)"""
continent_states["무역수지"] = continent_states["export_val"] - continent_states["import_val"]

print("---------- 🌐 대륙별 무역 성과 요약 🌐 ----------")
print(continent_states)

"""품목별 집중도 분석(Filtering)"""
best_conitent = continent_states["무역수지"].idxmax()
print(f"분석 결과 : {best_conitent} 대륙과의 거래에서 가장 큰 무역 수지 흑자가 발생했습니다.")



"""FTA 효과분석 : 평균 수출 단가(수출금액/중량)"""
df["평균수출단가"] = df["export_val"] / df["weight"]

"""FTA 여부에 따른 평균 단가 비교"""
fta_ans = df.groupby("fta_status")["평균수출단가"].mean()
# groupby

print("\n FTA 여부에 따른 평균 수출 단가 비교")
print(fta_ans)


"""시사점 도출"""
if fta_ans["Y"] > fta_ans["N"] :
    print("결과 : FTA 체결 국가의 평균 단가가 더 높게 나타나며 수출 경쟁력이 수치로 증명되었음")
else :
    print("결과 : FTA 체결 국가의 평균 단가가 미 체결 국가 간의 단가 차이에 대한 추가 분석이 필요함")



"""5. 품목별 집중도 분석. 수출 금액이 가장 큰 상위 2개 추출"""
top2_hs = df.groupby("hs_code")["export_val"].sum().nlargest(2).index.tolist()

print(f"\n수출 상위 2개 품목 : {top2_hs}")



"""해당 품목들의 국가별 수출 현황"""
top2_df = df[df["hs_code"].isin(top2_hs)]
country_focus = top2_df.groupby(["hs_code","ctry_name"])["export_val"].sum().reset_index()
print(country_focus)


"""날짜 데이터 월 정보 추출"""
df["ymd"] = pd.to_datetime(df["ymd"])
df["month"] = df["ymd"].dt.month
print(df.head())



"""시각화. 월별 수출입 추이 데이터 생성"""
monthly = df.groupby("month")[["export_val","import_val"]].sum()
plt.figure(figsize=(12,6))
plt.plot(monthly.index, monthly["export_val"], label="수출액")
plt.plot(monthly.index, monthly["import_val"], label="수입액")

plt.title("월별 수출입 실적 추이")
plt.xlabel("월(month)")
plt.ylabel("금액")
plt.show()


