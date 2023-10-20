# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WagesMaster(Document):
	@frappe.whitelist()
	def before_save(self):
		for x in self.get('wages'):
			for y in self.get('wages'):
				if x.idx != y.idx:
					if x.from_date == y.from_date:
						frappe.throw(f'You can not save from date at line {x.idx} and {y.idx}')