import os, sys, shutil, traceback
from zipfile import ZipFile
from aceutil import Log
import filecmp

class updateBuilder:
	def __init__(self):
		self.log = Log("builder")
		self.app_path = "C:\\Program Files (x86)\\myApp\\"
		self.update = "C:\\Users\\Scott\\Desktop\\MyNewBuild\\build\\exe.win32-3.7\\"
		self.update_dir = "C:\\Users\\Scott\\Desktop\\MyNewBuild\\Updates\\"
		self.differences = []

	def get_updated(self):
		for i in self.differences:
			folders = i[0].split("\\")
			if i[1] == "file":
				del folders[-1]
			path = ""
			for f in folders:
				path += f+"\\"
				if not os.path.isdir(self.update_dir+path):
					print("Creating folder %s" %self.update_dir+path)
					os.mkdir(self.update_dir+path)
		for i in self.differences:
			if i[1] == "file":
				print("copying file")
				print("src = %s" %self.update+i[0])
				print("dst = %s" %self.update_dir+i[0])
				shutil.copyfile(self.update+i[0], self.update_dir+i[0])
			
	
	def check_difference(self, old, new):
		try:
			return filecmp.cmp(old, new)
		except:
			return False

	def calc_differences(self, old, new):
		old_rel_path = old.replace(self.app_path, "")+"\\"
		new_rel_path = new.replace(self.update, "")+"\\"
		for item in os.listdir(new): ##scans through the updated files
			file_path = os.path.join(new, item) ##creates full path to the file being checked
			if os.path.isfile(file_path): #checkes if scanned item is a file
				print("item = %s" %item)
				if self.check_difference(self.app_path+old_rel_path+item, self.update+new_rel_path+item):
					print("no differences")
				else:
					self.differences.append([new_rel_path+item, "file"])
			elif os.path.isdir(file_path):
				new_dest = os.path.join(old, item)
				if not os.path.isdir(new_dest):
					#os.mkdir(new_dest)
					self.differences.append([new_rel_path+item, "folder"])
				self.calc_differences(new_dest, file_path)
	def unzipt(self):
		try:
			with ZipFile(self.tmpdir+"\\"+self.latestversion+".zip", 'r') as zipObj:
				zipObj.extractall(self.tmpdir+"\\"+self.latestversion)
			self.zipping=False
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("__init__ failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def tester(self):
		self.calc_differences(self.app_path, self.update)
		for i in self.differences:
			print(i)
		self.get_updated()
	def quitting(self):
		self.quit = True

if __name__ == "__main__":
	u = updateBuilder()
	u.tester()