from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException

import time

from mysmtp import send_email
from mycaptcha import solve_captcha


my_id = ""
my_pw = ""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)



def xpath(str) :
    return driver.find_element(By.XPATH, str)

def tag_name(str) :
    return driver.find_element(By.TAG_NAME, str)

def name(str) : 
    return driver.find_element(By.NAME, str)

def class_name(str) :
    return driver.find_element(By.CLASS_NAME, str)

def id(str) :
    return driver.find_element(By.ID, str)

times = 1000
def safety(func, n=5) :
    for _ in range(n * times) :
        try :
            func()
            return
        except WebDriverException :
            pass
        except Exception :
            pass
    
    raise WebDriverException


def safety_captcha() :
    while(True) :
        safety(lambda : class_name("capchaBtns").is_displayed())
        if class_name("capchaBtns").is_displayed() == True:
            safety(lambda : driver.execute_script('fnCapchaRefresh()'))
            safety(lambda : id('imgCaptcha').screenshot_as_png)
            answer = solve_captcha(id('imgCaptcha').screenshot_as_png)
            safety(lambda : xpath('//*[@id="divRecaptcha"]/div[1]/div[3]').click())
            safety(lambda : xpath('//*[@id="txtCaptcha"]').send_keys(answer))
        else :
            break


def refresh_loop() :
    recent = time.time()
    cnt = 10
    while(True) :
        safety(lambda : driver.refresh())
        safety(lambda : driver.switch_to.default_content())
        safety(lambda : driver.switch_to.frame(name('ifrmSeat')))
        safety_captcha()
        cnt += 1
        if cnt > 10 :
            cnt = 0
            print(time.time() - recent)
            recent = time.time()
        

        # 좌석 체크
        safety(lambda : xpath('/html/body/div[1]/div[3]/div[2]/div[1]'))
        tier_list = xpath('/html/body/div[1]/div[3]/div[2]/div[1]')
        for a in tier_list.find_elements(By.TAG_NAME, 'a'):
            if a.get_attribute("rc") != "0" or a.find_elements(By.TAG_NAME, "span")[1].text != "매진" :
                a.click()
                return


def 로그인() :
    safety(lambda : driver.get('https://ticket.interpark.com/Gate/TPLogin.asp'))
    safety(lambda : driver.switch_to.frame(tag_name('iframe')))
    safety(lambda : name('userId').send_keys(my_id))
    safety(lambda : name('userPwd').send_keys(my_pw))
    safety(lambda : xpath('//*[@id="btn_login"]').click())


def 티켓창열기() :
    safety(lambda : driver.get("https://tickets.interpark.com/special/sports/promotion?seq=22"))
    safety(lambda : xpath('//*[@id="__next"]/div/div/div/div[3]/div/div/button').click())
    safety(lambda : xpath('//*[@id="__next"]/div/div/div/div[2]/div[2]/ul/li[7]/div/div[3]/button').click())
    safety(lambda : driver.switch_to.window(driver.window_handles[1]), 50)
    safety(lambda : driver.switch_to.frame(name('ifrmSeat')), 50)



def 구역선택() :
    refresh_loop()
    # 구역선택 버튼
    safety(lambda : xpath('/html/body/div[1]/div[3]/div[2]/div[3]/a[2]/img').click())
            

def 좌석선택() :
    # 좌석선택
    safety(lambda : driver.switch_to.frame("ifrmSeatDetail"))
    safety(lambda : xpath('/html/body/table/tbody/tr/td/img[2]').click())
    # 좌석선택 버튼
    safety(lambda : driver.switch_to.default_content())
    safety(lambda : driver.switch_to.frame(name('ifrmSeat')))
    safety(lambda : xpath('//*[@id="NextStepImage"]').click())

def 구역선택으로_돌아가기() :
    # 돌아가기 버튼
    driver.switch_to.default_content()
    driver.switch_to.frame(name("ifrmSeat"))
    xpath('/html/body/form[1]/div/div[1]/div[3]/div/div[4]/p[1]/a/img').click()

def 결제창() :
    # 매수 선택
    safety(lambda : driver.switch_to.default_content())
    safety(lambda : driver.switch_to.frame(name("ifrmBookStep")))
    safety(lambda : Select(xpath('/html/body/div[1]/div[1]/div/table/tbody/tr/td/table/tbody/tr/td[3]/select')).select_by_visible_text('1매'))
    # 다음 버튼
    safety(lambda : driver.switch_to.default_content())
    safety(lambda : xpath('//*[@id="SmallNextBtnImage"]').click())
    # 생년월일 선택
    safety(lambda : driver.switch_to.frame(name("ifrmBookStep")))
    safety(lambda : xpath('//*[@id="YYMMDD"]').send_keys('001127'))
    # 다음 버튼
    safety(lambda : driver.switch_to.default_content())
    safety(lambda : xpath('//*[@id="SmallNextBtnImage"]').click())
    # 무통장 입금 선택
    safety(lambda : driver.switch_to.frame(name("ifrmBookStep")))
    safety(lambda : xpath('//*[@id="Payment_22004"]/td/input').click())
    # 국민은행 선택
    safety(lambda : Select(xpath('//*[@id="BankCode"]')).select_by_visible_text('국민은행'))
    # 다음 버튼
    safety(lambda : driver.switch_to.default_content())
    safety(lambda : xpath('//*[@id="SmallNextBtnImage"]').click())
    # 모두 동의 체크
    safety(lambda : driver.switch_to.frame(name("ifrmBookStep")))
    safety(lambda : xpath('//*[@id="checkAll"]').click())
    # 마지막 결제 버튼
    safety(lambda : driver.switch_to.default_content())
    safety(lambda : xpath('//*[@id="LargeNextBtnImage"]').click())

    


def 성공이메일보내기() :
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()


#메인
성공횟수 = 0
while(성공횟수 <= 7) :
    try :
        로그인()
        티켓창열기()

        while(True) : 
            구역선택()
            try :
                좌석선택()
                break
            except WebDriverException :
                #좌석 선택 실패시 구역선택으로 다시 돌아가기
                구역선택으로_돌아가기()

        결제창()
        성공횟수 += 1
        print(f"{성공횟수}째 결제 완료!!!!!")
        성공이메일보내기()
        
    except WebDriverException :
        time.sleep(1)
    except Exception :
        time.sleep(1)
    finally :
        safety(lambda : driver.switch_to.window(driver.window_handles[0]))
        driver = webdriver.Chrome(options=chrome_options)