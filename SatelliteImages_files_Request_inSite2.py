# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 16:16:41 2025

@author: minjeong
"""

import os.path
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import  Service
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import traceback


while True:
    try:
        # Chrome 옵션 설정
        options = webdriver.ChromeOptions()
        options.add_argument('--force-device-scale-factor=0.8')
        prefs = {
            "download.default_directory": False,  # 다운로드 파일 저장 경로
            "download.prompt_for_download": False,       # 다운로드 팝업 비활성화
            "download.directory_upgrade": True,         # 디렉토리 업그레이드 활성화
            "safebrowsing.enabled": True                # 안전 다운로드 활성화
        }
        options.add_experimental_option("prefs", prefs)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options = options)
        
        # 웹사이트 열기 (로그인 화면)
        driver.get("https://data.kma.go.kr/cmmn/main.do")  # URL 수정 필요
        
        time.sleep(1)
        t = 0.5
        wait = WebDriverWait(driver, 60)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]')))
        login_button.click()
        time.sleep(t)
        driver.find_element(By.ID, "loginId").send_keys("alldaywalk@naver.com") # 로그인 ID 수정
        driver.find_element(By.ID, "passwordNo").send_keys("wodnr0428!")  # 로그인 PW 수정
        time.sleep(t)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbtn"]')))
        login_button.click()
        time.sleep(t)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mypageBtn"]')))
        login_button.click()
        
        # 자료 신청 대기목록 들어가기
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="snb"]/nav/ul/li[5]/a')))
        button.click()
        time.sleep(1)
        
        # all Check
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheck"]')))
        button.click()
        time.sleep(t)
        
        for i in range(1, 187):
            # all Check
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheck"]')))
            button.click()
            time.sleep(t)
            
            # all Check
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheck"]')))
            button.click()
            time.sleep(t)
            
            # Request Data
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frm"]/div[1]/div[2]/button[1]')))
            button.click()
            time.sleep(t)
            
            # 기상청 FTP
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="method1"]')))
            button.click()
            time.sleep(t)
            
            # E-mail
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email1"]')))
            button.click()
            time.sleep(t)
            
            # 요청
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-datapop"]/div/div[2]/div[3]/button[2]')))
            button.click()
            time.sleep(t)
            
            # 용도 신청
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reqstPurposeCd7"]')))
            button.click()
            time.sleep(t)
            
            # 요청2
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sltUsePop"]/div/div/div[2]/div/a[2]')))
            button.click()
            time.sleep(t)
            
            # 확인
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[3]/button')))
            button.click()
            time.sleep(t)
            
            # print("작업 완료")
            # break
    except Exception as e:
        print("에러 :", e)
        print(traceback.format_exc())
        
        driver.quit()
        
        try:
            driver.quit()
        except Exception as e:
            pass
        time.sleep(5)
    