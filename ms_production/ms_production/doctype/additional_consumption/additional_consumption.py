# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AdditionalConsumption(Document):
	@frappe.whitelist()
	def set_data_in_items_table(self):
		if self.reference_doc == 'Production':
			doc = frappe.get_all('Production',
										filters={'date':self.date , 'docstatus': 1 ,},
										fields=['name','supervisor','supervisor_name'],)
			for d in doc:
				doc_child = frappe.get_all('Items Production', 
									 		filters={'parent':str(d.name)} ,
											fields=['item','job_order','target_warehouse',])
				for dc in doc_child:
					doc_child_qty = frappe.get_all('Qty Details', 
									 		filters={'parent':str(d.name),'item':dc.item,"additional_consumption_status":False,} ,
											fields=['ok_qty','name'], order_by='idx desc',limit = 1)
					for dcq in doc_child_qty:
						self.append("items_table",{
							'reference_doc': (d.name) ,
							'child_reference_doc': dcq.name,
							'item': (dc.item),
							'item_name': frappe.get_value("Item",(dc.item),"item_name"),
							'source_warehouse': dc.target_warehouse ,
							'ok_quantity': dcq.ok_qty,
							'supervisor': d.supervisor ,
							'supervisor_name': d.supervisor_name,
						},),


		elif self.reference_doc == 'Downstream Processes':
			moc = frappe.get_all('Downstream Processes',
										filters={'date':self.date , "downstream_process":self.reference_process , 'docstatus': 1 , } ,
										fields=['name','supervisor','supervisor_name'],)
			# frappe.throw(str(moc))
			for m in moc:
				moc_child = frappe.get_all('Downstream Items Production', 
									 		filters={'parent':str(m.name)} ,
											fields=['item','job_order','target_warehouse',])
				for mc in moc_child:
					moc_child_qty = frappe.get_all('Downstream Qty Details', 
									 		filters={'parent':str(m.name),'item':mc.item, "additional_consumption_status":False} ,
											fields=['ok_qty','name'], order_by='idx desc',limit = 1)
					for mcq in moc_child_qty:
						self.append("items_table",{
							'reference_doc': (m.name) ,
							'child_reference_doc': mcq.name,
							'item': (mc.item),
							'item_name': frappe.get_value("Item",(mc.item),"item_name"),
							'source_warehouse': mc.target_warehouse ,
							'ok_quantity': mcq.ok_qty,
							'supervisor': m.supervisor ,
							'supervisor_name': m.supervisor_name,
						},),
		
		check_table = self.get("items_table")
		if check_table:
			self.set_data_in_supervisor_wages_table()
			self.calculate_total_ok_qty()
		else:
			if self.reference_doc=="Production":
				frappe.throw(f'There is no data present for "Production" on date {self.date}')
			else:
				if self.reference_process:
					frappe.throw(f'There is no data present for "Downstream Processes" of "{self.reference_process}" on date {self.date}')

	@frappe.whitelist()
	def calculate_total_ok_qty(self):
		# frappe.msgprint('A row has been added to the links table 🎉 ')

		total_ok_qty =0
		for jtp in self.get("items_table"):
			total_ok_qty = total_ok_qty+ jtp.ok_quantity

		self.total_ok_quantity=total_ok_qty


	@frappe.whitelist()
	def set_data_in_supervisor_wages_table(self):
		supervisor = list(set([d.supervisor for d in self.get("items_table")]))
		# frappe.throw(str(supervisor))
		for s in supervisor:
			wages=0
			cor = frappe.get_all("Wages Master",filters = {"Employee": s},fields = ["name"])
			if cor:
				cos = frappe.get_all("Child Wages Master",filters = {"parent": cor[0].name ,"from_date": ['<=',self.date]},fields = ["wages_per_hour"], order_by = 'from_date DESC')
				if cos:
					wages =(cos[0].wages_per_hour)


			self.append("supervisor_wages_table",{
							'supervisor_id': s ,
							'supervisor_name': frappe.get_value("Employee",str(s),"employee_name"),
							'wages_per_hours': wages,

						},),

	@frappe.whitelist()
	def find_avalable_qty(self):
		for ci in self.get("consumption_table"):
			ci.available_qty = self.get_available_quantity(ci.cunsumption_item , ci.source_warehouse)

	def get_available_quantity(self,item_code, warehouse):
		filters = {"item_code": item_code,"warehouse": warehouse}
		fields = ["SUM(actual_qty) as available_quantity"]
		
		result = frappe.get_list("Stock Ledger Entry", filters=filters, fields=fields)
		
		if result and result[0].get("available_quantity"):
			return result[0].get("available_quantity")
		else:
			return 0

	def before_save(self):
		self.calculate_total_ok_qty()

	def before_submit(self):

		self.material_issue_stock_entry()
		
		self.additional_consumption_stock_entry()
		self.status_maintain()

	def before_cancel(self):
		# pass
		self.status_maintain_on_cancle()

	@frappe.whitelist()
	def material_issue_stock_entry(self):
		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Material Issue"
		se.company = self.company
		se.posting_date = self.date
		for g in self.get("consumption_table"):
			se.append(
					"items",
					{
						"item_code": g.cunsumption_item,
						"qty": g.qty,
						"s_warehouse": g.source_warehouse,
					},)
		se.additional_consumption=self.name
		se.insert()
		se.save()
		se.submit()

		doc = frappe.db.get_all("Stock Entry", fields=["name","total_outgoing_value"], order_by="creation DESC", limit=1)
		self.add_cons_items= doc[0].total_outgoing_value
			# frappe.db.set_value("Supplier", doc[0].name, "name", self.name)


	@frappe.whitelist()
	def additional_consumption_stock_entry(self):
		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Additional Consumption"
		se.company = self.company
		se.posting_date = self.date
		for i in self.get("items_table"):
			se.append(
					"items",
					{
						"item_code": i.item,
						"qty": i.ok_quantity,
						"s_warehouse": i.source_warehouse,
					},)
			
			se.append(
					"items",
					{
						"item_code": i.item,
						"qty": i.ok_quantity,
						"t_warehouse": i.source_warehouse,
						"is_finished_item":True,
						
					},)
		for h in self.get("supervisor_wages_table"):
			se.append(
					"additional_costs",
					{
						"expense_account":self.expense_account_for_consumption,
						"description": "Wages Consumption of - " + str(h.supervisor_id) + "_"+str(h.supervisor_name),
						"amount": h.wages_per_hours * h.work_hours,
					},)
		se.append(
					"additional_costs",
					{
						"expense_account":self.expense_account_for_consumption,
						"description": "Amount Consumption of Items ",
						"amount": self.add_cons_items,
					},)
		se.additional_consumption=self.name
		se.insert()
		se.save()
		last_stock_entry = frappe.db.get_all("Stock Entry", fields=["name"], order_by="creation DESC", limit=1)
		last_stock_entry_doc = frappe.get_doc("Stock Entry",last_stock_entry[0].name)
		for d in last_stock_entry_doc.items:
			for p in last_stock_entry_doc.items:
				if d.s_warehouse:
					if d.item_code == p.item_code and d.s_warehouse == p.t_warehouse and d.qty == p.qty:
						# frappe.msgprint("hiii..............")
						p.set_basic_rate_manually = True
						p.basic_rate = d.basic_rate
		last_stock_entry_doc.submit()

		# se.submit()

	@frappe.whitelist()
	def status_maintain(self):
		if self.reference_doc== "Production":
			doctype_name= "Qty Details"
		elif self.reference_doc == 'Downstream Processes':
			doctype_name= "Downstream Qty Details"
		
		fiels_name = "additional_consumption_status"
		
		for dod in self.get("items_table"):
			document_name= str(dod.child_reference_doc)
			frappe.set_value(doctype_name , document_name , fiels_name , True )

	@frappe.whitelist()
	def status_maintain_on_cancle(self):
		if self.reference_doc== "Production":
			doctype_name= "Qty Details"
		elif self.reference_doc == 'Downstream Processes':
			doctype_name= "Downstream Qty Details"
		
		fiels_name = "additional_consumption_status"
		
		for dod in self.get("items_table"):
			document_name= str(dod.child_reference_doc)
			frappe.set_value(doctype_name , document_name , fiels_name , False )

