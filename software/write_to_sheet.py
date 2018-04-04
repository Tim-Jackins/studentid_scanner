import time
import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=False, default='John Doe', help='Name of student you want to document')
ap.add_argument("-i", "--id", required=False, default='01134', help='ID # of that student')
ap.add_argument("-t", "--transition", required=False, default='Exiting', help='Transitioning')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
name = args['name']
studentid = args['id']
transition = args['transition']

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_id.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key('16Raypiv_F8OfcykO2V-4ToXJf2CYSo2ziBE4CNMVmxQ').sheet1

#print (time.strftime("%H:%M:%S")) 
## 12 hour format ##
current_datetime = time.strftime("%I:%M:%S") + time.strftime("%d/%m/%Y")

infoToWrite = []
infoToWrite.append(current_datetime)
infoToWrite.append(name)
infoToWrite.append(studentid)
infoToWrite.append(transition)

count = 1
while not sheet.acell('A' + str(count)).value == '':
	print(count)
	count += 1
row = count

for i in range(len(infoToWrite)):
	#print('{0}{1} data: {2}'.format(chr(65 + i), 1, info[i]))
	print(infoToWrite[i])
	sheet.update_acell(chr(65 + i) + str(row), str(infoToWrite[i]))

#print(sheet.acell('A2').value == '')
#print(type(sheet.acell('A1').value))










