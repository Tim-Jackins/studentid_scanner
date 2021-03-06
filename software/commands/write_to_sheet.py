import time
import argparse
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

start_time = time.time()

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-n', '--name', required=False, default='John Doe', help='Name of the student you want to document')
ap.add_argument('-i', '--id', required=False, default='12345678', help='ID# of the student you want to document')
ap.add_argument('-t', '--transition', required=False, default='Exiting', help='The transition state of the student (either Entering or Exiting)')
ap.add_argument('-e', '--error', required=False, default='False', help='Whether there is an error (either True or False)')
ap.add_argument('-em', '--err_message', required=False, default='', help='An explanation of the error (an error message or a read out of what the scanner picked up)')
ap.add_argument('-ex', '--err_exception', required=False, default='', help='The literal error message')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
name = str(args['name'])
studentid = str(args['id'])
transition = str(args['transition'])
error = bool(args['error'])
err_message = str(args['err_message'])
err_exception = str(args['err_exception'])

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
home_directory = 'jtimmins'
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/{0}/.credentials/client_id.json'.format(home_directory), scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(os.environ['student_id_SPREADSHEET_TOKEN']).sheet1

current_datetime = time.strftime("%I:%M:%S") + time.strftime("%d/%m/%Y")

infoToWrite = []

if error:
	infoToWrite.append(current_datetime)
	infoToWrite.append(name)
	infoToWrite.append(studentid)
	infoToWrite.append(transition)
else:
	infoToWrite.append(current_datetime)
	infoToWrite.append('ERROR')
	infoToWrite.append(err_message)
	infoToWrite.append(err_exception)

row = len(sheet.col_values(1)) + 1

for i in range(len(infoToWrite)):
	#print(infoToWrite[i])
	sheet.update_acell(chr(65 + i) + str(row), str(infoToWrite[i]))

print('Finished in {0}'.format(round(time.time() - start_time, 2)))