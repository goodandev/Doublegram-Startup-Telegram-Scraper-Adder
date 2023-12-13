#!/bin/env python3
# Author : Doublegram.me
import os, sys, csv, time, traceback, random, requests, configparser, uuid, socket

global is_update
global last_version
global notice
global translations

import banner, menu, settings

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
	print()
	print(" [+] Select your language")
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

	lang = chosen_lang
	os.system("clear")


if lang == 'IT' or lang == 'EN':
	with open('translations/'+lang+'.data', encoding="UTF-8") as f:
		cpass = configparser.RawConfigParser()
		cpass.read_file(f)

		for each_section in cpass.sections():
			for (each_key, each_val) in cpass.items(each_section):
				translations[each_key] = each_val

breaker = False 

current_version = '1.3.1'
current_edition = 'STARTUP_EDITION'
serial_id = 'EO9K2W3E9JRF76E5671DIEM3'

url = "https://dblgrm.me/version_verification.php?edition="+current_edition

try:
	resp = requests.get(url)
	last_version = resp.text
except:
	print(" "+translations['impossibile_conn'])
	choise = input(" "+translations['invio_continuare'])
	breaker = True
	sys.exit()


if last_version != current_version and last_version != 'no':
	is_update = True
else:
	is_update = False

url = "https://dblgrm.me/notice.php?ver="+current_version+'&edition='+current_edition
resp = requests.get(url)
notice = resp.text

if notice == 'no':
	notice = False



cpass = configparser.RawConfigParser()

settings.checkSettings(if_false_create=True)
banner.banner(is_update,last_version,notice,start=True)
menu.PrincipalMenu(show_menu=False)
