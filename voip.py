import os, sys, time, re, configparser, traceback, datetime, signal, random, asyncio, settings, banner, shutil, colors, menu
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ApiIdInvalidError, PeerFloodError, FloodWaitError, UserPrivacyRestrictedError
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest, ImportChatInviteRequest, ExportChatInviteRequest
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon import errors
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import PeerUser

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

colors.getColors()
log = settings.getSetting('log','general_settings')

if log != translations['disabilitato_first_cap'] and log != translations['abilitato_first_cap']:
	log = translations['disabilitato_first_cap']


breaker_analysis = 0
analysis_running = 0

def getVoips():
	voip = []
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	for each_section in cpass.sections():
		z = 0
		account = {}
		for (each_key, each_val) in cpass.items(each_section):
			if z == 0:
				name = each_val
				account['name'] = name
			elif z == 1:
				phone = each_val
				account['phone'] = phone
			elif z == 2:
				apiID =  each_val
				account['apiID'] = apiID
			elif z == 3:
				hashID = each_val
				account['hashID'] = hashID
			elif z == 4:
				ids = each_val
				account['id'] = ids
			elif z == 5:
				access_hash = each_val
				account['access_hash'] = access_hash
			elif z == 6:
				username = each_val
				account['username'] = username
			elif z == 7:
				status = each_val
				account['status'] = status
			else:
				break
			z = z+1

		voip.append(account)

	return voip


def getName(client):
	if client.get_me().last_name == None:
		last_name = ''
	else:
		last_name = client.get_me().last_name

	name = client.get_me().first_name+" "+last_name
	
	return name


def getRestricted(client):
	limited = False
	analyze_account = settings.getSetting('analyze_account','general_settings')

	try:
		client.send_message('@'+analyze_account,message="Restrictions Test")
	except FloodWaitError as e:
		limited = False
	except Exception as e:
		limited = True

	return limited


def getFlood(client):
	flood = False
	analyze_account = settings.getSetting('analyze_account','general_settings')

	try:
		client.send_message('@'+analyze_account,message="Flood Test")

	except errors.FloodWaitError as e:
		flood = True
	except FloodWaitError as e:
		flood = True
	except Exception as e:
		flood = False

	return flood


def getUsername(client):
	username = client.get_me().username

	return username


def getId(client):
	ids = client.get_me().id

	return ids


def getAccessHash(client):
	access_hash = client.get_me().access_hash

	return access_hash


def test_connection(phone,apiID,hashID,silent_mode):
	try:
		client = TelegramClient('sessions/'+phone, apiID, hashID)

	except ApiIdInvalidError:
		client = False
	except Exception as e:
		client = False

	try:
		client.connect()
		if not client.is_user_authorized():
			client.send_code_request(phone)  
			client.sign_in(phone, input(colors.cy+" "+translations['inserisci_codice_ricevuto']+" "+colors.gr))
		else:
			if silent_mode == False:
				print(colors.cy+" "+translations['accesso_eseguito_correttamente'])
	
	except ApiIdInvalidError:
		client = False
	except Exception as e:
		client = False

	return client


def ManageAccountList(write_method):
	if write_method == 0:
		print()
		print(colors.wm+colors.wy+" "+translations['crea_nuova_lista_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_1'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_2'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_3'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_4'])
		print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_5'])
		print()
		print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
		print()
		print(colors.cy+"  y |"+colors.wreset+" "+translations['procedi_first_cap'])
		print()
		
		print(colors.cy+" "+translations['digita_scelta_arrow_line'])
		choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
	
	else:
		choise = 'Y'

	if choise == 'Y' or choise == 'y':
		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()

		if write_method == 0:

			print()
			print(colors.wm+colors.wy+" "+translations['crea_nuova_lista_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_1'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_2'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_3'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_4'])
			print(" "+colors.wy+translations['crea_nuova_lista_cap_txt_5'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
			print()

			original = r'data/config.data'
			target = r'data/backup-config.data'

			shutil.copyfile(original, target)
			method = 'w'
			start = 0
		
		elif write_method == 1:
			method = 'a'
			cpass = configparser.RawConfigParser()
			cpass.read('data/config.data', encoding="UTF-8")
			start = len(cpass.sections())
			print()
			print(colors.wm+colors.wy+" "+translations['aggiungi_account_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_1'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_2'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_3'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro'])
			print()

		print(" "+translations['quanti_account_inserire'])
		print()
		
		print(colors.cy+" "+translations['digita_scelta_arrow_line'])
		num_voip = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)

		if num_voip == 'q' or num_voip == 'Q' or num_voip == '':
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			if write_method == 0:
				menu.ManageAccounts()
			else:
				menu.PrincipalMenu()
		try:
			num_voip = int(num_voip)

			if num_voip == 0:
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				ManageAccountList(write_method)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			ManageAccountList(write_method)

		if write_method == 0:
			i = 0
		elif write_method == 1:
			i = start
			num_voip = num_voip+start

		if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()

		while i < num_voip:
			print()
			print(colors.wm+colors.wy+" "+translations['aggiungi_account_cap']+" "+colors.wreset)
			print()
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_1'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_2'])
			print(" "+colors.wy+translations['aggiungi_account_cap_txt_3'])
			print()
			print(colors.cy+" "+colors.cy+translations['premi_q_indietro']+"  ")
			print()
			print(colors.gr+" "+translations['inserisci_dati_account_line'])
			print(colors.gr+" "+translations['inserisci_dati_account_n']+str(i+1))
			print(colors.gr+" "+translations['inserisci_dati_account_line'])
			time.sleep(0.2)

			phone = input(colors.cy+" "+translations['inserisci_numero_telefono']+" "+colors.gr)
			time.sleep(0.2)

			if phone == 'q' or phone == 'Q' or phone == '':
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				if write_method == 0:
					menu.ManageAccounts()
				else:
					menu.PrincipalMenu()

			apiID = input(colors.cy+" "+translations['inserisci_api_id']+" "+colors.gr)
			time.sleep(0.2)

			if apiID == 'q' or apiID == 'Q' or apiID == '':
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				if write_method == 0:
					menu.ManageAccounts()
				else:
					menu.PrincipalMenu()

			hashID = input(colors.cy+" "+translations['inserisci_hash_id']+" "+colors.gr)
			time.sleep(0.2)

			if hashID == 'q' or hashID == 'Q' or hashID == '':
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				if write_method == 0:
					menu.ManageAccounts()
				else:
					menu.PrincipalMenu()

			print(colors.cy+" "+translations['tentativo_connessione'])
			try:
				client = test_connection(phone,apiID,hashID,silent_mode=False)
			except Exception as e:
				break

			if client != False: 
				name = getName(client)
				username = getUsername(client)
				if username == None:
					username = '/'

				credenziali = configparser.RawConfigParser()
				credenziali.add_section('credenziali'+str(i))
				credenziali.set('credenziali'+str(i), 'name', name)
				credenziali.set('credenziali'+str(i), 'phone', phone)
				credenziali.set('credenziali'+str(i), 'apiID', apiID)
				credenziali.set('credenziali'+str(i), 'hashID', hashID)
				credenziali.set('credenziali'+str(i), 'id', client.get_me().id)
				credenziali.set('credenziali'+str(i), 'access_hash', client.get_me().access_hash)
				credenziali.set('credenziali'+str(i), 'username', '@'+username)
				credenziali.set('credenziali'+str(i), 'status', 'Enabled')

				setup = open('data/config.data', method)
				credenziali.write(setup)
				setup.close()

				print()
				print(colors.gr+" "+translations['account_aggiunto_successo'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				
				client.disconnect()

				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
			else:
				print()
				print(colors.re+" "+translations['errore_connessione_account'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				break

			i = i+1 

		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		menu.PrincipalMenu()

	elif choise == 'q' or choise == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		if write_method == 0:
			menu.ManageAccounts()
		else:
			menu.PrincipalMenu()

	else:
		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		ManageAccountList(write_method)
		
	
def handler(signum, frame) -> int:
	if analysis_running == 1:
		res = 0
		while res != 'Y' and res != 'y' and res != 'N' and res != 'n':
			print()

			print()
			print(colors.cy+" "+translations['vuoi_interrompere'])
			print(colors.cy+" "+translations['vuoi_interrompere_line'])
			res = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)
			print()
		if res == 'y' or res == 'Y':
			global breaker_analysis
			breaker_analysis = True
			python = sys.executable
			os.execl(python, python, * sys.argv)

signal.signal(signal.SIGINT, handler)


def blockBreaker():
	global breaker_analysis
	breaker_analysis = 0


def activeAnalysis():
	global analysis_running
	analysis_running = 1


def blockAnalysis():
	global analysis_running
	analysis_running = 0


def AnalyzeAccounts():
	activeAnalysis()

	if log == translations['disabilitato_first_cap']:
		os.system("clear")
		banner.banner()
	else:
		print()
		print()

	print()
	print(colors.cy+translations['analisi_account_line'])
	print(colors.cy+translations['analisi_account_cap'])
	print(colors.cy+translations['analisi_account_line'])
	print()

	restricted_count = 0
	flood_count = 0
	cant_connect = 0
	voips = getVoips() 
	i = 0

	for account in voips:
		if breaker_analysis == 0:
			print(colors.wm+colors.wy+" - "+account['name']+colors.wreset)

			try:
				client = test_connection(account['phone'],account['apiID'],account['hashID'],silent_mode=True)
			except:
				print(colors.re+" "+translations['impossibile_questo_account'])
				print()
				cant_connect = cant_connect + 1

			is_client = True
			
			try:
				me = client.get_me()
				if me == None:
					is_client = False
			except:
				is_client = False

			if client != False and is_client == True:

				name = getName(client)
				restricted = getRestricted(client)
				flood = getFlood(client)
				username = getUsername(client)
				
				if username == None:
					username = '/'
				else:
					username = '@'+username
				
				ids = getId(client)
				access_hash = getAccessHash(client)
				userfull = client(GetFullUserRequest(client.get_me()))
				
				try:
					bio = userfull.full_user.about
				except:
					bio = ''

				client.disconnect()
				account['name'] = name
				account['id'] = ids
				account['access_hash'] = access_hash
				account['username'] = username

				if restricted == True:
					restricted_txt = colors.re+translations['si_first_cap']
					restricted_count = restricted_count + 1
				else:
					restricted_txt = colors.wy+translations['no_first_cap']

				if flood == True:
					flood_txt = colors.re+translations['si_first_cap']
					flood_count = flood_count + 1
				else:
					flood_txt = colors.wy+translations['no_first_cap']

				if bio == None:
					bio = '/'

				if account['status'] == 'Enabled':
					status_txt = translations['abilitato_first_cap']
				else:
					status_txt = translations['disabilitato_first_cap']
				
				print(colors.cy+" "+translations['nome_completo']+" "+colors.wy+name)
				print(colors.cy+" "+translations['username_first_cap']+": "+colors.wy+username)
				print(colors.cy+" "+translations['telefono']+": "+colors.wy+account['phone'])
				print(colors.cy+" "+translations['stato_doublegram']+": "+colors.wy+status_txt)
				print(colors.cy+" "+translations['biografia']+":")
				print(" "+colors.wy+bio)
				print(colors.cy+" "+translations['limitato']+": "+colors.wy+restricted_txt)
				print(colors.cy+" "+translations['flood']+": "+colors.wy+flood_txt)
				print()
				print("------------------------------")
				print()

			else:
				print(colors.re+" "+translations['impossibile_questo_account'])
				print()
				account['status'] = 'Disabled'
				cant_connect = cant_connect + 1

			i = i + 1

	if breaker_analysis == 0:
		
		print(" "+colors.wm+colors.wy+" "+str(i)+" "+translations['account_totali_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wg+colors.wy+" "+str(i - restricted_count - cant_connect - flood_count)+" "+translations['account_liberi_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wo+colors.wy+" "+str(flood_count)+" "+translations['account_flood_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wr+colors.wy+" "+str(restricted_count)+" "+translations['account_limitati_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wr+colors.wy+" "+str(cant_connect)+" "+translations['account_falliti_cap']+" "+colors.wreset)
		print()

		i = 0
		f = 0
		length = len(voips)
		
		while i < length:
			
			if f == 0:
				method = 'w'
			else:
				method = 'a'	

			accounts = configparser.RawConfigParser()
			
			accounts.add_section('credenziali'+str(i))
		 
			accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
			accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
			accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
			accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
			accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
			accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
			accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
			accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
			
			setup = open('data/config.data', method) 
			accounts.write(setup)
			setup.close()
			
			f = f+1
			i = i+1
	else:
		blockBreaker()

	blockAnalysis()

	menu.continueToPrincipal()


def AccountSelector(mode):
	print()
	if mode == 'adding':
		print(colors.wm+colors.wy+" "+translations['inserisci_utenti_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_per_destinazione']+" ")
		print(" "+colors.cy+translations['seleziona_account_per_destinazione_line'])
	elif mode == 'updatesurname':
		print(colors.wm+colors.wy+" "+translations['modifica_cognome_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_cognome'])
		print(" "+colors.cy+translations['seleziona_account_cognome_line'])
	elif mode == 'updatename':
		print(colors.wm+colors.wy+" "+translations['modifica_nome_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_nome'])
		print(" "+colors.cy+translations['seleziona_account_nome_line'])
	elif mode == 'updatebio':
		print(colors.wm+colors.wy+" "+translations['modifica_bio_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_bio'])
		print(" "+colors.cy+translations['seleziona_account_bio_line'])
	elif mode == 'updateusername':
		print(colors.wm+colors.wy+" "+translations['modifica_username_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_username'])
		print(" "+colors.cy+translations['seleziona_account_username_line'])
	elif mode == 'members':
		print(colors.wm+colors.wy+" "+translations['preleva_e_aggiungi_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_prelevare'])
		print(colors.cy+" "+translations['seleziona_account_prelevare_line'])
		print()
	elif mode == 'members-r':
		#print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)
		#print()
		print(colors.gr+" "+translations['seleziona_account_prelevare'])
		print(colors.cy+" "+translations['seleziona_account_prelevare_line'])
		print()
	elif mode == 'editvoip':
		print(colors.wm+colors.wy+" "+translations['abilita_disabilita_cap']+" "+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_account_ab_dis']+" ")
		print()
		print(colors.cy+translations['ab_dis_line'])
		print("      "+colors.wg+colors.wy+'  '+colors.wreset+ " = "+translations['abilitato_cap']+"    "+colors.wr+colors.wy+'  '+colors.wreset+ " = "+translations['dis_cap'])
		print(colors.cy+translations['ab_dis_line'])
	elif mode == 'deletevoip':
		print(colors.wm+colors.wy+" "+translations['scollega_account_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['scollega_account_cap_txt_1'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_2'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_3'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_4'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_5'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_6'])
		print()
		print(" "+colors.cy+translations['premi_q_indietro'])
		print()
		print(colors.gr+" "+translations['seleziona_account_scollegare'])
		print(colors.cy+translations['seleziona_account_scollegare_line'])

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	i = 1

	n_abilitati = 0
	n_disabilitati = 0	
	
	for each_section in cpass.sections():
		z = 0
		for (each_key, each_val) in cpass.items(each_section):
			if z == 0:
				name = each_val
			elif z == 1:
				apiID =  each_val
			elif z == 2:
				hashID = each_val
			elif z == 7:
				status = each_val
			
			z = z+1

		if mode == 'editvoip':
			if status == 'Enabled':
				n_abilitati = n_abilitati + 1
				status = colors.wg+colors.wy+'  '+colors.wreset
			else:
				n_disabilitati = n_disabilitati + 1
				status = colors.wr+colors.wy+'  '+colors.wreset

			if i < 10:
				print(colors.cy+"  "+str(i) +" | "+status+' '+name)
			else:
				print(colors.cy+" "+str(i) +" | "+status+' '+name)

		else:
			if i < 10:
				print(colors.cy+"  " +str(i) +" | "+colors.wy+name)
			else:
				print(colors.cy+" "+str(i) +" | "+colors.wy+name)

		i = i + 1

	if mode == 'editvoip':
		print()
		print(" "+colors.wg+colors.wy+" "+str(n_abilitati)+" "+translations['account_abilitati_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wr+colors.wy+" "+str(n_disabilitati)+" "+translations['account_disabilitati_cap']+" "+colors.wreset)

	if i == 1 and mode != 'editvoip':
		print()
		print(colors.re+" "+translations['no_account_selezionabile']+colors.wreset)
	print()
	print(colors.cy+"  q | <- "+translations['torna_indietro'])
	print()
	choise = menu.setChoise()

	return choise


def GroupChannelSelector(voip_index):
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	target_group = 'q'

	try:
		voip_index = int(voip_index)-1
	except:
		return False

	try:
		client = test_connection(cpass['credenziali'+str(voip_index)]['phone'],cpass['credenziali'+str(voip_index)]['apiID'],cpass['credenziali'+str(voip_index)]['hashID'],silent_mode=True)
	except:
		target_group = False
		client = False
	
	if client != False:

		chats = []
		last_date = None
		chunk_size = 200
		groups=[]

		try: 
			result = client(GetDialogsRequest(
						 offset_date=last_date,
						 offset_id=0,
						 offset_peer=InputPeerEmpty(),
						 limit=chunk_size,
						 hash = 0
					 ))
			chats.extend(result.chats)
			client.disconnect()
		except Exception as e:
			try:
				client.disconnect()
			except:
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				menu.PrincipalMenu()
			return False
		
		k = 0

		for chat in chats:
			try:
				if hasattr(chat, 'access_hash'):
					if chat.access_hash != None:
						groups.append(chat)
						k = k + 1
			except Exception as o:
				continue

		i=0

		if k > 0:
			for group in groups:
				
				if i < 9:
					print(colors.cy + '  ' + str(i+1) + ' |' + ' ' + colors.wy + group.title)
				else:
					print(colors.cy + ' ' + str(i+1) + ' |' + ' ' + colors.wy + group.title)
				
				i = i + 1
		else:
			try:
				client.disconnect()
			except:
				pass
			
			print()
			print(colors.re+" "+translations['nessun_selezionabile'])

		print()
		print(colors.cy+"  q | <- "+translations['torna_indietro']) 
		g_index = menu.setChoise()

		if g_index != 'q' and g_index != 'Q':
			try:
				g_index = int(g_index)-1
				target_group=groups[g_index]
			except:
				target_group = False
		else:
			target_group = 'q'
	else:
		target_group = False
	return target_group


def EditAccount():
	voip_index = AccountSelector('editvoip')
	voips = getVoips() 
	i = 0

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			EditAccount()

	found = False

	for account in voips:
		if i == (int(voip_index)-1):
			found = True
			if account['status'] == 'Enabled':
				account['status'] = 'Disabled'
				status = 'Disabled'
			else:
				account['status'] = 'Enabled'
				status = 'Enabled'

			name = account['name']

		i = i + 1

	if found == False:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		print(colors.re+" "+translations['scelta_non_valida'])
		EditAccount()
	
	i = 0
	f = 0
	length = len(voips)
	
	while i < length:
		if f == 0:
			method = 'w'
		else:
			method = 'a'	

		accounts = configparser.RawConfigParser()
		
		accounts.add_section('credenziali'+str(i))
	 
		accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
		accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
		accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
		accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
		accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
		accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
		accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
		accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
		
		setup = open('data/config.data', method) 
		accounts.write(setup)
		setup.close()
		
		f = f+1
		i = i+1

	if log == translations['disabilitato_first_cap']:
		os.system('clear')
		banner.banner()

		if status == 'Enabled':
			status_txt = translations['abilitato_lower']
		else:
			status_txt = translations['disabilitato_lower']

		print(colors.gr+" - "+translations['account_first_cap']+" "+name+" "+status_txt+" "+translations['con_successo'])
	EditAccount()


def DeleteAccount():
	voip_index = AccountSelector('deletevoip')
	voips = getVoips() 
	i = 0

	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.ManageAccounts()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			DeleteAccount()
	
	i = 0
	f = 0
	length = len(voips)
	
	if voip_index_mem < 1 or voip_index_mem > length:
		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		print(colors.re+" "+translations['scelta_non_valida'])
		DeleteAccount()

	if log == translations['disabilitato_first_cap']:
		os.system('clear')
		banner.banner()
		print()
		print(colors.wm+colors.wy+" "+translations['scollega_account_cap']+" "+colors.wreset)
		print()
		print(" "+colors.wy+translations['scollega_account_cap_txt_1'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_2'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_3'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_4'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_5'])
		print(" "+colors.wy+translations['scollega_account_cap_txt_6'])
		print()
		print(" "+colors.cy+translations['premi_q_indietro'])
		print()
		
		voip_index_this = int(voip_index)-1
		
		print(colors.re+" "+translations['sei_sicuro_rimuovere']+" "+voips[voip_index_this]['name']+"?")
		print()
		print(colors.cy+"  y | "+colors.wy+" "+translations['procedi_first_cap'])
		print()		
		print(colors.cy+" "+translations['digita_scelta_arrow_line'])
		
		choise = input(colors.cy+" "+translations['digita_tua_scelta_arrow']+" "+colors.gr)

		if choise == 'q' or choise == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			DeleteAccount()
		
		elif choise != 'y' and choise != 'Y':
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			DeleteAccount()
		
		elif choise == 'y' or choise == 'Y':

			cpass = configparser.RawConfigParser()
			cpass.read('data/config.data', encoding="UTF-8")
			
			voip_index_this = int(voip_index)-1

			try:
				client = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
			except:
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				print(colors.re+" "+translations['impossibile_collegarsi_dest_selezionato'])
				client.disconnect()
				
			logged_out = False
			sessions = client(functions.account.GetAuthorizationsRequest()) 
			for session in sessions.authorizations:
				if str(session.api_id) == str(cpass['credenziali'+str(voip_index_this)]['apiID']):
					result = client.log_out()
					logged_out = True

			while i < length:

				if i != (int(voip_index)-1):
					if f == 0:
						method = 'w'
					else:
						method = 'a'

					if (int(voip_index)-1) == 0 and i == 1:
						method = 'w'	

					accounts = configparser.RawConfigParser()
					
					accounts.add_section('credenziali'+str(f))
				 
					accounts.set('credenziali'+str(i), 'name', voips[i]['name'])
					accounts.set('credenziali'+str(i), 'phone', voips[i]['phone'])
					accounts.set('credenziali'+str(i), 'apiID', voips[i]['apiID'])
					accounts.set('credenziali'+str(i), 'hashID', voips[i]['hashID'])
					accounts.set('credenziali'+str(i), 'id', voips[i]['id'])
					accounts.set('credenziali'+str(i), 'access_hash', voips[i]['access_hash'])
					accounts.set('credenziali'+str(i), 'username', voips[i]['username'])
					accounts.set('credenziali'+str(i), 'status', voips[i]['status'])
					
					setup = open('data/config.data', method) 
					accounts.write(setup)
					setup.close()
				
				else:
					if i == 0 and (int(voip_index)-1) == 0:
						accounts = configparser.RawConfigParser()
						setup = open('data/config.data', 'w') 
						accounts.write(setup)
						setup.close()

					name = voips[i]['name']

				f = f+1
				i = i+1
	
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
				
			print(colors.gr+" [+] "+translations['account_first_cap']+" "+name+" "+translations['eliminato_successo'])
			if logged_out == False:
				print(colors.re+" "+translations['ma_non_sconnesso']+colors.wreset)
			
			DeleteAccount()
