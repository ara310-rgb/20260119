# import streamlit as st
import pandas as pd
import numpy as np


trade = pd.read_csv("./raw_trade_data.csv", encoding="utf-8")
# print(trade)
# print(trade.info())


"""1. HS CODE 85 시작 찾기"""
cond_hs = trade["hs_code"].astype(str).str.startswith("85")
"""trade가 갖고 있는 [열=series]
모든 필드중에 필드명 hs code를 찾아서 문자로 바꾼 다음 숫자 85를 찾아라"""
# print(cond_hs)


"""2. 미국, 베트남 국가명 가져오기"""
cond_country = trade["국가명"].isin(["미국","베트남"])


# print(cond_country) # -> 미국, 베트남이 T,F로 보임


"""3. 수출 금액이 0원인 데이터를 제외"""
cond_value = trade["수출금액"] > 0
# print(trade.head(10))
# print(cond_value) # -> 결과 값이 T,F로 보임


# """4. 결합"""
# step1 = trade[cond_hs]
# step2 = step1[cond_country]
step3 = trade[cond_hs & cond_country & cond_value]

# print(f"------------------------------ 🙋 상위 10개 확인 -----------------------------")
# print(step3.head(10))

# trade.to_csv("저장할 파일명.csv", encoding="utf-8")



"""🚀 2번 문제 전처리 과정 클렌징 및 정규화"""
"""1. 중량 컬럼 결측치 처리"""
print(trade.head(15))
hs_mean = trade.groupby("hs_code")["중량"].mean()
# groupby -> hs코드가 같은것 끼리 묶어줌
# mean -> 평균을 구해줌
# print(hs_mean)

# for 변수 in 자료구조(dict,list 등) : 
for hs in hs_mean.index :
    """1)현재 순서의 HS코드에 해당하는 평균값을 가져오기"""
    avg_val1 = hs_mean[hs]
    """2)원본 데이터에서 해당 HS코드이면서 중량이 비어있는 행만 찾기"""
    target = (trade["hs_code"] == hs) & (trade["중량"].isna())
    """3)해당되는 칸에만 평균값을 대입"""
    trade.loc[target,"중량"] = avg_val1

# trade.loc[trade["중량"].isna()] == 0

# """수출입구분 컬럼의 데이터가 영문으로 되어 있다면 수출,수입으로 변경"""
trade.loc[trade["수출입구분"] == "Export", "수출입구분"] = "수출"
trade.loc[trade["수출입구분"] == "import", "수출입구분"] = "수입"
# loc : 행을 찾고 어느 열의 데이터를 수정할거니?
# iloc : 행을 찾고 index 번호를 찾는것



"""3.수출금액 단위 변환 원 -> 백만달러   (금액/1470)/1000000 새컬럼 만들기"""
exchange_rate = 1470
trade["수출금액_M_USD"] = (trade["수출금액"]/exchange_rate)/1000000
# -> 새로 만든 필드명["수출금액_M_USD"]은 = (수출금액/1470)/1000000 이다



"""4. 데이터 타입 최종 확인"""
print("\n ---- [최종 데이터 확인] -----")
print(trade.dtypes)

print("\n ---- [클렌징 결과 샘플 확인] -----")
print(trade[["날짜","hs_code","수출입구분","수출금액_M_USD"]].head())
# -> 필드 여러개 갖고올 때에는 이중괄호! [[]]

# 최종데이터 저장 cleaned_trade_data
trade.to_csv("./cleaned_trade_data.csv", encoding="utf-8", index=False)
print("과제2 완료 'cleaned_trade_data'이 저장되었습니다.")