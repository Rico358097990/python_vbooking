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
		self.page = 2
	
	def getWanted(self, page_source):
		pattern = re.compile('<div class="grab_icon_div">.*?</div>.*?<td class="td2">(.*?)<br></td>',re.S)
		result = re.findall(pattern,page_source)
		print result
		#for r in result:
			#print r
			#self.timeComp(r[1])
			#self.getMeLabel(r, page_source)
		#print result.group(1)  #测试输出

	
	def getMeLabel(self,r,page_source):
		str = '<i class="label icon_mycp01" title="我的产品">我的产品</i>'
		paStr = '<div class="order_detail">.*?<div class="grab_icon_div">(.*?)</div>.*?<td class="td2">"' + r + '".*?</div>'
		pattern = re.compile(paStr,re.S)
		result = re.search(pattern,page_source)
		if result:
			print result.group(1).strip()
		

	def getPage(self,driver):
		self.getWanted(driver.page_source)
		
	def nextPage(self,driver):
		element = driver.find_element_by_id("next_id")
		if element:
			element.click()
			try:
				while True:
					pattern = re.compile('<a.*?class="current".*?>(.*?)</a>',re.S)
					result = re.search(pattern,driver.page_source)
					#print result.group(1).strip()
					if self.page == int(result.group(1).strip()):
						self.page = self.page + 1
						break
			finally:
				pass
		else:
			self.orDown = False
		
		
	def timeComp(self, t1):
		strpTime = datetime.datetime.strptime(t1, "%Y-%m-%d  %H:%M:%S")
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
		
		
		element4 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID,"ctl00_liDingzhi")))
		element4.click()
		
		element5 = WebDriverWait(self.driver, 10).until(
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

	