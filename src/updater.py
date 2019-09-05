import os, sys, threading, subprocess, shutil, tempfile, requests, configparser, traceback
from tkinter import *
from tkinter.ttk import *
from urllib.request import urlopen
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from acl import perms
from zipfile import ZipFile
from aceutil import Log
if os.name == 'nt':
    import win32api, win32con
    pass
if getattr(sys, 'frozen', False):
	exe_path = os.path.dirname(sys.executable)
elif __file__:
	exe_path = os.path.dirname(os.path.abspath(__file__))
	pass
class Updater:
	def __init__(self):
		self.log = Log("Updater")
		self.quit = False
		self.pro = 0
		self.download=False
		self.tmpdir = ""
		self.latestversion = ""
		self.copies = []
		self.zipping = False
	def rec_copy(self, src, dest, rt):
		try:
			for item in os.listdir(src):
				file_path = os.path.join(src, item)
				if os.path.isfile(file_path):
					self.copies.append([file_path, dest])
				elif os.path.isdir(file_path):
					new_dest = os.path.join(dest, item)
					if not os.path.isdir(new_dest):
						os.mkdir(new_dest)
					self.rec_copy(file_path, new_dest, False)
			if rt:
				return self.copies
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("rec_copy failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def unzipt(self):
		try:
			with ZipFile(self.tmpdir+"\\"+self.latestversion+".zip", 'r') as zipObj:
				zipObj.extractall(self.tmpdir+"\\"+self.latestversion)
			self.zipping=False
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("unzipt failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def install_update(self):
		try:
			self.download = False
			self.update_status("Download Completed, Applying Update\nPlease Wait.")
			self.pro = 65
			t = threading.Thread(target=self.unzipt)
			self.zipping = True
			t.start()
			while self.zipping:
				self.root.update()
				self.root.update_idletasks()
			files = self.rec_copy(self.tmpdir+"\\"+self.latestversion, self.path, True)
			x = 0
			for i in files:
				x += 1
				self.progress['value'] = 65+int(x/(len(files)/30))
				self.pro = 65+int(x/(len(files)/30))
				self.progress.update()
				self.root.update()
				self.root.update_idletasks()
				shutil.copy(i[0], i[1])
			self.update_status("Update Complete. Cleaning up.\n")
			shutil.rmtree(self.tmpdir)
			self.pro = 100
			self.progress['value'] = 100
			self.root.update()
			self.root.update_idletasks()
			self.progress.update()
			self.update_status("Done. Continuing to Applicaton.\n")
			subprocess.Popen(self.path+self.app+" 'True'")
			self.quitting()
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("install_update failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def download_update(self, url, fname):
		try:
			self.tmpdir = tempfile.mkdtemp()
			with open(self.tmpdir+"\\"+fname, 'wb') as f:
				response = requests.get(url, stream=True)
				total = response.headers.get('content-length')
				if total is None:
					f.write(response.content)
				else:
					downloaded = 0
					total = int(total)
					for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
						downloaded += len(data)
						f.write(data)
						done = int(50*downloaded/total)
						self.pro=10+done
			self.download = True
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("download_update failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def start_updating(self, version):
		try:
			self.update_status("Starting Update Process.\nPlease Wait")
			try:
				perms(self.log, self.path, ["Users", "Everyone"]).check_perm()
			except:
				self.log.log("Could not set Permissions, This requires Administator Privilages")
			self.update_status("Permissions Have been Granted\n")
			self.pro=10
			dl = "%s/%s.zip" %(self.url, version)
			t = threading.Thread(target=self.download_update,args=(dl, version+".zip"))
			self.update_status("Downloading Update\n")
			t.start()
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("start_updating failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
			self.update_status("This Application Requires to be run as Administator, or have Permission Granted.\nPlease Speak to your Administator.")
			self.pro=0	
	def get_version_number(self, filename):
		try:
			self.log.log("version from file %s" %filename)
			info = GetFileVersionInfo (filename, "\\")
			ms = info['FileVersionMS']
			ls = info['FileVersionLS']
			return [str(HIWORD (ms)), str(LOWORD (ms)), str(HIWORD (ls)), str(LOWORD (ls))]
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("get_version_number failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
			return ["0", "0", "0", "0"]
	def update_status(self, text):
		try:
			self.status.configure(text=text)
			self.status.update()
			self.root.update()
			self.root.update_idletasks()
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("update_status failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def check_version(self):
		try:
			self.update_status("Getting Application Version\n")
			self.version = ".".join(self.get_version_number(self.path+self.app))
			self.log.log("checking File Version %s" %self.path+self.app)
			self.log.log("got version %s" %self.version)
			self.update_status("Application Version %s\nChecking for Updates" %self.version)
			respose = urlopen(self.url+"/"+self.php)
			self.log.log("checking for updartes from %s" %self.url+"/"+self.php)
			charset=respose.info().get_content_charset()
			self.latestversion = respose.read().decode(charset)
			self.log.log("latest=%s : current=%s" %(self.latestversion, self.version))
			if self.version != self.latestversion:
				self.update_status("Update Required\n")
				self.pro=5
				return True, self.latestversion
			else:
				self.update_status("No Update Required\n")
				self.pro=100
				self.root.update()
				self.root.update_idletasks()
				return False, "0.0.0.0"
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("check_version failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def gen_config(self):
		try:
			self.log.log("Creating New Config File")
			config = configparser.ConfigParser()
			config['APPLICATION'] = {}
			config['APPLICATION']['app'] = 'app.exe'
			config['APPLICATION']['path'] = 'C:\\Program Files (x86)\\My App\\'
			config['UPDATE'] = {}
			config['UPDATE']['url'] = 'http://0.0.0.0'
			config['UPDATE']['php'] = 'updater.php'
			with open('updater.ini', 'w') as configfile:
				config.write(configfile)
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("gen_config failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def read_config(self):
		try:
			config = configparser.ConfigParser()
			config.read(exe_path+'\\updater.ini')
			if config['UPDATE']['url'] == "http://0.0.0.0":
				self.update_status("Config File Not Set.\nPlease Change updater.ini with correct information")
				return False
			else:
				self.url = config['UPDATE']['url']
				self.php = config['UPDATE']['php']
				self.app = config['APPLICATION']['app']
				self.path = config['APPLICATION']['path']
				self.log.log(self.url)
				self.log.log(self.php)
				self.log.log(self.app)
				self.log.log(self.path)
				return True
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("read_config failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def check_config(self):
		try:
			self.log.log("Checking Config %s" %exe_path+'\\updater.ini')
			if os.path.isfile(exe_path+'\\updater.ini'):
				self.log.log("isfile")
				return self.read_config()
			else:
				self.gen_config()
				self.update_status("Config File Not Set.\nPlease Change updater.ini with correct information")
				return False
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("check_config failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def UI(self):
		try:
			self.log.log("Application Starting")
			self.root = Tk()
			self.root.iconbitmap(exe_path+'\\icon.ico')
			self.root.title("Updater")
			self.root.protocol("WM_DELETE_WINDOW", self.quitting)
			ws = self.root.winfo_screenwidth() # width of the screen
			hs = self.root.winfo_screenheight() # height of the screen
			x = (ws/2)-(300/2)
			y = (hs/2)-(50/2)
			self.root.geometry("300x50+%s+%s" %(int(x), int(y)))
			self.root.attributes("-topmost", True)
			self.root.attributes("-topmost", False)
			
			self.status = Label(self.root, text="Checking for Updates\n")
			self.status.pack(side=TOP, fill=X, expand=1)
			self.progress=Progressbar(self.root, orient=HORIZONTAL,length=100,mode='determinate')
			self.progress.pack(fill=X, expand=1)
			if self.check_config():
				vc = self.check_version()
				if vc[0]:
					self.start_updating(vc[1])
				else:
					subprocess.Popen(self.path+self.app+" 'True'")
					self.quitting()
			while not self.quit:
				self.root.update_idletasks()
				self.root.update()
				self.progress['value']=self.pro
				if self.download:
					self.install_update()
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("UI failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def quitting(self):
		self.quit = True
if __name__ == "__main__":
	u = Updater()
	u.UI()