# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobOrder(Document):
	@frappe.whitelist()
	def set_data_raw_item(self):
		doc= frappe.get_all("Raw Item Child", 
					  						filters = {"parent": (frappe.get_value("Production Schedule", self.production_schedule ,"material_cycle_time"))},
											fields =["downstream_process","item","item_name","qty"])
		# frappe.throw(str(doc))
		for entry in doc:
			self.append(
				"raw_item",
				{
					"downstream_process": entry.downstream_process,
					"item": entry.item,
					"item_name": entry.item_name,
					"qty": entry.qty * self.total_quantity_of_production,
				},
			)


