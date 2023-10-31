# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DownstreamProcesses(Document):
	@frappe.whitelist()
	def method_to_set_data_in_table (self):
		if (self.production) and (not self.downstream_process):
			frappe.throw("Please select 'Downstream Process'")

		t__w =frappe.get_value("Machine Shop Setting",self.company,"target_warehouse_dp")
		for d in self.get("production"):
			items_doc= frappe.get_all("Items Production" ,
												filters = {"parent": str(d.production)},
												fields = ["job_order","item","item_name","target_warehouse"])
			for i in items_doc:
				self.append("items",{
						'job_order': (i.job_order) ,
						'item': str(i.item),
						'item_name': str(i.item_name),
						'target_warehouse': t__w ,
					},),
	
		# self.method_to_set_raw_item()
	@frappe.whitelist()
	def set_warehouse_if_not(self):
		target_ware =frappe.get_value("Machine Shop Setting",self.company,"target_warehouse_dp")
		for t in self.get("items"):
			if not t.target_warehouse:
				t.target_warehouse=	target_ware

	@frappe.whitelist()
	def method_to_set_raw_item (self):
		if not self.downstream_process:
			frappe.throw("Please select 'Downstream Process'")
		s__w =frappe.get_value("Machine Shop Setting",self.company,"source_warehouse_dp")
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
										'source_warehouse': s__w if i.item != me.item else None,
										'available_qty': self.get_available_quantity(me.item,s__w) if i.item != me.item else 0
										
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
													'source_warehouse': s__w if i.item != y.item else None,
													'available_qty': self.get_available_quantity(y.item,s__w) if i.item != y.item else 0
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
							'target_warehouse':frappe.get_value("Machine Shop Setting",self.company,"mr_warehouse_dp"),
							
						},),
			if l.cr_qty:
				self.append("rejected_items_reasons",{
							'job_order': l.job_order,
							'finished_item': l.item,
							'rejection_type': "CR",
							'qty': l.cr_qty,
							'target_warehouse':frappe.get_value("Machine Shop Setting",self.company,"cr_warehouse_dp"),
							
						},),
			if l.rw_qty:
				self.append("rejected_items_reasons",{
							'job_order': l.job_order,
							'finished_item': l.item,
							'rejection_type': "RW",
							'qty': l.rw_qty,
							'target_warehouse':frappe.get_value("Machine Shop Setting",self.company,"rw_warehouse_dp"),
							
						},),
	@frappe.whitelist()
	def before_submit(self):		
		self.manifacturing_stock_entry()
		documents =self.get('rejected_items_reasons')
		if documents:
			self.transfer_stock_entry()

	@frappe.whitelist()
	def before_save(self):
		self.validate_total_qty()	


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
			se.downstream_process = self.name	
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
			se.downstream_process = self.name		
			se.insert()
			se.save()
			se.submit()


	def get_available_quantity(self,item_code, warehouse):
		filters = {"item_code": item_code,"warehouse": warehouse}
		fields = ["SUM(actual_qty) as available_quantity"]
		result = frappe.get_list("Stock Ledger Entry", filters=filters, fields=fields)
		
		if result and result[0].get("available_quantity"):
			return result[0].get("available_quantity")
		else:
			return 0
		
	@frappe.whitelist()	
	def set_available_qty(self):
		for ri in self.get('raw_items'):
			if ri.raw_item and ri.source_warehouse:
				ri.available_qty = self.get_available_quantity(ri.raw_item,ri.source_warehouse)

	@frappe.whitelist()	
	def validate_total_qty(self):
		total_item_qty=0
		for item in self.get('items'):
			total_item_qty= total_item_qty + item.qty
	
		if self.total_qty != total_item_qty:
			frappe.throw(f'The Total qty is not matched it should be equal to {total_item_qty}')
		# frappe.throw("hii.......")


	@frappe.whitelist()	
	def test_method(self):
		rows = self.get('raw_items')
		for r in rows:
			if r.item=='1010100007':
				r.standard_qty=333

		# frappe.throw(str(rows[0].clear()))





# =====================================================================================================
# # Copyright (c) 2023, Abhishek Chougule and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class DownstreamProcesses(Document):
# 	@frappe.whitelist()
# 	def method_to_set_data_in_table (self):
# 		if (self.production) and (not self.downstream_process):
# 			frappe.throw("Please select 'Downstream Process'")

# 		t__w =frappe.get_value("Machine Shop Setting",self.company,"target_warehouse_dp")
# 		for d in self.get("production"):
# 			items_doc= frappe.get_all("Items Production" ,
# 												filters = {"parent": str(d.production)},
# 												fields = ["job_order","item","item_name","target_warehouse"])
# 			for i in items_doc:
# 				avalable_ok_qty = frappe.get_all('Qty Details', 
# 									 		filters={'parent':str(d.production) ,"item" :i.item} ,
# 											fields=['ok_qty','job_order'], order_by='idx asc',)
# 				aval_ok_qty=0
# 				for av in avalable_ok_qty:
# 					if str(av.job_order) == str(i.job_order):
# 						aval_ok_qty=av.ok_qty
# 					# frappe.throw(str(aval_ok_qty))
# 				self.append("items",{
# 						'job_order': (i.job_order) ,
# 						'item': str(i.item),
# 						'item_name': str(i.item_name),
# 						'target_warehouse': t__w ,
# 						'available_ok_qty': aval_ok_qty
# 					},),
	
# 		# self.method_to_set_raw_item()
# 	@frappe.whitelist()
# 	def set_warehouse_if_not(self):
# 		target_ware =frappe.get_value("Machine Shop Setting",self.company,"target_warehouse_dp")
# 		for t in self.get("items"):
# 			if not t.target_warehouse:
# 				t.target_warehouse=	target_ware

# 	@frappe.whitelist()
# 	def method_to_set_raw_item (self):
# 		if not self.downstream_process:
# 			frappe.throw("Please select 'Downstream Process'")
# 		s__w =frappe.get_value("Machine Shop Setting",self.company,"source_warehouse_dp")
# 		for i in self.get("items"):
# 			if not i.item:
# 				frappe.throw("Please insert Items")
# 			if i.job_order:
# 				tera = frappe.get_all('Raw Item Child', filters={'parent':(frappe.get_value("Production Schedule",(frappe.get_value("Job Order",(i.job_order),"production_schedule")),"material_cycle_time")),'downstream_process': self.downstream_process} ,fields=['item',"item_name","qty"])
# 				for me in tera:

# 					self.append("raw_items",{
# 										'job_order': i.job_order,
# 										'item': str(i.item),
# 										'item_name': str(i.item_name),
# 										'raw_item': me.item,
# 										'raw_item_name': str(me.item_name),
# 										'required_qty':me.qty*i.qty,
# 										'standard_qty':me.qty,
# 										'source_warehouse': s__w if i.item != me.item else None,
# 										'available_qty': self.get_available_quantity(me.item,s__w) if i.item != me.item else 0
										
# 									},),

# 				self.append("qty_details",{
# 									'job_order': i.job_order,
# 									'item': str(i.item),
# 									'operation': self.downstream_process,
									
# 								},),


# 			else:
# 				demo =frappe.get_all('Material Cycle Time', filters={'item':i.item ,'company':self.company,"from_date" :["<",self.date]} ,fields=['name',], order_by='from_date desc',limit = 1 )
# 				if demo:
# 					for t in demo:
# 						kaju=frappe.get_all('Raw Item Child', filters={'parent':t.name,'downstream_process': self.downstream_process} ,fields=['item',"item_name","qty"])
# 						if kaju:
# 							for y in kaju:
# 								self.append("raw_items",{
# 													'item': str(i.item),
# 													'item_name': str(i.item_name),
# 													'raw_item': y.item,
# 													'raw_item_name': str(y.item_name),
# 													'required_qty':y.qty*i.qty,
# 													'standard_qty':y.qty,
# 													'source_warehouse': s__w if i.item != y.item else None,
# 													'available_qty': self.get_available_quantity(y.item,s__w) if i.item != y.item else 0
# 												},),
								
# 				self.append("qty_details",{
# 						'job_order': i.job_order,
# 						'item': str(i.item),
# 						'operation': self.downstream_process,
						
# 					},),


# 	@frappe.whitelist()
# 	def calculate_total_qty(self):
# 		total_quantity = 0
# 		for g in self.get("qty_details"):
# 			g.total_qty = g.ok_qty + g.cr_qty + g.mr_qty + g.rw_qty
# 			total_quantity = total_quantity+ g.total_qty

# 		self.total_qty = total_quantity



# 	@frappe.whitelist()
# 	def set_data_in_rejected_items_reasons(self):

# 		for l in self.get("qty_details"):
# 			if l.mr_qty:

# 				self.append("rejected_items_reasons",{
# 							'job_order': l.job_order,
# 							'finished_item': l.item,
# 							'rejection_type': "MR",
# 							'qty': l.mr_qty,
# 							'target_warehouse':frappe.get_value("Machine Shop Setting",self.company,"mr_warehouse_dp"),
							
# 						},),
# 			if l.cr_qty:
# 				self.append("rejected_items_reasons",{
# 							'job_order': l.job_order,
# 							'finished_item': l.item,
# 							'rejection_type': "CR",
# 							'qty': l.cr_qty,
# 							'target_warehouse':frappe.get_value("Machine Shop Setting",self.company,"cr_warehouse_dp"),
							
# 						},),
# 			if l.rw_qty:
# 				self.append("rejected_items_reasons",{
# 							'job_order': l.job_order,
# 							'finished_item': l.item,
# 							'rejection_type': "RW",
# 							'qty': l.rw_qty,
# 							'target_warehouse':frappe.get_value("Machine Shop Setting",self.company,"rw_warehouse_dp"),
							
# 						},),
# 	@frappe.whitelist()
# 	def before_submit(self):		
# 		self.manifacturing_stock_entry()
# 		self.transfer_stock_entry()

# 	@frappe.whitelist()
# 	def before_save(self):
# 		self.validate_total_qty()	


# 	@frappe.whitelist()
# 	def manifacturing_stock_entry(self):
# 		for p in self.get("items"):      
# 			se = frappe.new_doc("Stock Entry")
# 			se.stock_entry_type = "Manufacture"
# 			se.company = self.company
# 			se.posting_date = self.date
# 			peacock = len(self.get("raw_items"))
# 			for g in self.get("raw_items"):
# 				if (str(p.job_order) == str(g.job_order)) and (p.item == g.item) and (p.item == g.raw_item ):
# 					for b in self.get("qty_details"):
# 						if  (str(p.job_order) == str(b.job_order)) and (p.item == b.item):
# 							se.append(
# 									"items",
# 									{
# 										"item_code": p.item,
# 										"qty": b.ok_qty,
# 										"s_warehouse": g.source_warehouse,
# 									},)
# 							se.append(
# 							"items",
# 							{
# 								"item_code": p.item,
# 								"qty": b.ok_qty,
# 								"t_warehouse": p.target_warehouse,
# 								'is_finished_item':True
# 							},)

# 				elif(str(p.job_order) == str(g.job_order)) and (p.item == g.item) and (p.item != g.raw_item):
# 					for v in self.get("qty_details"):
# 						if (str(p.job_order) == str(v.job_order)) and (p.item == v.item):
# 							se.append(
# 									"items",
# 									{
# 										"item_code": g.raw_item,
# 										"qty": g.standard_qty * v.ok_qty ,
# 										"s_warehouse": g.source_warehouse,
# 									},)
					
# 				elif g==peacock:
# 					frappe.throw(f'There is Row Item {g.item} present in "Raw Items" table')
# 			se.downstream_process = self.name	
# 			se.insert()
# 			se.save()
# 			se.submit()


# 	@frappe.whitelist()
# 	def transfer_stock_entry(self):
# 		se = frappe.new_doc("Stock Entry")
# 		se.stock_entry_type = "Material Transfer"
# 		se.company = self.company
# 		se.posting_date = self.date
# 		peahen = len(self.get("raw_items"))
# 		for p in self.get("items"):
# 			for g in self.get("raw_items"):
# 				if (str(p.job_order) == str(g.job_order)) and (p.item == g.item) and (p.item == g.raw_item ):
# 					for b in self.get("rejected_items_reasons"):
# 						if  (str(p.job_order) == str(b.job_order)) and (p.item == b.finished_item):
# 							se.append(
# 									"items",
# 									{
# 										"item_code": p.item,
# 										"qty": b.qty,
# 										"s_warehouse": g.source_warehouse,
# 										"t_warehouse": b.target_warehouse,
# 									},)
					
# 				elif g==peahen:
# 					frappe.throw(f'There is Row Item {g.item} present in "Raw Items" table')
# 		se.downstream_process = self.name		
# 		se.insert()
# 		se.save()
# 		se.submit()


# 	def get_available_quantity(self,item_code, warehouse):
# 		filters = {"item_code": item_code,"warehouse": warehouse}
# 		fields = ["SUM(actual_qty) as available_quantity"]
# 		result = frappe.get_list("Stock Ledger Entry", filters=filters, fields=fields)
		
# 		if result and result[0].get("available_quantity"):
# 			return result[0].get("available_quantity")
# 		else:
# 			return 0
		
# 	@frappe.whitelist()	
# 	def set_available_qty(self):
# 		for ri in self.get('raw_items'):
# 			if ri.raw_item and ri.source_warehouse:
# 				ri.available_qty = self.get_available_quantity(ri.raw_item,ri.source_warehouse)

# 	@frappe.whitelist()	
# 	def validate_total_qty(self):
# 		total_item_qty=0
# 		for item in self.get('items'):
# 			total_item_qty= total_item_qty + item.qty
	
# 		if self.total_qty != total_item_qty:
# 			frappe.throw(f'The Total qty is not matched it should be equal to {total_item_qty}')
# 		# frappe.throw("hii.......")


# 	@frappe.whitelist()	
# 	def test_method(self):
# 		frappe.msgprint('Done........')
# 		# frappe.db.set_value("Stock Entry Detail","770cd8ec01","basic_rate",100)
# 		# frappe.db.set_value("Stock Entry Detail","770cd8ec01","basic_amount",1000)
# 		# frappe.db.set_value("Stock Entry Detail","770cd8ec01","additional_cost",280)
# 		# frappe.db.set_value("Stock Entry Detail","770cd8ec01","valuation_rate",128)
# 		# frappe.db.set_value("Stock Entry Detail","770cd8ec01","amount",1280)

# 		# frappe.db.set_value("Stock Entry Detail","e58df51b6d","basic_rate",75)
# 		# frappe.db.set_value("Stock Entry Detail","e58df51b6d","basic_amount",1125)
# 		# frappe.db.set_value("Stock Entry Detail","e58df51b6d","additional_cost",420)
# 		# frappe.db.set_value("Stock Entry Detail","e58df51b6d","valuation_rate",103)
# 		# frappe.db.set_value("Stock Entry Detail","e58df51b6d","amount",1545)

# 		# frappe.db.set_value("Stock Entry","MAT-STE-2023-00402","total_outgoing_value",2325)
# 		# frappe.db.set_value("Stock Entry","MAT-STE-2023-00402","total_incoming_value",2825)
# 		# frappe.db.set_value("Stock Entry","MAT-STE-2023-00402","value_difference",500)
# 		# # frappe.db.set_value("Stock Entry Detail","e58df51b6d","amount",1545)
# 		# pass

# 		# se = frappe.new_doc("Stock Entry")
# 		# se.stock_entry_type = "Additional Consumption"
# 		# se.company = "Phadke Engineers Pvt. Ltd."
# 		# se.append(
# 		# 		"additional_costs",
# 		# 		{
# 		# 			"expense_account":"Expenses Included In Asset Valuation - PEPL" ,
# 		# 			"amount":500,
# 		# 			"description": 'additional expense',

# 		# 		},)
# 		# se.append(
# 		# 		"items",
# 		# 		{
# 		# 			"s_warehouse": "Production - PEPL",
# 		# 			"item_code": '1010100018',
# 		# 			"qty":10,
# 		# 			"basic_rate":100,
# 		# 			"basic_amount":1000,
# 		# 			"additional_cost":0,
# 		# 			"valuation_rate":100,
# 		# 			"amount":1000,
# 		# 			"is_finished_item":0,
# 		# 		},)
# 		# se.append(
# 		# 		"items",
# 		# 		{
# 		# 			"s_warehouse": "Production - PEPL",
# 		# 			"item_code": '1010100007',
# 		# 			"qty":15,
# 		# 			"basic_rate":75,
# 		# 			"basic_amount":1125,
# 		# 			"additional_cost":0,
# 		# 			"valuation_rate":75,
# 		# 			"amount":1125,
# 		# 			"is_finished_item":0,
# 		# 		},)
# 		# se.append(
# 		# 		"items",
# 		# 		{
# 		# 			"s_warehouse": "Consumables - PEPL",
# 		# 			"item_code": 'INSERT',
# 		# 			"qty":20,
# 		# 			"basic_rate":10,
# 		# 			"basic_amount":200,
# 		# 			"additional_cost":0,
# 		# 			"valuation_rate":10,
# 		# 			"amount":200,
# 		# 			"is_finished_item":0,
# 		# 		},)
# 		# se.append(
# 		# 		"items",
# 		# 		{
# 		# 			"t_warehouse": "Production - PEPL",
# 		# 			"item_code": '1010100018',
# 		# 			"qty":10,
# 		# 			"basic_rate":100,
# 		# 			"basic_amount":1000,
# 		# 			"additional_cost":280,
# 		# 			"valuation_rate":128,
# 		# 			"amount":1280,
# 		# 			"is_finished_item":1,
# 		# 		},)
# 		# se.append(
# 		# 		"items",
# 		# 		{
# 		# 			"t_warehouse": "Production - PEPL",
# 		# 			"item_code": '1010100007',
# 		# 			"qty":15,
# 		# 			"basic_rate":75,
# 		# 			"basic_amount":1125,
# 		# 			"additional_cost":420,
# 		# 			"valuation_rate":103,
# 		# 			"amount":1545,
# 		# 			"is_finished_item":1,
# 		# 		},)
	
# 		# se.insert()
# 		# se.save()
# 		# se.submit()

# 		# frappe.throw(str(rows[0].clear()))


# 	# @frappe.whitelist()
# 	# def sample(self):
		

