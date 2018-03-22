import time
import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, default='John Doe', help='Name of student you want to document')
ap.add_argument("-i", "--id", required=True, default='01134', help='ID # of that student')
ap.add_argument("-t", "--transition", required=True, default='Exiting', help='Transitioning')
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
infoToWrite[0].append(current_datetime)
infoToWrite[0].append(name)
infoToWrite[0].append(studentid)
infoToWrite[0].append(transition)

columns = []
for i in range(len(infoToWrite)):
	columns.append(chr(65 + i))

count = 1

for row in range(len(infoToWrite)):
	for col, info in zip(columns, infoToWrite[row]):
		sheet.update_acell(col + row, info)

print(sheet.range('A1:A5'))












