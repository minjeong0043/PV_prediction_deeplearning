from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

# 크롬 드라이버 경로 설정
# chrome_driver_path = "C:/Users/leejunwoo/Downloads/chromedriver.exe"  # 크롬 드라이버 경로로 변경

# 다운로드 경로 설정
download_dir = "D:\\mj Kim\\file"  # 다운로드할 경로로 변경
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

with open(os.path.join(download_dir, "filename.txt"), "wb") as file:
    # 파일 쓰기 로직
    pass
# Chrome 옵션 설정
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # 다운로드 파일 저장 경로
    "download.prompt_for_download": False,       # 다운로드 팝업 비활성화
    "download.directory_upgrade": True,         # 디렉토리 업그레이드 활성화
    "safebrowsing.enabled": True                # 안전 다운로드 활성화
}
options.add_experimental_option("prefs", prefs)

# 드라이버 초기화
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(options= options)
# 웹사이트 열기 (로그인 화면)
driver.get("https://datasvc.nmsc.kma.go.kr/datasvc/html/login/login.do")  # URL 수정 필요

time.sleep(1)

try:
    # 로그인
    # driver.find_element(By.ID, "userId").send_keys("@@@여기 아이디 입력@@@") # 로그인 ID 수정
    # driver.find_element(By.ID, "tempPassword").send_keys("@@@여기 비밀번호 입력@@@")  # 로그인 PW 수정
    # driver.find_element(By.ID, "loginBtn").click()  # 로그인 버튼 ID 수정
    input("로그인 후 Enter")
    wait = WebDriverWait(driver, 10)

    selenium_cookies = driver.get_cookies()
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

    # 쿠키 확인
    print("쿠키:", cookies)

    time.sleep(1)

    # 1. 메인화면에서 데이터 서비스 > 다운로드로 이동
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "데이터 서비스")))
    mover = driver.find_element(By.LINK_TEXT, "데이터 서비스")
    acts = ActionChains(driver)
    acts.move_to_element(mover).perform()

    time.sleep(0.1)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "다운로드")))
    driver.find_element(By.LINK_TEXT, "다운로드").click()

    time.sleep(1)

    # 2. 첫 번째 페이지에서 '다운로드' 버튼 클릭
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@value='다운로드']")))
    driver.find_element(By.XPATH, "//input[@value='다운로드']").click()

    time.sleep(1)

    # 3. 새로 뜨는 팝업 창에서 모든 '다운로드' 버튼 클릭
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[-1])  # 새 창으로 전환
    code_num = 246676
    # download_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@value='다운로드']")))
    driver.get(f"http://datasvc.nmsc.kma.go.kr/datasvc/html/req/selectSatFileStorage.do?orderUsq={code_num}")
    time.sleep(3)
    # 4. 파일 이름 추출
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-data")))

    file_elements = driver.find_elements(By.XPATH, "//*[@id='search-data']//tr/td[1]")
    file_names = [file.get_attribute("innerText").strip() for file in file_elements]
    for idx, file_name in enumerate(file_names, start=1):
        print(f"{idx}: {file_name}")

    # 이름 추출 후 창 닫기, 다운로드는 백그라운드에서 돌아감
    driver.close()

    # 세션 설정
    session = requests.Session()

    # 가져온 쿠키 전달
    session.cookies.update(cookies)

    # 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        # "Referer": "https://datasvc.nmsc.kma.go.kr/datasvc/html/req/selectSatFileStorage.do?orderUsq=246368",
        "Referer" : f"https://datasvc.nmsc.kma.go.kr/datasvc/json/req/selectSatDataMetaInfo.do?orderUsq={code_num}",
    }

    # 파일 다운로드 URL
    for idx, file_name in enumerate(file_names):
        download_url = f"https://datasvc.nmsc.kma.go.kr/datasvc/json/req/selectSatDataMetaInfo.do?orderUsq={code_num}&fileName={file_name}"

        # 다운로드 요청
        response = session.get(download_url, headers=headers, stream=True)

        # 파일 저장
        if response.status_code == 200:
            save_path = os.path.join(download_dir, file_name)
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"{idx+1}/{len(file_names)}: {file_name} 다운로드 완료: {save_path}")
        else:
            print(f"{idx+1}: {file_name} 다운로드 실패! 상태 코드: {response.status_code}")

finally:
    # 브라우저 닫기
    driver.quit()