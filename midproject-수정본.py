import webbrowser
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import koreanize_matplotlib
import plotly.express as px

st.set_page_config(page_title='방한 외래관광객들을 위한 패키지 상품', page_icon='🛬', layout='wide')

tab1, tab2, tab3, tab4 = st.tabs(['2018-2019년도 방한 외래관광객들의 동향', '2018-2019년도 방한 외래관광객들의 소비', '최근 방한여행객 동향','방한 외래관광객 유치방안'])


with tab1:
    st.markdown('# 2018-2019년도 방한 외래관광객들의 동향')
    df_guk = pd.read_csv('data/국가별 방한외래 관광객.csv')
    df_guk = df_guk.drop('Unnamed: 0', axis=1)
    df_guk['기준연월'] = df_guk['기준연월'].astype('str')
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.subheader('방한 외래 관광객수 추이')
        option = st.multiselect('나라를 선택해주세요.', options=df_guk['국가명'].unique())
        df_guk_plot = df_guk.loc[df_guk['국가명'].isin(option)]
        fig = px.line(df_guk_plot, x='기준연월', y='value', color=df_guk_plot['국가명'])
        st.plotly_chart(fig)

    df_pur = pd.read_csv('data/외래관광객 방문목적.csv')
    df_p = df_pur.set_index('Unnamed: 0', drop=True)
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        country = st.selectbox('나라를 선택해주세요.', options= df_p.index)
        labels = ['여가, 위락, 휴식','사업 또는 전문 활동','교육 (어학 프로그램, 연수 등)','종교 및 순례','기타']
        st.subheader(f'{country}여행객들의 방문 목적')
        fig = px.pie(df_p, values = df_p.loc[country], names=labels)
        st.plotly_chart(fig)
    
    df_a = df_p.drop('전체')
    df_a = df_a.reset_index()
    df_a.rename({'Unnamed: 0':'나라명'}, axis=1, inplace=True)
    df_melt = df_a.melt(id_vars='나라명',var_name='방문목적', value_name='방문자수')
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.subheader('나라별 여행객들의 방문 목적')
        fig, ax = plt.subplots()
        sns.barplot(data=df_melt, x=df_melt['나라명'], y=df_melt['방문자수'], hue='방문목적')
        plt.xticks(rotation=60)
        st.pyplot(fig)
    
    df_re = pd.read_csv('data/지역별_추이.csv', encoding='cp949')
    df_re["기준년월"] = pd.to_datetime(df_re["기준년월"], format="%Y%m")
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.subheader('방한 외래 관광객 지역별 방문 추이')
        option_1 = st.multiselect('지역을 선택해주세요.', options=df_re['광역지자체'].unique())
        df_re_plot = df_re.loc[df_re['광역지자체'].isin(option_1)]
        fig_1 = px.line(df_re_plot, x='기준년월', y='방문자수', color=df_re_plot['광역지자체'])
        st.plotly_chart(fig_1)
    
    
    
with tab2:
    st.markdown('# 2018-2019년도 방한 외래관광객들의 소비')
    
    st.markdown('### 지역별 소비금액')
    df_consume = pd.read_csv('data/지역별소비.csv')
    df_consume_melt = df_consume.melt(id_vars='지자체',var_name='연도',value_name='소비금액')
    fig= plt.figure(figsize=(12,3))
    sns.barplot(data=df_consume_melt.sort_values('소비금액', ascending=False), x='지자체', y='소비금액', hue='연도')
    plt.xticks(rotation=60)
    st.pyplot(fig)
    st.markdown('외래 관광객의 지역별 소비금액을 시각화한 것으로 서울에 대부분의 소비가 몰려있는 것을 확인할 수가 있다.')
    
    st.markdown('### 나라별 관광 소비금액')
    df_coun_consume = pd.read_csv('data/나라별지출.csv')
    df_coun_melt = df_coun_consume.melt(id_vars = '국가',var_name='소비단위',value_name='소비인원')
    fig = plt.figure(figsize=(12,3))
    sns.barplot(data=df_coun_melt, x='국가', y='소비인원', hue='소비단위')
    plt.xticks(rotation=60)
    st.pyplot(fig)
    st.markdown('나라별 소비금액을 시각화한 것으로 중국과 일본의 소비가 제일 많으며 고액 소비는 중국이 90% 이상을 차지하고 있는것으로 보아 면세점, 백화점에서의 대부분 소비는 중국 관광객으로 보인다.')
    
    st.markdown('### 업종별 관광소비 금액')
    df_typeb = pd.read_csv('data/업종별소비.csv')
    df_typeb_melt = df_typeb.melt(id_vars = '업종',var_name='연도', value_name='소비금액')
    fig = plt.figure(figsize=(12,3))
    sns.barplot(data=df_typeb_melt.sort_values('소비금액',ascending=False), x='업종', y='소비금액', hue='연도')
    plt.xticks(rotation= 60)
    st.pyplot(fig)
    st.markdown('업종별 관광객들의 소비를 시각화한 것으로 호텔, 면세점, 백화점과 같은 고액 소비가 이루어지는곳이 외래 관광객들의 관광매출 대부분을 차지하는 것을 알 수가 있다.')
    
    cols = st.columns([0.15, 0.7, 0.15])
    with cols[1]:
        st.markdown('### 방문자수와 인당소비액 비교')
        fig, axe1 = plt.subplots(figsize=(10,10))
        axe2 = axe1.twinx()
        sns.barplot(ax = axe1, data=df_re, x="광역지자체", y="인당 소비액", ci=None, color='red')
        sns.lineplot(ax = axe2, data=df_re, x="광역지자체", y="방문자수", color='blue')
        axe2.legend(["방문자수", "인당 소비액"]) 
        plt.xticks(rotation= 60)
        st.pyplot(fig)
        st.markdown('방문자 수에 비해 인당 소비액이 높은 곳들을 공략하면 많은 관광 수익을 얻을 수 있을 거라고 추측됩니다.')
    
    st.markdown('## 고액소비의 대부분이 중국에 몰려있고 그 소비가 대부분 서울과 호텔, 면세점, 백화점에 편중되어 있는것으로 보아 고액소비자의 많은 비율을 중국 관광객이 차지하고있다.')

with tab3:
    st.markdown('# 최근 방한여행객 동향')
    df_country = pd.read_csv('data/방한여행객국적.csv')
    # fig = plt.figure(figsize=(10,10))
    plt.rcParams['font.size'] = 7
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.subheader('나라별 최근 방한 여행객 수')
        fig, ax = plt.subplots()
        ax.pie(df_country['방한관광객'], labels=df_country['국적'], autopct='%.1f%%', shadow=True, radius=1)
        st.pyplot(fig, clear_figure = True)
        st.markdown('2022년 9월 기준 최근 1년 방한 여행객 수를 국적으로 분류하여 시각화한 것으로 과거에는 중국과 일본 관광객이 가장 많은 수를 차지하였으나 최근에 미국 관광객이 가장 많이 방문을한다.')
    
    df_num_tour = pd.read_csv('data/방한외래관광객추이.csv')
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.markdown('### 방한 외래관광객 수')
        fig, ax = plt.subplots()
        sns.lineplot(data=df_num_tour, x='기준년월', y='방한 외래관광객')
        plt.xticks(rotation= 60)
        st.pyplot(fig)
        st.markdown('2022년 9월 기준 최근 1년 방한 여행객 수를 시각화한 것으로 최근 그 수가 점점 늘어남을 확인할 수 있다.')
    
    df_tourincome = pd.read_csv('data/최근1년관광수입.csv')
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.markdown('### 관광수입')
        fig = plt.figure()
        sns.lineplot(data=df_tourincome, x='기준연월', y='관광수입')
        plt.xticks(rotation= 60)
        st.pyplot(fig)
        st.markdown('2022년 9월 기준 최근 1년 관광수입을 시각화한 것으로 관광수입이 점점 늘어남을 확인 할 수 있다.')
    
    df_percon = pd.read_csv('data/최근1년1인당관광수입.csv')
    cols = st.columns([0.25, 0.5, 0.25])
    with cols[1]:
        st.markdown('### 1인당 관광수입')
        fig = plt.figure()
        sns.lineplot(data=df_percon, x='기준연월', y='1인당 관광수입')
        plt.xticks(rotation=60)
        st.pyplot(fig)
        st.markdown('2022년 9월 기준 최근 1년 1인당 관광수입을 시각화한 것으로 관광수입이 점점 줄어듬을 확인 할 수 있다.')
    
    st.markdown('### 관광수입은 늘어나나 1인당 관광수입이 줄어드는 것으로 보아 과거 고액소비에 주를 이루었던 중국 관광객보다 미국 관광객이 늘어나면서 관광소비의 추세가 지역문화로 바뀌어감을 볼 수 있다.')


with tab4:
    st.markdown('# 방한 외래관광객 유치방안')
    st.markdown('### 외래관광객들이 관심을 가질만한 패키지 상품 제안')
    st.markdown('##### 1. 한국 야구 응원문화 패키지')
    st.markdown('''과거에는 일본과 중국의 관광객 수가 주를 이루었지만 최근에는 미국 관광객이 주를 이루고 있으며 관광객수와 
총 관광소비액도 증가하고 있다. 그러나 1인당 관광소비액은 줄어드는 것으로 보아 중국 관광객들의 
면세점, 백화점에서 많은 소비가 소비액의 주를 이루던 떄와는 다르게 비교적 소비액이 적은 지역문화를 체험하는 추세로
바뀌어 가는것을 알 수가 있다. 이에 기반하여 전국야구 관광 패키지를 제안하고자 한다.
과거 2020년 한국의 야구응원 문화(시끌벅적한 응원가, 치어리더, 빠던등)를 부러워하는 미국 국민들의 민심을 
미국 야후기사에서 실은적이 있으며 평소 MLB 보스턴 레드삭스 팬이던 골드버그 미국대사관도 한국 야구응원 
문화를 즐기는 모습이 언론에 포착이 된적이있다. 그 당시에는 코로나 유행으로 인하여 시행하지 못하였고 
최근 한류의 흥행으로 인하여 늘어나는 미국 관광객을 노린 상품으로 전국에 있는 야구장을 즐기며, 
오전에는 지역문화를 체험하고 오후에는 야구문화를 체험하는 상품을 제안한다.
이 상품으로 서울에 몰려있는 관광객의 수를 지방으로 분산하여 그 지역의 문화를 체험하며소비패턴을 분산하고 지역의 
문화를 홍보할 수 있는 효과를 기대한다.''')
    url = 'https://www.joongang.co.kr/article/23762245'
    url_2 = 'https://www.chosun.com/sports/baseball/2022/08/21/2Z3TIHDY45BYHGLC5GXX6IPQH4/'
    
    if st.button('미국야구팬 KBO리그의 관심집중'):
        webbrowser.open_new_tab(url)
        
    if st.button('미국대사관도 즐기는 KBO리그'):
        webbrowser.open_new_tab(url_2)
        
    st.image('https://images.chosun.com/resizer/DdI0X6Q6-JtHrMbRRqpD1E-iDR0=/616x0/smart/cloudfront-ap-northeast-1.images.arcpublishing.com/chosun/SRWPAOLCBNCNPPEOJ6UJYSI3NQ.jpg')
    
    
    st.markdown('##### 2. 한국 전통 문화관광 경주패키지')
    df_seoul = pd.read_csv('data/서울시 주요 관광지 별 외국인 입장객.csv')
    cols = st.columns([0.45, 0.1, 0.45])
    with cols[0]:
        fig = plt.figure()
        df_seoul.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(kind='bar', rot=310, title='서울 주요 관광지 top5')
        st.pyplot(fig)
    with cols[2]:
        fig = plt.figure()
        df_gyeong = pd.read_csv('data/경기도 주요 관광지 별 외국인 입장객.csv')
        df_gyeong.sort_values(by='입장객수', ascending=False).groupby(['관광지명'])['입장객수'].sum().nlargest().plot(kind='bar',rot=310, title='경기도 주요 관광지 top5')
        st.pyplot(fig)
    
    st.markdown('''외국인들이 가장 많이 찾는 서울 주요 관광지를 보면 한국의 전통 문화에 관심이 많다는 것을 알 수 있다. 우리나라에서 한국의 역사를 가장 많이 담고있는 곳은 어디인가.
    당연히 경주라고 얘기할 것이다. 경주에는 석굴암, 동굴과 월지, 불국사, 첨성대 등 많은 유적지를 담고 있으며 한국의 전통 문화를 즐기러 여행을 온 방한 외국인들이게는
    영원히 기억에 남을만한 추억을 만들어줄 수 있을거라 생각합니다. 거기에 외국인들이 많이 찾는 경기도 주요 관광지를 보면 에버랜드에 많이 방문하는 것을 알 수 있는데 경주에는 방한 외국인들의
    익스트림 니즈도 만족시킬 수 있는 경주월드가 있습니다. 전통 문화 코스와 놀이공원 코스로 상품을 기획해본다면 해외 관광객 유치와 더불어 지역 경제를 살릴 수 있는 좋은 효과를 볼 수 있을 것이다.''')
    
    url_3 = 'http://www.kbsm.net/news/view.php?idx=248817'
    if st.button('경주 관광시장'):
        webbrowser.open_new_tab(url_3)
    
    cols = st.columns([0.25, 0.25, 0.25, 0.25])
    with cols[0]:
        st.image('http://www.cha.go.kr/unisearch/images/national_treasure/1612705.jpg')
    with cols[1]:
        st.image("https://www.gyeongju.go.kr/upload/content/thumb/20200626/227F27B4DDFD408592026D640C8AE4C0.jpg")
    with cols[2]:    
        st.image("https://www.gyeongju.go.kr/upload/content/thumb/20200317/5F92275758614941B3EB69A32A12CA4E.jpg")
    with cols[3]:    
        st.image("https://www.gyeongju.go.kr/upload/content/thumb/20200317/E662154B36F14F55AC45805A7702D6AD.jpg")
 