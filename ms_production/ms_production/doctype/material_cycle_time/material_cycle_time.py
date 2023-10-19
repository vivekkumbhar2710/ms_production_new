# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaterialCycleTime(Document):
	@frappe.whitelist()
	def set_auto_item_in_row_items(self):
		self.append("row_items",{
						'item': self.item,
						'item_name': self.item_name,
						'qty': 1
					},),
	