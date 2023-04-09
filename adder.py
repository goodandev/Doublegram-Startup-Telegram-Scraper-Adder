import os, sys, csv, re, time, configparser, traceback, random, banner, asyncio,menu, colors, settings
from telethon.sync import TelegramClient
from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth
from telethon.tl.functions.messages import GetDialogsRequest, ImportChatInviteRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError, UsersTooMuchError
from voip import AccountSelector, GroupChannelSelector, test_connection, getVoips, activeAnalysis, blockAnalysis
from datetime import date

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


async def VoipAdderJob(client,users,selected_group,group_entity_complete,invite,phone,change_account_n_requests,stop_max_adding,casual_pause_times,between_adding_pause,start_point_members_file,add_using,account_name):
	try:
		await client.connect()
		if not await client.is_user_authorized():
			await client.send_code_request(phone)
			await client.sign_in(phone, input(colors.cy+' '+translations['inserisci_codice_ricevuto']+' '+colors.gr))
			await client.get_me()

	except Exception as e:
		client = False
		print("")
		print(colors.wm+colors.wy+" "+translations['account_utilizzato_cap']+" "+account_name+colors.wreset)
		print(colors.re+" "+translations['impossibile_questo_account']+colors.wreset)

	if client != False:
		async with client:
			this_voip = await client.get_me()
			
			print("")
			print(colors.wm+colors.wy+" "+translations['account_utilizzato_cap']+" "+this_voip.first_name+colors.wreset)
			
			breaker = False

			for user in users:
				if user['last_added'] == 1:
					last_added_n = last_added_n + 1

			if stop_max_adding != translations['nessun_limite']:
				if last_added_n >= int(stop_max_adding):
					breaker = True
					print(" "+translations['interruzione_limite_raggiunto'])

			try:
				target_group_entity = await client.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))
			except:
				print(colors.re+" "+translations['errore_imprevisto'])
				target_group_entity = False

			if target_group_entity != False and breaker == False:

				n = 0
				generic_error = 0
				fd = 0

				for user in users:

					if change_account_n_requests != translations['nessun_limite']:
						if n == int(change_account_n_requests):
							print("")
							print(" "+translations['passaggio_account_successivo'])
							break

					if (n+1) % 70 == 0:
						if casual_pause_times != translations['nessuna_pausa']:
							print(" "+translations['pausa']+" "+str(casual_pause_times))
							params = []
							i = 0
							for pause_step in casual_pause_times:
								if i == 0:
									params_0 = pause_step
								else:
									params_1 = pause_step
								i = i + 1

							if i == 1:
								time.sleep(params_0)
							else:
								time.sleep(random.randrange(params_0,params_1))

					user_can_be_added = True 

					if start_point_members_file == translations['da_interrotto']:
						if user['elaborated'] != '0':
							user_can_be_added = False
						else:
							fd = fd+1

					if add_using == 'Username' and user_can_be_added != False:
						if user['username'] == '':
							user_can_be_added = False

					if user_can_be_added != False and breaker == False:
						exit = True

						if add_using == translations['username_first_cap']:
							try:
								user_to_add = await client.get_input_entity(user['username'])
								exit = False
							except Exception as e:
								exit = True

						elif add_using == translations['id_utente_cap']:
							try:
								user_to_add =  InputPeerUser(user['id'], user['access_hash'])
								exit = False
							except Exception as e:
								exit = True            
						
						elif add_using == translations['user_id_opt']:
							if user['username'] == "":
								user_to_add =  InputPeerUser(user['id'], user['access_hash'])
							else:
								try:
									user_to_add = await client.get_input_entity(user['username'])
									exit = False
								except Exception as e:
									exit = True                        

						if target_group_entity != False and exit == False:

							print("")
							print(" "+translations['utente_arrow']+" "+str(user['id'])+" -> ", end=" ")

							try:
								await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
								print(" "+colors.wg+" "+colors.wreset)
								
								user['elaborated'] = 1
								user['last_added'] = 1
								n += 1

								if between_adding_pause != translations['nessuna_pausa']:
									params = []
									i = 0
									for pause_step in between_adding_pause:
										if i == 0:
											params_0 = pause_step
										else:
											params_1 = pause_step
										i = i + 1

									if i == 1:
										time.sleep(params_0)
									else:
										time.sleep(random.randrange(params_0,params_1))

							except PeerFloodError as e:
								voip_error = True
								print(" "+colors.wr+translations['flood_cap']+colors.wreset)
								print("")
								break
							
							except UserPrivacyRestrictedError:
								if between_adding_pause != translations['nessuna_pausa']:
									
									params = []
									i = 0
									
									for pause_step in between_adding_pause:
										if i == 0:
											params_0 = pause_step
										else:
											params_1 = pause_step
										i = i + 1

									if i == 1:
										time.sleep(params_0)
									else:
										time.sleep(random.randrange(params_0,params_1))

								user['elaborated'] = 1
								n += 1
								print(" "+colors.wr+" "+colors.wreset)
							
							except FloodWaitError as e:
								print()
								print()
								print(colors.wr+" "+translations['account_flood']+colors.wreset)
								voip_error = True
								print(colors.re+" "+translations['attesa_richiesta']+" ", e.seconds, end=" ")
								print(" "+translations['secondi'])
								print("")
								break

							except Exception as e:
								print(" "+colors.wr+" "+colors.wreset)
								
								user['elaborated'] = 1
								n += 1
								
								if between_adding_pause != translations['nessuna_pausa']:
									#print("[+] Pausa tra un'aggiunta e l'altra")
									params = []
									i = 0
									for pause_step in between_adding_pause:
										if i == 0:
											params_0 = pause_step
										else:
											params_1 = pause_step
										i = i + 1

									if i == 1:
										time.sleep(params_0)
									else:
										time.sleep(random.randrange(params_0,params_1))
						else:
							if exit == True:
								print("")
								user['elaborated'] = 1
								print(" "+translations['utente_arrow']+" "+str(user['id'])+" -> ", end=" ")
								print(" "+colors.wr+" "+colors.wreset)

				v = 0
				for user in users:
					if v == 0:
						with open("members/members.csv",'w',encoding='UTF-8') as f:
							writer = csv.writer(f,delimiter=",",lineterminator="\n")
							writer.writerow(['username','user id', 'access hash','name','group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated'])
							writer.writerow([user['username'],user['id'],user['access_hash'],user['name'],user['group'],user['group_id'],user['is_bot'],user['is_admin'],user['dc_id'],user['have_photo'],user['phone'],user['elaborated']])           
							v = v + 1
					else:
						with open("members/members.csv",'a',encoding='UTF-8') as f:
							writer = csv.writer(f,delimiter=",",lineterminator="\n")
							writer.writerow([user['username'],user['id'],user['access_hash'],user['name'],user['group'],user['group_id'],user['is_bot'],user['is_admin'],user['dc_id'],user['have_photo'],user['phone'],user['elaborated']])           
	return users

			
async def StartAdder(voips,selected_group,group_entity_complete,invite,all_participants,all_kicked,all_banned):
	activeAnalysis()
	print("")
	print(colors.wm+colors.wy+" "+translations['aggiunta_membri_cap']+colors.wreset)
	print(colors.wm+colors.wy+" "+translations['destinazione_cap']+" "+selected_group.title+colors.wreset)
	print("")

	change_account_n_requests = settings.getSetting('change_account_n_requests','adding_settings')
	if change_account_n_requests != translations['nessun_limite']:
		change_account_n_requests = [int(s) for s in re.findall(r'\b\d+\b', change_account_n_requests)]
		change_account_n_requests = int(''.join(str(i) for i in change_account_n_requests))

	stop_max_adding = settings.getSetting('stop_max_adding','adding_settings')
	if stop_max_adding != translations['nessun_limite']:
		stop_max_adding = [int(s) for s in re.findall(r'\b\d+\b', stop_max_adding)]
		stop_max_adding = int(''.join(str(i) for i in stop_max_adding))

	casual_pause_times = settings.getSetting('casual_pause_times','adding_settings')
	if casual_pause_times != translations['nessuna_pausa']:
		casual_pause_times = [int(s) for s in re.findall(r'\b\d+\b', casual_pause_times)]
		casual_pause_times_txt = str(','.join(str(i) for i in casual_pause_times))

	between_adding_pause = settings.getSetting('between_adding_pause','adding_settings')
	if between_adding_pause != translations['nessuna_pausa']:
		between_adding_pause = [int(s) for s in re.findall(r'\b\d+\b', between_adding_pause)]
		between_adding_pause_txt = str(','.join(str(i) for i in between_adding_pause))

	change_account_pause = settings.getSetting('change_account_pause','adding_settings')
	if change_account_pause != translations['nessuna_pausa']:
		change_account_pause = [int(s) for s in re.findall(r'\b\d+\b', change_account_pause)]
		change_account_pause_txt = str(','.join(str(i) for i in change_account_pause))

	start_point_members_file = settings.getSetting('start_point_members_file','adding_settings')
	add_using = settings.getSetting('add_using','adding_settings')

	users = []
	users_final = []
	
	i = 0
	users_already = 0

	with open(r"members/members.csv", encoding='UTF-8') as f:  
		rows = csv.reader(f,delimiter=",",lineterminator="\n")
		next(rows, None)
		for row in rows:
			user = {}
			user['username'] = row[0]
			user['id'] = int(row[1])
			user['access_hash'] = int(row[2])
			user['name'] = row[3]
			user['elaborated'] = row[11]
			user['is_bot'] = row[6]
			user['is_admin'] = row[7]
			user['phone'] = row[10]
			user['dc_id'] = row[8]
			user['have_photo'] = row[9]
			user['last_added'] = 0
			user['group'] = row[4]
			user['group_id'] = row[5]
			users.append(user)

			if all_participants != False:
				found = False
				for partecipant in all_participants:
					if partecipant.access_hash == user['access_hash']:
						found = True
						user['elaborated'] = 1
						users_already = users_already + 1

			if all_kicked != False:
				found = False
				for partecipant in all_kicked:
					if partecipant.access_hash == user['access_hash']:
						found = True
						user['elaborated'] = 1

			if all_banned != False:
				found = False
				for partecipant in all_banned:
					if partecipant.access_hash == user['access_hash']:
						found = True
						user['elaborated'] = 1


		users_final = users
		print(colors.cy+" "+translations['utenti_ignorati_gia_presenti']+str(users_already))
	
	t = 0

	print(colors.cy+" "+translations['avvio_adding_in_corso'])

	for account in voips:
		if account['status'] == 'Enabled':
			if change_account_pause != translations['nessuna_pausa']:
				params = []
				i = 0
				for pause_step in change_account_pause:
					if i == 0:
						params_0 = pause_step
					else:
						params_1 = pause_step
					i = i + 1

				if t > 0:
					if i == 1:
						time.sleep(params_0)
					else:
						time.sleep(random.randrange(params_0,params_1))
				else:
					t = t+1

			client_voip = TelegramClient('sessions/'+account['phone'],account['apiID'],account['hashID'])

			phone = account['phone']
			await asyncio.gather(
				VoipAdderJob(client_voip,users_final,selected_group,group_entity_complete,invite,phone,change_account_n_requests,stop_max_adding,casual_pause_times,between_adding_pause,start_point_members_file,add_using,account['name'])
			)


def startAdder(voips,selected_group,group_entity_complete,invite,all_participants,all_kicked,all_banned):
	asyncio.new_event_loop().run_until_complete(StartAdder(voips,selected_group,group_entity_complete,invite,all_participants,all_kicked,all_banned))
