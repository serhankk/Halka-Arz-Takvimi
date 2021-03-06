#!/usr/bin/env python3

"""
Halka arz edilmiş şirketleri döker.
"""

import os
import platform
import codecs
from datetime import date
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

today = date.today()
today = today.strftime("%d-%m-%Y")

path = os.getcwd() + r"\output"
PUBLIC_OFFER_OUTPUT = fr"{path}\PUBLIC-OFFER.csv"

IS_EXIST = os.path.exists(path)
print('[LOG] Çıktı klasörü mevcut mu: ' + str(IS_EXIST))

if not IS_EXIST:
    os.makedirs(path)
    print(f'[LOG] {path} klasörü oluşturuldu')

operating_system = platform.system()
if operating_system.lower() == "windows":
    print("[LOG] İşletim Sistemi: " + operating_system)
    DRIVER = os.getcwd() + r"\windows\geckodriver"
    print("[LOG] Driver: " + DRIVER)


elif operating_system.lower() == "linux":
    print("[LOG] İşletim Sistemi: " + operating_system)
    DRIVER = os.getcwd() + "/linux/geckodriver"
    print("[LOG] Driver: " + DRIVER)

fireFoxOptions = webdriver.FirefoxOptions()
service = Service(fr"{DRIVER}")
child_service = Service(fr"{DRIVER}")
fireFoxOptions.add_argument("--headless")

driver = webdriver.Firefox(options=fireFoxOptions, service=service)

driver.get("https://halkarz.com/")
print("[LOG] Site açıldı")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("[LOG] Sayfanın en altına inildi")

    try:
        load_more = driver.find_element(By.CLASS_NAME, "misha_loadmore")
        print("[LOG] Daha fazla butonu bulundu.")

        load_more.click()
        print("[LOG] Daha fazla hisse yükleniyor...")
    except NoSuchElementException:
        break

print("[LOG] Yüklenecek hisse senetlerinin sonu!")

stocks_list = driver.find_elements(By.CLASS_NAME, "halka-arz-list")
print("[LOG] Hisse senetleri listesi alındı")
for num, il_content in enumerate(stocks_list, 1):
    output = codecs.open(PUBLIC_OFFER_OUTPUT, "a", "utf-8")
    print("[LOG] Şirket bilgisi alınıyor:")

    il_bist_code = il_content.find_element(By.CLASS_NAME, "il-bist-kod").text
    print("[LOG] Bist kodu alındı")

    il_company_name = il_content.find_element(By.CLASS_NAME, "il-halka-arz-sirket").text
    print("[LOG] Şirket adı alındı")

    il_company_detail_link = il_content.find_element(
        By.CLASS_NAME, "il-halka-arz-sirket").find_element(
            By.CSS_SELECTOR, 'a').get_attribute("href")
    print("[LOG] Şirket detay linki alındı")

    child_driver = webdriver.Firefox(options=fireFoxOptions, service=child_service)

    child_driver.get(il_company_detail_link)
    print(f'[LOG] Açılacak link: "{il_company_detail_link}"')
    print("[LOG] Şirket detay sayfası açıldı")

    public_offer_price = child_driver.find_element(
        By.XPATH,
        "/html/body/div[1]/section[2]/div/div[1]/article[2]/table/tbody/tr[2]/td[2]/strong").text
    print("[LOG] Şirket detaylarından halka arz fiyatı bulundu")

    child_driver.close()
    print("[LOG] Şirket detay sayfası kapatıldı")

    il_public_offering_date = il_content.find_element(
        By.CLASS_NAME, "il-halka-arz-tarihi").text
    print("[LOG] Halka arz tarihi alındı")

    output.write(f'{num}, "{il_bist_code}", "{il_company_name}", \
    "{public_offer_price}", "{il_public_offering_date}"\n')
    print(f"[INFO] {num}, {il_bist_code}, {il_company_name}, {public_offer_price}, \
    {il_public_offering_date}")
    print("[LOG] Şirket bilgileri basıldı")
    output.close()

print("[LOG] Program başarıyla sonlandırıldı")
