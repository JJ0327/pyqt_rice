import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QTextBrowser, QGridLayout
import requests
from bs4 import BeautifulSoup
from datetime import date
import re

def get_html(url):                  #해당 페이지의 html소스를 출력하는 함수
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html


def get_diet(code, ymd, weekday):
    schMmealScCode = code  # int
    schYmd = ymd  # str

    num = weekday + 1  # int 0월1화2수3목4금5토6일
    URL = (
            "http://stu.dge.go.kr/sts_sci_md01_001.do?"
            "schulCode=D100000282&schulCrseScCode=4&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
    )
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')           #html소스를 beautifulSoup에 넣음
    element = soup.find_all("tr")                       #tr테그들중 3번째에서 td태그 추출(html소스에서 급식이 있던부분)
    element = element[2].find_all('td')
    try:
        element = element[num]  # 요청하는 날짜의 요일번째수의 td태그의 내용 추출
        element = str(element)
        element = element.replace('[', '')          # 불필요한 문자들 제거
        element = element.replace(']', '')
        element = element.replace('<br/>', '\n')
        element = element.replace('<td class="textC last">', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('</td>', '')
        element = element.replace('(h)', '')
        element = element.replace('.', '')
        element = re.sub(r"\d", "", element)
    except:
        element = " "
    return element

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.le = QLineEdit()                   #날짜를 입력할 줄편집기 기본입력값(yymmdd)
        self.le.setPlaceholderText('yymmdd')
        self.le.returnPressed.connect(self.get_dit) #enter 키 누를시 get_dit()

        self.btn = QPushButton('Start')         #Start버튼
        self.btn.clicked.connect(self.get_dit)  #누를시 get_dit

        self.lbl = QLabel('날짜를 입력하세요.')

        self.tb = QTextBrowser()            #텍스트 브라우저생성

        grid = QGridLayout()                #그리드 레이아웃으로 위치 설정
        grid.addWidget(self.le, 0, 0, 1, 3)
        grid.addWidget(self.btn, 0, 3, 1, 1)
        grid.addWidget(self.lbl, 1, 0, 1, 4)
        grid.addWidget(self.tb, 2, 0, 1, 4)

        self.setLayout(grid)

        self.setWindowTitle('Web Crawler')      #윈도우창 위치설정
        self.setGeometry(100, 100, 450, 650)
        self.show()



    def get_dit(self):      #급식 받아오는 부분
        datee = self.le.text()          #날짜 받아옴

        if datee:
            Ydate = '20' + datee[0:2]       #년/월/일 따로 추출
            Mdate = datee[2:4]
            Ddate = datee[4:6]
            d2 = date(int(Ydate),int(Mdate),int(Ddate)) #date객체생성
            local_date = d2.strftime("%Y.%m.%d")
            local_weekday = d2.weekday()

            meal_date = str(local_date)
            l_wkday = int(local_weekday)

            b_b = get_diet(1, meal_date, l_wkday)   #급식 받아옴
            l_l = get_diet(2, meal_date, l_wkday)
            d_d = get_diet(3, meal_date, l_wkday)

            self.tb.append("조식")        #텍스트 브라우저에 입력
            self.tb.append(b_b)

            self.tb.append("정식")
            self.tb.append(l_l)

            self.tb.append("석식")
            self.tb.append(d_d)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())