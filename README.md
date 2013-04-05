botname = "BotNameHere"

password = "BotPasswordHere" 
rooms = []
file = open("rooms.txt", "r")
for name in file.readlines():
 if len(name.strip())>0: rooms.append(name.strip())
defaultRoom = ""

############################################
def hexc(e):
 et, ev, tb = sys.exc_info()
 if not tb: print(str(e))
 while tb:
  	lineno = tb.tb_lineno
 fn = tb.tb_frame.f_code.co_filename
 tb = tb.tb_next
 print("(%s:%i) %s" % (fn, lineno, str(e)))
