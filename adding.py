import os, sys, csv, re, time, configparser, traceback, random, asyncio, banner, adder, colors, menu, settings
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, AddChatUserRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights
from datetime import datetime, timedelta
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, ChannelParticipantsBanned, ChannelParticipantsKicked
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest, EditBannedRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.functions.messages import ExportChatInviteRequest
from voip import AccountSelector, GroupChannelSelector, test_connection, getVoips, activeAnalysis, blockAnalysis

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


def AddUsers(voip_index):

	cpass = configparser.RawConfigParser()
	cpass.read('data/config.data', encoding="UTF-8")

	u  = 0

	with open(r"members/members.csv", encoding='UTF-8') as f:  
		rows = csv.reader(f,delimiter=",",lineterminator="\n")
		next(rows, None)
		for row in rows:
			u = u + 1

	if u > 0:
		is_error = False

		if voip_index == None:
			voip_index = AccountSelector('adding')
		else:
			is_error = True

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
					os.system("clear")
					banner.banner()
				print(colors.re+" [!] Scelta non valida")
				AddUsers(voip_index=None)

			if log == translations['disabilitato_first_cap']:
				os.system("clear")
				banner.banner()

			if is_error == True:
				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				print()
				print(colors.re+" "+translations['impossibile_questo_account'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)
				AddUsers(None)

			print()
			print(colors.wm+colors.wy+" "+translations['inserisci_utenti_cap']+" "+colors.wreset)
			print()
			print(colors.gr+" "+translations['seleziona_destinazione_cap']+" ")
			print(colors.cy+translations['line_destinazione_cap'])
			selected_group = GroupChannelSelector(voip_index)
			
			if selected_group == 'q' or selected_group == 'Q':
				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				AddUsers(voip_index=None)
			else:
				if selected_group == False:
					if log == translations['disabilitato_first_cap']:
						os.system("clear")
						banner.banner()
					AddUsers(voip_index)

				voips = getVoips()
				voip_index_this = int(voip_index)-1

				try:
					client_voip = test_connection(cpass['credenziali'+str(voip_index_this)]['phone'],cpass['credenziali'+str(voip_index_this)]['apiID'],cpass['credenziali'+str(voip_index_this)]['hashID'],silent_mode=True)
				except:
					if log == translations['disabilitato_first_cap']:
						os.system("clear")
						banner.banner()
					print(colors.re+" "+translations['impossibile_collegarsi_selezionato'])
					AddUsers(voip_index=None)

				if not hasattr(selected_group, 'access_hash'):
					selected_group.access_hash = selected_group.migrated_to.access_hash

				try:
					group_entity_complete =  client_voip.get_entity(InputPeerChannel(selected_group.id, selected_group.access_hash))

				except:
					print(colors.re+" "+translations['non_possibile_collegarsi_destinazione'])
					client_voip.disconnect()
					menu.PrincipalMenu()

				try:
					invite = client_voip(ExportChatInviteRequest(group_entity_complete.id))
				except:
					invite = False

				if log == translations['disabilitato_first_cap']:
					os.system("clear")
					banner.banner()
				
				print(translations['recupero_presenti'])

				try:
					
					all_participants = client_voip.get_participants(selected_group, aggressive=False)
				except:
					print(translations['recupero_presenti_1'])
					all_participants = False

				try:
					all_kicked = client_voip.get_participants(selected_group, aggressive=False, filter=ChannelParticipantsKicked)
				except:
					print(translations['recupero_presenti_2'])
					all_kicked = False

				try:
					all_banned = client_voip.get_participants(selected_group, aggressive=False, filter=ChannelParticipantsBanned)
				except:
					print(translations['recupero_presenti_3'])
					all_banned = False

				client_voip.disconnect()

				adder.startAdder(voips,selected_group,group_entity_complete,invite,all_participants,all_kicked,all_banned)
				blockAnalysis()
				print()
				print(colors.cy+" "+translations['operazione_adding_conclusa'])
				print(colors.cy+" "+translations['line_op_adding_conclusa'])
				choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

				if log == translations['disabilitato_first_cap']:
					os.system('clear')
					banner.banner()
				menu.AddingMenu()
			
	else:
		print()
		print(colors.re+" "+translations['lista_membri_vuota']+"\n "+translations['preleva_membri_per_aggiungerli'])
		print(colors.cy+" "+translations['line_op_adding_conclusa'])
		choise = input(colors.cy+" "+translations['invio_continuare']+" "+colors.gr)

		if log == translations['disabilitato_first_cap']:
			os.system('clear')
			banner.banner()
		menu.AddingMenu()
