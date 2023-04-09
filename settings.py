import os, configparser, colors, banner, menu, re, sys
import configparser

translations = {}

lang = False

try:
	with open('data/lang.data', encoding="UTF-8") as f:
		cpass = configparser.RawConfigParser()
		cpass.read_file(f)

		for each_section in cpass.sections():
			for (each_key, each_val) in cpass.items(each_section):
				value = each_val

		lang = value

except IOError:
	print(" [+] Choose a language")
	print(" 1 | English")
	print(" 2 | Italiano")
	print()

	choise = False

	while choise != '1' and choise != '2':
		choise = input("[+] -->")

	if choise == '1':
		chosen_lang = 'EN'
	elif choise == '2':
		chosen_lang = 'IT'
	else:
		chosen_lang = 'EN'
	
	lang_setting = configparser.RawConfigParser()
	lang_setting.add_section('lang')
	lang_setting.set('lang', 'choise', chosen_lang)
	setup = open('data/lang.data', 'w')
	lang_setting.write(setup)
	setup.close()

	lang = choise

if lang == 'IT' or lang == 'EN':
	with open('translations/'+lang+'.data', encoding="UTF-8") as f:
		cpass = configparser.RawConfigParser()
		cpass.read_file(f)

		for each_section in cpass.sections():
			for (each_key, each_val) in cpass.items(each_section):
				translations[each_key] = each_val


colors.getColors()

def checkSettings(if_false_create):
	cpass = configparser.RawConfigParser()
	try:
		with open('data/settings.data', encoding="UTF-8") as f:
			cpass.read_file(f)
			return True
	except IOError:
		print(colors.wy+" "+translations['impostazioni_base_configurate'])
		if if_false_create == False:
			return False
		else:
			log = translations['disabilitato_first_cap']
			settings = configparser.RawConfigParser()
			settings.add_section("general_settings")
			settings.set("general_settings", "log", translations['disabilitato_first_cap'])
			settings.set("general_settings", "analyze_account", "doublegram_test_user")
			setup = open("data/settings.data", "w")
			settings.write(setup)

			settings.add_section("adding_settings")
			settings.set("adding_settings", "change_account_n_requests", "20 "+translations['richieste'])
			settings.set("adding_settings", "change_account_pause", "1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "consecutive_error_breaker", "30 "+translations['errori'])
			settings.set("adding_settings", "start_point_members_file", translations['da_interrotto'])
			settings.set("adding_settings", "add_using", translations['user_id_opt'])
			settings.set("adding_settings", "between_adding_pause", "1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "casual_pause_times", "3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
			settings.set("adding_settings", "stop_max_adding", translations['nessun_limite'])
			setup = open("data/settings.data", "w")
			settings.write(setup)
			
			setup.close()
			return log


def getSetting(name,section):
	cpass = configparser.RawConfigParser()
	cpass.read('data/settings.data', encoding='UTF-8')

	value = 'False'

	for each_section in cpass.sections():
		for (each_key, each_val) in cpass.items(each_section):
			if each_section == section and each_key == name:
				value = each_val
	return value


def getLang():
	cpass = configparser.RawConfigParser()
	cpass.read('data/lang.data', encoding='UTF-8')

	value = 'False'

	for each_section in cpass.sections():
		for (each_key, each_val) in cpass.items(each_section):
			value = each_val

	if value == 'IT':
		value = 'Italiano'
	elif value == 'EN':
		value = 'English'

	return value


def SetLanguage():
	log = getSetting('log','general_settings')

	language = getLang()

	print()
	print(colors.wm+colors.wy+" "+translations['modifica_lingua_cap']+" "+colors.wreset)
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"English")
	print(colors.cy+"  2 | "+colors.wy+"Italiano")
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.SettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetLanguage()

	new_lang = 'EN'

	if int(choise) == 1:
		new_lang = 'EN'
	elif int(choise) == 2:
		new_lang = 'IT'

	config = configparser.ConfigParser()
	config.read('data/lang.data', encoding="UTF-8")  
	cnfFile = open('data/lang.data', "w", encoding="UTF-8")
	config.set("lang","choise",new_lang)
	config.write(cnfFile)
	cnfFile.close()

	if log == translations['disabilitato_first_cap']:
		os.system('clear')
		banner.banner()

	os.remove("data/settings.data")

	python = sys.executable
	os.execl(python, python, * sys.argv)

	
def SetLogs():
	log = getSetting('log','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['mantieni_log_cap']+" "+colors.wreset)
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['abilitato_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['disabilitato_first_cap'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.SettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","log",translations['abilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()
		log = translations['abilitato_first_cap']
		
		python = sys.executable
		os.execl(python, python, * sys.argv)

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","log",translations['disabilitato_first_cap'])
		config.write(cnfFile)
		cnfFile.close()
		log = translations['disabilitato_first_cap']

		python = sys.executable
		os.execl(python, python, * sys.argv)

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetLogs()


def SetAnalyzeAccount():
	log = getSetting('log','general_settings')

	analyze_account = getSetting('analyze_account','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['account_analisi_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['account_analisi_cap_txt_1'])
	print(colors.wy+" "+translations['account_analisi_cap_txt_2'])
	print(colors.wy+" "+translations['account_analisi_cap_txt_3'])
	print(colors.wy+" "+translations['account_analisi_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+"doublegram_test_user")
	print(colors.cy+" 2 | "+colors.wy+translations['inserisci_username_manualmente'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.SettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("general_settings","analyze_account",'doublegram_test_user')
		config.write(cnfFile)
		cnfFile.close()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")
		
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		choise = menu.setChoise()

		config.set("general_settings","analyze_account",choise)
		config.write(cnfFile)
		cnfFile.close()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetAnalyzeAccount()

	if log == translations['disabilitato_first_cap']:
		os.system('clear')
		banner.banner()

	menu.SettingsMenu()


def SetChangeEveryNAdded():
	log = getSetting('log','general_settings')

	change_account_n_requests = getSetting('change_account_n_requests','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['limite_richieste_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['limite_richieste_cap_txt_1'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_2'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_3'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_4'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_5'])
	print(colors.wy+" "+translations['limite_richieste_cap_txt_6'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"5 "+translations['richieste'])
	print(colors.cy+"  2 | "+colors.wy+"10 "+translations['richieste'])
	print(colors.cy+"  3 | "+colors.wy+"15 "+translations['richieste'])
	print(colors.cy+"  4 | "+colors.wy+"20 "+translations['richieste'])
	print(colors.cy+"  5 | "+colors.wy+"25 "+translations['richieste'])
	print(colors.cy+"  6 | "+colors.wy+"30 "+translations['richieste'])
	print(colors.cy+"  7 | "+colors.wy+"35 "+translations['richieste'])
	print(colors.cy+"  8 | "+colors.wy+"40 "+translations['richieste'])
	print(colors.cy+"  9 | "+colors.wy+"45 "+translations['richieste'])
	print(colors.cy+" 10 | "+colors.wy+"50 "+translations['richieste'])
	print(colors.cy+" 11 | "+colors.wy+"55 "+translations['richieste'])
	print(colors.cy+" 12 | "+colors.wy+"60 "+translations['richieste'])
	print(colors.cy+" 13 | "+colors.wy+"65 "+translations['richieste'])
	print(colors.cy+" 14 | "+colors.wy+"70 "+translations['richieste'])
	print(colors.cy+" 15 | "+colors.wy+"75 "+translations['richieste'])
	print(colors.cy+" 16 | "+colors.wy+"80 "+translations['richieste'])
	print(colors.cy+" 17 | "+colors.wy+"85 "+translations['richieste'])
	print(colors.cy+" 18 | "+colors.wy+"90 "+translations['richieste'])
	print(colors.cy+" 19 | "+colors.wy+"95 "+translations['richieste'])
	print(colors.cy+" 20 | "+colors.wy+"100 "+translations['richieste'])
	print(colors.cy+" 21 | "+colors.wy+translations['nessun_limite'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetChangeEveryNAdded()

	if int(choise) < 21:

		value = 5*int(choise)
		value = str(value)+" "+translations['richieste']

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_n_requests",value)
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '21':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_n_requests",translations['nessun_limite'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetChangeEveryNAdded()


def SetPauseBetweenAccounts():
	log = getSetting('log','general_settings')

	change_account_pause = getSetting('change_account_pause',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_prossimo_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_prossimo_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_prossimo_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_prossimo_cap_txt_3'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"3-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-60 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-180 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-300 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-600 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-900 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()
	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetPauseBetweenAccounts()

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) <= 10:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) > 10 and int(choise) < 20:
		if int(choise) == 11:
			value = "120"
		elif int(choise) == 12:
			value = "180"
		elif int(choise) == 13:
			value = "300"
		elif int(choise) == 14:
			value = "600"
		elif int(choise) == 15:
			value = "900"
		elif int(choise) == 16:
			value = "1800"
		elif int(choise) == 17:
			value = "3600"
		elif int(choise) == 18:
			value = "7200"
		elif int(choise) == 19:
			value = "21600"
		elif int(choise) == 20:
			value = "43200"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",value + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) >= 20 and int(choise) < 33:
		if int(choise) == 21:
			value = "0-3"
		elif int(choise) == 22:
			value = "1-3"
		elif int(choise) == 23:
			value = "1-5"
		elif int(choise) == 24:
			value = "1-10"
		elif int(choise) == 25:
			value = "3-5"
		elif int(choise) == 26:
			value = "3-10"
		elif int(choise) == 27:
			value = "3-60"
		elif int(choise) == 28:
			value = "3-120"
		elif int(choise) == 29:
			value = "3-180"
		elif int(choise) == 30:
			value = "3-300"
		elif int(choise) == 31:
			value = "3-600"
		elif int(choise) == 32:
			value = "3-900"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '33':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","change_account_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetPauseBetweenAccounts()


def SetStopMaxAdding():
	log = getSetting('log','general_settings')

	stop_max_adding = getSetting('stop_max_adding',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['limite_aggiunte_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_1'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_2'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_3'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_4'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_5'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_6'])
	print(colors.wy+" "+translations['limite_aggiunte_cap_txt_7'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+translations['inserisci_valore'])
	print(colors.cy+"  2 | "+colors.wy+translations['nessun_limite'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()

	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetStopMaxAdding()
	
	if int(choise) == 1:
		print()
		print(" "+translations['inserisci_massimo_utenti'])
		choise_num = menu.setChoise()

		try:
			value = int(choise_num)
			value = str(value)+" "+translations['utenti']
			config = configparser.ConfigParser()
			config.read('data/settings.data', encoding="UTF-8") 
			cnfFile = open('data/settings.data', "w", encoding="UTF-8")
			config.set("adding_settings","stop_max_adding",value)
			config.write(cnfFile)
			cnfFile.close()

			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()

			menu.AddingSettingsMenu()
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			SetStopMaxAdding()	

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","stop_max_adding",translations['nessun_limite'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetStopMaxAdding()


def SetConsecutiveErrorsBreaker():
	log = getSetting('log','general_settings')

	consecutive_error_breaker = getSetting('consecutive_error_breaker',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['limite_errori_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['limite_errori_cap_txt_1'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_2'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_3'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_4'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_5'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_6'])
	print(colors.wy+" "+translations['limite_errori_cap_txt_7'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+""+colors.wy+"1 "+translations['errore'])
	print(colors.cy+"  2 | "+colors.wy+""+colors.wy+"2 "+translations['errori'])
	print(colors.cy+"  3 | "+colors.wy+""+colors.wy+"3 "+translations['errori'])
	print(colors.cy+"  4 | "+colors.wy+""+colors.wy+"4 "+translations['errori'])
	print(colors.cy+"  5 | "+colors.wy+""+colors.wy+"5 "+translations['errori'])
	print(colors.cy+"  6 | "+colors.wy+""+colors.wy+"10 "+translations['errori'])
	print(colors.cy+"  7 | "+colors.wy+""+colors.wy+"15 "+translations['errori'])
	print(colors.cy+"  8 | "+colors.wy+""+colors.wy+"20 "+translations['errori'])
	print(colors.cy+"  9 | "+colors.wy+""+colors.wy+"25 "+translations['errori'])
	print(colors.cy+" 10 | "+colors.wy+""+colors.wy+"30 "+translations['errori'])
	print(colors.cy+" 11 | "+colors.wy+""+colors.wy+"35 "+translations['errori'])
	print(colors.cy+" 12 | "+colors.wy+""+colors.wy+"40 "+translations['errori'])
	print(colors.cy+" 13 | "+colors.wy+""+colors.wy+"45 "+translations['errori'])
	print(colors.cy+" 14 | "+colors.wy+""+colors.wy+"50 "+translations['errori'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()
	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetConsecutiveErrorsBreaker()

	if int(choise) < 5:

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","consecutive_error_breaker",str(choise)+" "+translations['errori'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) >= 5 and int(choise) <= 14:

		value = (int(choise)-4)*5

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","consecutive_error_breaker",str(value)+" "+translations['errori'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetConsecutiveErrorsBreaker()


def SetStartPoint():
	log = getSetting('log','general_settings')

	start_point_members_file = getSetting('start_point_members_file',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['punto_inizio_membri_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_1'])
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_2'])
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_3'])
	print(colors.wy+" "+translations['punto_inizio_membri_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['da_interrotto'])
	print(colors.cy+" 2 | "+colors.wy+translations['da_inizio'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","start_point_members_file",translations['da_interrotto'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","start_point_members_file",translations['da_inizio'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetStartPoint()


def SetAddUsing():
	log = getSetting('log','general_settings')

	add_using = getSetting('add_using','general_settings')

	print()
	print(colors.wm+colors.wy+" "+translations['seleziona_metodo_aggiunta_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_1'])
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_2'])
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_3'])
	print(colors.wy+" "+translations['seleziona_metodo_aggiunta_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+" 1 | "+colors.wy+translations['username_first_cap'])
	print(colors.cy+" 2 | "+colors.wy+translations['id_utente_cap'])
	print(colors.cy+" 3 | "+colors.wy+translations['user_id_opt'])
	print()
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()

	elif choise == '1':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","add_using",translations['username_first_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '2':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","add_using",translations['id_utente_cap'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '3':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","add_using",translations['user_id_opt'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetAddUsing()


def SetAddPause():
	log = getSetting('log','general_settings')

	between_adding_pause = getSetting('between_adding_pause',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['pause_aggiunte_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_1'])
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_2'])
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_3'])
	print(colors.wy+" "+translations['pause_aggiunte_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"180 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 13 | "+colors.wy+"300 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 14 | "+colors.wy+"600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 15 | "+colors.wy+"900 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 16 | "+colors.wy+"1800 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 17 | "+colors.wy+"3600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 18 | "+colors.wy+"7200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 19 | "+colors.wy+"21600 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 20 | "+colors.wy+"43200 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 21 | "+colors.wy+"0-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"0-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+"1-3 sec ("+translations['casuale']+")")
	print(colors.cy+" 24 | "+colors.wy+"1-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 25 | "+colors.wy+"1-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 26 | "+colors.wy+"3-5 sec ("+translations['casuale']+")")
	print(colors.cy+" 27 | "+colors.wy+"3-10 sec ("+translations['casuale']+")")
	print(colors.cy+" 28 | "+colors.wy+"3-20 sec ("+translations['casuale']+")")
	print(colors.cy+" 29 | "+colors.wy+"3-30 sec ("+translations['casuale']+")")
	print(colors.cy+" 30 | "+colors.wy+"3-60 sec ("+translations['casuale']+")")
	print(colors.cy+" 31 | "+colors.wy+"3-120 sec ("+translations['casuale']+")")
	print(colors.cy+" 32 | "+colors.wy+"3-180 sec ("+translations['casuale']+")")
	print(colors.cy+" 33 | "+colors.wy+"3-300 sec ("+translations['casuale']+")")
	print(colors.cy+" 34 | "+colors.wy+"3-600 sec ("+translations['casuale']+")")
	print(colors.cy+" 35 | "+colors.wy+"3-900 sec ("+translations['casuale']+")")
	print(colors.cy+" 36 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()
	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetAddPause()

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) <= 20:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60
		elif int(choise) == 11:
			value = 120
		elif int(choise) == 12:
			value = 180
		elif int(choise) == 13:
			value = 300
		elif int(choise) == 14:
			value = 600
		elif int(choise) == 15:
			value = 900
		elif int(choise) == 16:
			value = 1800
		elif int(choise) == 17:
			value = 3600
		elif int(choise) == 18:
			value = 7200
		elif int(choise) == 19:
			value = 21600
		elif int(choise) == 20:
			value = 43200

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) > 20 and int(choise) < 36:
		if int(choise) == 21:
			value = "0-3"
		elif int(choise) == 22:
			value = "0-5"
		elif int(choise) == 23:
			value = "1-3"
		elif int(choise) == 24:
			value = "1-5"
		elif int(choise) == 25:
			value = "1-10"
		elif int(choise) == 26:
			value = "3-5"
		elif int(choise) == 27:
			value = "3-10"
		elif int(choise) == 28:
			value = "3-20"
		elif int(choise) == 29:
			value = "3-30"
		elif int(choise) == 30:
			value = "3-60"
		elif int(choise) == 31:
			value = "3-120"
		elif int(choise) == 32:
			value = "3-180"
		elif int(choise) == 33:
			value = "3-300"
		elif int(choise) == 34:
			value = "3-600"
		elif int(choise) == 35:
			value = "3-900"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",value + " "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '36':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","between_adding_pause",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetAddPause()


def SetRandomPause():
	log = getSetting('log','general_settings')

	casual_pause_times = getSetting('casual_pause_times',"adding_settings")

	print()
	print(colors.wm+colors.wy+" "+translations['pausa_casuale_cap']+" "+colors.wreset)
	print()
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_1'])
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_2'])
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_3'])
	print(colors.wy+" "+translations['pausa_casuale_cap_txt_4'])
	print()
	print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
	print()
	print(colors.cy+"  1 | "+colors.wy+"1 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  2 | "+colors.wy+"2 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  3 | "+colors.wy+"3 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  4 | "+colors.wy+"4 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  5 | "+colors.wy+"5 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  6 | "+colors.wy+"10 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  7 | "+colors.wy+"15 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  8 | "+colors.wy+"20 "+translations['abbreviazione_secondi'])
	print(colors.cy+"  9 | "+colors.wy+"30 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 10 | "+colors.wy+"60 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 11 | "+colors.wy+"120 "+translations['abbreviazione_secondi'])
	print(colors.cy+" 12 | "+colors.wy+"0-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 13 | "+colors.wy+"0-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 14 | "+colors.wy+"1-3 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 15 | "+colors.wy+"1-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 16 | "+colors.wy+"1-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 17 | "+colors.wy+"3-5 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 18 | "+colors.wy+"3-10 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 19 | "+colors.wy+"3-20 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 20 | "+colors.wy+"3-30 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 21 | "+colors.wy+"3-60 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 22 | "+colors.wy+"3-120 "+translations['abbreviazione_secondi']+" ("+translations['casuale']+")")
	print(colors.cy+" 23 | "+colors.wy+translations['nessuna_pausa'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	choise = menu.setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingSettingsMenu()
	
	try:
		int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetRandomPause()

	if int(choise) <= 5:
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",choise + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) <= 11:
		if int(choise) == 6:
			value = 10
		elif int(choise) == 7:
			value = 15
		elif int(choise) == 8:
			value = 20
		elif int(choise) == 9:
			value = 30
		elif int(choise) == 10:
			value = 60
		elif int(choise) == 11:
			value = 120

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",str(value) + " "+translations['abbreviazione_secondi'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif int(choise) > 11 and int(choise) < 23:
		if int(choise) == 12:
			value = "0-3"
		elif int(choise) == 13:
			value = "0-5"
		elif int(choise) == 14:
			value = "1-3"
		elif int(choise) == 15:
			value = "1-5"
		elif int(choise) == 16:
			value = "1-10"
		elif int(choise) == 17:
			value = "3-5"
		elif int(choise) == 18:
			value = "3-10"
		elif int(choise) == 19:
			value = "3-20"
		elif int(choise) == 20:
			value = "3-30"
		elif int(choise) == 21:
			value = "3-60"
		elif int(choise) == 22:
			value = "3-120"

		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",value + " sec ("+translations['casuale']+")")
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	elif choise == '23':
		config = configparser.ConfigParser()
		config.read('data/settings.data', encoding="UTF-8")  
		cnfFile = open('data/settings.data', "w", encoding="UTF-8")
		config.set("adding_settings","casual_pause_times",translations['nessuna_pausa'])
		config.write(cnfFile)
		cnfFile.close()

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()

		menu.AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SetRandomPause()

