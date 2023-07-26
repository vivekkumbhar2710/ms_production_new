# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt 
import frappe
from frappe.model.document import Document
from frappe.utils.data import nowdate
import json

def getVal(val):
        return val if val is not None else 0

class Production(Document):
	@frappe.whitelist()
	def get_od(self):
		pass
	# 	od=frappe.db.get_list("Item",fields=['name','cycle_time'],filters={'name':self.item})
	# 	for i in od:
	# 		doc=frappe.get_doc("Item",i.name)
	# 		for j in doc.get('other_details'):
	# 				self.append("other_details",{
	# 					'machine':j.machine,
	# 					'operation':j.operation,
	# 					'source_warehouse':j.source_warehouse,
	# 					'target_warehouse':j.target_warehouse,
	# 					'operator':j.operator,
	# 					'cycle_time':j.cycle_time,
	# 					'salary':j.salary,
	# 					'shift':j.shift,
	# 					'is_done':j.is_done,
	# 					'ok_qty':j.ok_qty,
	# 					'cr_qty':j.cr_qty,
	# 					'mr_qty':j.mr_qty,
	# 					'rw_qty':j.rw_qty,
	# 					'total_qty':j.total_qty,
	# 					'worked_time':j.worked_time,
	# 					'earned_min':j.earned_min,
	# 					'time_diffrence':j.time_diffrence,
	# 				})
	# 				self.append("qty_details",{
	# 					'operation':j.operation,
	# 					'cycle_time':j.cycle_time,
	# 					'ok_qty':j.ok_qty,
	# 					'cr_qty':j.cr_qty,
	# 					'mr_qty':j.mr_qty,
	# 					'rw_qty':j.rw_qty,
	# 					'total_qty':j.total_qty,
	# 					'worked_time':j.worked_time,
	# 					'earned_min':j.earned_min,
	# 					'time_diffrence':j.time_diffrence,
	# 				})

					
	@frappe.whitelist()
	def get_opdetails(self):
		emp=frappe.db.get_list("Employee",fields=['name','default_shift','designation','ctc'],filters={'name':self.operator})
		for i in emp:
			self.shift=i.default_shift
			self.salary=i.ctc

	@frappe.whitelist()
	def totalqty_em(doc,method):
		doc.total_qty=getVal(doc.ok_qty)+getVal(doc.cr_qty)+getVal(doc.mr_qty)+getVal(doc.rw_qty)
		doc.earned_time=getVal(doc.cycle_time)*getVal(doc.total_qty)
		

	@frappe.whitelist()
	def time_diff(doc,method):
		doc.time_difference= getVal(doc.worked_time) - getVal(doc.earned_time)

	@frappe.whitelist()
	def consumable_amount(self):
		for i in self.get('consumable_details'):
			i.amount  = getVal(i.qty) * getVal(i.rate)

	@frappe.whitelist()
	def fetch_oprations(doc,method):
		if(doc.operation is None):
			return
		od=frappe.db.get_list("Item",fields=['name','cycle_time'],filters={'name':doc.item})
		for i in od:
			cdoc=frappe.get_doc("Item",i.name)
			for j in cdoc.get('other_details'):
					if(j.machine == doc.machine and j.operation == doc.operation):
						doc.source_warehouse = j.source_warehouse
						doc.target_warehouse = j.target_warehouse
						doc.cycle_time = j.cycle_time
						break

    
	def before_save(self):
		frappe.msgprint("THIS IS SHIT!")
		downtime_time=0.0
		total=0.0   
		curren_time_diff=0.0
		for i in self.get('downtime_reason_details'):
			downtime_time=downtime_time+i.time
		
		curren_time_diff= getVal(self.time_difference)
		total = getVal(self.worked_time) + downtime_time
		if total!=self.required_time or curren_time_diff<0:
			if( curren_time_diff < 0):
				frappe.throw('Worked Time must be greater than Earned Time!')
			frappe.throw('Time Diffrence or Worked Time Not Matched !')

		rej_reasons = 0
		for i in self.get('item_rejection_reason'):
			rej_reasons += i.qty
		rej_qty = getVal(self.cr_qty)+getVal(self.mr_qty)
		if(rej_reasons!=rej_qty):
			frappe.throw("Mention the reasons of all rejected Items")

	def cancel_stock_entry(self,stock_entry_name):
		try:
			# Get the Stock Entry document
			stock_entry = frappe.get_doc("Stock Entry", stock_entry_name)

			# Cancel the Stock Entry
			stock_entry.cancel()

			# Save the document
			stock_entry.save()

			frappe.db.commit()
			frappe.msgprint("Stock Entry '{stock_entry_name}' has been cancelled successfully.")
		except frappe.DoesNotExistError:
			frappe.msgprint(f"Stock Entry '{stock_entry_name}' not found.")
		except Exception as e:
			frappe.msgprint(f"Error cancelling Stock Entry '{stock_entry_name}': {str(e)}")
	import frappe

	def amend_canceled_stock_entry(original_stock_entry_name):
		try:
			# Get the original Stock Entry document
			original_stock_entry = frappe.get_doc("Stock Entry", original_stock_entry_name)

			# Create a new Stock Entry based on the canceled one
			new_stock_entry = frappe.copy_doc(original_stock_entry, ignore_no_copy=True)

			# Make necessary modifications to the new Stock Entry
			# For example, you might want to change quantities, items, or other details

			# Save the new Stock Entry

			new_stock_entry.insert()

			frappe.db.commit()
			frappe.msgprint(f"Amended Stock Entry '{original_stock_entry_name}' has been created successfully: {new_stock_entry.name}")
		except frappe.DoesNotExistError:
			print(f"Stock Entry '{original_stock_entry_name}' not found.")
		except Exception as e:
			print(f"Error amending Stock Entry '{original_stock_entry_name}': {str(e)}")

# # Usage example
# amend_canceled_stock_entry("SE-00001")

        
        
	def create_stock_transfer(self):
		if(self.stock_entry!=None):
				self.amend_canceled_stock_entry(self.stock_entry)
    
		total_cost_of_item = 0
		items = [
			{
                "item_code": self.raw_item,
                "qty": self.total_qty,
                "s_warehouse": self.source_warehouse,
                "set_basic_rate_manually":1,
                "basic_rate": frappe.get_value("Item", self.raw_item, "valuation_rate"),
                "item_name": frappe.get_value("Item", self.raw_item, "item_name"),
            }
		]

		for i in self.get('consumable_details'):
			total_cost_of_item+=(i.rate*i.qty)
			items.append(
				{
					"item_code": i.item if i.item is not None else "oil",
					"qty": i.qty,
					"s_warehouse": i.source_warehouse,
					"set_basic_rate_manually":1,
        			"basic_rate": i.rate,
					# "rate": i.rate,
				}
			)
		items.append(
    			{	
                "item_code": self.item ,
                "qty": self.total_qty,
                "t_warehouse": self.target_warehouse,
                "set_basic_rate_manually":1,
                "basic_rate": frappe.get_value("Item", self.item, "valuation_rate"),
                "item_name": frappe.get_value("Item", self.item, "item_name"),
				"basic_amount":total_cost_of_item+(frappe.get_value("Item", self.raw_item, "valuation_rate")*self.total_qty),
				'set_basic_rate_manually' :1,
				'is_finished_item':1
                
            }
		)
		
		stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Manufacture",
        "items": items
        })

		stock_entry.insert()
		stock_entry.submit()
		self.stock_entry = stock_entry.name
		frappe.msgprint(str(self.stock_entry))
		print(f"Stock Transfer created with name: {stock_entry.name}")
		

	
	def before_submit(self):
		self.create_stock_transfer()
	
	def on_cancel(self):
		self.cancel_stock_entry(self.stock_entry)
	def before_validation(self):
		frappe.msgprint("YUUUUUU!")
		if(self.stock_entry!=None):
				self.amend_canceled_stock_entry(self.stock_entry)
	def on_amend(self):
		frappe.msgprint("THJIS IS WORKING!")
		
	
