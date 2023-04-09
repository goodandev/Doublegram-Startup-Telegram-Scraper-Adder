import os, sys, csv, time, configparser, traceback, colors, menu, asyncio, settings, banner
from voip import AccountSelector, GroupChannelSelector, test_connection, getVoips, activeAnalysis, blockAnalysis
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import functions, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser

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

log = settings.getSetting('log','general_settings')


def AddMembers():
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = AccountSelector(mode='members')
	
	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		menu.MembersMenu()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			AddMembers()

		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()

		voips = getVoips()
		length = len(voips)
	
		if voip_index_mem < 1 or voip_index_mem > length:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			AddMembers()
		
		voip_index_name = int(voip_index)-1
		voip_name = cpass['credenziali'+str(voip_index_name)]['name']
		print()
		print(colors.wm+colors.wy+" "+translations['preleva_e_aggiungi_cap']+" "+colors.wreset)
		print(colors.wm+colors.wy+" "+translations['account_utilizzato_cap']+" "+voip_name+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_da_cui_prelevare_cap'])
		print(" "+colors.cy+translations['seleziona_da_cui_prelevare_line'])
		
		selected_group = GroupChannelSelector(voip_index)
		
		if selected_group == 'q' or selected_group == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			menu.MembersMenu()
		elif selected_group == False:
			print()
			print(colors.re+" "+translations['impossibile_questo_account'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			AddMembers()
		else:	
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			scrape_result = ScrapeMethodSelector(voip_index, selected_group, voip_name, mode='Add')


def RewriteMembers():
	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")
	
	voip_index = AccountSelector(mode='members-r')
	
	if voip_index == 'q' or voip_index == 'Q':
		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		menu.MembersMenu()
	else:
		try:
			voip_index_mem = int(voip_index)
		except:
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			RewriteMembers()

		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		
		voips = getVoips()
		length = len(voips)
		
		if voip_index_mem < 1 or voip_index_mem > length:
			if log == translations['disabilitato_first_cap']:
				os.system('clear')
				banner.banner()
			print(colors.re+" "+translations['scelta_non_valida'])
			RewriteMembers()


		voip_index_name = int(voip_index)-1
		voip_name = cpass['credenziali'+str(voip_index_name)]['name']
		
		print()
		print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)
		print(colors.wm+colors.wy+" "+translations['account_utilizzato_cap']+" "+voip_name+colors.wreset)
		print()
		print(colors.gr+" "+translations['seleziona_da_cui_prelevare_cap'])
		print(colors.cy+translations['seleziona_da_cui_prelevare_line'])
		
		selected_group = GroupChannelSelector(voip_index)
		if selected_group == 'q' or selected_group == 'Q':
			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			menu.MembersMenu()
		elif selected_group == False:
			print()
			print(colors.re+" "+translations['impossibile_questo_account'])
			choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()
			RewriteMembers()
		else:
			try:
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				scrape_result = ScrapeMethodSelector(voip_index, selected_group, voip_name, mode='Rewrite')
			except Exception as e:
				print()
				print(colors.re+" "+translations['impossibile_scaricare_da_destinazione'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				RewriteMembers()
			
		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		menu.MembersMenu()


def ScrapeMembers(voip_index, selected_group, mode, d, tot_recent_users, channel_connect, client):

	if mode == 'Rewrite':
		method = 'w'
		list_already = False
	elif mode == 'Add':
		method = 'a'
		list_already = []
		with open(r"members/members.csv", encoding='UTF-8') as f:  
			rows = csv.reader(f,delimiter=",",lineterminator="\n")
			next(rows, None)
			for row in rows:
				list_already.append(str(row[1]))

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = int(voip_index)-1

	if client != False:
		try:
			target_group_entity = client.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))
			is_target = True
		except Exception as e:
			is_target = False
		
		if is_target == True:
			try:
				activeAnalysis()
				all_admin = client.get_participants(target_group_entity, aggressive=False, filter=ChannelParticipantsAdmins)
				blockAnalysis()
			except:
				all_admin = False

			try:
				print()
				print(colors.gr+" "+translations['prelevo_membri'])
				all_participants = client.get_participants(target_group_entity, aggressive=False)
				client.disconnect()

			except Exception as e:
				all_participants = False
		else:
			all_participants = False

		if all_participants != False:
			with open("members/members.csv",method,encoding='UTF-8') as f:
				
				print(colors.gr+" "+translations['salvo_membri_in_file'])
				print(colors.gr+" "+translations['attendi'])
				
				writer = csv.writer(f,delimiter=",",lineterminator="\n")
				if method == 'w':
					writer.writerow(['username','user id', 'access hash', 'name', 'group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated'])
				
				voips = getVoips()

				for user in all_participants:
					found_in_own = False
					found_in_already = False

					for x in voips:
						if x['id'] == str(user.id):
							found_in_own = True

					if mode == 'Add':
						for x in list_already:
							if x == str(user.id):
								found_in_already = True

					if found_in_own == False and found_in_already == False:
						if user.username:
							username = user.username
						else:
							username = ""
						if user.first_name:
							first_name = user.first_name
						else:
							first_name = ""
						if user.last_name:
							last_name = user.last_name
						else:
							last_name = ""
						name = (first_name + ' ' + last_name).strip()

						if user.photo:
							try:
								dc_id = user.photo.dc_id
								have_photo = True
							except:
								dc_id = False
								have_photo = False
						else:
							dc_id = False
							have_photo = False

						if user.bot != False:
							is_bot = True
						else:
							is_bot = False

						if user.phone != None:
							phone = user.phone
						else:
							phone = False

						is_admin = False

						if all_admin != False:
							for admin in all_admin:
								if admin.id == user.id:
									is_admin = True

						writer.writerow([username,user.id,user.access_hash,name,selected_group.title,selected_group.id,is_bot,is_admin,dc_id,have_photo,phone,0])      
			added = True
		else:
			added = False

		return added


def ScrapeMethodSelector(voip_index, selected_group, voip_name, mode):

	if mode == 'Rewrite':
		method = 'w'
	elif mode == 'Add':
		method = 'a'
		list_already = []
		
		with open(r"members/members.csv", encoding='UTF-8') as f:  
			rows = csv.reader(f,delimiter=",",lineterminator="\n")
			next(rows, None)
			for row in rows:
				list_already.append(str(row[1]))

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = int(voip_index)-1

	client = test_connection(cpass['credenziali'+str(voip_index)]['phone'],cpass['credenziali'+str(voip_index)]['apiID'],cpass['credenziali'+str(voip_index)]['hashID'],silent_mode=True)
	
	if client != False:

		channel_connect = client.get_entity(selected_group)
		channel_full_info = client(GetFullChannelRequest(channel=channel_connect))

		try:
			activeAnalysis()
			all_admin = client.get_participants(channel_connect, aggressive=False, filter=ChannelParticipantsAdmins)
			blockAnalysis()
		except:
			all_admin = False

		total = channel_full_info.full_chat.participants_count

		total_recent_request = client(functions.channels.GetParticipantsRequest(
								channel=channel_connect,
								filter=types.ChannelParticipantsRecent(),
								offset=0,
								limit=200,
								hash=0
							))

		total_recent_request_users = total_recent_request.users
		tot_recent_users = int(total_recent_request.count)

		d = tot_recent_users/200

		print()
		print(colors.wm+colors.wy+" "+translations['preleva_e_sovrascrivi_cap']+" "+colors.wreset)
		print(colors.wm+colors.wy+" "+translations['account_utilizzato_cap']+" "+voip_name+colors.wreset)

		result = ScrapeMembers(voip_index, selected_group, mode, d, tot_recent_users, channel_connect, client)

		if result != True:

			print()
			try:
				activeAnalysis()
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=201,
									limit=400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 4%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=401,
									limit=600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 6%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=601,
									limit=800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 8%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=801,
									limit=1000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 10%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1001,
									limit=1200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 12%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1201,
									limit=1400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 14%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1401,
									limit=1600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 16%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1601,
									limit=1800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 18%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=1801,
									limit=2000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 20%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2001,
									limit=2200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 22%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2201,
									limit=2400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 24%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2401,
									limit=2600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 26%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2601,
									limit=2800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 28%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=2801,
									limit=3000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 30%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3001,
									limit=3200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 32%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3201,
									limit=3400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 34%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3401,
									limit=3600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 36%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3601,
									limit=3800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 38%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=3801,
									limit=4000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 40%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4001,
									limit=4200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 42%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4201,
									limit=4400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 44%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4401,
									limit=4600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 46%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4601,
									limit=4800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 48%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=4801,
									limit=5000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 50%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5001,
									limit=5200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 52%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5201,
									limit=5400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 54%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5401,
									limit=5600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 56%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5601,
									limit=5800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 58%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=5801,
									limit=6000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 60%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6001,
									limit=6200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 62%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6201,
									limit=6400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 64%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6401,
									limit=6600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 66%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6601,
									limit=6800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 68%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=6801,
									limit=7000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 70%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7001,
									limit=7200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 72%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7201,
									limit=7400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 74%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7401,
									limit=7600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 76%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7601,
									limit=7800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 78%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=7801,
									limit=8000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 80%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8001,
									limit=8200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 82%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8201,
									limit=8400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 84%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8401,
									limit=8600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 86%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8601,
									limit=8800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 88%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=8801,
									limit=9000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 90%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9001,
									limit=9200,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 92%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9201,
									limit=9400,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 94%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9401,
									limit=9600,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 96%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9601,
									limit=9800,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 98%", end="\r")
				
				total_recent_request_call = client(functions.channels.GetParticipantsRequest(
									channel=channel_connect,
									filter=types.ChannelParticipantsRecent(),
									offset=9801,
									limit=10000,
									hash=0
								))
				total_recent_request_users = total_recent_request_users + total_recent_request_call.users
				print(colors.gr+" [+] Completamento: 100%", end="\r")

				blockAnalysis()

				all_participants = total_recent_request_users
				
				if all_participants != False:
					with open("members/members.csv",method,encoding='UTF-8') as f:

						print(colors.gr+" "+translations['salvo_membri_in_file'])
						print(colors.gr+" "+translations['attendi'])

						writer = csv.writer(f,delimiter=",",lineterminator="\n")
						if method == 'w':
							writer.writerow(['username','user id', 'access hash','name','group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated'])
						
						voips = getVoips()

						for user in all_participants:

							found_in_own = False
							found_in_already = False
							
							for x in voips:
								if x['id'] == str(user.id):
									found_in_own = True

							if mode == 'Add':
								for x in list_already:
									if x == str(user.id):
										found_in_already = True

							if found_in_own == False and found_in_already == False:
								if user.username:
									username = user.username
								else:
									username = ""
								if user.first_name:
									first_name = user.first_name
								else:
									first_name = ""
								if user.last_name:
									last_name = user.last_name
								else:
									last_name = ""
								name = (first_name + ' ' + last_name).strip()

								if user.photo:
									dc_id = user.photo.dc_id
									have_photo = True
								else:
									dc_id = False
									have_photo = False

								if user.bot != False:
									is_bot = True
								else:
									is_bot = False

								if user.phone != None:
									phone = user.phone
								else:
									phone = False

								is_admin = False

								if all_admin != False:
									for admin in all_admin:
										if admin.id == user.id:
											is_admin = True

								writer.writerow([username,user.id,user.access_hash,name,selected_group.title,selected_group.id,is_bot,is_admin,dc_id,have_photo,phone,0])      
						added = True
				else:
					added = False
			except Exception as e:
				added = False

		else:
			added = True

		if added == True:
			print(colors.gr+" "+translations['lista_salvata'])
		else:
			print(colors.re+" "+translations['impossibile_scaricare_da_destinazione'])

		client.disconnect()

		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

		if log == translations['disabilitato_first_cap']:
			os.system("clear")
			banner.banner()
		menu.MembersMenu()


async def scrapeBigGroup(voip_index, selected_group, mode, d, tot_recent_users):
	if mode == 'Rewrite':
		method = 'w'
	elif mode == 'Add':
		method = 'a'

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	voip_index = int(voip_index)-1

	try:
		client = TelegramClient('sessions/'+cpass['credenziali'+str(voip_index)]['phone'],cpass['credenziali'+str(voip_index)]['apiID'],cpass['credenziali'+str(voip_index)]['hashID'])
	except Exception as e:
		print(colors.re+" "+translations['non_possibile_prova_altro_account'])

	added = False 

	if client != False:

		async with client:

			print(colors.gr+" "+translations['tentativo_metodo_due'])
			
			try:
				target_group_entity = await client.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))
			except Exception as e:
				target_group_entity = False

			try:
				all_admin = await client.get_participants(target_group_entity, aggressive=False, filter=ChannelParticipantsAdmins)
			except:
				all_admin = False

			try:
				await client.connect()
				if not await client.is_user_authorized():
					await client.send_code_request(cpass['credenziali'+str(voip_index)]['phone'])
					await client.sign_in(cpass['credenziali'+str(voip_index)]['phone'], input(colors.cy+'[+] Inserisci il codice ricevuto su Telegram --> '+colors.gr))
					await client.get_me()

			except Exception as e:
				client = False

			if client != False and target_group_entity != False:

				all_participants = ''
				n_users = 0
				f = 0
				y = 1
				l = 0
				u = 0

				for x in range(int(d)):

					perc = round((100*int(x))/round(int(d)))
					print(str(perc)+"%", end="\r")

					if f == 0:
						o = int(f)*200
						k = int(y)*200
					else:
						o = int(f)*200+1
						k = int(y)*200

					try:
						result = await client(functions.channels.GetParticipantsRequest(
								channel=target_group_entity,
								filter=types.ChannelParticipantsRecent(),
								offset=o,
								limit=k,
								hash=0
							))
						if u == 0:
							all_participants = result.users
						else:
							all_participants = all_participants+result.users

						b = 0
						for user in result.users:
							b = b+1

						u = u + 1

					except Exception as e:
						y = y + 1
						f = f + 1
						break

					y = y + 1
					f = f + 1

					if len(result.users) == 0:
						break

				diff = int(tot_recent_users)-int(k)

				if int(diff) > 0:
					try:
						result = await client(functions.channels.GetParticipantsRequest(
								channel=target_group_entity,
								filter=types.ChannelParticipantsRecent(),
								offset=k,
								limit=tot_recent_users,
								hash=0
							))

						all_participants = all_participants+result.users

					except Exception as e:
						await client.disconnect()

				await client.disconnect()

				if all_participants != False:
					with open("members/members.csv",method,encoding='UTF-8') as f:
						
						print(colors.gr+" "+translations['salvo_membri_in_file'])
						print(colors.gr+" "+translations['attendi'])
						
						writer = csv.writer(f,delimiter=",",lineterminator="\n")
						if method == 'w':
							writer.writerow(['username','user id', 'access hash','name','group', 'group id', 'is_bot', 'is_admin', 'dc_id', 'have_photo', 'phone', 'elaborated'])
						
						for user in all_participants:
							if user.username:
								username = user.username
							else:
								username = ""
							if user.first_name:
								first_name = user.first_name
							else:
								first_name = ""
							if user.last_name:
								last_name = user.last_name
							else:
								last_name = ""
							name = (first_name + ' ' + last_name).strip()

							if user.photo:
								dc_id = user.photo.dc_id
								have_photo = True
							else:
								dc_id = False
								have_photo = False

							if user.bot != False:
								is_bot = True
							else:
								is_bot = False

							if user.phone != None:
								phone = user.phone
							else:
								phone = False

							is_admin = False

							if all_admin != False:
								for admin in all_admin:
									if admin.id == user.id:
										is_admin = True

							writer.writerow([username,user.id,user.access_hash,name,selected_group.title,selected_group.id,is_bot,is_admin,dc_id,have_photo,phone,0])      
						
						print(colors.gr+" "+translations['lista_salvata'])
						added = True
				else:
					added = False
			else:
				added = False
	else:
		added = False

	return added


def scrapeBigGroupInitializer(voip_index, selected_group, mode, d, tot_recent_users):
	result = asyncio.run(scrapeBigGroup(voip_index, selected_group, mode, d, tot_recent_users))
	return result
	