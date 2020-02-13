#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Chosen Shows Scraper
# Jonathan Rodiger - 2019

driver = webdriver.Chrome()

with open('showlist.csv', 'w') as out:
	out.write('EVENT NAME\tVENUE NAME\tORGANIZER NAME\tSTART DATE\tSTART TIME\tEND DATE\tEND TIME\tALL DAY EVENT\tCATEGORIES\tEVENT COST\tEVENT WEBSITE\tSHOW MAP LINK?\tSHOW MAP?\tEVENT DESCRIPTION\tDetails\tAttendance\tgcal_start\tgcal_stop\n')
	with open('event_links.txt', 'r') as f:
		for line in f:
			url = line.strip('\n')
			driver.get(url)

			print(url)

			# event name
			try:
				event_name = driver.find_element_by_id("seo_h1_tag").get_attribute("textContent")
				print('event name:')
				print(event_name)
			except:
				event_name = ''

			# time + date
			try:
				time_date = driver.find_element_by_class_name('_5xhk').get_attribute("textContent")
				print('time and date:')
				print(time_date)
				# TODO: check if at shows up twice (event over multiple days)
				# TODO: strip time zone info from end time
				start_date = time_date.split(' at ')[0]
				end_date = start_date
				start_time, end_time = time_date.split(' at ')[1].split(' – ')
				end_time = end_time.split(' ')
				end_time = end_time[0] + ' ' + end_time[1]
			except:
				start_time = ''
				end_time = ''

			# time + date gcal format
			try:
				time_date_gcal = driver.find_element_by_class_name('_5xhk').get_attribute("content")
				print('time and date gcal:')
				print(time_date_gcal)
				if 'to' in time_date_gcal:
					start_date_time_gcal, end_date_time_gcal = time_date_gcal.split(' to ')
				else:
					start_date_time_gcal = time_date_gcal
					end_date_time_gcal = time_date_gcal
			except:
				start_date_time_gcal = ''
				end_date_time_gcal = ''

			# venue name
			try:
				venue = driver.find_element_by_xpath("//a[@class='_5xhk']").get_attribute("textContent")
			except:
				try:
					venue = driver.find_element_by_xpath("//span[@class='_5xhk'][1]").get_attribute("textContent")
				except:
					venue = ''
			print('venue:')
			print(venue)

			# address
			try:
				address = driver.find_element_by_xpath("//*[@id='u_0_k']/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div/div").get_attribute("textContent")
				print('address:')
				print(address)
			except:
				address = ''

			# description
			try:
				description = driver.find_element_by_class_name('_63ew').get_attribute("textContent")
				# print('description:')
				# print(description)
			except:
				description = ''

			print('\n')

			# write event info
			out.write('\t'.join([event_name,venue,'',start_date,start_time,end_date,end_time,'','','',url,address,'','',description,'',start_date_time_gcal,end_date_time_gcal]) + '\n')
