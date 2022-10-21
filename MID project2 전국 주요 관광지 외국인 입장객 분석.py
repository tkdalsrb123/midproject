#!/usr/bin/env python
# coding: utf-8

# # 전국 주요관광지 외국인 입장객 통계

# ## 파일 읽어오기

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import plotly.express as px


# In[8]:


import koreanize_matplotlib

# 그래프에 retina display 적용
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
# retina보다 svg가 훨씬 선명하게 보인다


# In[9]:


pd.Series([1,-3,5,-7,9]).plot(title='한글', figsize=(6,1))
# 마이너스 값도 잘 표시되는지 체크
# 한글이 깨지지 않는지 체크


# In[10]:


glob("*입장객*.xls")


# In[11]:


df19 = pd.read_excel("2019년 주요관광지점 입장객통계(전국).xls", header=1)


# In[12]:


df19


# In[13]:


df18 = pd.read_excel("2018년 주요관광지점 입장객통계(전국).xls", header=1)
df18


# ## 데이터 미리보기

# ### 요약정보 확인

# In[14]:


# (행, 열)정보를 확인합니다.

df19.shape


# In[15]:


# 데이터의 요약정보를 확인합니다.

df19.info()


# ### 결측치 확인

# In[16]:


# 결측치를 확인합니다.

df19.isnull().sum()


# In[17]:


# 결측치를 시각화하여 위치를 파악합니다.

sns.heatmap(df19.isna(), cmap='Greys')


# ## 데이터 전처리(1) 19년도

# ### 컬럼명 변경

# In[18]:


# 변경이 필요한 컬럼명을 확인합니다.

df19.columns


# In[19]:


# 로데이터에 근거해 unnamed 컬럼의 컬럼명을 바꿔줍니다.

df19 = df19.rename(columns={'Unnamed: 0':'시도','Unnamed: 1':'군구','Unnamed: 2':'관광지명','Unnamed: 3':'내/외국인','Unnamed: 4':'총계'})
df19


# ### 불필요한 컬럼 삭제

# In[20]:


# 불필요한 컬럼을 삭제합니다.

df19 = df19.drop(['총계', '인원계'], axis=1)


# In[21]:


df19.head(2)


# ### tidy data만들기

# In[22]:


# melt를 활용해 long form 형태로 데이터를 만들어줍니다.
# 어떤 variable과 value가 나오는지 확인합니다.

pd.melt(df19, id_vars=['시도', '군구', '관광지명', '내/외국인'])


# In[23]:


#위에서 확인한 var, value에 알맞은 컬럼명을 지정해줍니다.

df19 = pd.melt(df19, id_vars=['시도', '군구', '관광지명', '내/외국인'], var_name='연도월', value_name='입장객수')
df19.head(3)


# ### 불필요한 행 제거하기

# In[24]:


# 내/외국인 컬럼 중 값이 합계인 행을 모두 제거합니다.

sights19 = df19.loc[~(df19['내/외국인']=='합계')]
sights19


# In[25]:


# 최종 데이터셋의 정보를 확인합니다.

sights19.info()


# In[26]:


sights19.shape


# In[27]:


sights19.isnull().sum()


# In[28]:


sights19.to_csv("19년도 전국 주요 관광지 별 외국인 입장객.csv", index=False)


# ## 데이터 전처리(2) 18년도

# ### 컬럼명 변경

# In[29]:


# 변경이 필요한 컬럼명을 확인합니다.

df18.columns


# In[30]:


# 로데이터에 근거에 컬럼명을 변경해줍니다.

df18 = df18.rename(columns={'Unnamed: 0':'시도', 'Unnamed: 1':'군구', 'Unnamed: 2':'관광지명', 
                     'Unnamed: 3':'유료/무료', 'Unnamed: 4':'세부구분',
       'Unnamed: 5':'내/외국인', 'Unnamed: 6':'총계'})


# In[31]:


# 변경된 결과를 확인합니다.

df18.tail(2)


# ### 불필요한 컬럼 삭제

# In[32]:


# 불필요한 컬럼을 삭제합니다.

df18 = df18.drop(['세부구분','총계', '인원계'], axis=1)


# In[33]:


# 삭제한 결과를 확인합니다.

df18.columns


# ### tidy data 만들기

# In[34]:


# melt를 활용해 long form 형태로 데이터를 만들어줍니다.
# 어떤 variable과 value가 나오는지 확인합니다.

pd.melt(df18, id_vars=['시도', '군구', '관광지명', '유료/무료', '내/외국인'])


# In[35]:


# var과 value값에 적절한 컬럼명을 지정해줍니다.

df18 = pd.melt(df18, id_vars=['시도', '군구', '관광지명', '유료/무료', '내/외국인'], var_name='연도월', value_name='입장객수')
df18.head(3)


# ### 불필요한 행 제거하기

# In[36]:


# 내/외국인 컬럼 중 값이 합계인 행을 모두 제거합니다.

sights18 = df18.loc[~(df18['내/외국인']=='합계')]
sights18


# In[37]:


# 최종 데이터셋의 정보를 확인합니다.

sights18.info()


# In[38]:


sights18.shape


# In[39]:


sights18.isna().sum()


# In[72]:


sights18.to_csv("18년도 전국 주요 관광지 별 외국인 입장객.csv", index=False)


# ## concat으로 데이터 합치기

# In[40]:


# 18년도 데이터와 19년도 데이터를 하나의 데이터셋으로 합쳐줍니다.
sights = pd.concat([sights18,sights19], axis=0)


# In[41]:


sights


# In[42]:


# 병합된 데이터셋의 결측치를 확인합니다.

sights.isnull().sum()


# In[43]:


# 중복값은 없는지 확인합니다.

sights[sights.duplicated()]


# ## 병합된 데이터의 기술통계 및 요약정보 확인하기

# In[44]:


# 기술통계를 확인합니다.

sights.describe()


# In[45]:


# 요약정보를 확인합니다.

sights.info()


# ## 분석 및 시각화

# ### 데이터 타입 변환하기

# In[46]:


# 입장객수 컬럼의 값을 확인합니다.

sights['입장객수']


# In[47]:


# 입장객수 컬럼을 데이터 분석에 적합한 수치 데이터로 변환합니다.
#그러나 결측치가 섞여있을 때는 astype()으로 제대로 변환되지 않으므로 pd.to_numeric으로 변환합니다.
# errors='coerce'로 지정하여 결측값은 강제로 변환합니다.

sights['입장객수'] = pd.to_numeric(sights['입장객수'], errors='coerce')


# In[48]:


# sample 데이터를 뽑아 확인합니다.

sights.sample(5)


# ### 연도 파생변수 생성하기

# In[49]:


# 연도별 비교를 위해 연도월 컬럼에서 파생변수를 생성해줍니다.

sights['연도'] = sights['연도월'].str[:4]
sights.head(2)


# ### 내국인 데이터 지우기

# In[50]:


# 내국인과 외국인의 입장객수의 차이로 시각화 비교가 어렵습니다.
# 내국인 데이터를 삭제하고 확인해줍니다.

sights = sights.loc[(sights['내/외국인']=='외국인')]
sights.sample(5)


# In[51]:


# 내/외국인 분류 컬럼은 불필요해졌으므로 삭제해줍니다.

sights.drop(columns='내/외국인', inplace=True)


# In[52]:


sights


# In[53]:


sights.shape


# In[73]:


sights.to_csv("18-19년도 전국 주요 관광지 별 외국인 입장객 병합.csv", index=False)


# ### 시각화하기

# In[54]:


sights


# #### 18~19년 간 시도별 외국인 관광객 입장객 수

# In[55]:


# 18~19년 간 시도별 외국인 관광객 입장객 수 비교

sights.groupby(["시도", '연도'])["입장객수"].sum().unstack().plot(kind='bar', figsize=(12,6), rot=310, title='시도별 외국인 관광객 입장객 수')


# * 18년과 19년 모두 경기도, 서울특별시, 강원도, 제주도 순으로 주요 관광지를 입장했다.
# * 경기도, 서울특별시, 제주도의 주요 관광지는 18년에 비해 19년에 더 많은 외국인 관광객이 입장하였다.19년 방한객 인원이 18년보다 많아 전반적으로 각 지자체별 19년도 주요 관광객 외국인 입장객 수가 더 많은 것으로 해석할 수 있다.
# * 강원도는 근소한 차이로 18년에 더 많은 외국인들이 방문하였다.

# #### 전국단위 주요 관광지

# In[56]:


# 2018년~19년 누적 입장객수 높은 관광지

sights.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(
    kind='bar', figsize=(12,6), rot=310, title='전국단위 주요 관광지 top5', color='pink')


# #### 경기도 주요 군구

# In[57]:


# 경기도에서 관광지 입장객 수가 많은 주요 군구 TOP5를 알아보겠습니다.
# 경기도인 행만 호출하여 새로운 df를 만듭니다.

gyeonggi = sights.loc[sights['시도'] == '경기도']
gyeonggi


# In[58]:


# 연도별, 군구별 입장객수를 합하여 경기도 군구별 외국인 관광객 입장객수 top4를 확인합니다.

gyeonggi.groupby(['군구','연도'])['입장객수'].sum().unstack().plot(kind='bar', figsize=(12,6), rot=310, title='경기도 군구별 연도별 외국인 관광객 입장객 수')


# * 용인시 파주시, 고양시, 가평군 순으로 주요 관광지의 외국인 관광객 입장객 수가 많았다.

# #### 경기도 주요 관광지

# In[59]:


gyeonggi.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(
    kind='bar', figsize=(12,6), rot=310, title='경기도 주요 관광지 top5')


# #### 서울시 주요 군구

# In[60]:


seoul = sights.loc[sights['시도'] == '서울특별시']
seoul


# In[61]:


seoul.groupby(['군구','연도'])['입장객수'].sum().unstack().plot(kind='bar', figsize=(12,6), rot=310, title='서울 군구별 연도별 외국인 관광객 입장객 수')


# #### 서울시 주요 관광지

# In[62]:


seoul.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(
    kind='bar', figsize=(12,6), rot=310, title='서울 주요 관광지 top5')


# In[74]:


seoul.to_csv("서울시 주요 관광지 별 외국인 입장객.csv", index=False)


# #### 강원도 주요 군구

# In[63]:


gangwon = sights.loc[sights['시도'] == '강원도']
gangwon


# In[64]:


gangwon.groupby(['군구','연도'])['입장객수'].sum().unstack().plot(kind='bar', figsize=(12,6), rot=310, title='강원도 군구별 연도별 외국인 관광객 입장객 수')


# #### 강원도 주요 관광지

# In[65]:


gangwon.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(
    kind='bar', figsize=(12,6), rot=310, title='강원도 주요 관광지 top5')


# In[75]:


gangwon.to_csv("강원도 주요 관광지 별 외국인 입장객.csv", index=False)


# #### 제주도 주요 군구

# In[66]:


jeju = sights.loc[sights['시도'] == '제주특별자치도']
jeju


# In[67]:


jeju.groupby(['군구','연도'])['입장객수'].sum().unstack().plot(kind='bar', figsize=(12,6), rot=310, title='제주도 군구별 연도별 외국인 관광객 입장객 수')


# #### 제주도 주요 관광지

# In[68]:


jeju.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(
    kind='bar', figsize=(12,6), rot=310, title='제주도 주요 관광지 top5')


# In[76]:


jeju.to_csv("제주도 주요 관광지 별 외국인 입장객.csv", index=False)


# #### 유료/무료 관광지 입장객 수 비교

# In[69]:


print(plt.colormaps()) #컬러맵 골라쓰기


# In[70]:


sns.countplot(data=sights, x='유료/무료', palette='coolwarm')


# In[71]:


sns.barplot(data=sights, x='유료/무료', y='입장객수', estimator='sum', errorbar=None, palette='coolwarm')

