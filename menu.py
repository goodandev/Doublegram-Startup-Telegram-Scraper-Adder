import configparser, csv, os, sys, colors, settings, banner, requests
from voip import ManageAccountList, AnalyzeAccounts, AccountSelector, GroupChannelSelector, EditAccount, DeleteAccount
from members import AddMembers, RewriteMembers
from adding import AddUsers

colors.getColors()

log = settings.getSetting('log','general_settings')

translations = {}

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
	print(' 1 | Engligh')
	print(' 2 | Italiano')
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


def setChoise():
	print(colors.cy+" "+translations['set_choise_line'])
	choise = input(colors.cy+" "+translations['set_choise_txt']+colors.gr)
	
	return choise


def continueToPrincipal():
	print(colors.cy+translations['continue_principal_line'])
	choise = input(colors.cy+translations['continue_principal_txt']+colors.gr)
	
	if log == translations['disabilitato_first_cap']:
		os.system('clear')
		banner.banner()
	PrincipalMenu()


def PrincipalMenu(show_menu=True):
	if show_menu == True:
		log = settings.getSetting('log','general_settings')

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
	else:
		log = settings.getSetting('log','general_settings')
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
	
	cpass = configparser.RawConfigParser()
	
	try:
		with open('data/config.data', encoding="UTF-8") as f:
			cpass.read_file(f)
			
			print()
			print(colors.cy+translations['menu_principale_line'])
			print(colors.cy+translations['menu_principale_text'])
			print(colors.cy+translations['menu_principale_line'])
			print(colors.wm+colors.wy+" - "+translations['account_plurale_cap']+" "+colors.wreset)

			print(colors.cy+"  1 | "+colors.wy+translations['aggiungi_account'])
			print(colors.cy+"  2 | "+colors.wy+translations['gestione_account'])
			print(colors.cy+"  3 | "+colors.wy+translations['analisi_account'])
			print(colors.wm+colors.wy+" - "+translations['membri_cap']+" "+colors.wreset)
			print(colors.cy+"  4 | "+colors.wy+translations['preleva_da'])
			print(colors.wm+colors.wy+" - "+translations['adding_cap']+" "+colors.wreset)
			print(colors.cy+"  5 | "+colors.wy+translations['centro_adding'])
			print(colors.wm+colors.wy+" - "+translations['altro_cap']+" "+colors.wreset)
			print(colors.cy+"  6 | "+colors.wy+translations['impostazioni'])
			print(colors.cy+"  7 | "+colors.wy+translations['impostazioni_adding'])
			
			print()
			print(colors.cy+"  8 | "+translations['esci'])
			
			try:
				choise = int(setChoise())
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				PrincipalMenu();

	except IOError:
		PrincipalMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		ManageAccountList(1)
		
	elif choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		MembersMenu()

	elif choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		ManageAccounts()

	elif(choise == 3):
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AnalyzeAccounts()

	elif(choise == 5):
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingMenu()

	elif(choise == 6):
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SettingsMenu()

	elif(choise == 7):
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingSettingsMenu()

	elif(choise == 8):
		sys.exit()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		PrincipalMenu()


def MembersMenu():
	choise = 1
	cpass = configparser.RawConfigParser()
	
	try:
		with open(r"members/members.csv", encoding='UTF-8') as f:
			users = []
			users_final = []
			num_users = 0
			num_bot = 0
			num_admin = 0
			num_not_photo = 0
			num_phone = 0

			i = 0

			with open(r"members/members.csv", encoding='UTF-8') as f:  
				rows = csv.reader(f,delimiter=",",lineterminator="\n")
				next(rows, None)
				for row in rows:
					num_users = num_users + 1

					if row[6] == 'True':
						num_bot = num_bot + 1

					if row[7] == 'True':
						num_admin = num_admin + 1

					if row[9] == 'False':
						num_not_photo = num_not_photo + 1

					if row[10] != 'False':
						num_phone = num_phone + 1
			print()
			print(colors.cy+translations['preleva_line'])
			print(colors.cy+translations['preleva_txt'])
			print(colors.cy+translations['preleva_line'])
			
			print()
			print("  "+translations['lista_attuale_include'])
			print()
			print("  "+colors.wm+colors.wy+translations['numero_utenti']+":"+str(int(num_users))+colors.wreset, end='')
			print("  "+colors.wm+colors.wy+translations['numero_bot']+":"+str(num_bot)+colors.wreset)
			print()
			print("  "+colors.wm+colors.wy+translations['numero_admin']+":"+str(num_admin)+colors.wreset, end='')
			print("  "+colors.wm+colors.wy+translations['numero_senza_foto']+":"+str(num_not_photo)+colors.wreset)
			print()
			print("  "+colors.wm+colors.wy+translations['numero_telefono_visibile']+":"+str(num_phone)+colors.wreset)
			print()

			print(colors.cy+"  1 | "+colors.wy+translations['seleziona_account_e']+" "+colors.re+translations['sovrascrivi']+colors.wy+" "+translations['la_lista_attuale'])
			print(colors.cy+"  2 | "+colors.wy+translations['seleziona_account_e']+" "+colors.re+translations['aggiungi']+colors.wy+" "+translations['alla_lista_attuale'])
			print(colors.cy+"  3 | "+colors.wy+translations['procedi_adding'])
			print()
			print(colors.cy+"  q | <- "+translations['torna_menu_principale'])
			choise = setChoise()

			if choise == 'q' or choise == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				PrincipalMenu()

			try:
				choise = int(choise)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				MembersMenu()

			if choise == 1:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				RewriteMembers()

			elif choise == 3:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				AddingMenu()

			elif choise == 2:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				AddMembers()

			else:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				MembersMenu()

	except IOError:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		MembersMenu()


def AddingMenu():
	choise = 1
	cpass = configparser.RawConfigParser()
	
	print()
	print(colors.cy+translations['aggiungi_membri_line'])
	print(colors.cy+translations['aggiungi_membri_txt'])
	print(colors.cy+translations['aggiungi_membri_line'])
	print(colors.cy+" 1 | "+colors.wy+translations['scegli_e_avvia'])
	print(colors.cy+" 2 | "+colors.wy+translations['impostazioni_adding'])

	print()
	print(colors.cy+" q | <- "+translations['torna_menu_principale'])
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		PrincipalMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddUsers(voip_index=None)

	elif choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingSettingsMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingMenu()


def ManageAccounts():
	choise = 1
	cpass = configparser.RawConfigParser()
	
	print()
	print(colors.cy+translations['gestione_account_line'])
	print(colors.cy+translations['gestione_account_txt'])
	print(colors.cy+translations['gestione_account_line'])
	print(colors.wm+colors.wy+" - "+translations['lista_account_cap']+" "+colors.wreset)
	print(colors.cy+"  1 | "+colors.wy+translations['crea_nuova_lista'])
	print(colors.cy+"  2 | "+colors.wy+translations['abilita_dis_account'])
	print(colors.cy+"  3 | "+colors.wy+translations['scollega_account'])
	print()
	print(colors.cy+"  q | <- "+translations['torna_menu_principale'])
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		PrincipalMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		ManageAccounts()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		ManageAccountList(0)

	if choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		EditAccount()


	elif choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		DeleteAccount()


	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		ManageAccounts()


def SettingsMenu(close=False):

	choise = 1
	cpass = configparser.RawConfigParser()

	log = settings.getSetting('log','general_settings')
	analyze_account = settings.getSetting('analyze_account','general_settings')
	language_set = settings.getLang()
	
	print()
	print(colors.cy+translations['impostazioni_line'])
	print(colors.cy+translations['impostazioni_txt'])
	print(colors.cy+translations['impostazioni_line'])
	print(colors.cy+" 1 | "+colors.wy+translations['mantieni_log']+" " + colors.cy + log)
	print(colors.cy+" 2 | "+colors.wy+translations['utente_analisi']+" " + colors.cy + analyze_account)
	print(colors.cy+" 3 | "+colors.wy+translations['lingua']+" " + colors.cy + language_set)
	print()
	print(colors.cy+" q | <- "+translations['torna_menu_principale'])
	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		PrincipalMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SettingsMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetLogs()

	if choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetAnalyzeAccount()

	if choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetLanguage()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		SettingsMenu()


def AddingSettingsMenu():
	settings.checkSettings(if_false_create=True)
	choise = 1
	cpass = configparser.RawConfigParser()

	change_account_n_requests = settings.getSetting('change_account_n_requests','adding_settings')
	change_account_pause = settings.getSetting('change_account_pause','adding_settings')
	consecutive_error_breaker = settings.getSetting('consecutive_error_breaker','adding_settings')
	start_point_members_file = settings.getSetting('start_point_members_file','adding_settings')
	add_using = settings.getSetting('add_using','adding_settings')
	between_adding_pause = settings.getSetting('between_adding_pause','adding_settings')
	casual_pause_times = settings.getSetting('casual_pause_times','adding_settings')
	stop_max_adding = settings.getSetting('stop_max_adding','adding_settings')
	
	print()
	print(colors.cy+translations['imp_adding_line'])
	print(colors.cy+translations['imp_adding_txt'])
	print(colors.cy+translations['imp_adding_line'])

	print(colors.wm+colors.wy+" - "+translations['regole_account_cap']+" "+colors.wreset)
	print(colors.cy+"  1 | "+colors.wy+translations['cambia_account_ogni']+" " + colors.cy + change_account_n_requests)
	print(colors.cy+"  2 | "+colors.wy+translations['pausa_uso_account']+" " + colors.cy + change_account_pause)
	print(colors.cy+"  3 | "+colors.wy+translations['err_consecutivi']+" " + colors.cy + consecutive_error_breaker)
	
	print(colors.wm+colors.wy+" - "+translations['regole_aggiunte_cap']+" "+colors.wreset)
	print(colors.cy+"  4 | "+colors.wy+translations['punto_inizio']+" " + colors.cy + start_point_members_file)
	print(colors.cy+"  5 | "+colors.wy+translations['aggiungi_tramite']+" " + colors.cy + add_using)
	print(colors.cy+"  6 | "+colors.wy+translations['pausa_aggiunta_altra']+" " + colors.cy + between_adding_pause)
	print(colors.cy+"  7 | "+colors.wy+translations['durata_pausa_casuale']+" " + colors.cy + casual_pause_times)
	print(colors.cy+"  8 | "+colors.wy+translations['blocca_adding_a']+" " + colors.cy + stop_max_adding)
	
	print()
	print(colors.cy+"  q | <- "+translations['centro_adding'])

	choise = setChoise()

	if choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingMenu()

	try:
		choise = int(choise)
	except:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingSettingsMenu()

	if choise == 1:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetChangeEveryNAdded()

	if choise == 2:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetPauseBetweenAccounts()

	if choise == 3:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetConsecutiveErrorsBreaker()

	if choise == 4:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetStartPoint()

	if choise == 5:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetAddUsing()

	if choise == 6:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetAddPause()

	if choise == 7:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetRandomPause()

	if choise == 8:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		settings.SetStopMaxAdding()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		AddingSettingsMenu()
