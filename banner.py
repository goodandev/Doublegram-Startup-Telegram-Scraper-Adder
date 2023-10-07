import colors, time, requests, os, configparser
from random import randint
global translations

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

with open('translations/'+lang+'.data', encoding="UTF-8") as f:
	cpass = configparser.RawConfigParser()
	cpass.read_file(f)

	for each_section in cpass.sections():
		for (each_key, each_val) in cpass.items(each_section):
			translations[each_key] = each_val


colors.getColors()

def banner(is_update=False,last_version=False,notice=False,start=False):
	if start == True:
		os.system("clear")
		print()
		print(colors.cy+" .::::::::::..        "+colors.gr+"                  ")
		print(colors.cy+" -+++++++++++++=-.    "+colors.gr+"                  ")
		print(colors.cy+" -+++       .:++++-   "+colors.gr+"                  ")
		print(colors.cy+" -+++          =+++:  "+colors.gr+"     ............ ")
		print(colors.cy+" -+++           +++=  "+colors.gr+"  .--::...::---::.")
		print(colors.cy+" -+++           ++++  "+colors.gr+" .--:       :--:  ")
		print(colors.cy+" -+++           ++++  "+colors.gr+" :--:        ---  ")
		print(colors.cy+" -+++           ++++  "+colors.gr+" .--:.     .:--:  ")
		print(colors.cy+" -+++          :+++-  "+colors.gr+"   :---------:.   ")
		print(colors.cy+" -+++         :++++   "+colors.gr+"  :--..           ")
		print(colors.cy+" -+++------==++++-    "+colors.gr+" .---:........    ")
		print(colors.cy+" -===========-:.      "+colors.gr+"  .:-----------:  ")
		print("                                   :--. ")
		print("                       "+colors.gr+" :::::...:::--:  ")
		print("                       "+colors.gr+" .::::::::::..   ")
		
		time.sleep(0.5)
		print()
		print(" "+translations['piu_informazioni_su'])
		print(" "+translations['per_supporto_scrivere'])
		time.sleep(2)

		if is_update == True:
			print()
			print(" "+translations['aggiornamento_cap'])
			print(" - Doublegram "+last_version+" "+translations['ora_disponibile'])

		if notice != False:
			print()
			print(" "+translations['note_sviluppatore_cap'])
			print(" "+notice)

		if is_update == True or notice != False:
			print()
			choise = input(" "+translations['invio_continuare'])
		
		os.system("clear")

	print(colors.gr+"------------------------")
	print(colors.gr+"|"+colors.wy+colors.wm+" -------------------- "+colors.wreset+colors.gr+"|")
	print(colors.gr+"|"+colors.wm+colors.wy+" | DOUBLEGRAM V1.2  | "+colors.wreset+colors.gr+"|")
	print(colors.gr+"|"+colors.wm+colors.wy+" | STARTUP EDITION  | "+colors.wreset+colors.gr+"|")
	print(colors.gr+"|"+colors.wy+colors.wm+" -------------------- "+colors.wreset+colors.gr+"|")
	print(colors.gr+"------------------------")
