##########################################################
# BOTTEH CHATANGO BOT BY SORCHMASTER
# Thanks to
# Lumz Soda and others ^^
##########################################################
# python imports
##########################################################
import ch
import random
import sys
import os
import re
import cgi
import traceback
import time
import urllib
import datetime
import binascii
import youtube
#import helperCmd
import json
import cmds
################
###########################################################
#ENDS HERE
###########################################################
###########################################################
#VARS
###########################################################
lockdown = False
##################
# TIMER STUFF #
startTime = time.time()
################
#STATUS
#######
filename = "status.txt"
file = open(filename, 'w')
print("[INF]Setting status to online...")
time.sleep(2)
file.write("Awake")
file.close()
#

#definitions
dictionary = dict() #volatile... of course...
f = open("definitions.txt", "r") # read-only
print("[INF]Loading Definitions...")
time.sleep(1)
for line in f.readlines():
	try:
		if len(line.strip())>0:
			word, definition, name = json.loads(line.strip())
			dictionary[word] = json.dumps([definition, name])
	except:
		print("[ERR]Cant load definition: %s" % line)
f.close()

#OWNER#
spermitted = []
f = open("spermitted.txt", "r") # read-only
print("[INF]Loading Supermasters...")
time.sleep(1)
for name in f.readlines():
	if len(name.strip())>0: spermitted.append(name.strip())
f.close()
# END #

#MASTERS#
permitted = []
f = open("permitted.txt", "r") # read-only
print("[INF]Loading Masters...")
time.sleep(1)
for name in f.readlines():
	if len(name.strip())>0: permitted.append(name.strip())
f.close()
# END #

#HALF MASTERS# 
hpermitted = []
f = open("hpermitted.txt", "r") # read-only
print("[INF]Loading Half Masters....")
time.sleep(1)
for name in f.readlines():
	if len(name.strip())>0: hpermitted.append(name.strip())
f.close()
#END #

#WHITELIST# 
whitelist = []
f = open("whitelist.txt", "r") # read-only
print("[INF]Loading Whitelists...")
time.sleep(1)
for name in f.readlines():
	if len(name.strip())>0: whitelist.append(name.strip())
f.close()
#END #

#ROOMS#
rooms = []
f = open("rooms.txt", "r") # read-only
print("[INF]Loading Rooms...")
time.sleep(1)
for name in f.readlines():
	if len(name.strip())>0: rooms.append(name.strip())
f.close()
#END#
###########################################################
## Thu 14 Apr 2011 00:05:52 BST
###########################################################
if sys.version_info[0] > 2:
	import urllib.request as urlreq
else:
	import urllib2 as urlreq

dancemoves = [
	"(>^.^)> (>^.^<) <(^.^)>",
]
activated = False # Disabled on default
prefix = "$" # command prefix for some commands

def getUptime():
    """
    Returns the number of seconds since the program started.
    """
    # do return startTime if you just want the process start time
    return time.time() - startTime

#SYSTEM UPTIME
def uptime():
 
     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"
 
     total_seconds = float(contents[0])
 
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
 
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
 
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
     return string;

class TestBot(ch.RoomManager):
	def onInit(self):
		self.setNameColor("A9F")
		self.setFontColor("540")
		self.setFontFace("1")
		self.setFontSize(11)
		self.enableBg()
		self.enableRecording()
		
	def getAccess(self, user):
		if user.name in spermitted: return 4
		elif user.name in permitted: return 3
		elif user.name in hpermitted: return 2
		elif user.name in whitelist: return 1
		else: return 0
	
	def onConnect(self, room):
		print("[INF] Connected to %s" % room.name)
	
	def onReconnect(self, room):
		print("[INF] Reconnected to %s" % room.name)
	
	def onDisconnect(self, room):
		print("[INF] Disconnected to %s" % room.name)
		
	def onJoin(self, room, user):
			if lockdown: return
			if self.getAccess(user) >= 4:
				room.message("-jumps up- waves at " "<b>"+ user.name.title() +"</b>" "^^", True)
			elif self.getAccess(user) >= 3:#
				room.message("ohai master " "<b>"+ user.name.title() +"</b>" " ^^", True)#
			#elif self.getAccess(user) >= 2:#		
				#room.message("huggles half master " + user.name + " ^^")#
	
	def onMessage(self, room, user, message):
		# make global (if they will be changed in commands)
		global activated
		global lockdown
		## print to console
		if room.getLevel(self.user) > 0: # if bot is mod
			print("[%s]\033[94m[MSG]\033[0m\033[31m[LVL %s]\033[0m[%s][%s] %s: %s" % (time.strftime("%d/%m/%y- %H:%M:%S", 
time.localtime(time.time())), self.getAccess(user), room.name, message.ip, user.name.title(), message.body)) # with ip
		else:
			print("[%s]\033[94m[MSG]\033[0m\033[31m[LVL %s]\033[0m[%s] %s: %s" % (time.strftime("%d/%m/%y- %H:%M:%S", time.localtime(time.time())), 
self.getAccess(user), room.name, user.name.title(), message.body)) # with ip # without ip
		if self.user == user: return # ignore self
		if self.getAccess(user) == 0: return # ignore non-whitelisted
		if self.getAccess(user) < 4 and lockdown: return #ignore everyone when in lockdown
		#split message into command and args
		data = message.body.split(" ", 1)
		if len(data) > 1:
			cmd, args = data[0], data[1] # if command and args
		else:
			cmd, args  = data[0], ""# if command and no args
		
		
		# implied command?
		if len(cmd) > 0:
			if cmd[0].lower() == prefix.lower():
				used_prefix = True
				cmd = cmd[1:].lower()
			else: used_prefix = False
		else: return
		#BOT CALL INGORE CASE

		# call bot name, activate if deactivated (bot)
		if cmd.upper() == room.user.name.upper() and len(args) == 0:# IGNORES CASE NOW
			if not activated and self.getAccess(user) < 2: return
			responce = ["yeah? %s" % user.name, "hmmhm", "o-o yesh?", "hi ^^"]
			room.message(random.choice(responce))
			activated = True

		# call bot name with command after
		elif cmd.upper() == room.user.name.upper() and len(args) != 0:# IGNORES CASE NOW
			activated = True
			used_prefix = True
			data = args.split(" ", 1)
			if len(data) > 1:
				cmd, args = data[0], data[1] # if command and args
			else:
				cmd, args  = data[0], "" # if command and no args

		# not activated, no commands
		if not activated: return
		
		# hide/deactive bot (hide)
		if cmd == "hide" and self.getAccess(user) >= 2: # level 2+
			activated = False
			room.message(cgi.escape("I ish hiding >_> %s" % user.name.title()))
		
		#eval
		elif cmd == "eval" and self.getAccess(user) >= 4: # level 4+
			try:
				ret = eval(args)
				room.message(str(repr(ret)+" ^-^"))
			except:
				room.message("failed to evaluate")
		#hello
		elif used_prefix and (cmd == "hello" or cmd == "sup"): room.message("Herro %s :3" % user.name.title())	

		# message delay in seconds (delay 10)
		elif used_prefix and cmd == "delay":
			self.setTimeout(int(args), room.message, "heh that was %s of bordem >_>" % args)
		
		# server uptime (uptime)
		elif used_prefix and cmd == "uptime":
			room.message("sys uptime: %s" % uptime())
		# server uptime (uptime)
		elif used_prefix and cmd == "sut":
			room.message("I have been playing for: %s" % getUptime())

		# heart/ily (<3 bot, ily bot)
		elif used_prefix and (cmd == "<3" or cmd == "ily" or cmd == "ilu"):
			room.message(random.choice(["<3 u too %s" % user.name, "Wonders over to %s and sits besides them o-o" % user.name.title(),]))
		# heart/ily (<3 bot, ily bot)
		elif used_prefix and (cmd == "wtf" or cmd == "omfg" or cmd == "omg"):
			room.message(random.choice(["Woah o.O %s" % user.name, "eep something wrong %s" % user.name.title(),]))
		
		elif used_prefix and cmd == "flipcoin":
			room.message(random.choice(["%s flips a coin and gets heads" % user.name.title(), "%s flips a coin and gets tails" % user.name.title(), "%s flips a coin and it falls off the table o.O" % user.name.title(),]))

		elif used_prefix and cmd == "spin-bottle":
			room.message("<b>%s</b> spins the bottle after it spins it lands on <b>%s</b> ^^" % (user.name.title(), random.choice(room.usernames.title())), True)
				
		# kill bot (eeps)
		elif used_prefix and cmd == "eeps" and self.getAccess(user) >= 4:
			if user.name.lower() == "sorchmaster":
				room.message("Mutters something before leaving")
				time.sleep(1)				
				self.stop()
			else:
				room.message("wish i could =/")
		# Save stuffs
		elif used_prefix and cmd == "sav":
			if user.name in permitted or spermitted:
				room.message("I ish saved everything ^^")				
				print("[SAV] Saving Definitions..")
				f = open("definitions.txt", "w")
				for word in dictionary:
					definition, name = json.loads(dictionary[word])
					f.write(json.dumps([word, definition, name])+"\n")
				f.close()
				print("[SAV] Saving SuperMasters..")
				f = open("spermitted.txt", "w")
				f.write("\n".join(spermitted))
				f.close()
				print("[SAV] Saving Masters..")
				f = open("permitted.txt", "w")
				f.write("\n".join(permitted))
				f.close()
				print("[SAV] Saving HalfMasters..")
				f = open("hpermitted.txt", "w")
				f.write("\n".join(hpermitted))
				f.close()
				print("[SAV] Saving Whitelist..")
				f = open("whitelist.txt", "w")
				f.write("\n".join(whitelist))
				f.close()
				print("[SAV] Saving Rooms..")
				f = open("rooms.txt", "w")
				f.write("\n".join(rooms))
				f.close()
				print("[SAV] Saving Whitelist..")
				f = open("whitelist.txt", "w")
				f.write("\n".join(whitelist))
				f.close()
			else:
				room.message("wish i could =/")



		# cookie responce (cookie?)
		elif cmd =="cookie?":
			room.message(random.choice(["yesh" , "sure ^^" , "no ty =/" , "O_O gimme" , "cookie...YESH" , "^^" , "COOKIE" , "-noms cookie- thankies"]))


		
		#what room
		elif used_prefix and cmd=="whatroom":
			room.message("<b>%s</b> this is <b>http://%s.chatango.com</b>" % (user.name.title(), room.name), True)

		#bye 
		elif used_prefix and (cmd == "bye" or cmd == "cya"):
				room.message("awww bye " + user.name.title() + " =(")
		# half masters
		elif used_prefix and cmd == "hmasters":
			if len(args) >= 3:
				do, name = args.lower().split(" ", 1)
				if self.getAccess(ch.User(name)) > 3 or self.getAccess(user) < 2:
					room.message("no. =/")
					return
				if do == "add":
					if name in hpermitted: room.message("%s is already a hmaster. ^^" % name, True)
					else:
						hpermitted.append(name)
						room.message("<b>%s</b> it has been done. ^^ remember do not add people that abuse me ^^" % user.name.title(), True)
				elif do == "remove":
					if name not in hpermitted: room.message("%s is not a hmaster. ^^" % name, True)
					else:
						hpermitted.remove(name)
						room.message("it has been done. ^^ sowwy =/", True)
				else:
					room.message("what? >.>", True)
			else:
				if len(hpermitted) == 0: room.message("I have no half masters. ^^", True)
				else: room.message("My Half Masters: <b>%s</b> -waves at you all-" % ", ".join(hpermitted), True)
		# room add
		elif used_prefix and cmd == "room":
			if len(args) >= 3:
				do, name = args.lower().split(" ", 1)
				if self.getAccess(ch.User(name)) > 4 or self.getAccess(user) < 4:
					room.message("no. =/")
					return
				if do == "add":
					if name in rooms: room.message("%s in my list. ^^" % name, True)
					else:
						rooms.append(name)
						room.message("it has been done. ^^ I ish there ^^", True)
						self.joinRoom(name)
				elif do == "remove":
					if name not in rooms: room.message("%s is not in my list =/. ^^" % name, True)
					else:
						rooms.remove(name)
						room.message("it has been done. ^^ sowwy =/", True)
						self.leaveRoom(name)
				else:
					room.message("what? >.>", True)
			else:
				if len(rooms) == 0: room.message("hell i have no rooms how is this possible. ^^", True)
				else: room.message("Please use my rooms command use botteh rooms")
		# masters
		elif used_prefix and cmd == "masters":
			if len(args) >= 3:
				do, name = args.lower().split(" ", 1)
				if self.getAccess(ch.User(name)) > 3 or self.getAccess(user) <= 3:
					room.message("no. =/")
					return
				if do == "add":
					if name in permitted: room.message("%s is already a master. ^^" % name, True)
					else:
						permitted.append(name)
						room.message("<b>%s</b> it has been done. ^^ remember do not add people that abuse me ^^" % user.name.title(), True)
				elif do == "remove":
					if name not in permitted: room.message("%s is not a master. ^^" % name, True)
					else:
						permitted.remove(name)
						room.message("it has been done. ^^ sowwy =/", True)
				else:
					room.message("what? >.>", True)
			else:
				if len(permitted) == 0: room.message("I have no masters. ^^", True)
				else: room.message("My masters: <b>%s</b> they are just amazing ^^" %  ", ".join(permitted), True)

		# whitelist
		elif used_prefix and cmd == "whitelist":
			if len(args) >= 3:
				do, name = args.lower().split(" ", 1)
				if self.getAccess(ch.User(name)) > 2:
					room.message("no. =/")
					return
				if do == "add":
					if self.getAccess(user) >= 2:
						if name in whitelist:
							room.message("%s is already whitelisted. ^^" % name, True)
						else:
							whitelist.append(name)
							room.message("<b>%s</b> it has been done. ^^ remember do not add people that abuse me ^^" % user.name, True)
					else:
						room.message("%s it has not been possible to connect your call please hang up and try again" % user.name)
				elif do == "remove":
					if self.getAccess(user) <= 1:
						room.message("no. =/")
						return
					if name not in whitelist: room.message("%s is not whitelisted. ^^" % name, True)
					else:
						whitelist.remove(name)
						room.message("it has been done. ^^ sowwy =/", True)
				else:
					room.message("what? >.>", True)
			else:
				if len(whitelist) == 0: room.message("I have no whitelisted members. ^^", True)
				elif len(whitelist) == 1: room.message("I have 1 whitelisted member. ^^", True)
				else: room.message("I have %s whitelisted members. ^^" % len(whitelist), True)
				
		# bot rooms
		elif (used_prefix and cmd == "whereiam" or cmd =="rooms"):
			room.message("I can be found in: <b>%s</b>" % ",".join(rooms),True)
		
		# user count
		elif used_prefix and cmd == "howmany":
			room.message("i see: " + str(room.usercount))

		# help command
		elif used_prefix and (cmd == "help" or cmd == "?" or cmd == "??"):
			room.message("<a href=\"http://i7.sr1.in/botteh/\" target=\"_blank\"><b>Command list</b></a> Follow me on <a href=\"http://twitter.com/followbotteh/\" target=\"_blank\"><b>Twitter<b></a>", True)

		# join room
		elif (used_prefix and cmd == "goto" or cmd == "aport")  and len(args) > 0:
			if user.name in permitted or spermitted:
				print("[INF] Joining %s..." % args.split()[0])
				self.joinRoom(args.split()[0])
				room.message("k there. ^^")

		# say
		elif used_prefix and cmd == "say" and len(args) > 0:
			if self.getAccess(user) >= 1:
				room.message("<b>%s</b> -%s-" % (args, user.name.title()), True)
			else:
				room.message("no. ^^")

		# what access
		elif used_prefix and cmd == "lvl":
			if len(args) >= 3:
				do, name = args.lower().split(" ", 1)
				if self.getAccess(ch.User(name)) > 4 or self.getAccess(user) < 2:
					room.message("no. =/")
					return
				if do == "check":
					if name in whitelist: room.message("%s is level 1. <b>(whitelist)</b> ^^" % name, True)
					else:
						if name in permitted: room.message("%s is level 3 <b>(master)</b>" % name, True)
						elif name in hpermitted: room.message("%s is level 2 <b>(hmaster)</b>" % name, True)
						elif name in spermitted: room.message("%s is level 4 <b>(owner)</b> O.o" % name, True)
						elif name not in whitelist or permitted or hpermitted: room.message("%s is level 0 <b>(i ignore these)</b>" % name, True)
		# lockdown
		elif (used_prefix and cmd == "sleep"):
			if self.getAccess(user) == 4:
				if len(args.split()) > 0 and args.split()[0].lower() == "wakeup":
					lockdown = False
					room.message("I am awake. ^^")
					filename ="status.txt"
					print("[INF]Setting status to normal mode...")
					file = open(filename, 'w')
					file.write("Awake")
					file.close()
				else:
					lockdown = True
					filename = "status.txt"
					file = open(filename, 'w')
					print("[INF]Setting status to lockdown...")
					file.write("Sleeping")
					file.close()
					room.message("I am sleeping. ^^")
					
			else:
				room.message("no. ^^")

		# kill
		elif (used_prefix and cmd == "kill")  and len(args) > 0:
			if self.getAccess(user) >= 1:
				room.message("Hands %s a grenade -waits 10 seconds- *BOOM* %s is KEELED xD" % (args, args,))
			else:
				room.message("no. ^^")
		# kill
		elif used_prefix and (cmd == "huggle" or cmd =="hug")  and len(args) > 0:
			if self.getAccess(user) >= 1:
				room.message(random.choice(["*HUGGLES* %s" % args, "*SQUEEZES* %s" % args,]))
			else:
				room.message("no. ^^")
		# fake find
		elif (used_prefix and cmd == "locate") and len(args) > 0:
			if self.getAccess(user) >= 1:
				name = args.split()[0].lower()
				if not ch.User(name).roomnames:  room.message("dont see them. ^^")
				else: room.message("%s they are in <b>%s</b> >_>" % (user.name, ", ".join(ch.User(name).roomnames)), True)
			else:
				room.message("no. ^^")
		# give cookie
		elif (used_prefix and cmd == "givecookie")  and len(args) > 0:
				room.message("gives %s a cookie ^^" % args)
		# leave room
		elif (used_prefix and cmd == "leave" or cmd == "ninjafy") and len(args) > 0:
			if user.name in permitted or spermitted:
				self.leaveRoom(args)
				room.message("k gone. ^^")
			else:
				room.message("no. ^^")

		# give cookie
		elif (used_prefix and cmd == "define")  and len(args) > 0:
			try:
				word, definition = args.split(":", 1)
				word = word.lower()
			except:
				word = args.split()[0].lower()
				definition = ""
			if len(word.split()) > 1:
				room.message("error: no phrases")
				return
			if len(args.split()) > 1 and args.lower().split()[1] == "ud":
				if word in dictionary:
					definition, name = json.loads(dictionary[word])
					if name == user.name or self.getAccess(user) >= 3:
						del dictionary[word]
						room.message("okies :3")
						return
					else:
						room.message("<b>%s</b> you can not remove this define only masters or the person who defined the word may remove definitions ^^" % user.name, True)
						return
				else:
					room.message("<b>%s</b> is not yet defined you can define it by typing <b>botteh define %s: meaning</b>" % args, True)
			elif len(definition) > 0: #if there's a colon somewhere
				if word in dictionary: 
					room.message("<b>%s</b> erm... thats already defined. You can not define it again >_>" % user.name.title(), True)
				else:
					dictionary[word] = json.dumps([definition, user.name])
					room.message(word + ": " + definition + " *by* " "<b>"+ user.name.title() + "</b>", True)
			else:
				if word in dictionary:
					definition, name = json.loads(dictionary[word])
					room.message("<b>" + word + "</b>" ":" + definition + " *by* " "<b>" + name + "</b>", True)
				else:
					room.message("<b>%s</b> is not yet defined you can define it by saying <b>botteh define %s: meaning</b>  ^^" % (args, args), True)

	
		# dance
		elif (used_prefix and cmd == "dance"):
			if self.getAccess(user) >= 1:
				for i, msg in enumerate(dancemoves):
					self.setTimeout(i / 2, room.message, msg)
			else:
				room.message("no dances for you >_>")
   
		# youtube search
		elif (used_prefix and cmd == "tube" or used_prefix and cmd == "ytb"):
			search = args.split()
			def everything_between(text,begin,end):
				idx1=text.find(begin)
				idx2=text.find(end,idx1)
				return ' '.join(text[idx1+len(begin):idx2].strip().split())
			try:
				raw = str(urllib.request.urlopen("http://gdata.youtube.com/feeds/api/videos?vq=%s&racy=include&orderby=relevance&max-results=1" % "+".join(search)).read())
				id = helperCmd.everything_between(raw,'http://www.youtube.com/watch?v=','&amp;')
				info = youtube.Video(id)
				link = "http://www.youtube.com/watch?v="+id
				room.message("%s, i found: \"%s\" by %s. %s" % (user.name.title(), info.get_title()[:50], info.get_auth()[:50], link), True)
			except:
				room.message("Error: Nothing found for %s =/" % args)						

		#						
		# Persona
		#
		#redo "split message into command and args"
		data = message.body.split(" ", 1)
		if len(data) > 1:
			cmd, args = data[0], args # if command and args
		else:
			cmd, args  = data[0], ""# if command and no args
		# butterfly responce (8|8)
		if cmd =="8|8":
			room.message(random.choice(["Omg sexy *chases* ^w^" , "woah" , "I want one =/" , "O_O -watches-" , "O.o -touchs-" , "^^" , "oooo"]))

		elif cmd == "><>":
			room.message(random.choice(["eeee fishes ^^" , "o.o fish" , "I want one =/" , "waves at fishy ^^" , "O.o -touchs-" , "^^" , "oooo fish"]))
		
		def onFloodWarning(self, room):
			room.reconnect()
	
	
		def onUserCountChange(self, room):
			print("users: " + str(room.usercount))

		
########################################################################################
# Bot username password and rooms
########################################################################################
def hexc(e):
	et, ev, tb	= sys.exc_info()
	if not tb: print(str(e))
	while tb:
		lineno = tb.tb_lineno
		fn	= tb.tb_frame.f_code.co_filename
		tb	= tb.tb_next
	print("(%s:%i) %s" % (fn, lineno, str(e)))
	
if __name__ == "__main__":
	error = 0
	try:
		os.system("clear") # clear console on launch
		TestBot.easy_start(rooms, cmds.botname, cmds.password)
	except KeyboardInterrupt:
		print("[ERR] Console initiated a kill.")
	except Exception as e:
		print("[ERR] Fatal error.")
		error = 1
		hexc(e)
	print("[SAV] Saving Definitions..")
	f = open("definitions.txt", "w")
	for word in dictionary:
		definition, name = json.loads(dictionary[word])
		f.write(json.dumps([word, definition, name])+"\n")
	f.close()
	print("[SAV] Saving SuperMasters..")
	f = open("spermitted.txt", "w")
	f.write("\n".join(spermitted))
	f.close()
	print("[SAV] Saving Masters..")
	f = open("permitted.txt", "w")
	f.write("\n".join(permitted))
	f.close()
	print("[SAV] Saving HalfMasters..")
	f = open("hpermitted.txt", "w")
	f.write("\n".join(hpermitted))
	f.close()
	print("[SAV] Saving Whitelist..")
	f = open("whitelist.txt", "w")
	f.write("\n".join(whitelist))
	f.close()
	print("[SAV] Saving Rooms..")
	f = open("rooms.txt", "w")
	f.write("\n".join(rooms))
	f.close()
#STATUS
#
	filename = "status.txt"
	f = open(filename, 'w')
	print ("[INF] Setting status offline...")
	f.write("In deep sleep")
	f.close()
#

	if error == 1:
		print("Waiting 10 seconds for you to read the error..")
		time.sleep(10)
	print("[INF] Shutting down..")
########################################################################################
