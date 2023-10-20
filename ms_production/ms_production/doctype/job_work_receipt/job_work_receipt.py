# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobWorkReceipt(Document):
	@frappe.whitelist()
	def before_submit(self):
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Material Receipt"
			se.company = self.company
			se.posting_date = self.posting_date
			se.posting_time = self.posting_time
			for p in self.get("item"):
				se.append(
						"items",
						{
							"item_code": p.item_code,
							"qty": p.qty,
							"t_warehouse": p.warehouse,
							"allow_zero_valuation_rate": 1
						},)
						

			se.job_work_receipt = self.name		
			se.insert()
			se.save()
			se.submit()
