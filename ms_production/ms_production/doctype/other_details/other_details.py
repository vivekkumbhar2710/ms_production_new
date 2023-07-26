# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OtherDetails(Document):

	@frappe.whitelist()
	def get_operations(machine):
		# Add your logic here to fetch operations based on the selected machine
		operations = frappe.get_all("Machine Operations", filters={"machine": machine}, pluck="operation")

		return operations
