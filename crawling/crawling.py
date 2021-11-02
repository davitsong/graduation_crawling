from selenium import webdriver
import openpyxl
import requests
session=requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
}
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

# 워크북 새로 민들기
wb = openpyxl.Workbook()

sheet = wb.active

sheet.append(["개설학기","과목","캠퍼스","교수명","평점","과제","조모임","학점비율"])



#html = session.get(WIKI_URL, headers=headers).content
#bsObj = BeautifulSoup(html, "html.parser”)

driver=webdriver.Chrome('C:\graduationproject\chromedriver')

##profiler=webdriver.Firefox(executable_path='C:\graduationproject\geckodriver')

driver.implicitly_wait(3)

#go to the login page / login
##profiler.set_preference("network.proxy.type", 1)
##profiler.set_preference("network.proxy.socks",'127.0.0.1')
##profiler.set_preference("network.proxy.socks_port",9050)
##driver = webdriver.Firefox(firefox_profile=profiler)
#driver.implicitly_wait(15)
##driver.get("The URL I want to scrape")

driver.get('https://everytime.kr/login')
driver.find_element_by_name('userid').send_keys('harry3749')
driver.find_element_by_name('password').send_keys('smart0413*')
driver.find_element_by_xpath('//*[@class="submit"]/input').click()


#강의 평가 메뉴 선택
driver.find_element_by_xpath('//*[@href="/lecture"]').click()


#일반교양
# lec_list=["현대사회와윤리","언어의이해","협상의기술","논리와사고",
#           "문학과창의적사고","현대인의의사소통","서양철학입문","동양철학입문"
#     ,"인간관계론","매스컴과현대사회","인간심리의이해","마케팅의이해","회계의이해"
#     ,"사회학의이해","경제학입문","문화인류학입문","세계시민의식","글로벌문화와리더십","한국의문화와유산"
#     ,"동양사의이해","한국사의이해","서양사의이해","현대생활과디자인","대중예술의이해",
#           "미술의이해","예술과건축","시각과이미지","사진예술의이해","디지털디자인입문","교양일본어","교양중국어",
#           "교양한문","교양스페인어","교양독일어","교양프랑스어"]


#핵심교양
#lec_list=["정보사회와저작권","현대사회와법","지식재산과법","예술과법",
#          "인권과국가","범죄와사회","국제관계와법","CTO특강","과학사","토목공학개론및테크노프레너싶",
#          "문제해결과SW프로그래밍","컴퓨터공학개론","산업시스템개론","화학공학개론"]

#기초교양
#lec_list=["영어","논리적사고와글쓰기","전공기초영어","공학글쓰기"]

#4-2전공
#lec_list=["정보검색","임베디드시스템및실험","기계학습"]

#졸프2
#lec_list=[""]



#3-2전공
#lec_list=["컴퓨터그래픽스","운영체제","오토마타","기초데이터베이스","네트워크프로그래밍","디지털시스템설계"]

#2-2전공
lec_list=["자료구조및프로그래밍","논리회로설계및실험","어셈블리언어및실습","데이터통신","멀티미디어응용수학"]

#4-1전공
#lec_list=["시스템프로그래밍","인공지능","소프트웨어공학","응용데이터베이스","네트워크보안"]

#3_1전공
#lec_list=["HCI윈도우즈프로그래밍","알고리즘분석","컴퓨터구조","프로그래밍언어론","컴퓨터네트워크"]

#2_1전공
#lec_list=["자료구조및프로그래밍","논리회로설계및실험","인터넷프로그래밍"]

#MSC수학
#lec_list=["대학수학","응용수학","선형대수학","통계학","확률및통계","컴퓨터응용통계"]

#MSC과학
#lec_list=["대학물리","대학화학","생물학","유기화학","물리화학"]

#MSC전산
#lec_list=["수치해석","객체지향프로그래밍","C-프로그래밍","웹프로그래밍","공학컴퓨터입문및실습"]

all = []                                #전체과목 list
for i in lec_list:
    score=''                  # score NaN 채우기 위함

    driver.find_element_by_name('keyword').send_keys(i)
    driver.find_element_by_xpath('//*[@type="submit"]').click()
    time.sleep(3)
    clips = driver.find_elements_by_class_name("lecture")
    class_name = []                                        #과목 list


    #print(len(clips))
    for info in range(len(clips)):
        clips = driver.find_elements_by_class_name("lecture")
        class_spe = []                              #수업 당 list
        clips[info].click()
        time.sleep(3)
        flag = 0
        flag1 = 0
        #url=driver.current_url
        #print(url)
        res = driver.page_source
        #print(res)
        soup = BeautifulSoup(res, "html.parser")

        information_list=soup.select("div.side.head p span")                  #2021.1학기에 개설인거 확인하기
        cnt=0
        for information in information_list:
            if cnt==2:
                print(information.text[0:6])
                if information.text[0:6]=='2021-2':
                    class_spe.append(information.text[0:6])
                    break
                else:
                    driver.back()
                    time.sleep(2)
                    flag = 1
                    break
            cnt+=1
        if flag ==1:
            continue


       # for information in information_list:
           # print(information)


        information_list= soup.select("div.side.head h2")       #강의명
        for information in information_list:
            class_spe.append(information.text)

        information_list = soup.select("div.side.head p span")     #캠퍼스
        for information in information_list:
            print(information.text)
            if(information.text=='서울캠퍼스'):
                class_spe.append(information.text)
                break
            else:                                                  #새종캠
                flag1=1
                driver.back()
                time.sleep(2)
                break

        if flag1==1:
            continue


        information_list = soup.select("div.side.head p span")          #교수명
        cnt=0
        for information in information_list:
            if cnt==1:
                class_spe.append(information.text)
                break
            cnt+=1


        information_list = soup.select("span.value")                    #평점
        for information in information_list:
            class_spe.append((information.text))
            score=(information.text)

        information_list = soup.select("div.side.article div.rating div.details p span ")     #과제
        #print(information_list)
        for information in information_list:
            if (score == '0'):
                class_spe.append('NaN')
            else:
                class_spe.append(information.text)
            break

        information_list = soup.select("div.side.article div.rating div.details p span ")  # 조모임
        #print(information_list)
        cnt=0
        for information in information_list:
            if cnt==1:
                if(score=='0'):
                    class_spe.append('NaN')
                else:
                    class_spe.append(information.text)
                break
            cnt +=1

        information_list = soup.select("div.side.article div.rating div.details p span ")  #학점 비율
        #print(information_list)
        cnt = 0
        for information in information_list:
            if cnt == 2:
                if (score == '0'):
                    class_spe.append('NaN')
                else:
                    class_spe.append(information.text)

            cnt +=1

        time.sleep(2)
        print(class_spe)                #각각 수업 print
        sheet.append(class_spe)     #엑셀 행 append
        class_name.append(class_spe)
        driver.back()

        #print(type(class_name))



    print(class_name)                  #모든 수업 print

    #driver.implicitly_wait(3)

    all.append(class_name)
    time.sleep(4)
    driver.back()
    time.sleep(4)



wb.save('2_2전공s.xlsx')

#df = pd.read_excel('일반교양.xlsx')   결측값제거 추후 처리
#df.fillna(0)
#df_nan = df[df.isna()]
#print(df_nan)
#wb.save('일반교양.xlsx')


print(all)





#컨테이너 선택
#clips=html.select('h2')
#print(clips)
#
# classname = filename_remover(str(soup.select("div.side.head h2")))# 수업
# print( len(classname))
# classname = classname[1:len(classname)-1]
# #campus=soup.find("div.side.head p span",{"class"}:"")# 캠퍼스
# professor=str(soup.select("div.side.head p   "))# 교수명
# rate=str(soup.select("span.value"))# 평점
#
# print("수업명",classname)
# print("캠퍼스",campus.get_text())
# print("교수명",filename_remover(professor))
# print("평점",filename_remover(rate))
