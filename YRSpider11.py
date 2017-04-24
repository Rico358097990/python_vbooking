#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Vbooking:
	
	def __init__(self, ytime):
		self.orDown = True
		self.meNum = 0
		self.driver = webdriver.Chrome()
		self.windowTime = datetime.datetime.now() - datetime.timedelta(days=ytime)
	
	def getWanted(self, page_source):
		pattern = re.compile('<td class="td2">(.*?) .*?<br /></td>',re.S)
		result = re.findall(pattern,page_source)
		for r in result:
			self.timeComp(r)
		#print result.group(1)  #测试输出

	
	def getMeLabel(self,driver):
		elements = driver.find_elements(By.CLASS_NAME, 'icon_mycp01')
		print len(elements)
		self.meNum = self.meNum + len(elements)
		

	def getPage(self,driver):
		self.getMeLabel(driver)
		self.getWanted(driver.page_source)
		
	def nextPage(self,driver):
		element = driver.find_element_by_id("next_id")
		if element:
			element.click()
		else:
			self.orDown = False
		
		
	def timeComp(self, t1):
		strpTime = datetime.datetime.strptime(t1, "%Y-%m-%d")
		print strpTime, self.windowTime
		if strpTime < self.windowTime:
			self.orDown = False
		else:
			pass
		
	
	def start(self):
		self.driver.get("http://vbooking.ctrip.com/")
		element = self.driver.find_element_by_name("txtOperid")
		element.clear
		element.send_keys("UID_M415845707")
		
		element2 = self.driver.find_element_by_name("txtPwd")
		element2.clear
		element2.send_keys("dm@223355")
		
		element3 = self.driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
		element3.send_keys(Keys.RETURN)
		
		
		element4 = WebDriverWait(self.driver, 0.2).until(
            EC.visibility_of_element_located((By.ID,"ctl00_liDingzhi")))
		element4.click()
		
		element5 = WebDriverWait(self.driver, 0.2).until(
            EC.visibility_of_element_located((By.ID,"head_OrderProcess")))
		element5.click()
		
		
		#print self.driver.page_source
		try:
			while self.orDown:
				self.getPage(self.driver)
				self.nextPage(self.driver)
				
		finally:
			print self.meNum
			self.driver.close()

			
		
		
if __name__ == "__main__":
	ytime = int(raw_input("请输入要查询多少天前的数据，以天为单位-->"))
	vb = Vbooking(ytime)
	vb.start()

	