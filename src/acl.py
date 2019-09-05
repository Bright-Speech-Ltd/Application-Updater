import ntsecuritycon as con
import win32security
import os
class perms:
	def __init__(self, log, file, users):
		self.log = log
		self.file = file
		self.users = users
		self.grants = []
	def grant(self):
		try:
			entries = [{'AccessMode': win32security.GRANT_ACCESS,
					'AccessPermissions': 0,
					'Inheritance': win32security.CONTAINER_INHERIT_ACE |
								   win32security.OBJECT_INHERIT_ACE,
					'Trustee': {'TrusteeType': win32security.TRUSTEE_IS_USER,
								'TrusteeForm': win32security.TRUSTEE_IS_NAME,
								'Identifier': ''}
								}
					for i in range(len(self.users))
					]
			for i in range(len(self.users)):
				entries[i]['AccessPermissions'] = (con.GENERIC_ALL | con.GENERIC_WRITE)
				entries[i]['Trustee']['Identifier'] = self.users[i]
			self.run(entries)
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("perms.grant failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def get_access_mask_str(self, mask):
		try:
			ACCESS_MASKS = ['FILE_READ_DATA', 'FILE_LIST_DIRECTORY', 'FILE_WRITE_DATA', 'FILE_ADD_FILE', 
							'FILE_APPEND_DATA', 'FILE_ADD_SUBDIRECTORY', 'FILE_CREATE_PIPE_INSTANCE', 'FILE_READ_EA',
							'FILE_WRITE_EA', 'FILE_EXECUTE', 'FILE_TRAVERSE', 'FILE_DELETE_CHILD', 
							'FILE_READ_ATTRIBUTES', 'FILE_WRITE_ATTRIBUTES', 'FILE_ALL_ACCESS', 'FILE_GENERIC_READ',
							'FILE_GENERIC_WRITE', 'FILE_GENERIC_EXECUTE']
			for t in ACCESS_MASKS:
				attr = getattr(con, t)
				if (attr & mask) == attr:
					yield t
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("perms.get_access_mask_str failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def check_perm(self):
		try:
			dacl = win32security.GetNamedSecurityInfo(self.file, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION).GetSecurityDescriptorDacl()
			CONVENTIONAL_ACES = {
				win32security.ACCESS_ALLOWED_ACE_TYPE : "ALLOW", 
				win32security.ACCESS_DENIED_ACE_TYPE : "DENY"
			}
			for n_ace in range(dacl.GetAceCount()):
				ace = dacl.GetAce(n_ace)
				(ace_type, ace_flags) = ace[0]
				if ace_type in CONVENTIONAL_ACES:
					mask, sid = ace[1:]
				else:
					mask, object_type, inherited_object_type, sid = ace[1:]
				name, domain, type = win32security.LookupAccountSid(None, sid)
				if name in self.users:
					perms = (','.join(self.get_access_mask_str(mask)).split(","))
					if not "FILE_GENERIC_WRITE" in perms:
						print("%s does not have write access. Enableding Write access for user" %name)
						self.grants.append(name)
					else:
						print("%s has write permissions" %name)
						self.users.remove(name)
			for i in self.users:
				if not i in self.grants:
					self.grants.append(i)
			print(self.grants)
			if len(self.grants) > 0:
				self.users = self.grants
				self.grant()
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("perms.check_perm failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def deny(self):
		try:
			if not os.path.exists(self.file):
				raise WindowsError('Path %s could not be found.' % self.file)
			total = 0
			for x in self.users:
				userx, domain, utype = win32security.LookupAccountName("", x)
				sd = win32security.GetFileSecurity(self.file, win32security.DACL_SECURITY_INFORMATION)
				dacl = sd.GetSecurityDescriptorDacl()
				num_delete = 0
				for index in range(0, dacl.GetAceCount()):
					ace = dacl.GetAce(index - num_delete)
					if userx == ace[2]:
						dacl.DeleteAce(index - num_delete)
						num_delete += 1
						total += 1
				if num_delete > 0:
					sd.SetSecurityDescriptorDacl(1, dacl, 0)
					win32security.SetFileSecurity(self.file, win32security.DACL_SECURITY_INFORMATION, sd)
			if total > 0:
				return True
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("perms.deny failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
	def run(self, entries):
		try:
			sd = win32security.GetNamedSecurityInfo(self.file, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION)
			dacl = sd.GetSecurityDescriptorDacl()
			dacl.SetEntriesInAcl(entries)
			win32security.SetNamedSecurityInfo(self.file, win32security.SE_FILE_OBJECT, win32security.DACL_SECURITY_INFORMATION | win32security.UNPROTECTED_DACL_SECURITY_INFORMATION, None, None, dacl, None)
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			self.log.error("perms.run failed\n%s, %s, %s, %s" %(err, exc_type, exc_obj, traceback.print_tb(exc_tb)))
if __name__ == "__main__":
	file = "C:\\Program Files (x86)\\Encryptor\\assets"
	users = ["Users", "Everyone"]
	#perms(file, ["Users", "Everyone"]).deny()
	perms(file, users).check_perm()
	#perms(file, ["Users"]).deny()
