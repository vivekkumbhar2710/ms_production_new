# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProductionSchedule(Document):
	@frappe.whitelist()
	def before_save(self):
		# self.validate_shift()
		pass

	@frappe.whitelist()
	def calculate_total_time(self):
		cycle_time = 0
		doc = frappe.get_all("Machine Item", filters = {"parent":self.material_cycle_time} ,fields =["cycle_time"])
		for d in doc:
			cycle_time =cycle_time +d.cycle_time

		self.total_time = cycle_time
		
		if self.total_quantity_of_production:
			self.total_production_time = self.total_time *self.total_quantity_of_production
		if self.total_production_per_day and self.total_quantity_of_production:
			self.total_qty_production_per_day = self.total_production_per_day/self.total_time
			self.total_days_of_production = self.total_production_time /self.total_production_per_day


	@frappe.whitelist()
	def validate_shift(self):
		validable_time=0
		data_list = [d.shift_time for d in self.shift_time]
		for q in data_list:
			w = frappe.get_value("Shift Time",q,"minutes")
			validable_time = validable_time + w
		if validable_time > 1440:
			frappe.throw("Regrettably, extending a single shift beyond its standard duration by 1440 minutes is not feasible for operational reasons.")
		else:
			self.total_production_per_day = validable_time
			
			self.calculate_total_time()