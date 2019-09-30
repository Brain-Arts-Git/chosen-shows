from bs4 import BeautifulSoup
import requests

##########################
## Chosen Shows Scraper ##
## -------------------- ##
## Jon Rodiger  -  2019 ##
##########################

with open('showlist.csv', 'w') as out:
	out.write('EVENT NAME\tVENUE NAME\tORGANIZER NAME\tSTART DATE\tSTART TIME\tEND DATE\tEND TIME\tALL DAY EVENT\tCATEGORIES\tEVENT COST\tEVENT WEBSITE\tSHOW MAP LINK?\tSHOW MAP?\tEVENT DESCRIPTION\tDetails\tAttendance\n')
	with open('event_links.txt', 'r') as f:
		for line in f:
			url = line.strip()

			# load html w/ requests
			response = requests.get(url, timeout=5)

			# parse page content w/ beatiful soup
			soup = BeautifulSoup(response.content, 'html.parser')
			pretty_html = str(soup.prettify())

			# event name
			event_name = soup.select('#seo_h1_tag')[0].get_text()

			# venue name
			venue_name = pretty_html.split('"Place","name":"')[1].split('"')[0]

			# address
			address = pretty_html.split('</a><div class="_5xhp fsm fwn fcg">')[1].split('</div>')[0]

			# event description
			description = pretty_html.split('}},"description":"')[1].split('","image":"')[0]
			description = description.replace('\\/', '/')

			# start date + time
			start_date_time = pretty_html.split(',"startDate":"')[1].split('"')[0]
			start_date, start_time = start_date_time.split('T')
			start_time = start_time.split('-')[0]

			# end date + time
			end_date_time = pretty_html.split('"endDate":"')[1].split('"')[0]
			end_date, end_time = end_date_time.split('T')
			end_time = end_time.split('-')[0]

			# write event info
			out.write('\t'.join([event_name,venue_name,'',start_date,start_time,end_date,end_time,'','','',url,'','','',description,'']) + '\n')

print('Success!')
