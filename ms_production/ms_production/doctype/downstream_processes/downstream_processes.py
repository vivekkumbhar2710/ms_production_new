# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DownstreamProcesses(Document):
	@frappe.whitelist()
	def method_to_set_data_in_table (self):
		if (self.production) and (not self.downstream_process):
			frappe.throw("Please select 'Downstream Process'")


		for d in self.get("production"):
			items_doc= frappe.get_all("Items Production" ,
												filters = {"parent": str(d.production)},
												fields = ["job_order","item","item_name","target_warehouse"])
			for i in items_doc:
				self.append("items",{
						'job_order': (i.job_order) ,
						'item': str(i.item),
						'item_name': str(i.item_name),
						'target_warehouse': i.target_warehouse,
					},),
	
		# self.method_to_set_raw_item()
				
	@frappe.whitelist()
	def method_to_set_raw_item (self):
		if not self.downstream_process:
			frappe.throw("Please select 'Downstream Process'")
		for i in self.get("items"):
			if not i.item:
				frappe.throw("Please insert Items")
			if i.job_order:
				tera = frappe.get_all('Raw Item Child', filters={'parent':(frappe.get_value("Production Schedule",(frappe.get_value("Job Order",(i.job_order),"production_schedule")),"material_cycle_time")),'downstream_process': self.downstream_process} ,fields=['item',"item_name","qty"])
				for me in tera:
					self.append("raw_items",{
										'job_order': i.job_order,
										'item': str(i.item),
										'item_name': str(i.item_name),
										'raw_item': me.item,
										'raw_item_name': str(me.item_name),
										'required_qty':me.qty*i.qty,
										'standard_qty':me.qty,
									},),

				self.append("qty_details",{
									'job_order': i.job_order,
									'item': str(i.item),
									'operation': self.downstream_process,
									
								},),


			else:
				demo =frappe.get_all('Material Cycle Time', filters={'item':i.item ,'company':self.company,"from_date" :["<",self.date]} ,fields=['name',], order_by='from_date desc',limit = 1 )
				if demo:
					for t in demo:
						kaju=frappe.get_all('Raw Item Child', filters={'parent':t.name,'downstream_process': self.downstream_process} ,fields=['item',"item_name","qty"])
						if kaju:
							for y in kaju:
								self.append("raw_items",{
													'item': str(i.item),
													'item_name': str(i.item_name),
													'raw_item': y.item,
													'raw_item_name': str(y.item_name),
													'required_qty':y.qty*i.qty,
													'standard_qty':y.qty,
												},),
								
				self.append("qty_details",{
						'job_order': i.job_order,
						'item': str(i.item),
						'operation': self.downstream_process,
						
					},),


	@frappe.whitelist()
	def calculate_total_qty(self):
		total_quantity = 0
		for g in self.get("qty_details"):
			g.total_qty = g.ok_qty + g.cr_qty + g.mr_qty + g.rw_qty
			total_quantity = total_quantity+ g.total_qty

		self.total_qty = total_quantity



	@frappe.whitelist()
	def set_data_in_rejected_items_reasons(self):

		for l in self.get("qty_details"):
			if l.mr_qty:

				self.append("rejected_items_reasons",{
							'job_order': l.job_order,
							'finished_item': l.item,
							'rejection_type': "MR",
							'qty': l.mr_qty,
							
						},),
			if l.cr_qty:
				self.append("rejected_items_reasons",{
							'job_order': l.job_order,
							'finished_item': l.item,
							'rejection_type': "CR",
							'qty': l.cr_qty,
							
						},),
			if l.rw_qty:
				self.append("rejected_items_reasons",{
							'job_order': l.job_order,
							'finished_item': l.item,
							'rejection_type': "RW",
							'qty': l.rw_qty,
							
						},),
	@frappe.whitelist()
	def before_submit(self):		
		self.manifacturing_stock_entry()
		self.transfer_stock_entry()


	@frappe.whitelist()
	def manifacturing_stock_entry(self):
		for p in self.get("items"):      
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Manufacture"
			se.company = self.company
			se.posting_date = self.date
			peacock = len(self.get("raw_items"))
			for g in self.get("raw_items"):
				if (str(p.job_order) == str(g.job_order)) and (p.item == g.item) and (p.item == g.raw_item ):
					for b in self.get("qty_details"):
						if  (str(p.job_order) == str(b.job_order)) and (p.item == b.item):
							se.append(
									"items",
									{
										"item_code": p.item,
										"qty": b.ok_qty,
										"s_warehouse": g.source_warehouse,
									},)
							se.append(
							"items",
							{
								"item_code": p.item,
								"qty": b.ok_qty,
								"t_warehouse": p.target_warehouse,
								'is_finished_item':True
							},)

				elif(str(p.job_order) == str(g.job_order)) and (p.item == g.item) and (p.item != g.raw_item):
					for v in self.get("qty_details"):
						if (str(p.job_order) == str(v.job_order)) and (p.item == v.item):
							se.append(
									"items",
									{
										"item_code": g.raw_item,
										"qty": g.standard_qty * v.ok_qty ,
										"s_warehouse": g.source_warehouse,
									},)
					
				elif g==peacock:
					frappe.throw(f'There is Row Item {g.item} present in "Raw Items" table')
				
			se.insert()
			se.save()
			se.submit()


	@frappe.whitelist()
	def transfer_stock_entry(self):
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Material Transfer"
			se.company = self.company
			se.posting_date = self.date
			peahen = len(self.get("raw_items"))
			for p in self.get("items"):
				for g in self.get("raw_items"):
					if (str(p.job_order) == str(g.job_order)) and (p.item == g.item) and (p.item == g.raw_item ):
						for b in self.get("rejected_items_reasons"):
							if  (str(p.job_order) == str(b.job_order)) and (p.item == b.finished_item):
								se.append(
										"items",
										{
											"item_code": p.item,
											"qty": b.qty,
											"s_warehouse": g.source_warehouse,
											"t_warehouse": b.target_warehouse,
										},)
						
					elif g==peahen:
						frappe.throw(f'There is Row Item {g.item} present in "Raw Items" table')
				
			se.insert()
			se.save()
			se.submit()


