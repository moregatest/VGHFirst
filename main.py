#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "selenium>=4.15.0",
#     "python-dotenv>=1.0.0",
#     "webdriver-manager>=4.0.0",
# ]
# ///

"""
VGH First Visit Registration Automation
自動初診掛號表單提交系統
"""

import os
import time
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class VGHRegistrationBot:
    def __init__(self):
        load_dotenv()
        self.registration_url = os.getenv('REGISTRATION_URL')
        self.user_data = {
            'id_number': os.getenv('ID_NUMBER'),
            'name': os.getenv('NAME'),
            'birth_date': os.getenv('BIRTH_DATE'),
            'phone': os.getenv('PHONE'),
            'address': os.getenv('ADDRESS'),
            'zipcode': os.getenv('ZIPCODE'),
            'emergency_contact_name': os.getenv('EMERGENCY_CONTACT_NAME'),
            'emergency_contact_phone': os.getenv('EMERGENCY_CONTACT_PHONE'),
            'passive_smoking': os.getenv('PASSIVE_SMOKING', 'no').lower() == 'yes',
            'smoking_habit': os.getenv('SMOKING_HABIT', 'no').lower() == 'yes',
            'drinking_habit': os.getenv('DRINKING_HABIT', 'no').lower() == 'yes',
            'betel_nut_habit': os.getenv('BETEL_NUT_HABIT', 'no').lower() == 'yes',
            'agree_data_collection': os.getenv('AGREE_DATA_COLLECTION', 'no').lower() == 'yes',
            'agree_satisfaction_survey': os.getenv('AGREE_SATISFACTION_SURVEY', 'no').lower() == 'yes',
        }
        self.auto_mode = os.getenv('AUTO_MODE', 'no').lower() == 'yes'
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """設置 Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)

    def find_and_click_radio_button(self):
        """尋找並點選 radio button"""
        try:
            print("正在搜尋可用的掛號時段...")
            
            # 尋找所有名為 regKey 的 radio button
            radio_buttons = self.driver.find_elements(By.NAME, "regKey")
            
            if not radio_buttons:
                print("未找到任何可用的掛號時段")
                return False
            
            # 點選第一個可用的時段
            radio_button = radio_buttons[0]
            value = radio_button.get_attribute('value')
            print(f"找到可用時段，時段代碼: {value}")
            
            # 點選 radio button
            self.driver.execute_script("arguments[0].click();", radio_button)
            print("已選擇掛號時段")
            
            # 等待頁面跳轉或表單出現
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"尋找或點選 radio button 時發生錯誤: {e}")
            return False

    def fill_form(self):
        """填寫表單"""
        try:
            print("開始填寫表單...")
            
            # 等待表單出現
            time.sleep(3)
            
            # 調試：列出所有輸入欄位
            print("偵測頁面中的表單欄位...")
            input_fields = self.driver.find_elements(By.TAG_NAME, "input")
            for i, field in enumerate(input_fields):
                field_name = field.get_attribute("name") or "無名稱"
                field_type = field.get_attribute("type") or "text"
                field_id = field.get_attribute("id") or "無ID"
                field_value = field.get_attribute("value") or ""
                field_placeholder = field.get_attribute("placeholder") or ""
                is_visible = field.is_displayed()
                print(f"欄位{i+1}: name='{field_name}', type='{field_type}', id='{field_id}', value='{field_value[:20]}', placeholder='{field_placeholder}', visible={is_visible}")
                if i >= 20:  # 限制顯示數量
                    break
            
            # 填寫身分證號 (實際欄位名稱: pid)
            try:
                id_field = self.driver.find_element(By.NAME, "pid")
                id_field.clear()
                id_field.send_keys(self.user_data['id_number'])
                print(f"已填寫身分證號: {self.user_data['id_number']}")
            except NoSuchElementException:
                print("警告: 無法找到身分證號欄位")
            
            # 填寫姓名 (實際欄位名稱: pname)
            try:
                name_field = self.driver.find_element(By.NAME, "pname")
                name_field.clear()
                name_field.send_keys(self.user_data['name'])
                print(f"已填寫姓名: {self.user_data['name']}")
            except NoSuchElementException:
                print("警告: 無法找到姓名欄位")
            
            # 填寫生日 (分別填寫年月日)
            birth_parts = self.user_data['birth_date'].split('/')
            if len(birth_parts) == 3:
                try:
                    # 年份
                    year_field = self.driver.find_element(By.NAME, "pbirth_yyyy")
                    year_field.clear()
                    year_field.send_keys(birth_parts[0])
                    
                    # 月份
                    month_field = self.driver.find_element(By.NAME, "pbirth_mm")
                    month_field.clear()
                    month_field.send_keys(birth_parts[1])
                    
                    # 日期
                    day_field = self.driver.find_element(By.NAME, "pbirth_dd")
                    day_field.clear()
                    day_field.send_keys(birth_parts[2])
                    
                    print(f"已填寫生日: {self.user_data['birth_date']}")
                except NoSuchElementException:
                    print("警告: 無法找到生日欄位")
            else:
                print("警告: 生日格式錯誤，請使用 YYYY/MM/DD 格式")
            
            # 嘗試不同的欄位名稱組合來填寫手機
            phone_field_names = ["mobile", "phone", "cellphone", "telephone"]
            phone_filled = False
            for field_name in phone_field_names:
                try:
                    phone_field = self.driver.find_element(By.NAME, field_name)
                    phone_field.clear()
                    phone_field.send_keys(self.user_data['phone'])
                    print(f"已填寫手機 (欄位: {field_name}): {self.user_data['phone']}")
                    phone_filled = True
                    break
                except NoSuchElementException:
                    continue
            
            if not phone_filled:
                print("警告: 無法找到手機欄位")
            
            # 填寫郵遞區號 (實際欄位名稱: zipcode)
            try:
                zipcode_field = self.driver.find_element(By.NAME, "zipcode")
                zipcode_field.clear()
                zipcode_field.send_keys(self.user_data['zipcode'])
                print(f"已填寫郵遞區號: {self.user_data['zipcode']}")
            except NoSuchElementException:
                print("警告: 無法找到郵遞區號欄位")
            
            # 填寫地址 (實際欄位名稱: addr)
            try:
                address_field = self.driver.find_element(By.NAME, "addr")
                address_field.clear()
                address_field.send_keys(self.user_data['address'])
                print(f"已填寫地址: {self.user_data['address']}")
            except NoSuchElementException:
                print("警告: 無法找到地址欄位")
            
            # 填寫緊急聯絡人姓名 (實際欄位名稱: emConName)
            try:
                emergency_name_field = self.driver.find_element(By.NAME, "emConName")
                emergency_name_field.clear()
                emergency_name_field.send_keys(self.user_data['emergency_contact_name'])
                print(f"已填寫緊急聯絡人姓名: {self.user_data['emergency_contact_name']}")
            except NoSuchElementException:
                print("警告: 無法找到緊急聯絡人姓名欄位")
            
            # 填寫緊急聯絡人電話 (實際欄位名稱: emConPhone)
            try:
                emergency_phone_field = self.driver.find_element(By.NAME, "emConPhone")
                emergency_phone_field.clear()
                emergency_phone_field.send_keys(self.user_data['emergency_contact_phone'])
                print(f"已填寫緊急聯絡人電話: {self.user_data['emergency_contact_phone']}")
            except NoSuchElementException:
                print("警告: 無法找到緊急聯絡人電話欄位")
            
            # 處理健康習慣選項
            self._handle_health_habits()
            
            # 處理個資同意選項
            self._handle_privacy_agreements()
            
            print("表單填寫完成")
            return True
            
        except Exception as e:
            print(f"填寫表單時發生錯誤: {e}")
            return False

    def _handle_health_habits(self):
        """處理健康習慣相關選項"""
        # 被動吸菸 (實際欄位名稱: smok_secondhand)
        try:
            if self.user_data['passive_smoking']:
                passive_smoking_yes = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_secondhand'][value='Y']")
                passive_smoking_yes.click()
                print("被動吸菸: 有")
            else:
                passive_smoking_no = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_secondhand'][value='N']")
                passive_smoking_no.click()
                print("被動吸菸: 無")
        except NoSuchElementException:
            print("未找到被動吸菸選項，跳過")
        
        # 吸菸習慣 (實際欄位名稱: smok_use)
        try:
            if self.user_data['smoking_habit']:
                smoking_yes = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_use'][value='Y']")
                smoking_yes.click()
                print("吸菸習慣: 有吸菸習慣")
            else:
                smoking_no = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_use'][value='N']")
                smoking_no.click()
                print("吸菸習慣: 不吸菸")
        except NoSuchElementException:
            print("未找到吸菸習慣選項，跳過")
        
        # 飲酒習慣 (實際欄位名稱: smok_drike)
        try:
            if self.user_data['drinking_habit']:
                drinking_yes = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_drike'][value='Y']")
                drinking_yes.click()
                print("飲酒習慣: 經常喝酒")
            else:
                drinking_no = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_drike'][value='N']")
                drinking_no.click()
                print("飲酒習慣: 不喝酒")
        except NoSuchElementException:
            print("未找到飲酒習慣選項，跳過")
        
        # 檳榔習慣 (實際欄位名稱: smok_betelnut)
        try:
            if self.user_data['betel_nut_habit']:
                betel_yes = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_betelnut'][value='Y']")
                betel_yes.click()
                print("檳榔習慣: 有嚼檳榔習慣")
            else:
                betel_no = self.driver.find_element(By.CSS_SELECTOR, "input[name='smok_betelnut'][value='N']")
                betel_no.click()
                print("檳榔習慣: 不嚼檳榔")
        except NoSuchElementException:
            print("未找到檳榔習慣選項，跳過")

    def _handle_privacy_agreements(self):
        """處理個資保護相關同意選項"""
        # 個資提供分院同意 (實際欄位名稱: q2)
        try:
            if self.user_data['agree_data_collection']:
                q2_agree = self.driver.find_element(By.CSS_SELECTOR, "input[name='q2'][value='Y']")
                q2_agree.click()
                print("個資提供分院: 同意")
            else:
                q2_disagree = self.driver.find_element(By.CSS_SELECTOR, "input[name='q2'][value='N']")
                q2_disagree.click()
                print("個資提供分院: 不同意")
        except NoSuchElementException:
            print("未找到個資提供分院選項，跳過")
        
        # 個資保護法滿意度調查同意 (實際欄位名稱: q3)
        try:
            if self.user_data['agree_satisfaction_survey']:
                q3_agree = self.driver.find_element(By.CSS_SELECTOR, "input[name='q3'][value='Y']")
                q3_agree.click()
                print("滿意度調查通知: 同意")
            else:
                q3_disagree = self.driver.find_element(By.CSS_SELECTOR, "input[name='q3'][value='N']")
                q3_disagree.click()
                print("滿意度調查通知: 不同意")
        except NoSuchElementException:
            print("未找到滿意度調查通知選項，跳過")

    def submit_form(self):
        """提交表單"""
        try:
            print("準備提交表單...")
            
            # 尋找掛號按鈕 (實際按鈕名稱: myButton, 值: 掛號)
            submit_button = self.driver.find_element(By.NAME, "myButton")
            submit_button.click()
            
            print("已點選掛號按鈕")
            
            # 等待頁面回應
            time.sleep(3)
            
            # 檢查是否有成功訊息或錯誤訊息
            try:
                # 檢查是否有提示訊息
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"系統訊息: {alert_text}")
                alert.accept()
                return True
            except:
                # 沒有 alert，檢查頁面內容變化
                current_url = self.driver.current_url
                print(f"當前頁面: {current_url}")
                
                # 檢查頁面是否有成功或錯誤訊息
                page_source = self.driver.page_source
                if "成功" in page_source or "完成" in page_source:
                    print("掛號成功！")
                    return True
                elif "錯誤" in page_source or "失敗" in page_source:
                    print("掛號失敗，請檢查填寫內容")
                    return False
                else:
                    print("表單已提交，請查看頁面結果")
                    return True
            
        except Exception as e:
            print(f"提交表單時發生錯誤: {e}")
            return False

    def run(self):
        """執行主要流程"""
        try:
            print("啟動 VGH 自動掛號系統...")
            
            # 檢查必要的環境變數
            if not self.registration_url:
                print("錯誤: 請在 .env 文件中設定 REGISTRATION_URL")
                return False
            
            if not all([self.user_data['id_number'], self.user_data['name'], 
                       self.user_data['birth_date'], self.user_data['phone']]):
                print("錯誤: 請在 .env 文件中設定完整的個人資料")
                return False
            
            # 設置瀏覽器
            self.setup_driver()
            
            # 開啟掛號頁面
            print(f"正在開啟掛號頁面: {self.registration_url}")
            self.driver.get(self.registration_url)
            
            # 等待頁面載入
            time.sleep(3)
            
            # 尋找並點選可用時段
            if not self.find_and_click_radio_button():
                return False
            
            # 填寫表單
            if not self.fill_form():
                return False
            
            # 檢查是否為自動模式
            if self.auto_mode:
                print("自動模式：直接提交表單")
                if self.submit_form():
                    print("掛號完成！")
                    return True
                else:
                    print("提交失敗")
                    return False
            else:
                # 手動確認模式
                try:
                    confirm = input("是否要提交表單？(y/N): ").strip().lower()
                    if confirm == 'y':
                        if self.submit_form():
                            print("掛號完成！")
                            return True
                        else:
                            print("提交失敗")
                            return False
                    else:
                        print("已取消提交，請手動檢查表單內容")
                        try:
                            input("按 Enter 鍵關閉瀏覽器...")
                        except EOFError:
                            time.sleep(5)
                        return True
                except EOFError:
                    print("自動取消提交，表單內容已填寫完成")
                    time.sleep(5)
                    return True
                
        except Exception as e:
            print(f"執行過程中發生錯誤: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()


def main():
    """主函數"""
    bot = VGHRegistrationBot()
    success = bot.run()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()