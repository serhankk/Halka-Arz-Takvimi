#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from os import getcwd

import platform
import codecs

operating_system = platform.system()
if operating_system.lower() == "windows":
    print("[LOG] İşletim Sistemi: " + operating_system)

elif operating_system.lower() == "linux":
    print("[LOG] İşletim Sistemi: " + operating_system)
    DRIVER = getcwd() + '/geckodriver'
    print("[LOG] Driver: " + DRIVER)

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.add_argument("--headless")

driver = webdriver.Firefox(options=fireFoxOptions)

driver.get('https://halkarz.com/')
print('[LOG] Site açıldı')

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('[LOG] Sayfanın en altına inildi')

    try:
        load_more = driver.find_element(By.CLASS_NAME, 'misha_loadmore')
        print('[LOG] Daha fazla butonu bulundu.')

        load_more.click()
        print('[LOG] Daha fazla hisse yükleniyor...')
    except:
        print('[LOG] Yüklenecek daha fazla hisse kalmadı')
        break

print('[LOG] Program sonu!')


stocks_list = driver.find_elements(By.CLASS_NAME, 'halka-arz-list')
print('[LOG] Hisse senetleri listesi alındı')
for num, il_content in enumerate(stocks_list, 1):
    output = codecs.open('output.csv', 'a', 'utf-8')
    print('[LOG] Şirket bilgisi alınıyor:')
    il_bist_code = il_content.find_element(By.CLASS_NAME, 'il-bist-kod').text
    print('[LOG] Bist kodu alındı')
    il_company_name = il_content.find_element(By.CLASS_NAME, 'il-halka-arz-sirket').text
    print('[LOG] Şirket adı alındı')
    il_company_detail_link = il_content.find_element(By.CLASS_NAME, 'il-halka-arz-sirket').find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    print('[LOG] Şirket detay linki alındı')
    if operating_system.lower() == 'windows':
        child_driver = webdriver.Firefox(options=fireFoxOptions)
    
    elif operating_system.lower() == 'linux':
        child_driver = webdriver.Firefox(executable_path=DRIVER, options=fireFoxOptions)
    child_driver.get(il_company_detail_link)
    print('[LOG] Açılacak link: "{}"'.format(il_company_detail_link))
    print('[LOG] Şirket detay sayfası açıldı')

    public_offer_price = child_driver.find_element(By.XPATH, '/html/body/div[1]/section[2]/div/div[1]/article[2]/table/tbody/tr[2]/td[2]/strong').text
    print('[LOG] Şirket detaylarından halka arz fiyatı bulundu')
  
    child_driver.close()
    print('[LOG] Şirket detay sayfası kapatıldı')
    il_public_offering_date = il_content.find_element(By.CLASS_NAME, 'il-halka-arz-tarihi').text
    print('[LOG] Halka arz tarihi alındı')

    output.write('{}, "{}", "{}", "{}", "{}"\n'.format(num, il_bist_code, il_company_name, public_offer_price, il_public_offering_date))
    print('[INFO] {}, {}, {}, {}, {}'.format(num, il_bist_code, il_company_name, public_offer_price, il_public_offering_date))
    print('[LOG] Şirket bilgileri basıldı')
    output.close()
    
print('[LOG] Program başarıyla sonlandırıldı')



