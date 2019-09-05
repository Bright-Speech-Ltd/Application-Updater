import sys, time, os
def no(): #fix for cButton function, used as a default command
	pass
class Error(Exception):
    pass
class utils():
	def __init__(self):
		import time
		self.varstore = {}
		self.textlen = 0
	def writelines(self, text): #print over same line
		self.text = text
		sys.stdout.write('\r' + ' ' * self.textlen + '\r')
		sys.stdout.flush()
		sys.stdout.write('\r' + str(self.text) + '\r')
		sys.stdout.flush()
		self.textlen = len(text)
	def sleeper(self, interval): #sleep in miliseconds
		interval = interval/1000
		time.sleep(interval)
	def var_store(self, text="", key=""):
		if ley != "":
			if text != "":
				self.varstore[key] = text
			else:
				return self.varstore[key]
	def pad(self, input, length):
		x = ""
		for i in range(length-len(str(input))):
			x+="0"
		x+=str(input)
		return x
	def help(self):
		commands = """
		writelines(text): wrights the text string to the stdout and then flushes the line, overwrights line each time.
		sleeper(interval): same as time.sleep(interval) but uses interval in miliseconds rather than seconds.
		var_store(text, key): stores the text string as a instanced variable. Stores multiple using unique key.
		pad(input, length): adds leading 0s to input untill input meets lenght
		"""
		return commands	
class TkUtils:
	def __init__(self, log, root):
		try:
			import Tkinter
			self.TkUtil = Tkinter
		except:
			import tkinter
			self.TkUtil = tkinter
		import threading
		import time
		import traceback
		self.traceback = traceback
		self.time = time
		self.threading = threading
		self.log = log
		self.root = root
		self.active_window = None
		self.active_side = None
		self.active_scroll = None
		self.run = False
		self.moving = False
	def cButton(self, element, borderwidth=0, width=0, height=0, fg="#07a501", bg="white", text="", relief="groove", padx=0, pady=0, command=no(), side=None, expand=0, fill=None, state="normal", anchor="nsew", cursor="hand2"): #basic button
		try:
			if state != "normal":
				cursor="arrow"
			b = self.TkUtil.Button(element, borderwidth=borderwidth, width=width, height=height, fg=fg, bg=bg, text=text, padx=padx, pady=pady, relief=relief, command=command, state=state, cursor=cursor)
			b.pack(side=side, expand=expand, fill=fill)
			return b
		except Exception as err:
			self.log.error("atk.cButton failed\n%s" %err)		
	def cFrame(self, element, bg="white", borderwidth=0, relief="groove", side=None, padx=0, pady=0, height=0, width=0, expand=0, fill=None, image=None, highlightbackground=None, highlightcolor=None, highlightthickness=0):#basic frame
		try:
			f = self.TkUtil.Frame(element, bg=bg, borderwidth=borderwidth, relief=relief, height=height, width=width, image=image, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness)
			f.pack(side=side, padx=padx, pady=pady, expand=expand, fill=fill)
			return f
		except Exception as err:
			self.log.error("atk.cFrame failed\n%s" %err)
			return None	
	def create_overlay(self, over, event, title, height=400, width=400):
		if self.active_window != None:
			self.clear_overlay(self.TkUtil.Event())
			self.create_overlay(over, event, title, height, width)
		else:
			try:
				try:
					rootx = self.root.winfo_width()
					rooty = self.root.winfo_height()
				except:
					rootx = 200
					rooty = 150
					self.log.log("create_overlay could not get width or height")
				window = self.TkUtil.Canvas(over, width=width, height=height, bg="white", relief="groove", highlightbackground="black", highlightcolor="black", highlightthickness=1, borderwidth=4)
				self.active_window = window
				window.pack_propagate(False)
				window.place(x=rootx/2-(width/2), y=(rooty/2)-(height/4))
				self.root.update_idletasks()
				self.root.update()
				spacer = self.cFrame(window, padx=7, pady=7, fill=self.TkUtil.BOTH)
				Title = self.TkUtil.Label(spacer, text=title, justify=self.TkUtil.RIGHT, font=("Helvetica", 10), bg="#EEEEEE", padx=10, pady=5, cursor="fleur")
				Title.pack(side=self.TkUtil.LEFT,  expand=1, fill=self.TkUtil.X)
				#Title.bind("<ButtonPress-1>", lambda e=self.TkUtil.Event(), w=window, run=True: self.move_window(e, w, run))
				#Title.bind("<ButtonRelease-1>", lambda e=self.TkUtil.Event(), w=window, run=False: self.move_window(e, w, run))
				Title.bind("<B1-Motion>", lambda e=event, w=window: self.move_window_thread(w, e))
				close = self.cButton(spacer, text="X", relief="raised", borderwidth=1, fg="black", side=self.TkUtil.RIGHT, command=lambda e=self.TkUtil.Event(): self.clear_overlay(e))
				spacer = self.cFrame(window, side=self.TkUtil.BOTTOM, pady=3)
				self.set_pos(window)
			except:
				self.log.log("atk.create_overlay failed")
				pass
			return "break"
	def clear_overlay(self, event): #clear overlayed canvas
		self.log.log("atk.autil clearing windows")
		if self.active_window != None:
			self.active_window.destroy()
			self.active_window = None
		return "break"
	def overlay(self, over, event, title, height=400, width=400):
		if self.active_window == None:
			self.create_overlay(over, event, title, width=width, height=height)
			return self.active_window
		else:
			self.clear_overlay(self.TkUtil.Event())
			self.create_overlay(over, event, title, width=width, height=height)
			return self.active_window
	def move_window(self, event, window, run):
		self.run = run
		if self.run:
			t= self.threading.Thread(target=self.move_window_thread,args=(window, event))
			t.start()
	def move_window_thread(self, window, event):
		try:
			if not self.moving:
				self.moving = True
				self.root.update_idletasks()
				self.root.update()
				#self.time.sleep(0.05)
				if(self.root.winfo_pointerx() != "??" and self.root.winfo_pointery() != "??"):
					window.place(x=(self.root.winfo_pointerx() - self.root.winfo_rootx())-window.winfo_width()/2, y=self.root.winfo_pointery() - self.root.winfo_rooty()-10)
					#self.time.sleep(0.05)
				self.moving= False
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("move_window_thread failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, self.traceback.print_tb(exc_tb)))
			pass	
	def set_pos(self, window):
		try:
			rootx = self.root.winfo_width()
			rooty= self.root.winfo_height()
			wx = window.winfo_width()
			wy = window.winfo_height()
		except:
			rootx = 200
			rooty = 150
			wx = 400
			wy = 400
			self.log.log("set_pos failed")
		window.place(x=(rootx/2)-(wx/2), y=(rooty/2)-(wy/2))
	def scrollable_area2(self, holder):
		try:
			base_frame = self.cFrame(holder, fill=self.TkUtil.BOTH, expand=1, padx=5, pady=5)
			base_frame.rowconfigure(0, weight=0) 
			base_frame.columnconfigure(0, weight=1)
			can = self.TkUtil.Canvas(base_frame, bg="white")
			can.pack(side=self.TkUtil.LEFT, expand=1, fill=self.TkUtil.BOTH)
			scrollArea = self.cFrame(base_frame, bg="white", side=self.TkUtil.LEFT, expand=1, fill=self.TkUtil.BOTH)
			can.create_window(0, 0, window=scrollArea, anchor='nw')
			Scroll = self.TkUtil.Scrollbar(base_frame, orient=self.TkUtil.VERTICAL)
			Scroll.config(command=can.yview)
			Scroll.pack(side=self.TkUtil.RIGHT, fill=self.TkUtil.Y)
			can.config(yscrollcommand=Scroll.set)
			scrollArea.bind("<Configure>",  lambda e=self.TkUtil.Event(), c=can: self.update_scrollregion(e, c))
			base_frame.bind("<Enter>", lambda e=self.TkUtil.Event():self.set_active(e, can))
			base_frame.bind("<Leave>", lambda e=self.TkUtil.Event():self.unset_active(e))
			return scrollArea, can
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("get_access_users failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, self.traceback.print_tb(exc_tb)))		
	def set_active(self, event, canvas):
		self.active_scroll = canvas
		pass
	def unset_active(self, event):
		self.active_scroll = None
		pass
	def reset_scroll(self, element):
		self.root.nametowidget(element.winfo_parent()).yview_moveto(0)
		self.root.nametowidget(element.winfo_parent()).yview_scroll(0, "units")
	def _on_mousescroll(self, event):
		if self.active_scroll != None:
			self.active_scroll.yview_scroll(-1*(event.delta/120), "units")
	def update_scrollregion(self, event, can):
		can.configure(scrollregion=can.bbox("all"))
		pass
	def OnCanvasConfigure(self, event, can, scroll):
		canvas_width = event.width
		can.itemconfig(scroll, width = canvas_width)
	def test_buttons(self, main, defaultIcon):
		self.root.update_idletasks()
		self.root.update()
		for i in range(20):
			Packer, state = self.cFrame(main, bg="white", borderwidth=2, width=400, relief=self.TkUtil.RAISED, fill=self.TkUtil.X, expand=1)
			L= self.TkUtil.Label(Packer, anchor=self.TkUtil.W, justify=self.TkUtil.LEFT, text="Test %s"%i, bg="red", borderwidth=0)
			L.pack(side=self.TkUtil.LEFT, fill=self.TkUtil.X)
			L2= self.TkUtil.Label(Packer, anchor=self.TkUtil.W, image=defaultIcon)
			L2.pack(side=self.TkUtil.RIGHT)
class Log: #class to write to log file with time stamps
	def __init__(self, appname):
		import os, traceback, time
		self.traceback = traceback
		self.os = os
		self.time = time
		if getattr(sys, 'frozen', False): #windows path fix
			self.exe = self.os.path.dirname(sys.executable)
		elif __file__:
			self.exe = self.os.path.dirname(__file__)
		if not os.path.exists(os.path.dirname(str(os.environ['USERPROFILE'])+"\\Documents\\%s\\" %appname)):
			os.makedirs(str(os.environ['USERPROFILE'])+"\\Documents\\%s\\" %appname)
		self.fname = str(os.environ['USERPROFILE'])+"\\Documents\\%s\\debug.log" %appname
		self.logfile = None
	def error(self, error):
		exc_type, exc_obj, exc_tb = sys.exc_info()
		trace_stack = self.traceback.extract_tb(exc_tb)[-1]
		trace_format = "Error in file "+str(trace_stack[0])+"\r		on line "+str(trace_stack[1])+", from module '"+str(trace_stack[2])+"'\r		"+str(trace_stack[3])
		try:
			self.logfile = open(self.fname, "a+")
		except:
			self.logfile = open(self.fname, "w+")
		strtime = str(self.time.strftime("%d-%m-%Y,(%z),%H:%M:%S"))
		self.logfile.write("error: %s, %s, %s\r" %(strtime, error, trace_format))
		self.logfile.close()
		self.logfile = None
	def log(self, log):
		try:
			self.logfile = open(self.fname, "a+")
		except:
			self.logfile = open(self.fname, "w+")
		strtime = str(self.time.strftime("%d-%m-%Y,(%z),%H:%M:%S"))
		self.logfile.write("log: %s, %s\r" %(strtime, log))
		self.logfile.close()
		self.logfile = None
