#Define global variables
__version__ = "1.1.2"
is_all_fine = True
is_good_rec_available = False
error_text = ""
valid_records = 0
has_phone = False
campaigns_array = []
template = []
import_array = []
contacts_array = []
ucce_username = "username@domain (with dots)"
ucce_pass = "password"
ucce_server = "server@domain (with dots)"
ucce_sql_username = "domain\\username"
ucce_sql_pass = "password"
ucce_sql_enable = False
ucce_sql_NT_auth = True
ucce_sql_port = "1433"
ucce_instance = ""

#Try to load all necessary libs
from PyQt5 import QtWidgets,QtGui #GUI
from PyQt5.QtCore import Qt #id in listWidgetItems
from PyQt5.QtCore import QTimer #make buttons temporary disabled
from datetime import date, time, datetime, timedelta #compare dates
import requests #HTTP
from vi_utils import * #Global functions 4 this project
from im_GUI import Ui_MainWindow, About_Dialog, Connection_Dialog

class CampaignManagerApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self): #Initialize Main Window
		super().__init__()
		self.setupUi(self)  #Initialize main window
		
		global is_all_fine, error_text, ucce_username, ucce_pass, ucce_server
		global ucce_sql_username, ucce_sql_pass, ucce_sql_enable, ucce_sql_NT_auth
		global ucce_instance, ucce_sql_port
		need_fill_connections = False
		
		#Connect About window to menu
		self.action_About.triggered.connect(self.open_about_dialog)
		#Connect Connection window to menu
		self.action_Settings.triggered.connect(self.open_connection_dialog)
		
		print("Try to open connection.bin")
		data_file = open_file("connection.bin")
		if data_file == -1:
			is_all_fine = False
			error_text = 'File "connection.bin" not found'
		elif data_file == -2:
			is_all_fine = False
			error_text = 'Error while opening "connection.bin"'
		else:
			error_text = 'Successfully'
		print(error_text)
		print("========================")
		if data_file == -1 or data_file == -2:
			print("Ask to make new file")
			FileNotFoundMessageBox = QtWidgets.QMessageBox()
			FileNotFoundMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
			FileNotFoundMessageBox.setWindowTitle("File not found")
			FileNotFoundMessageBox.setText(error_text + " Create new empty one?")
			YesButton = FileNotFoundMessageBox.addButton('Yes', QtWidgets.QMessageBox.AcceptRole)
			NoButton = FileNotFoundMessageBox.addButton('No', QtWidgets.QMessageBox.RejectRole)
			FileNotFoundMessageBox.exec()
			if FileNotFoundMessageBox.clickedButton() == YesButton:
				ucce_sql_username = getUser_name()
				ucce_sql_credentials = fromUserPass2Credentials(ucce_sql_username,ucce_sql_pass)
				text = encrypt_data(fromUserPass2Credentials("username@domain (with dots)","password"),
					"server@domain (with dots)",str(ucce_sql_enable),str(ucce_sql_NT_auth),
					ucce_sql_credentials,ucce_instance,ucce_sql_port)
				if text == -1:
					error_text = "Cann't load host's information"
					is_all_fine = False
				elif text == -2:	
					is_all_fine = False
					error_text = "Error encrypt data"
				else:
					is_all_fine = save_file("connection.bin",text)					
				if is_all_fine:
					error_text = 'File "connection.bin" created successfully'
					try:
						data_file = open_file("connection.bin")
						decrypted_text = decrypt_data(data_file)
						connection_data = load_connection_data(decrypted_text)
						is_all_fine = connection_data["is_all_fine"]
						error_text = connection_data["error_text"]						
					except:
						pass
					need_fill_connections = True
				else:
					error_text = 'Error creating file "connection.bin"'
				print(error_text)
			else:
				print("Not accepted by user")
			print("========================")
		else:
			print("Try to decrypt file")
			is_all_fine = True
			decrypted_text = decrypt_data(data_file)
			if decrypted_text == -2:
				is_all_fine = False
				error_text = 'Error opening file "connection.bin". Perhaps it created for different host or user. '
				error_text = error_text + 'You need create new one via "Connection\Settings"'
				print(error_text)
				print("========================")
				print("Ask to make new file")
				FileNotDecryptedMessageBox = QtWidgets.QMessageBox()
				FileNotDecryptedMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
				FileNotDecryptedMessageBox.setWindowTitle("File not found")
				FileNotDecryptedMessageBox.setText('Error opening file "connection.bin".'
					'Perhaps it created for different host or user. Create empty one?')
				YesButton = FileNotDecryptedMessageBox.addButton('Yes', QtWidgets.QMessageBox.AcceptRole)
				NoButton = FileNotDecryptedMessageBox.addButton('No', QtWidgets.QMessageBox.RejectRole)
				FileNotDecryptedMessageBox.exec()
				if FileNotDecryptedMessageBox.clickedButton() == YesButton:
					ucce_sql_username = getUser_name()
					ucce_sql_credentials = fromUserPass2Credentials(ucce_sql_username,ucce_sql_pass)
					text = encrypt_data(fromUserPass2Credentials("username@domain (with dots)","password"),
						"server@domain (with dots)",str(ucce_sql_enable),str(ucce_sql_NT_auth),
						ucce_sql_credentials,ucce_instance,ucce_sql_port)
					if text == -1:
						error_text = "Cann't load host's information"
						is_all_fine = False
					elif text == -2:	
						is_all_fine = False
						error_text = "Error encrypt data"
					else:
						is_all_fine = save_file("connection.bin",text)					
					if is_all_fine:
						error_text = 'File "connection.bin" created successfully'
						try:
							data_file = open_file("connection.bin")
							decrypted_text = decrypt_data(data_file)
							connection_data = load_connection_data(decrypted_text)
							is_all_fine = connection_data["is_all_fine"]
							error_text = connection_data["error_text"]							
						except:
							pass
						need_fill_connections = True
					else:
						error_text = 'Error creating file "connection.bin"'
					print(error_text)
				else:
					print("Not accepted by user")
				print("========================")					
			elif decrypted_text == -1:
				is_all_fine = False
				error_text = "Cann't load this host's information"
				print(error_text)
				print("========================")			
			else:
				print("Successfully")
				print("========================")			
				connection_data = load_connection_data(decrypted_text)
				is_all_fine = connection_data["is_all_fine"]
				error_text = connection_data["error_text"]				
		if is_all_fine:
			ucce_username = connection_data["ucce_username"]
			ucce_pass = connection_data["ucce_pass"]
			ucce_server = connection_data["ucce_server"]
			ucce_sql_enable = connection_data["ucce_sql_enable"]
			ucce_sql_NT_auth = connection_data["ucce_sql_NT_auth"]
			ucce_sql_username = connection_data["ucce_sql_username"]
			ucce_sql_pass = connection_data["ucce_sql_pass"]
			ucce_instance = connection_data["ucce_instance"]
			ucce_sql_port = connection_data["ucce_sql_port"]
			#Filters activation
			self.comboBox_Filter.currentIndexChanged.connect(self.comboFilter_changed)
			self.comboBox_Condition.currentIndexChanged.connect(self.comboCondition_changed)
			#Retrieve button activation
			self.pushButton_Retrieve.clicked.connect(self.clicked_retrieve)
			self.pushButton_Retrieve.setEnabled(True)
			#Link function for Load File button
			self.pushButton_LoadFile.clicked.connect(self.clicked_load_file)
			#Link function for Validate button
			self.pushButton_Validate.clicked.connect(self.clicked_validate)
			#Link function for Clear button
			self.pushButton_Clear.clicked.connect(self.clicked_clear)
			#Link function for DelRow button
			self.pushButton_DelRow.clicked.connect(self.clicked_del_row)
			#Link function for AddRow button
			self.pushButton_AddRow.clicked.connect(self.clicked_add_row)				
			#Link function for tableWidget itemsSelected
			self.tableWidget_Import.itemSelectionChanged.connect(self.tableWidget_Import_ItemSelected)			
			#Statusbar
			self.statusbar.setStyleSheet("color:green;font-weight:bold;")
			self.statusbar.showMessage("All's fine. Current version of application: " + __version__)
		else:
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
			self.statusbar.showMessage(error_text)
		if need_fill_connections:
			self.statusbar.showMessage("File created successfully. Current version of application: " + __version__)
			self.open_connection_dialog()

	def closeEvent(self,event): #Try to close dialogs windows if main one closed with cross
		print("Main window closed with cross")
		try:
			self.dialog_connect.close()
			print("dialog_connect closed successfully")	
		except:
			pass
		try:
			self.dialog_about.close()
			print("dialog_about closed successfully")
		except:
			pass
		print("========================")

#Part 1. HTTP functions:
	def ucce_http_request(self,url): #HTTP GET request
		global ucce_username,ucce_pass,ucce_server, is_all_fine,error_text
		response = None
		is_all_fine = False
		try:
			response = requests.get("https://" + ucce_server + url, 
				auth=(ucce_username, ucce_pass), verify=False)
			error_text = "Successfull"
			is_all_fine = True
		except requests.exceptions.Timeout:
			# Maybe set up for a retry, or continue in a retry loop
			error_text = "Timeout"
		except requests.exceptions.TooManyRedirects:
			# Tell the user their URL was bad and try a different one
			error_text = "TooManyRedirects"
		except requests.exceptions.HTTPError:
			error_text = "HTTPError"
		except requests.exceptions.SSLError:
			# Certificate
			error_text = "SSLError"
		except Exception as err:
			# catastrophic error.
			error_text = str(err)
		return response

	def get_template (self,url): #Get template for imports
		global template, is_all_fine, error_text
		template = []
		is_all_fine = True
		error_text = "Successful"
		try:
			response = self.ucce_http_request(url) #make http request
			header = response.content.decode().splitlines()[0] #Get header (to string, split to array, get 1st row)
			template = header.split(",")
		except Exception as err:
			error_text = str(err)
			is_all_fine = False

	def get_campaigns(self,url): #Get Campaigns
		global ucce_username,ucce_pass,ucce_server
		global is_all_fine, error_text, campaigns_array
		campaigns_array = []
		is_all_fine = True
		error_text = ""
		while not (url is None) and is_all_fine:
			try:
				response = self.ucce_http_request(url) #make http request
				url = None #And clear url for loop avoid
				if response is None:
					error_text = "Error: " + error_text
					is_all_fine = False
				elif response.status_code == 401:   #unauthorized
					error_text = str(response.status_code) + " - " + response.reason
					error_text = error_text + ". Please, check connections properties (Connection\Settings)"
					is_all_fine = False
				elif response.status_code == 200: #all's fine
					error_text = "Data recieved successfully"
				else:
					is_all_fine = False
					error_text = str(response.status_code) + " - " + response.reason
			except Exception as err:
				is_all_fine = False
				error_text = "Error while calling 'ucce_http_request': " + str(err)
				
			if is_all_fine: 
				try:
					root = ElementTree.fromstring(response.content)
					campaigns = root.find('campaigns')
					nextPage = root.find('pageInfo').find('nextPage')
					#get campaigns list					
					for campaign in campaigns:
						campaing_array = []
						campaign_id = campaign.find('refURL').text
						campaign_id = campaign_id[campaign_id.find('/campaign/') + len('/campaign/'):]
						refURL = campaign.find('refURL').text
						changeStamp = campaign.find('changeStamp').text
						abandonEnabled = campaign.find('abandonEnabled').text
						abandonPercent = campaign.find('abandonPercent').text
						amdTreatmentMode = campaign.find('amdTreatmentMode').text
						e_campaignPrefix = campaign.find('campaignPrefix')
						if not (e_campaignPrefix is None):
							campaignPrefix = e_campaignPrefix.text
						else:
							campaignPrefix = ""
						campaignPurposeType = campaign.find('campaignPurposeType').text
						cpa_enabled = campaign.find('callProgressAnalysis').find('enabled').text
						cpa_record = campaign.find('callProgressAnalysis').find('record').text
						cpa_minSilencePeriod = campaign.find('callProgressAnalysis').find('minSilencePeriod').text
						cpa_analysisPeriod = campaign.find('callProgressAnalysis').find('analysisPeriod').text
						cpa_minimumValidSpeech = campaign.find('callProgressAnalysis').find('minimumValidSpeech').text
						cpa_maxTimeAnalysis = campaign.find('callProgressAnalysis').find('maxTimeAnalysis').text
						cpa_maxTermToneAnalysis = campaign.find('callProgressAnalysis').find('maxTermToneAnalysis').text
						e_description = campaign.find('description')
						if not (e_description is None):
							description = e_description.text
						else:
							description = ""
						e_dialingMode = campaign.find('dialingMode')
						if not (e_dialingMode is None):
							dialingMode = e_dialingMode.text
						else:
							dialingMode = "INBOUND"						
						enabled = campaign.find('enabled').text
						endDate = campaign.find('endDate').text
						endTime = campaign.find('endTime').text
						ipAmdEnabled = campaign.find('ipAmdEnabled').text
						ipTerminatingBeepDetect = campaign.find('ipTerminatingBeepDetect').text
						linesPerAgent = campaign.find('linesPerAgent').text
						maxAttempts = campaign.find('maxAttempts').text
						maximumLinesPerAgent = campaign.find('maximumLinesPerAgent').text
						minimumCallDuration = campaign.find('minimumCallDuration').text
						name = campaign.find('name').text
						noAnswerRingLimit = campaign.find('noAnswerRingLimit').text
						personalizedCallbackEnabled = campaign.find('personalizedCallbackEnabled').text
						predictiveCorrectionPace = campaign.find('predictiveCorrectionPace').text
						predictiveGain = campaign.find('predictiveGain').text
						rescheduleCallbackMode = campaign.find('rescheduleCallbackMode').text
						e_reservationPercentage = campaign.find('reservationPercentage')
						if not (e_reservationPercentage is None):
							reservationPercentage = e_reservationPercentage.text
						else:
							reservationPercentage = "0"	
						answeringMachineDelay = campaign.find('retries').find('answeringMachineDelay').text
						busySignalDelay = campaign.find('retries').find('busySignalDelay').text
						customerAbandonedDelay = campaign.find('retries').find('customerAbandonedDelay').text
						customerNotHomeDelay = campaign.find('retries').find('customerNotHomeDelay').text
						dialerAbandonedDelay = campaign.find('retries').find('dialerAbandonedDelay').text
						noAnswerDelay = campaign.find('retries').find('noAnswerDelay').text
						startDate = campaign.find('startDate').text
						startTime = campaign.find('startTime').text
						timeZone_URL = campaign.find('timeZone').find('refURL').text
						timeZone_Name = campaign.find('timeZone').find('displayName').text

						#fill array of campaigns
						campaing_array = [campaign_id,name,refURL,changeStamp,abandonEnabled,abandonPercent,
						amdTreatmentMode,campaignPrefix,campaignPurposeType,cpa_enabled,cpa_record,cpa_minSilencePeriod,
						cpa_analysisPeriod,cpa_minimumValidSpeech,cpa_maxTimeAnalysis,cpa_maxTermToneAnalysis,
						description,dialingMode,enabled,endDate,endTime,ipAmdEnabled,ipTerminatingBeepDetect,
						linesPerAgent,maxAttempts,maximumLinesPerAgent,minimumCallDuration,noAnswerRingLimit,
						predictiveCorrectionPace,predictiveGain,rescheduleCallbackMode,reservationPercentage,
						answeringMachineDelay,busySignalDelay,customerAbandonedDelay,customerNotHomeDelay,
						dialerAbandonedDelay,noAnswerDelay,startDate,startTime,timeZone_URL,timeZone_Name,
						personalizedCallbackEnabled]
						campaigns_array.append(campaing_array)
					#is there more campaigns? If yes, recieve them data too
					if not (nextPage is None):
						url = nextPage.text
						url = url[url.find('/unifiedconfig'):]
				except Exception as err:
					error_text = "Error while parsing campaigns data" + str(err)
					is_all_fine = False

	def ucce_http_import(self,url,value): #Import
		global ucce_username,ucce_pass,ucce_server
		import_result = ""
		try:
			response = requests.post("https://" + ucce_server + url, 
				auth=(ucce_username, ucce_pass), headers = {"Content-Type": "application/xml"}, 
				data = value, verify=False)
			if response.status_code == 200: 	#All's fine
				import_result = "200 - successful"
			elif response.status_code == 400:	#Need to parse body
				try:
					import_result = str(response.status_code) + " - " + response.reason + ":"
					root = ElementTree.fromstring(response.content)
					for apiError in root:
						error_text = apiError.find('errorMessage').text
						error_text = ' '.join(error_text.strip().split('\n'))
						import_result += "\n\t" + error_text
				except:
					import_result = str(response.status_code) + " - " + response.reason		
			elif response.status_code == 503:	#Need to parse body
				import_result = str(response.status_code) + " - " + response.reason + "\n"
				import_result += "More then 30 requests in queue. Try again later."
			else:								#Another error
				import_result = str(response.status_code) + " - " + response.reason
		except requests.exceptions.Timeout:
			# Maybe set up for a retry, or continue in a retry loop
			import_result = "Timeout"
		except requests.exceptions.TooManyRedirects:
			# Tell the user their URL was bad and try a different one
			import_result = "TooManyRedirects"
		except requests.exceptions.HTTPError:
			import_result = "HTTPError"
		except requests.exceptions.SSLError:
			# Certificate
			import_result = "SSLError"
		except:
			# catastrophic error.
			import_result = "Other error"
		return import_result
	
	def ucce_http_del(self,value): #Clear import
		global ucce_username,ucce_pass,ucce_server
		del_result = ""
		try:
			response = requests.delete("https://" + ucce_server + value, 
				auth=(ucce_username, ucce_pass), verify=False)
			if response.status_code == 200: 	#All's fine
				del_result = "200 - successful"
			elif response.status_code == 400:	#Need to parse body
				try:
					del_result = str(response.status_code) + " - " + response.reason + ":"
					root = ElementTree.fromstring(response.content)
					for apiError in root:
						error_text = apiError.find('errorMessage').text
						error_text = ' '.join(error_text.strip().split('\n'))
						del_result += "\n\t" + error_text
				except:
					del_result = str(response.status_code) + " - " + response.reason		
			else:								#Another error
				del_result = str(response.status_code) + " - " + response.reason
		except requests.exceptions.Timeout:
			# Maybe set up for a retry, or continue in a retry loop
			del_result = "Timeout"
		except requests.exceptions.TooManyRedirects:
			# Tell the user their URL was bad and try a different one
			del_result = "TooManyRedirects"
		except requests.exceptions.HTTPError:
			del_result = "HTTPError"
		except requests.exceptions.SSLError:
			# Certificate
			del_result = "SSLError"
		except:
			# catastrophic error.
			del_result = "Other error"
		return del_result

	def ucce_http_get_status(self,url): #Get contacts with status
		global ucce_username,ucce_pass,ucce_server,contacts_array
		status_result = ""
		contacts_array = []
		is_all_fine = True
		
		while not (url is None) and is_all_fine:
			try:
				response = self.ucce_http_request(url) #make http request
				url = None #And clear url for loop avoid
				if response.status_code == 401:   #unauthorized
					status_result = str(response.status_code) + " - " + response.reason
					status_result = status_result + ". Please, check connections properties (Connection\Settings)"
					is_all_fine = False
				elif response.status_code == 200: #all's fine
					status_result = "200 - successful"
				else:
					is_all_fine = False
					status_result = str(response.status_code) + " - " + response.reason				
			except requests.exceptions.Timeout:
				# Maybe set up for a retry, or continue in a retry loop
				status_result = "Timeout"
				is_all_fine = False
			except requests.exceptions.TooManyRedirects:
				# Tell the user their URL was bad and try a different one
				status_result = "TooManyRedirects"
				is_all_fine = False
			except requests.exceptions.HTTPError:
				status_result = "HTTPError"
				is_all_fine = False
			except requests.exceptions.SSLError:
				# Certificate
				status_result = "SSLError"
				is_all_fine = False
			except:
				# catastrophic error.
				status_result = "Other error"
				is_all_fine = False
			
			if is_all_fine: 
				try:
					root = ElementTree.fromstring(response.content)
					contacts = root.find('importContacts')
					nextPage = root.find('pageInfo').find('nextPage')
					#get contacts data					
					for contact in contacts:
						contact_array = []
						contact_id = contact.find('refURL').text
						contact_id = contact_id[contact_id.find('/import/') + len('/import/'):]	
						contact_id = int(contact_id)
						refURL = contact.find('refURL').text
						e_accountNumber = contact.find('accountNumber')
						if not (e_accountNumber is None):
							accountNumber = e_accountNumber.text
						else:
							accountNumber = ""						
						callsMade = contact.find('callsMade').text
						callStatus = contact.find('callStatus').text
						callResultOverall = contact.find('callResultOverall').text
						e_firstName = contact.find('firstName')
						if not (e_firstName is None):
							firstName = e_firstName.text
						else:
							firstName = ""						
						e_lastName = contact.find('lastName')
						if not (e_lastName is None):
							lastName = e_lastName.text
						else:
							lastName = ""						
						importDate = contact.find('importDate').text
						e_phone01 = contact.find('phone01')
						if not (e_phone01 is None):
							phone01_callResult = e_phone01.find('callResult').text
							phone01_dstObserved = e_phone01.find('dstObserved').text
							phone01_gmtOffset = e_phone01.find('gmtOffset').text
							phone01_number = e_phone01.find('number').text
						else:
							phone01_callResult = ""
							phone01_dstObserved = ""
							phone01_gmtOffset = ""
							phone01_number = ""
						e_phone02 = contact.find('phone02')
						if not (e_phone02 is None):
							phone02_callResult = e_phone02.find('callResult').text
							phone02_dstObserved = e_phone02.find('dstObserved').text
							phone02_gmtOffset = e_phone02.find('gmtOffset').text
							phone02_number = e_phone02.find('number').text
						else:
							phone02_callResult = ""
							phone02_dstObserved = ""
							phone02_gmtOffset = ""
							phone02_number = ""						
						e_phone03 = contact.find('phone03')
						if not (e_phone03 is None):
							phone03_callResult = e_phone03.find('callResult').text
							phone03_dstObserved = e_phone03.find('dstObserved').text
							phone03_gmtOffset = e_phone03.find('gmtOffset').text
							phone03_number = e_phone03.find('number').text
						else:
							phone03_callResult = ""
							phone03_dstObserved = ""
							phone03_gmtOffset = ""
							phone03_number = ""						
						e_phone04 = contact.find('phone04')
						if not (e_phone04 is None):
							phone04_callResult = e_phone04.find('callResult').text
							phone04_dstObserved = e_phone04.find('dstObserved').text
							phone04_gmtOffset = e_phone04.find('gmtOffset').text
							phone04_number = e_phone04.find('number').text
						else:
							phone04_callResult = ""
							phone04_dstObserved = ""
							phone04_gmtOffset = ""
							phone04_number = ""						
						e_phone05 = contact.find('phone05')
						if not (e_phone05 is None):
							phone05_callResult = e_phone05.find('callResult').text
							phone05_dstObserved = e_phone05.find('dstObserved').text
							phone05_gmtOffset = e_phone05.find('gmtOffset').text
							phone05_number = e_phone05.find('number').text
						else:
							phone05_callResult = ""
							phone05_dstObserved = ""
							phone05_gmtOffset = ""
							phone05_number = ""						
						e_phone06 = contact.find('phone06')
						if not (e_phone06 is None):
							phone06_callResult = e_phone06.find('callResult').text
							phone06_dstObserved = e_phone06.find('dstObserved').text
							phone06_gmtOffset = e_phone06.find('gmtOffset').text
							phone06_number = e_phone06.find('number').text
						else:
							phone06_callResult = ""
							phone06_dstObserved = ""
							phone06_gmtOffset = ""
							phone06_number = ""
						e_phone07 = contact.find('phone07')
						if not (e_phone07 is None):
							phone07_callResult = e_phone07.find('callResult').text
							phone07_dstObserved = e_phone07.find('dstObserved').text
							phone07_gmtOffset = e_phone07.find('gmtOffset').text
							phone07_number = e_phone07.find('number').text
						else:
							phone07_callResult = ""
							phone07_dstObserved = ""
							phone07_gmtOffset = ""
							phone07_number = ""
						e_phone08 = contact.find('phone08')
						if not (e_phone08 is None):
							phone08_callResult = e_phone08.find('callResult').text
							phone08_dstObserved = e_phone08.find('dstObserved').text
							phone08_gmtOffset = e_phone08.find('gmtOffset').text
							phone08_number = e_phone08.find('number').text
						else:
							phone08_callResult = ""
							phone08_dstObserved = ""
							phone08_gmtOffset = ""
							phone08_number = ""
						e_phone09 = contact.find('phone09')
						if not (e_phone09 is None):
							phone09_callResult = e_phone09.find('callResult').text
							phone09_dstObserved = e_phone09.find('dstObserved').text
							phone09_gmtOffset = e_phone09.find('gmtOffset').text
							phone09_number = e_phone09.find('number').text
						else:
							phone09_callResult = ""
							phone09_dstObserved = ""
							phone09_gmtOffset = ""
							phone09_number = ""
						e_phone10 = contact.find('phone10')
						if not (e_phone10 is None):
							phone10_callResult = e_phone10.find('callResult').text
							phone10_dstObserved = e_phone10.find('dstObserved').text
							phone10_gmtOffset = e_phone10.find('gmtOffset').text
							phone10_number = e_phone10.find('number').text
						else:
							phone10_callResult = ""
							phone10_dstObserved = ""
							phone10_gmtOffset = ""
							phone10_number = ""
						contact_array = [contact_id,refURL,accountNumber,callsMade,
						callStatus,callResultOverall,firstName,lastName,importDate,
						phone01_callResult,phone01_dstObserved,phone01_gmtOffset,phone01_number,
						phone02_callResult,phone02_dstObserved,phone02_gmtOffset,phone02_number,
						phone03_callResult,phone03_dstObserved,phone03_gmtOffset,phone03_number,
						phone04_callResult,phone04_dstObserved,phone04_gmtOffset,phone04_number,
						phone05_callResult,phone05_dstObserved,phone05_gmtOffset,phone05_number,
						phone06_callResult,phone06_dstObserved,phone06_gmtOffset,phone06_number,
						phone07_callResult,phone07_dstObserved,phone07_gmtOffset,phone07_number,
						phone08_callResult,phone08_dstObserved,phone08_gmtOffset,phone08_number,
						phone09_callResult,phone09_dstObserved,phone09_gmtOffset,phone09_number,
						phone10_callResult,phone10_dstObserved,phone10_gmtOffset,phone10_number]
						contacts_array.append(contact_array)
					#is there more contacts?  If yes, recieve them data too
					if not (nextPage is None):
						url = nextPage.text
						url = url[url.find('/unifiedconfig'):]
				except Exception as err:
					status_result = "Error while parsing contacts data"
					print(str(err))
					is_all_fine = False
		return status_result

#Part 2. Business logic functions:
	def check_filter_campaigns(self): #Validate campaign's filters
			is_filter_fine = True
			error_text = "Successfully"
			CurrentText_Filter = str(self.comboBox_Filter.currentText())
			CurrentText_Value = str(self.comboBox_Value.currentText())
			if CurrentText_Filter in ["Campaign Name"]:
				if len(CurrentText_Value) > 32:
					is_filter_fine = False
					error_text = "Length of Campaign's Name in filter"
					error_text += " couldn't be greater than 32 symbols."
				else:
					is_filter_fine = True
			elif CurrentText_Filter in ["Campaign Description"]:
				if len(CurrentText_Value) > 255:
					is_filter_fine = False
					error_text = "Length of Campaign's Description in filter"
					error_text += " couldn't be greater than 255 symbols."
				elif len(CurrentText_Value) == 0:
					is_filter_fine = False
					error_text = "Please type a valid value in the filter"
				else:
					is_filter_fine = True				
			elif CurrentText_Filter in ["Campaign Prefix Digits"]:
				if len(CurrentText_Value) > 15:
					is_filter_fine = False
					error_text = "Length of Campaign's Prefix in filter"
					error_text += " couldn't be greater than 15 symbols."
				elif len(CurrentText_Value) == 0:
					is_filter_fine = False
					error_text = "Please type a valid value in the filter"
				elif CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols are allowed in"
					error_text += " Campaign's Prefix in filter."
				else:
					is_filter_fine = True				
			elif CurrentText_Filter in ["Lines Per Agent","Maximum Lines Per Agent"]:
				try:
					CurrentText_Value = CurrentText_Value.replace(",",".")
					CurrentText_Value = float(CurrentText_Value)
					is_filter_fine = True
				except:
					is_filter_fine = False
					error_text = "Lines and Maximum Lines Per Agent in filter"
					error_text += " could contain only numeric symbols, dot and comma."	
				if is_filter_fine:
					if CurrentText_Value > 100 or CurrentText_Value < 1:
						is_filter_fine = False
						error_text = "Lines and Maximum Per Agent in filter"
						error_text += " could be in range 1 - 100."	
					else:
						is_filter_fine = True
			elif CurrentText_Filter in ["Minimum Call Duration"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols are allowed in Minimum Call Duration in filter."
				else:
					if int(CurrentText_Value) > 10 or int(CurrentText_Value) < 0:
						is_filter_fine = False
						error_text = "Minimum Call Duration in filter could be in range 0 - 10."					
					else:
						is_filter_fine = True			
			elif CurrentText_Filter in ["Abandon Calls Limit Percent"]:
				try:
					CurrentText_Value = CurrentText_Value.replace(",",".")
					CurrentText_Value = float(CurrentText_Value)
					is_filter_fine = True
				except:
					is_filter_fine = False
					error_text = "Abandon Calls Limit Percent in filter could"
					error_text += " contain only numeric symbols, dot and comma."	
				if is_filter_fine:
					if CurrentText_Value > 100 or CurrentText_Value < 0:
						is_filter_fine = False
						error_text = "Abandon Calls Limit Percent in filter could be in range 0 - 100."	
					else:
						is_filter_fine = True			
			elif CurrentText_Filter in ["No Answer Ring Limit"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols are allowed in No Answer Ring Limit in filter."
				else:
					if int(CurrentText_Value) > 10 or int(CurrentText_Value) < 2:
						is_filter_fine = False
						error_text = "No Answer Ring Limit in filter could be in range 2 - 10."					
					else:
						is_filter_fine = True	
			elif CurrentText_Filter in ["Maximum Attempts"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols are allowed in Maximum Attempts in filter."
				else:
					if int(CurrentText_Value) > 100 or int(CurrentText_Value) < 1:
						is_filter_fine = False
						error_text = "Maximum Attempts in filter could be in range 1 - 100."					
					else:
						is_filter_fine = True
			elif CurrentText_Filter in ["No Answer Delay","Busy Signal Delay"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols are allowed in Time Delay fields in filter."
				else:
					if int(CurrentText_Value) > 999999 or int(CurrentText_Value) < 1:
						is_filter_fine = False
						error_text = "No Answer and Busy Signal Delays in filter could be in range 1 - 999999."					
					else:
						is_filter_fine = True
			elif CurrentText_Filter in ["Dialer Abandoned Delay","Customer Abandoned Delay","Answering Machine Delay"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols are allowed in Time Delay fields in filter."
				else:
					if int(CurrentText_Value) > 99999 or int(CurrentText_Value) < 1:
						is_filter_fine = False
						error_text = "Dialer Abandoned, Customer Abandoned and Answering Machine"
						error_text += " Delays in filter could be in range 1 - 99999."					
					else:
						is_filter_fine = True			
			elif CurrentText_Filter in ["Start Date","End Date"]:
				try:
					year,month,day = CurrentText_Value.split('-')
					date(int(year),int(month),int(day))
					is_filter_fine = True
				except:
					is_filter_fine = False
					error_text = "Incorrect Start or End Date. Correct format is YYYY-MM-DD."					
			elif CurrentText_Filter in ["Start Hours","End Hours"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols could be in Hours in filter."
				else:
					if int(CurrentText_Value) > 23 or int(CurrentText_Value) < 0:
						is_filter_fine = False
						error_text = "Hours in filter could be in range 0 - 23."					
					else:
						is_filter_fine = True
			elif CurrentText_Filter in ["Start Minutes","End Minutes"]:
				if CurrentText_Value.isnumeric() == False:
					is_filter_fine = False
					error_text = "Only numeric symbols could be in Minutes in filter."
				else:
					if int(CurrentText_Value) > 59 or int(CurrentText_Value) < 0:
						is_filter_fine = False
						error_text = "Minutes in filter could be in range 0 - 59."					
					else:
						is_filter_fine = True
			if not is_filter_fine:
				#Error message
				FilterErrorMessageBox = QtWidgets.QMessageBox()
				FilterErrorMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
				FilterErrorMessageBox.setWindowTitle("Incorrect filter")
				FilterErrorMessageBox.setText(error_text)
				YesButton = FilterErrorMessageBox.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
				FilterErrorMessageBox.exec()
			return is_filter_fine, error_text

	def filter_campaigns(self): #Apply campaign's filter
		global campaigns_array
		CurrentText_Filter = str(self.comboBox_Filter.currentText())
		CurrentText_Condition = str(self.comboBox_Condition.currentText())
		CurrentText_Value = str(self.comboBox_Value.currentText())
		if CurrentText_Filter in ["Campaign Enable","Abandon Calls Limit Enable","Personalized Callback",
			"Enable CPA","Enable IP AMD"]:
			if CurrentText_Filter == "Campaign Enable":
				index = 18
			elif CurrentText_Filter == "Abandon Calls Limit Enable":
				index = 4
			elif CurrentText_Filter == "Personalized Callback":
				index = 42
			elif CurrentText_Filter == "Enable CPA":
				index = 9
			elif CurrentText_Filter == "Enable IP AMD":
				index = 21
			if CurrentText_Condition == "Equal":
				if CurrentText_Value == "Checked":
					for campaign in deepcopy(campaigns_array):
						if campaign[index] != "true":
							campaigns_array.remove(campaign)
				elif CurrentText_Value == "Not Checked":
					for campaign in deepcopy(campaigns_array):
						if campaign[index] == "true":
							campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Not Equal":
				if CurrentText_Value == "Checked":
					for campaign in deepcopy(campaigns_array):
						if campaign[index] == "true":
							campaigns_array.remove(campaign)	
				elif CurrentText_Value == "Not Checked":
					for campaign in deepcopy(campaigns_array):
						if campaign[index] != "true":
							campaigns_array.remove(campaign)							
		elif CurrentText_Filter in ["Campaign Name","Campaign Description","Campaign Prefix Digits"]:
			if CurrentText_Filter == "Campaign Name":
				index = 1
			elif CurrentText_Filter == "Campaign Description":
				index = 16
			elif CurrentText_Filter == "Campaign Prefix Digits":
				index = 7
			if CurrentText_Condition == "Contains":
				for campaign in deepcopy(campaigns_array):
					if CurrentText_Value not in campaign[index]:
						campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Ends With":
				for campaign in deepcopy(campaigns_array):
					if  campaign[index][-len(CurrentText_Value):] != CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Starts With":
				for campaign in deepcopy(campaigns_array):
					if  campaign[index][:len(CurrentText_Value)] != CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Is Blank":
				for campaign in deepcopy(campaigns_array):
					if  campaign[index] != "":
						campaigns_array.remove(campaign)
		elif CurrentText_Filter in ["Dialing Mode","Campaign Type"]:
			if CurrentText_Filter == "Dialing Mode":
				index = 17
			elif CurrentText_Filter == "Campaign Type":
				index = 8
			if CurrentText_Condition == "Equal":		
				for campaign in deepcopy(campaigns_array):
					if campaign[index] != CurrentText_Value:
						campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Not Equal":
				for campaign in deepcopy(campaigns_array):
					if campaign[index] == CurrentText_Value:
						campaigns_array.remove(campaign)
		elif CurrentText_Filter in ["Lines Per Agent","Maximum Lines Per Agent","Minimum Call Duration",
			"Abandon Calls Limit Percent","No Answer Ring Limit","Maximum Attempts","Dialer Abandoned Delay",
			"No Answer Delay","Busy Signal Delay","Customer Abandoned Delay","Answering Machine Delay"]:
			CurrentText_Value = float(CurrentText_Value.replace(',', '.'))
			if CurrentText_Filter == "Lines Per Agent":
				index = 23
			elif CurrentText_Filter == "Maximum Lines Per Agent":
				index = 25
			elif CurrentText_Filter == "Minimum Call Duration":
				index = 26
			elif CurrentText_Filter == "Abandon Calls Limit Percent":
				index = 5
			elif CurrentText_Filter == "No Answer Ring Limit":
				index = 27
			elif CurrentText_Filter == "Maximum Attempts":
				index = 24
			elif CurrentText_Filter == "Dialer Abandoned Delay":
				index = 36
			elif CurrentText_Filter == "No Answer Delay":
				index = 37
			elif CurrentText_Filter == "Busy Signal Delay":
				index = 33
			elif CurrentText_Filter == "Customer Abandoned Delay":
				index = 34
			elif CurrentText_Filter == "Answering Machine Delay":
				index = 32
			if CurrentText_Condition == "Equal":
				for campaign in deepcopy(campaigns_array):
					if float(campaign[index]) != CurrentText_Value:
						campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Greater Then":
				for campaign in deepcopy(campaigns_array):
					if  float(campaign[index]) <= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Less Then":
				for campaign in deepcopy(campaigns_array):
					if  float(campaign[index]) >= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Not Equal":
				for campaign in deepcopy(campaigns_array):
					if  CurrentText_Value == float(campaign[index]):
						campaigns_array.remove(campaign)		
		elif CurrentText_Filter in ["Start Date","End Date"]:
			CurrentText_Value = date(int(CurrentText_Value[:4]),int(CurrentText_Value[5:7]),int(CurrentText_Value[8:]))
			if CurrentText_Filter == "Start Date":
				index = 38
			elif CurrentText_Filter == "End Date":
				index = 19
			if CurrentText_Condition == "Equal":
				for campaign in deepcopy(campaigns_array):
					campaign_Date = date(int(campaign[index][:4]),int(campaign[index][5:7]),int(campaign[index][8:]))
					if campaign_Date != CurrentText_Value:
						campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Greater Then":
				for campaign in deepcopy(campaigns_array):
					campaign_Date = date(int(campaign[index][:4]),int(campaign[index][5:7]),int(campaign[index][8:]))
					if  campaign_Date <= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Less Then":
				for campaign in deepcopy(campaigns_array):
					campaign_Date = date(int(campaign[index][:4]),int(campaign[index][5:7]),int(campaign[index][8:]))
					if  campaign_Date >= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Not Equal":
				for campaign in deepcopy(campaigns_array):
					campaign_Date = date(int(campaign[index][:4]),int(campaign[index][5:7]),int(campaign[index][8:]))
					if  campaign_Date == CurrentText_Value:
						campaigns_array.remove(campaign)
		elif CurrentText_Filter in ["Start Hours","End Hours"]:
			CurrentText_Value = int(float(CurrentText_Value.replace(',', '.')))
			if CurrentText_Filter == "Start Hours":
				index = 39
			elif CurrentText_Filter == "End Hours":
				index = 20
			if CurrentText_Condition == "Equal":
				for campaign in deepcopy(campaigns_array):
					if int(campaign[index][:campaign[index].find(":")]) != CurrentText_Value:
						campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Greater Then":
				for campaign in deepcopy(campaigns_array):
					if  int(campaign[index][:campaign[index].find(":")]) <= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Less Then":
				for campaign in deepcopy(campaigns_array):
					if  int(campaign[index][:campaign[index].find(":")]) >= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Not Equal":
				for campaign in deepcopy(campaigns_array):
					if  int(campaign[index][:campaign[index].find(":")]) == CurrentText_Value:
						campaigns_array.remove(campaign)
		elif CurrentText_Filter in ["Start Minutes","End Minutes"]:
			CurrentText_Value = int(float(CurrentText_Value.replace(',', '.')))
			if CurrentText_Filter == "Start Minutes":
				index = 39
			elif CurrentText_Filter == "End Minutes":
				index = 20
			if CurrentText_Condition == "Equal":
				for campaign in deepcopy(campaigns_array):
					if int(campaign[index][campaign[index].find(":")+1:]) != CurrentText_Value:
						campaigns_array.remove(campaign)				
			elif CurrentText_Condition == "Greater Then":
				for campaign in deepcopy(campaigns_array):
					if  int(campaign[index][campaign[index].find(":")+1:]) <= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Less Then":
				for campaign in deepcopy(campaigns_array):
					if  int(campaign[index][campaign[index].find(":")+1:]) >= CurrentText_Value:
						campaigns_array.remove(campaign)
			elif CurrentText_Condition == "Not Equal":
				for campaign in deepcopy(campaigns_array):
					if  int(campaign[index][campaign[index].find(":")+1:]) == CurrentText_Value:
						campaigns_array.remove(campaign)

	def campaign_selected(self, item = None): #Campaign is selected in Campaign's list
		global campaigns_array, valid_records, has_phone
		print('Clear fields')
		self.selected_CampaignClear()
		print("========================")
		if item is None:
			item = self.listWidget_Campaigns_List.currentItem()
		for list_item in self.listWidget_Campaigns_List.findItems("*", Qt.MatchWildcard):
			font = list_item.font() #Current font
			font.setBold(False)
			list_item.setFont(font) #Clear bold for all elements
		font = self.listWidget_Campaigns_List.currentItem().font()
		font.setBold(True)
		self.listWidget_Campaigns_List.currentItem().setData(Qt.FontRole, font) #And add to current
		selected_campaign_id = item.data(Qt.UserRole)
		print('Campaign with id ' + selected_campaign_id + ' selected')
		print("========================")
		self.statusbar.showMessage("")
		self.pushButton_Import.clicked.connect(lambda: self.clicked_import(selected_campaign_id))
		self.pushButton_ClearImport.clicked.connect(lambda: self.clicked_clear_import(selected_campaign_id))
		self.pushButton_ClearImport.setEnabled(True)
		self.pushButton_Download.clicked.connect(lambda: self.clicked_download(selected_campaign_id))		
		self.pushButton_Download.setEnabled(True)
		if valid_records > 0 and has_phone:
			self.pushButton_Import.setEnabled(True)
			self.checkBox_Overwrite.setEnabled(True)
        
	def log_result (self,import_result): #Log imports result to file
		current_date = str(datetime.today().strftime('%Y%m%d'))
		current_campaign = self.listWidget_Campaigns_List.currentItem()
		import_result = "============================================================================\n" + import_result
		import_result = str(datetime.now().strftime('%H:%M:%S')) + " Logging" + import_result
		if current_campaign is None:
			current_campaign = "none"
		else:
			current_campaign = current_campaign.text()
		log_file_name = "logs/" + current_date + "/" + current_date + "_" + current_campaign + ".txt"			
		save_file (log_file_name,import_result,"a+")
		
#Part 4. GUI functions:
#=============Modal Windows=============================#
	def open_about_dialog(self): #----------------
		self.dialog_about = AboutDialogNew()
		Text = "API Import Manager\n"
		Text += "Developed by Viktor84e\n"
		Text += "E-mail for contact or donate: Viktor84e@gmail.com\n\n"
		Text += "Libraries used and licensing information:\n"
		Text += "==================================\n"
		Text += "|  Module:                         |  Version: |         License:        |\n"
		Text += "|------------------------------------------------------------------|\n"
		Text += "|  Python                          |  3.8.1     |           PSFL            |\n"
		Text += "|  PyQt5                           |  5.13.2   |      GNU GPL v3      |\n"
		Text += "|  requests                       |  2.23.0   | Apache License v2 |\n"
		Text += "|  cryptography               |  2.8        | Apache License v2 |\n"
		Text += "|------------------------------------------------------------------|\n"
		Text += "| API Import Manager      |  " + __version__ + "    |       GNU GPL v3     |\n"
		Text += "==================================\n\n"
		Text += "Sourсe url: "
		self.dialog_about.label.setText(Text)
		Text = '<a href="https://github.com/Viktor-84e/API-Import-Manager">https://github.com/Viktor-84e/API-Import-Manager</a>'		
		self.dialog_about.label2.setText(Text)
		self.dialog_about.label2.setOpenExternalLinks(True)
		self.dialog_about.show()

	def open_connection_dialog(self):
		global ucce_username, ucce_pass, ucce_server, ucce_sql_port, ucce_instance
		global ucce_sql_username, ucce_sql_pass, ucce_sql_enable, ucce_sql_NT_auth
		self.dialog_connect = ConnectionDialogNew()

		try:
			self.dialog_connect.buttonBox.clicked.disconnect()
		except:
			pass
		
		if ucce_username is None:
			ucce_username = ""
		if ucce_username is None:
			ucce_pass = ""	
		if ucce_server is None:
			ucce_pass = ""						
		if ucce_sql_username is None:
			ucce_pass = ""	
		if ucce_sql_pass is None:
			ucce_pass = ""
		if ucce_sql_port is None:
			ucce_sql_port = ""
		if ucce_instance is None:
			ucce_instance = ""
		if ucce_username.find('@') > 0:
			self.dialog_connect.lineEdit_username.setText(ucce_username[:ucce_username.find('@')])
			self.dialog_connect.lineEdit_domain.setText(ucce_username[ucce_username.find('@') + 1:])
		else:
			self.dialog_connect.lineEdit_username.setText(ucce_username)
			self.dialog_connect.lineEdit_domain.setText("")			

		self.dialog_connect.lineEdit_pass.setText(ucce_pass)
		self.dialog_connect.lineEdit_server.setText(ucce_server)
		self.dialog_connect.buttonBox.clicked.connect(self.clicked_save_connect)
		self.dialog_connect.show()
		
	def clicked_save_connect(self):
		global ucce_username, ucce_pass, ucce_server, is_all_fine, error_text
		global ucce_sql_username, ucce_sql_pass, ucce_sql_enable, ucce_sql_NT_auth
		global ucce_sql_port, ucce_instance
		print("Save connection settings")
		newusername = self.dialog_connect.lineEdit_username.text()
		newdomain = self.dialog_connect.lineEdit_domain.text()
		ucce_pass = self.dialog_connect.lineEdit_pass.text()
		ucce_server = self.dialog_connect.lineEdit_server.text()		
		if len(newdomain) > 0:
			ucce_username = newusername + "@" + newdomain
		else:
			ucce_username = newusername
		ucce_credentials = fromUserPass2Credentials(ucce_username,ucce_pass)
		ucce_sql_credentials = fromUserPass2Credentials(ucce_sql_username,ucce_sql_pass)
		text = encrypt_data(ucce_credentials,ucce_server,str(ucce_sql_enable),
			str(ucce_sql_NT_auth),ucce_sql_credentials,ucce_instance,ucce_sql_port)
		if text == -1:
			error_text = "Cann't load host's information"
			is_all_fine = False
		elif text == -2:	
			is_all_fine = False
			error_text = "Error encrypt data"
		else:
			is_all_fine = save_file("connection.bin",text)					
		if is_all_fine:
			error_text = "Data saved successfully."
			self.pushButton_Retrieve.setEnabled(True)
			try:
				self.pushButton_Retrieve.clicked.disconnect()
			except:
				pass
			self.pushButton_Retrieve.clicked.connect(self.clicked_retrieve)
			self.statusbar.setStyleSheet("color:green;font-weight:bold;")
		else:
			error_text = 'Error while saving "connection.bin"'
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
		self.statusbar.showMessage(error_text)
		print(error_text)
		print("========================")

#=======================================================#
	def selected_CampaignClear(self): #Clear Campaign Detail window
		self.pushButton_Import.setEnabled(False)
		self.checkBox_Overwrite.setEnabled(False)		
		try:
			self.pushButton_Import.clicked.disconnect()
		except:
			pass
		self.pushButton_ClearImport.setEnabled(False)
		try:
			self.pushButton_ClearImport.clicked.disconnect()
		except:
			pass
		self.pushButton_Download.setEnabled(False)		
		try:
			self.pushButton_Download.clicked.disconnect()
		except:
			pass			
		
	def fill_ListWidgetItem(self, campaign_id = ""): #Fill campaign list with names & ids
		global campaigns_array
		for campaign in campaigns_array:
			ListWidgetItem = QtWidgets.QListWidgetItem(campaign[1])
			ListWidgetItem.setData(Qt.UserRole,campaign[0])
			self.listWidget_Campaigns_List.addItem(ListWidgetItem)
			if campaign_id == campaign[0]: 				#If selected element is predefined
				self.listWidget_Campaigns_List.setCurrentItem(ListWidgetItem)
				self.campaign_selected(ListWidgetItem)

	def fill_tableImportHeader(self): #Fill table header with data from template
		global template
		self.tableWidget_Import.setColumnCount(len(template)+1)
		self.tableWidget_Import.setRowCount(1)
		TableWidgetItem = QtWidgets.QTableWidgetItem() #=========
		TableWidgetItem.setText("Validation") #=========
		TableWidgetItem.setFlags(TableWidgetItem.flags() ^ Qt.ItemIsEditable) #=========
		self.tableWidget_Import.setItem(0,0,TableWidgetItem) #=========		
		TableWidgetColumn = 0
		for HeaderColumn in template:
			#Drop-down header
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)] = QtWidgets.QComboBox()
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].addItem("IGNORE")
			for HeaderColumn2 in template:
				globals()["self.tableWidget_Import" + str(TableWidgetColumn)].addItem(HeaderColumn2)
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].currentIndexChanged.connect(
				self.comboBox_Import_changed)
			self.tableWidget_Import.setCellWidget(0,TableWidgetColumn+1, globals()[
				"self.tableWidget_Import" + str(TableWidgetColumn)])
			TableWidgetColumn += 1
		self.tableWidget_Import.resizeColumnsToContents()

	def fill_tableImport(self,xfile): #Fill table with loaded from file data
		global import_array, template
		print("Loading data")
		import_result = "Loading file: " + xfile + "\n" 
		import_bad = 0
		import_good = 0
		try:
			self.tableWidget_Import.itemChanged.disconnect()
		except:
			pass
		current_option_array = []
		for TableWidgetColumn in range (len(template)): #Get all current selected values
			current_option = globals()["self.tableWidget_Import" + str(TableWidgetColumn)].currentText()
			current_option_array.append(current_option)
		
		filtered_current_option_array = current_option_array[:] #get number of selected fields 
		for element in current_option_array:
			if element == "IGNORE":
				filtered_current_option_array.remove("IGNORE")
		selected_fields_number = len(filtered_current_option_array)
		
		import_row_number = 0
		import_row_index = 0
		for import_row in import_array:
			if len(import_row) != selected_fields_number:
				import_result += "Row #" + str(import_row_number + 1) + " not loaded. "
				import_result += "Selected fields number (" + str(selected_fields_number) + ") "
				import_result += "doesn't match to real number (" + str(len(import_row)) + ") in row.\n"
				import_bad += 1
			else:
				TableWidgetRowCount = self.tableWidget_Import.rowCount()
				self.tableWidget_Import.setRowCount(TableWidgetRowCount + 1)
				for TableWidgetColumn in range (len(template)):
					if globals()["self.tableWidget_Import" + str(TableWidgetColumn)].currentText() != "IGNORE":
						TableWidgetItem = QtWidgets.QTableWidgetItem()
						TableWidgetItem.setText(import_row[import_row_index])
						self.tableWidget_Import.setItem(TableWidgetRowCount,TableWidgetColumn+1,TableWidgetItem)
						TableWidgetItemV = QtWidgets.QTableWidgetItem()
						TableWidgetItemV.setText("Not validate yet")
						TableWidgetItemV.setBackground(QtGui.QColor(255, 50, 50))
						TableWidgetItemV.setFlags(TableWidgetItemV.flags() ^ Qt.ItemIsEditable)
						self.tableWidget_Import.setItem(TableWidgetRowCount,0,TableWidgetItemV)
						import_row_index += 1
				import_result += "Row #" + str(import_row_number + 1) + " loaded successfully.\n"
				import_good += 1
			import_row_number += 1
			import_row_index = 0
		if import_good > 0:
			self.pushButton_Validate.setEnabled(True)
			self.pushButton_Clear.setEnabled(True)
		self.log_result (import_result)
		if import_row_number == import_good:
			self.statusbar.setStyleSheet("color:green;font-weight:bold;")
		elif import_good == 0:
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
		else:
			self.statusbar.setStyleSheet("color:GoldenRod;font-weight:bold;")
		self.tableWidget_Import.resizeColumnsToContents()
		#Link function for tableWidget itemChanged
		self.tableWidget_Import.itemChanged.connect(self.tableWidget_Import_ItemChanged)
		self.statusbar.showMessage("Imported " + str(import_good) + " from " + str(import_row_number) + " records")
		print(import_result)
		print("========================")
		
#============Clicked campaign's buttons=================#
	def clicked_retrieve(self): #Retrieve button clicked. Step one. Clear & disable Retrieve button
		is_filter_fine = True
		error_text = ""
		print("Validate campaign's filters")
		is_filter_fine, error_text = self.check_filter_campaigns()
		print(error_text)
		print("========================")
		if is_filter_fine:
			self.pushButton_Retrieve.setEnabled(False)
			self.tableWidget_Import.setColumnCount(0)
			self.tableWidget_Import.setRowCount(0)
		self.setCursor(Qt.WaitCursor)
		self.statusbar.setStyleSheet("color:GoldenRod;font-weight:bold;")
		self.statusbar.showMessage("It could take some time. Please wait")		
		QTimer.singleShot(300, lambda: self.clicked_retrieve2(is_filter_fine,error_text))

	def clicked_retrieve2(self,is_filter_fine,error_text_temp): #Retrieve button clicked. Step two. Get new data
		global is_all_fine, error_text
		if is_all_fine and is_filter_fine:
			error_text = error_text_temp
			print("Clear current campaigns list")
			self.listWidget_Campaigns_List.clear()
			self.selected_CampaignClear()
			print("========================")
		if is_all_fine and is_filter_fine:
			print("Get campaigns list")
			self.get_campaigns("/unifiedconfig/config/campaign?sort=name%20asc&resultsPerPage=100")
			print(error_text)
			print("========================")			
		if is_all_fine and is_filter_fine:
			print("Apply campaigns filter")
			self.filter_campaigns()
			print("========================")
		if is_all_fine and is_filter_fine:
			self.statusbar.setStyleSheet("color:green;font-weight:bold;")			
			print("Fill campaigns list")			
			self.fill_ListWidgetItem()
			self.listWidget_Campaigns_List.itemClicked.connect(self.campaign_selected)
			print("========================")
		else:
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
		if is_all_fine and is_filter_fine:
			print("Get template for imports")
			self.get_template("/unifiedconfig/config/campaign/import/template")
			print(error_text)
			print("========================")
			print("Fill Import table header")
			self.fill_tableImportHeader()
			print("========================")
			self.pushButton_LoadFile.setEnabled(True)
			self.pushButton_AddRow.setEnabled(True)
		self.statusbar.showMessage(error_text)
		self.setCursor(Qt.ArrowCursor)
		self.pushButton_Retrieve.setEnabled(True)

	def clicked_load_file(self): #Load import file
		global import_array
		import_array = []
		xfile, filters = QtWidgets.QFileDialog.getOpenFileName(self, "Select plain-text file with separators")
		load_result = -1
		if xfile:  #not to continue while file isn't selected
			import_file = open_file(xfile)
			if import_file == -1 or import_file == -2:
				self.statusbar.setStyleSheet("color:red;font-weight:bold;")
				self.statusbar.showMessage("Error while loading import file")
				load_result = -3
				print("Error opening file")		
			else:
				try:
					self.setCursor(Qt.WaitCursor)
					import_file = import_file.readlines()
					row_count = len(import_file)
					print("Loading data from file")
					self.statusbar.setStyleSheet("color:green;font-weight:bold;")
					self.statusbar.showMessage("")
					import_array = []
					Separator = self.lineEdit_Separator.text()
					if row_count > 10000:
						print("To many records. Ask to load first 10000")
						ImportMaxRecMessageBox = QtWidgets.QMessageBox()
						ImportMaxRecMessageBox.setIcon(QtWidgets.QMessageBox.Warning)
						ImportMaxRecMessageBox.setWindowTitle("File not found")
						ImportMaxRecMessageBox.setText('File is too large.\n'
							'You can import up to 10,000 records in one request.\n'
							'Load first 10,000 records?')
						YesButton = ImportMaxRecMessageBox.addButton('Yes', QtWidgets.QMessageBox.AcceptRole)
						NoButton = ImportMaxRecMessageBox.addButton('No', QtWidgets.QMessageBox.RejectRole)
						ImportMaxRecMessageBox.exec()
						if ImportMaxRecMessageBox.clickedButton() == YesButton:
							for index in range(10000):
								line = import_file[index].replace("\r","").replace("\n","")								
								if Separator == "\\t":
									import_array.append(line.split("\t"))
								else:
									import_array.append(line.split(Separator))
							load_result = len (import_array)
						else:
							self.statusbar.setStyleSheet("color:red;font-weight:bold;")
							self.statusbar.showMessage("Select a smaller file")
							print("Select a smaller file")
							load_result = -5						
					else:
						for line in import_file:
							line = line.replace("\r","").replace("\n","")
							if Separator == "\\t":
								import_array.append(line.split("\t"))	
							else:
								import_array.append(line.split(Separator))
						load_result = len (import_array)
					self.setCursor(Qt.ArrowCursor)
				except:
					self.statusbar.setStyleSheet("color:red;font-weight:bold;")
					self.statusbar.showMessage("Error while parcing import file")
					print("Error while parcing import file")
					load_result = -4					
		else:
			load_result = -2
			print("File not selected")
		if load_result > 0:
			self.statusbar.setStyleSheet("color:green;font-weight:bold;")
			self.statusbar.showMessage("")
			self.pushButton_Import.setEnabled(False)
			self.checkBox_Overwrite.setEnabled(False)			
			self.fill_tableImport(xfile)
		else:
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
			self.statusbar.showMessage("Error while loading import file or import file is empty")		
			print("0 records loaded")
		print("========================")

	def clicked_validate(self): #Validate loaded data
		global valid_records, has_phone
		has_phone = False
		total_records = 0
		valid_records = 0
		self.setCursor(Qt.WaitCursor)
		print("Validating")
		TableWidgetRowCount = self.tableWidget_Import.rowCount()
		TableWidgetColumnCount = self.tableWidget_Import.columnCount()
		for row in range(1,TableWidgetRowCount):
			isvalid = True
			column = 1
			if self.tableWidget_Import.item(row,0).text() != "Valid":
				while isvalid and column < TableWidgetColumnCount:
					header = globals()["self.tableWidget_Import" + str(column-1)].currentText()
					item = self.tableWidget_Import.item(row,column)
					if item == None:
						value = ""
					else:
						value = item.text()
					if header == "AccountNumber" and len(value) > 30:
						isvalid = False
						causeText = header + " > 30"
					elif (header == "FirstName" or header == "FirstName") and len(value) > 50:
						isvalid = False
						causeText = header + " > 50"
					elif header[:5] == "Phone":
						has_phone = True
						if len(value) > 20:
							isvalid = False
							causeText = header + " > 20"
						elif value.isnumeric() == False:
							isvalid = False
							causeText = header + " isn't numeric"						
					elif header == "TimeZoneBias" and value.isnumeric() == False:
						isvalid = False
						causeText = header + " isn't numeric"
					elif header == "TimeZoneBias":
						if  value.isnumeric() == False:
							isvalid = False
							causeText = header + " isn't numeric"
						elif int(value) not in range(-780,720):
							isvalid = False
							causeText = header + " not in (–780,720)" 
					elif header == "DstObserved" and value not in ("true","false"):
						isvalid = False
						causeText = header + " not in (true,false)"
					column += 1
			else:
				has_phone = True
			if isvalid:
				self.tableWidget_Import.item(row,0).setText("Valid")
				self.tableWidget_Import.item(row,0).setBackground(QtGui.QColor(50, 255, 50))
				valid_records += 1						
			else:
				self.tableWidget_Import.item(row,0).setText(causeText)
				self.tableWidget_Import.item(row,0).setBackground(QtGui.QColor(255, 50, 50))						
			total_records += 1
		if valid_records == total_records and has_phone:
			self.statusbar.setStyleSheet("color:green;font-weight:bold;")
			validate_result = "Valid are " + str(valid_records) + " from " + str(total_records) + " records"			
		elif valid_records == 0:
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
			validate_result = "Valid are " + str(valid_records) + " from " + str(total_records) + " records"
		elif has_phone == False:
			self.statusbar.setStyleSheet("color:red;font-weight:bold;")
			validate_result = "At least one Phone field is required in import"
		else:
			self.statusbar.setStyleSheet("color:GoldenRod;font-weight:bold;")
			validate_result = "Valid are " + str(valid_records) + " from " + str(total_records) + " records"
		campaign = self.listWidget_Campaigns_List.currentItem()
		if (campaign is not None) and valid_records > 0 and has_phone: #if campaign is selected enable import button
			self.pushButton_Import.setEnabled(True)
			self.checkBox_Overwrite.setEnabled(True)
		else:
			self.pushButton_Import.setEnabled(False)
			self.checkBox_Overwrite.setEnabled(False)
		self.tableWidget_Import.resizeColumnsToContents()
		self.statusbar.showMessage(validate_result)
		self.log_result (validate_result + "\n")
		print(validate_result)
		print("========================")
		self.setCursor(Qt.ArrowCursor)

	def clicked_import(self,campaignid): #Import validated data. Step one. Disable Import button
		self.pushButton_Import.setEnabled(False)
		self.checkBox_Overwrite.setEnabled(False)
		self.setCursor(Qt.WaitCursor)	
		self.statusbar.setStyleSheet("color:GoldenRod;font-weight:bold;")
		self.statusbar.showMessage("It could take some time. Please wait")	
		QTimer.singleShot(300, lambda: self.clicked_import2(campaignid))

	def clicked_import2(self,campaignid): #Import validated data. Step two
		global campaigns_array
		print("Get url for campaign" + str(campaignid))
		for campaign in campaigns_array: #get url for current campaignID
			if campaign[0] == campaignid:
				url = campaign[2] + "/import"
		print(url)
		print("========================")
		print("Collect data")
		RowCount = self.tableWidget_Import.rowCount()
		ColumnCount = self.tableWidget_Import.columnCount()
		headers = []
		for column in range(1,ColumnCount): #get current headers
			headers.append (globals()["self.tableWidget_Import" + str(column-1)].currentText())
		values = []
		for row in range(1,RowCount):  #get non-ignored valid values
			if self.tableWidget_Import.item(row,0).text() == "Valid":
				value = []
				for column in range(1,ColumnCount):
					if headers[column-1] != "IGNORE":
						if self.tableWidget_Import.item(row,column) is None:
							value.append("")
						else:
							value.append(self.tableWidget_Import.item(row,column).text())
				values.append(value)
		headers_result = []
		for header in headers:
			if header != "IGNORE":
				headers_result.append(header)
		values.insert(0,headers_result)
		print("========================")
		print("Forming import's body")
		if True: #Forming import's body
			import_body =  "<import>\n"
			import_body +=  "	<fileContent>\n"
			import_body +=  "		<![CDATA[\n"
			for import_row in values:
				import_body += "			" + ",".join(import_row) + "\n"
			import_body +=  "		]]>\n"
			import_body +=  "	</fileContent>\n"
			import_body +=  "	<delimiter>,</delimiter>\n"
			if self.checkBox_Overwrite.checkState() == 2:
				import_body +=  "	<overwriteData>true</overwriteData>\n"
			import_body +=  "</import>\n"
		print("========================")
		print("Starting import")
		import_result = self.ucce_http_import(url,import_body)
		print(import_result)
		print("========================")
		#Result message
		result_message = QtWidgets.QMessageBox()
		self.statusbar.setStyleSheet("color:Red;font-weight:bold;")		
		if import_result == "200 - successful": #success
			result_message.setIcon(QtWidgets.QMessageBox.Information)
			self.statusbar.setStyleSheet("color:Green;font-weight:bold;")
			self.statusbar.showMessage("Processed successfully")
			result_message.setWindowTitle("Processed successfully")	
			print("Clear successfully imported data")
			left_items = []			
			try:
				self.tableWidget_Import.itemChanged.disconnect()
			except:
				pass
			for row in range(1,RowCount): #Temp store non-Valid items
				if self.tableWidget_Import.item(row,0).text() != "Valid":
					left_item = []
					for column in range(self.tableWidget_Import.columnCount()):
						if self.tableWidget_Import.item(row,column) is not None:
							left_item.append(self.tableWidget_Import.item(row,column).clone())
						else:
							left_item.append(None)
					left_items.append(left_item)
			self.tableWidget_Import.setRowCount(1)		#Clear tableWidget_Import
			row = 1
			for stored_item in left_items:		#Restore non-Valid items in tableWidget_Import
				self.tableWidget_Import.setRowCount(self.tableWidget_Import.rowCount() + 1)
				column = 0
				for item in stored_item:
					if item is not None:
						self.tableWidget_Import.setItem(row,column,item)
					column += 1
				row += 1
			#Link function for tableWidget itemChanged
			self.tableWidget_Import.itemChanged.connect(self.tableWidget_Import_ItemChanged)
			self.tableWidget_Import.resizeColumnsToContents()
			print("========================")
		else:
			result_message.setIcon(QtWidgets.QMessageBox.Warning)
			result_message.setWindowTitle("Processed with errors")
			self.statusbar.showMessage("Processed with errors")			
		result_message.setText(import_result)
		self.log_result ("Import result: "+ import_result + "\n")
		self.setCursor(Qt.ArrowCursor)
		OkButton = result_message.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
		result_message.exec()

	def clicked_clear_import(self,campaignid): #Clear import. Step one. Disable Clear button
		self.pushButton_ClearImport.setEnabled(False)
		self.statusbar.setStyleSheet("color:GoldenRod;font-weight:bold;")
		self.statusbar.showMessage("It could take some time. Please wait")		
		self.setCursor(Qt.WaitCursor)		
		QTimer.singleShot(300, lambda: self.clicked_clear_import2(campaignid))

	def clicked_clear_import2(self,campaignid): #Clear import. Step two
		global campaigns_array
		print("Get url for campaign " + str(campaignid))
		for campaign in campaigns_array: #get url for current campaignID
			if campaign[0] == campaignid:
				url = campaign[2] + "/import"
		print(url)
		print("========================")
		print("Starting clear")
		clear_result = self.ucce_http_del(url)
		print(clear_result)
		print("========================")
		#Result message
		result_message = QtWidgets.QMessageBox()		
		if clear_result == "200 - successful": #success
			result_message.setIcon(QtWidgets.QMessageBox.Information)
			result_message.setWindowTitle("Processed successfully")
			self.statusbar.showMessage("Processed successfully")
			self.statusbar.setStyleSheet("color:Green;font-weight:bold;")			
		else:
			result_message.setIcon(QtWidgets.QMessageBox.Warning)
			self.statusbar.setStyleSheet("color:Red;font-weight:bold;")
			self.statusbar.showMessage("Processed with errors")
			result_message.setWindowTitle("Processed with errors")			
		result_message.setText(clear_result)
		OkButton = result_message.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
		self.log_result ("Clear import result: "+ clear_result + "\n")
		#self.pushButton_ClearImport.setEnabled(True) #it's not necessity to clear twice
		self.setCursor(Qt.ArrowCursor)
		self.statusbar.showMessage("It could take some time. Please wait")		
		result_message.exec()		

	def clicked_download(self,campaignid): #Download current status. Step one. Select file & Disable Download button
		xfile,xfilter = QtWidgets.QFileDialog.getSaveFileName(self, "Enter csv-file name", "", "plain text (*.csv);;plain text (*.txt)", "plain text (*.csv)")
		if xfile:  #not to continue while file isn't selected
			self.pushButton_Download.setEnabled(False)
			self.setCursor(Qt.WaitCursor)
			self.statusbar.setStyleSheet("color:GoldenRod;font-weight:bold;")
			self.statusbar.showMessage("It could take some time. Please wait")
			QTimer.singleShot(300, lambda: self.clicked_download2(campaignid,xfile))
		else:
			print("File not selected")

	def clicked_download2(self,campaignid,xfile): #Download current status. Step two
		global campaigns_array, contacts_array
		status_result = ""
		url = None
		print("Get url for campaign " + str(campaignid))
		for campaign in campaigns_array: #get url for current campaignID
			if campaign[0] == campaignid:
				url = campaign[2] + "/import?sort=accountNumber%20asc&resultsPerPage=100"
		print(url)
		print("========================")
		print("sending http request")
		status_result = self.ucce_http_get_status(url)
		print(status_result)
		print("========================")
		#Result message
		result_message = QtWidgets.QMessageBox()		
		result_message.setIcon(QtWidgets.QMessageBox.Warning)
		result_message.setWindowTitle("Processed with errors")
		self.statusbar.setStyleSheet("color:Red;font-weight:bold;")		
		if status_result == "200 - successful": #success
			print("saving file")
			file_text = "id,refURL,accountNumber,callsMade,"
			file_text += "callStatus,callResultOverall,firstName,lastName,importDate,"
			file_text += "phone01_callResult,phone01_dstObserved,phone01_gmtOffset,phone01_number,"
			file_text += "phone02_callResult,phone02_dstObserved,phone02_gmtOffset,phone02_number,"
			file_text += "phone03_callResult,phone03_dstObserved,phone03_gmtOffset,phone03_number,"
			file_text += "phone04_callResult,phone04_dstObserved,phone04_gmtOffset,phone04_number,"
			file_text += "phone05_callResult,phone05_dstObserved,phone05_gmtOffset,phone05_number,"
			file_text += "phone06_callResult,phone06_dstObserved,phone06_gmtOffset,phone06_number,"
			file_text += "phone07_callResult,phone07_dstObserved,phone07_gmtOffset,phone07_number,"
			file_text += "phone08_callResult,phone08_dstObserved,phone08_gmtOffset,phone08_number,"
			file_text += "phone09_callResult,phone09_dstObserved,phone09_gmtOffset,phone09_number,"
			file_text += "phone10_callResult,phone10_dstObserved,phone10_gmtOffset,phone10_number\n"			
			contacts_array.sort(key=lambda x: x[0]) #sorting by first (0) element of array (id)
			for contact in contacts_array:
				file_text += ','.join([str(elem) for elem in contact]) + "\n"
			file_text = file_text[:file_text.rfind("\n")]
			try:
				save_file (xfile,file_text)
				result_message.setIcon(QtWidgets.QMessageBox.Information)
				result_message.setWindowTitle("Processed successfully")
				status_result = "Results succesfully saved to file " + xfile
				self.statusbar.setStyleSheet("color:Green;font-weight:bold;")			
			except:
				status_result = "Error while saving file"
			print(status_result)
			print("========================")
		result_message.setText(status_result)				
		OkButton = result_message.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
		self.log_result ("Download current status: "+ status_result + "\n")			
		self.setCursor(Qt.ArrowCursor)
		self.pushButton_Download.setEnabled(True)
		self.statusbar.showMessage(status_result)		
		result_message.exec()

	def clicked_clear(self): #Clear loaded data
		self.setCursor(Qt.WaitCursor)
		print("Clear all data")
		self.tableWidget_Import.setRowCount(1)
		self.pushButton_Validate.setEnabled(False)
		self.pushButton_Clear.setEnabled(False)
		self.pushButton_DelRow.setEnabled(False)
		self.pushButton_Import.setEnabled(False)
		self.checkBox_Overwrite.setEnabled(False)
		self.tableWidget_Import.resizeColumnsToContents()
		self.statusbar.showMessage("")	
		print("========================")
		self.setCursor(Qt.ArrowCursor)

	def clicked_del_row(self): #Delete row
		global valid_records
		rows = []
		qlist = self.tableWidget_Import.selectedIndexes()
		for item in qlist:
			rows.append(item.row())
		rows = list(set(rows))
		if 0 in rows:
			rows.pop(0)
		rows.sort(reverse=True)	
		print("deleting " + str(len(rows)) + " rows")	
		for row in rows:
			if self.tableWidget_Import.item(row,0).text() == "Valid":
				valid_records -= 1	
			self.tableWidget_Import.removeRow(row)
		TableWidgetRowCount = self.tableWidget_Import.rowCount()
		print("check if there left some records")
		if TableWidgetRowCount < 2:
			self.pushButton_Validate.setEnabled(False)
			self.pushButton_Clear.setEnabled(False)
			self.pushButton_DelRow.setEnabled(False)
		if valid_records <= 0:
			self.pushButton_Import.setEnabled(False)
			self.checkBox_Overwrite.setEnabled(False)
		self.tableWidget_Import.resizeColumnsToContents()
		self.statusbar.showMessage("")
		print("========================")			

	def clicked_add_row(self): #Add row
		print("Add new row")
		TableWidgetRowCount = self.tableWidget_Import.rowCount()
		self.tableWidget_Import.setRowCount(TableWidgetRowCount + 1)
		TableWidgetItemV = QtWidgets.QTableWidgetItem()
		TableWidgetItemV.setText("Not validate yet")
		TableWidgetItemV.setBackground(QtGui.QColor(255, 50, 50))
		TableWidgetItemV.setFlags(TableWidgetItemV.flags() ^ Qt.ItemIsEditable)
		self.tableWidget_Import.setItem(TableWidgetRowCount,0,TableWidgetItemV)
		self.pushButton_Validate.setEnabled(True)
		self.tableWidget_Import.resizeColumnsToContents()
		self.statusbar.showMessage("")
		print("========================")	

#============Filters changed============================#
	def comboCondition_changed(self):
		CurrentText = str(self.comboBox_Condition.currentText())
		if CurrentText == "Is Blank":
			self.comboBox_Value.setCurrentText('')
			self.comboBox_Value.setEnabled(False)
		else:
			self.comboBox_Value.setEnabled(True)	

	def comboFilter_changed(self):
		CurrentText_Filter = str(self.comboBox_Filter.currentText())
		if CurrentText_Filter in ["Campaign Enable","Abandon Calls Limit Enable",
				"Personalized Callback","Enable CPA","Enable IP AMD"]:
			self.comboBox_Condition.setEnabled(True)
			self.comboBox_Condition.clear()
			self.comboBox_Condition.addItem("Equal")
			self.comboBox_Condition.addItem("Not Equal")
			self.comboBox_Value.setEnabled(True)
			self.comboBox_Value.setEditable(False)
			self.comboBox_Value.clear()			
			self.comboBox_Value.setStyleSheet("border: 1px solid gray;")
			self.comboBox_Value.addItem("Checked")
			self.comboBox_Value.addItem("Not Checked")
		elif CurrentText_Filter in ["Campaign Name","Campaign Description","Campaign Prefix Digits"]:
			self.comboBox_Condition.setEnabled(True)
			self.comboBox_Condition.clear()
			self.comboBox_Condition.addItem("Contains")
			self.comboBox_Condition.addItem("Ends With")
			self.comboBox_Condition.addItem("Starts With")
			self.comboBox_Condition.addItem("Is Blank")
			self.comboBox_Value.setEnabled(True)
			self.comboBox_Value.setEditable(True)
			self.comboBox_Value.clear()			
			self.comboBox_Value.setStyleSheet("QComboBox{border: 1px solid gray; background-color : white;}\n"
				"QComboBox::drop-down{border: 0px;}\n"
				"QComboBox::down-arrow{image: url(noimg);border-width: 0px;}")
		elif CurrentText_Filter == "Dialing Mode":
			self.comboBox_Condition.setEnabled(True)
			self.comboBox_Condition.clear()
			self.comboBox_Condition.addItem("Equal")
			self.comboBox_Condition.addItem("Not Equal")
			self.comboBox_Value.setEnabled(True)
			self.comboBox_Value.setEditable(False)
			self.comboBox_Value.clear()			
			self.comboBox_Value.setStyleSheet("border: 1px solid gray;")
			self.comboBox_Value.addItem("PREDICTIVEONLY")
			self.comboBox_Value.addItem("PROGRESSIVEONLY")
			self.comboBox_Value.addItem("PREVIEWONLY")
			self.comboBox_Value.addItem("PREVIEWDIRECTONLY")
			self.comboBox_Value.addItem("INBOUND")
		elif CurrentText_Filter in ["Lines Per Agent","Maximum Lines Per Agent","Minimum Call Duration",
				"Abandon Calls Limit Percent","No Answer Ring Limit","Maximum Attempts","Dialer Abandoned Delay",
				"No Answer Delay","Busy Signal Delay","Customer Abandoned Delay","Answering Machine Delay",
				"Start Hours","Start Minutes","Start Date","End Hours","End Minutes","End Date"]: 
			self.comboBox_Condition.setEnabled(True)
			self.comboBox_Condition.clear()
			self.comboBox_Condition.addItem("Equal")
			self.comboBox_Condition.addItem("Greater Then")
			self.comboBox_Condition.addItem("Less Then")
			self.comboBox_Condition.addItem("Not Equal")
			self.comboBox_Value.setEnabled(True)
			self.comboBox_Value.setEditable(True)
			self.comboBox_Value.clear()			
			self.comboBox_Value.setStyleSheet("QComboBox{border: 1px solid gray; background-color : white;}\n"
						"QComboBox::drop-down{border: 0px;}\n"
						"QComboBox::down-arrow{image: url(noimg);border-width: 0px;}")
		elif CurrentText_Filter == "Campaign Type":
			self.comboBox_Condition.setEnabled(True)
			self.comboBox_Condition.clear()
			self.comboBox_Condition.addItem("Equal")
			self.comboBox_Condition.addItem("Not Equal")
			self.comboBox_Value.setEnabled(True)
			self.comboBox_Value.setEditable(False)
			self.comboBox_Value.clear()			
			self.comboBox_Value.setStyleSheet("border: 1px solid gray;")
			self.comboBox_Value.addItem("agentCampaign")
			self.comboBox_Value.addItem("ivrCampaign")
		else: #NONE or error
			self.comboBox_Condition.setEnabled(False)
			self.comboBox_Condition.clear()
			self.comboBox_Value.setEnabled(False)
			self.comboBox_Value.clear()
			self.comboBox_Value.setCurrentText('')

#============Table_Import changed======================#
	def comboBox_Import_changed(self,index):
		global template
		print("header changed")
		current_option_array = []
		filtered_template = []
		self.pushButton_Import.setEnabled(False)
		self.checkBox_Overwrite.setEnabled(False)
		TableWidgetRowCount = self.tableWidget_Import.rowCount()
		for row in range(1,TableWidgetRowCount):
			self.tableWidget_Import.item(row,0).setText("Column changed")
			self.tableWidget_Import.item(row,0).setBackground(QtGui.QColor(255, 50, 50))			
		for TableWidgetColumn in range (len(template)): #Get all current selected values
			current_option = globals()["self.tableWidget_Import" + str(TableWidgetColumn)].currentText()
			current_option_array.append(current_option)
		for TableWidgetColumn in range (len(template)): #For all columns
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].currentIndexChanged.disconnect()
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].clear()
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].addItem("IGNORE")
			filtered_template = template[:]
			option_id = 0
			for current_option in current_option_array: #filter values
				if option_id != TableWidgetColumn and current_option in filtered_template:
					filtered_template.remove(current_option)
				option_id += 1
			for element in filtered_template: #and refill column header
				globals()["self.tableWidget_Import" + str(TableWidgetColumn)].addItem(element)
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].setCurrentText(
				current_option_array[TableWidgetColumn])
			globals()["self.tableWidget_Import" + str(TableWidgetColumn)].currentIndexChanged.connect(
				self.comboBox_Import_changed)
			self.tableWidget_Import.setCellWidget(0,TableWidgetColumn+1, globals()[
				"self.tableWidget_Import" + str(TableWidgetColumn)])				
		self.tableWidget_Import.resizeColumnsToContents()
		print("========================")

	def tableWidget_Import_ItemSelected(self): #Clicked item in tableWidget_Import
		rows = []
		qlist = self.tableWidget_Import.selectedIndexes()
		for item in qlist:
			rows.append(item.row())
		rows = list(set(rows))
		if 0 in rows:
			rows.pop(0)
		if len(rows) > 0:
			self.pushButton_DelRow.setEnabled(True)
		else:
			self.pushButton_DelRow.setEnabled(False)			

	def tableWidget_Import_ItemChanged(self,item): #Changed item in tableWidget_Import
		global valid_records
		row = item.row()
		column = item.column()
		print("item in position (" + str(column) + "," + str(row) + ") changed")
		if row != 0 and column != 0:
			if self.tableWidget_Import.item(row,0).text() == "Valid":
				valid_records -= 1
			if valid_records <= 0:
				self.pushButton_Import.setEnabled(False)
				self.checkBox_Overwrite.setEnabled(False)
			self.tableWidget_Import.item(row,0).setText("Data changed")
			self.tableWidget_Import.item(row,0).setBackground(QtGui.QColor(255, 50, 50))
			self.tableWidget_Import.resizeColumnsToContents()
		print("========================")
		
#=======================================================#
class AboutDialogNew(QtWidgets.QDialog,About_Dialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		
class ConnectionDialogNew(QtWidgets.QDialog,Connection_Dialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

def main():
    app = QtWidgets.QApplication(argv)  # Новый экземпляр QApplication
    window = CampaignManagerApp()  # Создаём объект класса CampaignManagerApp
    window.show()  # Показываем окно
    exit(app.exec_())  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
