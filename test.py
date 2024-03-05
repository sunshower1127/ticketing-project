from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.select import Select

from selenium.common.exceptions import JavascriptException

import pyautogui as auto
import time

import random

import re
import numpy
import os
import cv2 as cv
from pytesseract import image_to_string
# import warnings
# from win10toast import ToastNotifier
# import logging

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10, 1)
fast_wait = WebDriverWait(driver, 10, 0.3)

# def btn_click(xpath) :
#     wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# def key_send(str) :
#     wait.until()
# def login() :
#     




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

def captcha() :
    wait.until(EC.presence_of_element_located((By.ID, 'imgCaptcha')))
    image = id('imgCaptcha').screenshot_as_png

    with open(os.getcwd() + "\\captcha.png", "wb") as file:
        file.write(image)
    image = cv.imread(os.getcwd() + "\\captcha.png")

    # Set a threshold value for the image, and save
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 91, 1)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=1)

    cnts = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area < 50:
            cv.drawContours(image, [c], -1, (0, 0, 0), -1)
    kernel2 = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv.filter2D(image, -1, kernel2)
    result = 255 - image
    return image_to_string(result)
# # login

# my_id = "sunshower"
# my_pw = "p!1415926535"
# driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')
# driver.switch_to.frame(tag_name('iframe'))
# name('userId').send_keys(my_id)
# name('userPwd').send_keys(my_pw)
# xpath('//*[@id="btn_login"]').click()

# # step 1
# driver.get("https://tickets.interpark.com/special/sports/promotion?seq=22")
# xpath('//*[@id="__next"]/div/div/div/div[3]/div/div/button').click()
# xpath('//*[@id="__next"]/div/div/div/div[2]/div[2]/ul/li[7]/div/div[3]/button').click()

my_id = "sunshower"
my_pw = "p!1415926535"
driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')
driver.switch_to.frame(tag_name('iframe'))
name('userId').send_keys(my_id)
name('userPwd').send_keys(my_pw)
xpath('//*[@id="btn_login"]').click()

driver.get("https://tickets.interpark.com/goods/23014851")
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup-prdGuide"]/div/div[3]/button')))
xpath('//*[@id="popup-prdGuide"]/div/div[3]/button').click()
xpath('//*[@id="productSide"]/div/div[2]/a[1]').click()


# step 2
time.sleep(5)
driver.switch_to.window(driver.window_handles[1])


driver.switch_to.frame(name('ifrmSeat'))
while(True) :
    time.sleep(0.2)
    if class_name("capchaBtns").is_displayed() == True:
        # try:
        #     driver.execute_script('fnCheckOK()') 
        # except JavascriptException:
        #     print("fnCheckOK")
        driver.execute_script('fnCapchaRefresh()')
        answer = captcha()
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[3]')))
        xpath('//*[@id="divRecaptcha"]/div[1]/div[3]').click()
        xpath('//*[@id="txtCaptcha"]').send_keys(answer)


    else :
        break
    

driver.switch_to.frame("ifrmSeatDetail")

xpath('/html/body/table/tbody/tr/td/img[2]').click()
driver.switch_to.default_content()
driver.switch_to.frame(name("ifrmSeat"))
xpath('//*[@id="NextStepImage"]').click()

driver.switch_to.default_content()
driver.switch_to.frame(name("ifrmBookStep"))

time.sleep(0.3)
Select(xpath('/html/body/div[1]/div[1]/div/table/tbody/tr/td/table/tbody/tr/td[3]/select')).select_by_visible_text('1매')

driver.switch_to.default_content()
xpath('//*[@id="SmallNextBtnImage"]').click()

driver.switch_to.default_content()
driver.switch_to.frame(name("ifrmBookStep"))
xpath('//*[@id="YYMMDD"]').send_keys('001127')

driver.switch_to.default_content()
xpath('//*[@id="SmallNextBtnImage"]').click()

driver.switch_to.frame(name("ifrmBookStep"))
xpath('//*[@id="Payment_22004"]/td/input').click()

Select(xpath('//*[@id="BankCode"]')).select_by_visible_text('국민은행')

driver.switch_to.default_content()
xpath('//*[@id="SmallNextBtnImage"]').click()

driver.switch_to.frame(name("ifrmBookStep"))
xpath('//*[@id="checkAll"]').click()
