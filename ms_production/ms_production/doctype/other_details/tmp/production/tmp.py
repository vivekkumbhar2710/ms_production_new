
# Copyright (c) 2023, Nishant Shingate and contributors
# For license information, please see license.txt 
from typing import Self
import frappe
from frappe.model.document import Document
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

					
# 	@frappe.whitelist()
# 	def get_opdetails(self):
# 		emp=frappe.db.get_list("Employee",fields=['name','default_shift','designation','ctc'],filters={'name':self.operator})
# 		for i in emp:
# 			self.shift=i.default_shift
# 			self.salary=i.ctc

# 	@frappe.whitelist()
# 	def totalqty_em(doc,method):
# 		doc.total_qty=getVal(doc.ok_qty)+getVal(doc.cr_qty)+getVal(doc.mr_qty)+getVal(doc.rw_qty)
# 		doc.earned_time=getVal(doc.cycle_time)*getVal(doc.total_qty)
		

# 	@frappe.whitelist()
# 	def time_diff(doc,method):
# 		doc.time_difference= getVal(doc.worked_time) - getVal(doc.earned_time)

	@frappe.whitelist()
	def consumable_amount(self):
		for i in self.get('consumable_details'):
			i.amount  = getVal(i.qty) * getVal(i.rate)

# 	@frappe.whitelist()
# 	def fetch_oprations(doc,method):
# 		if(doc.operation is None):
# 			return
# 		od=frappe.db.get_list("Item",fields=['name','cycle_time'],filters={'name':doc.item})
# 		for i in od:
# 			cdoc=frappe.get_doc("Item",i.name)
# 			for j in cdoc.get('other_details'):
# 					if(j.machine == doc.machine and j.operation == doc.operation):
# 						doc.source_warehouse = j.source_warehouse
# 						doc.target_warehouse = j.target_warehouse
# 						doc.cycle_time = j.cycle_time
# 						break

    
# 	def before_save(self):
# 		downtime_time=0.0
# 		total=0.0   
# 		curren_time_diff=0.0
# 		for i in self.get('downtime_reason_details'):
# 			downtime_time=downtime_time+i.time
		
# 		curren_time_diff= getVal(self.time_difference)
# 		total = getVal(self.worked_time) + downtime_time
# 		if total!=self.required_time or curren_time_diff<0:
# 			if( curren_time_diff < 0):
# 				pass
# 				# frappe.throw('Worked Time must be greater than Earned Time!')
# 			# frappe.throw('Time Diffrence or Worked Time Not Matched !')

# 		rej_reasons = 0
# 		for i in self.get('item_rejection_reason'):
# 			rej_reasons += i.qty
# 		rej_qty = getVal(self.cr_qty)+getVal(self.mr_qty)
# 		# if(rej_reasons!=rej_qty):
# 		# 	frappe.throw("Mention the reasons of all rejected Items")
# 		for i in self.get('items'):
# 			self.append("raw_item",{
# 				'item':i.item,
# 			})
# 			# frappe.msgprint(str(i.item))
   
# 	def cancel_stock_entry(self,stock_entry_name):
# 		try:
# 			# Get the Stock Entry document
# 			stock_entry = frappe.get_doc("Stock Entry", stock_entry_name)

# 			# Cancel the Stock Entry
# 			stock_entry.cancel()

# 			# Save the document
# 			stock_entry.save()

# 			frappe.db.commit()
# 			frappe.msgprint("Stock Entry '{stock_entry_name}' has been cancelled successfully.")
# 		except frappe.DoesNotExistError:
# 			frappe.msgprint(f"Stock Entry '{stock_entry_name}' not found.")
# 		except Exception as e:
# 			frappe.msgprint(f"Error cancelling Stock Entry '{stock_entry_name}': {str(e)}")


# 	def amend_canceled_stock_entry(original_stock_entry_name):
# 		try:
# 			# Get the original Stock Entry document
# 			original_stock_entry = frappe.get_doc("Stock Entry", original_stock_entry_name)

# 			# Create a new Stock Entry based on the canceled one
# 			new_stock_entry = frappe.copy_doc(original_stock_entry, ignore_no_copy=True)

# 			# Make necessary modifications to the new Stock Entry
# 			# For example, you might want to change quantities, items, or other details

# 			# Save the new Stock Entry

# 			new_stock_entry.insert()

# 			frappe.db.commit()
# 			frappe.msgprint(f"Amended Stock Entry '{original_stock_entry_name}' has been created successfully: {new_stock_entry.name}")
# 		except frappe.DoesNotExistError:
# 			print(f"Stock Entry '{original_stock_entry_name}' not found.")
# 		except Exception as e:
# 			print(f"Error amending Stock Entry '{original_stock_entry_name}': {str(e)}")

# # # Usage example
# # amend_canceled_stock_entry("SE-00001")
	def getRawItemName(self, itemName):
		for i in self.get('raw_items'):
			if i.item == itemName:
				return i.raw_item
		return ""
	def getRawItemQty(self,itemName):
		for i in self.get('qty_details'):
			#considering ok qty only bcos other are rejected or need rework
			if i.item == itemName:
				return i.ok_qty
		return 0
       
	def getRawItemWareHouse(self, itemName):
		for i in self.get('raw_items'):
			if i.item == itemName:
				return i.source_warehouse
		return ""
	def getConsumables(self,itemName):
		consumables = []
		for i in self.get('consumable_details'):
			if(i.finished_item==itemName):
				consumables.append({
					"item_code": i.item if i.item is not None else "oil",
					"qty": i.qty,
					"s_warehouse": i.source_warehouse,
				})
		return consumables
          
	def getToolings(self,itemName):
		toolings = []
		for i in self.get('tooling_details'):
			if(i.finished_item==itemName):
				# frappe.msgprint(f"item: {i.tooling_item} qty: {i.qty} sware: {i.source_warehouse}")
				toolings.append({
					"item_code": i.tooling_item if i.tooling_item is not None else "insert",
					"qty": i.qty,
					"s_warehouse": i.source_warehouse,
				})
		return toolings

	def create_transfer_stock_entry(self):
		for i in self.get('rejected_items_reasons'):
			items = [
                {
                    "item_code": i.finished_item,
                    "qty": i.qty,
					"s_warehouse": self.getRawItemWareHouse(item_name),
                    "t_warehouse": i.target_warehouse,
                }
            ]
			stock_entry = frappe.get_doc({
    	    "doctype": "Stock Entry",
        	"stock_entry_type": "Material Transfer",
        	"items": items
        	})
			stock_entry.insert()
        
	def create_manufacture_stock_entry(self):
		for i in self.get('items'):
			item_name = i.item
			items = []
			items.append({
				"item_code" : self.getRawItemName(item_name),
				"qty" : self.getRawItemQty(item_name),
				"s_warehouse": self.getRawItemWareHouse(item_name),
			})
			for j in self.getConsumables(item_name):
				items.append(j)
			for j in self.getToolings(item_name):
				items.append(j)
			items.append(
				{
                "item_code": i.item,
                "qty":  self.getRawItemQty(item_name),
                "t_warehouse": i.target_warehouse,
				'is_finished_item':1
				}
			)

			stock_entry = frappe.get_doc({
    	    "doctype": "Stock Entry",
        	"stock_entry_type": "Manufacture",
        	"items": items
        	})
			stock_entry.insert()


   
            
            
            
		
# 	def create_stock_transfer(self):
# 		# if(self.stock_entry!=None):
# 		# 		self.amend_canceled_stock_entry(self.stock_entry)
    
# 		total_cost_of_item = 0
# 		items = [
# 			{
#                 "item_code": self.raw_item,
#                 "qty": self.total_qty,
#                 "s_warehouse": self.source_warehouse,
#                 "set_basic_rate_manually":1,
#                 "basic_rate": frappe.get_value("Item", self.raw_item, "valuation_rate"),
#                 "item_name": frappe.get_value("Item", self.raw_item, "item_name"),
#             }
# 		]

# 		for i in self.get('consumable_details'):
# 			total_cost_of_item+=(i.rate*i.qty)
# 			items.append(
# 				{
# 					"item_code": i.item if i.item is not None else "oil",
# 					"qty": i.qty,
# 					"s_warehouse": i.source_warehouse,
# 					"set_basic_rate_manually":1,
#         			"basic_rate": i.rate,
# 					# "rate": i.rate,
# 				}
# 			)
# 		items.append(
#     			{	
#                 "item_code": self.item ,
#                 "qty": self.total_qty,
#                 "t_warehouse": self.target_warehouse,
#                 "set_basic_rate_manually":1,
#                 "basic_rate": frappe.get_value("Item", self.item, "valuation_rate"),
#                 "item_name": frappe.get_value("Item", self.item, "item_name"),
# 				"basic_amount":total_cost_of_item+(frappe.get_value("Item", self.raw_item, "valuation_rate")*self.total_qty),
# 				'set_basic_rate_manually' :1,
# 				'is_finished_item':1
                
#             }
# 		)
		
# 		stock_entry = frappe.get_doc({
#         "doctype": "Stock Entry",
#         "stock_entry_type": "Manufacture",
#         "items": items
#         })

# 		stock_entry.insert()
# 		stock_entry.submit()
# 		self.stock_entry = stock_entry.name
# 		frappe.msgprint(str(self.stock_entry))
# 		print(f"Stock Transfer created with name: {stock_entry.name}")
		

	
# 	def before_submit(self):
# 		pass
# 		# self.create_stock_transfer()
	
# 	def on_cancel(self):
# 		self.cancel_stock_entry(self.stock_entry)
# 	def before_validation(self):
# 		if(self.stock_entry!=None):
# 				self.amend_canceled_stock_entry(self.stock_entry)
    
 

        
 
		
	
	#adding items from item table into raw table
	@frappe.whitelist()
	def update_raw_data(self,index,raw_items,item_operations):
		items = self.get('items')
 
		for ind in range(len(raw_items)):
			if(index-1==ind):
				self.append("raw_items",{
					'item':items[ind].item,
				},)
				self.append("item_operations",{
					'item':items[ind].item,
				},)
				
			else:
				self.append("raw_items",raw_items[ind])
				self.append("item_operations",item_operations[ind])
				
           
		if(len(raw_items)<index):
			self.append("raw_items",{
				'item':items[index-1].item,
			},),
			self.append("item_operations",{
				'item':items[index-1].item,
			},)
			
   
	@frappe.whitelist()
	def cycle_time_changed(self,index,qty_items):
		itemOperations = self.get('item_operations')
		if(itemOperations[index-1].operation!=None and itemOperations[index-1].machine!= None and itemOperations[index-1].cycle_time!=None and itemOperations[index-1].cycle_time!=0):
			for ind in range(len(qty_items)):
				if(index-1==ind):
					self.append("qty_details",{
						'operation': itemOperations[ind].operation,
						'cycle_time':  itemOperations[ind].cycle_time,
						'item': itemOperations[ind].item
					},)
				else:
					self.append("qty_details",qty_items[ind])
			if(len(qty_items)<index):
				self.append("qty_details",{
					'operation': itemOperations[index-1].operation,
					'cycle_time':  itemOperations[index-1].cycle_time,
					'item': itemOperations[index-1].item
				},),

	@frappe.whitelist()
	def add_rejection_reason(self,index,r_total_qty):
			itemOperations = self.get('item_operations')
     
	@frappe.whitelist()
	def calculate_rejection_qty(self):
		for i in self.get('qty_details'):
			if(getVal(i.cr_qty)!=0):
				self.append("rejected_items_reasons",{
					'finished_item': i.item,
					'rejection_type': 'CR',
					'qty': getVal(i.cr_qty),
				},),
    
			if(getVal(i.mr_qty)!=0):
				self.append("rejected_items_reasons",{
					'finished_item': i.item,
					'rejection_type': 'MR',
					'qty': getVal(i.mr_qty),
				},),
		
	@frappe.whitelist()
	def calculate_qty(self):
		t_total_qty = 0.0
		t_total_earned_time = 0.0
  
		for i in self.get('qty_details'):
			total_qty = 0.0
			total_qty +=  getVal(i.ok_qty)
			total_qty += getVal(i.cr_qty)
			total_qty += getVal(i.mr_qty)
			total_qty += getVal(i.rw_qty)
			i.total_qty = total_qty
			i.earned_min = total_qty * getVal(i.cycle_time)
			t_total_qty += getVal(i.total_qty)
			t_total_earned_time += getVal(i.earned_min)
   
		self.total_qty = t_total_qty
		self.total_earned_minutes = t_total_earned_time
		self.time_difference = self.required_time - self.total_earned_minutes
		# itemOperations = self.get('item_operations')
		# if(itemOperations[index-1].operation!=None and itemOperations[index-1].machine!= None and itemOperations[index-1].cycle_time!=None and itemOperations[index-1].cycle_time!=0):
		# 	for ind in range(len(qty_items)):
		# 		if(index-1==ind):
		# 			self.append("qty_details",{
		# 				'operation': itemOperations[ind].operation,
		# 				'cycle_time':  itemOperations[ind].cycle_time,
		# 			},)
		# 		else:
		# 			self.append("qty_details",qty_items[ind])
		
		# 	if(len(qty_items)<index):
		# 		self.append("qty_details",{
		# 			'operation': itemOperations[index-1].operation,
		# 			'cycle_time':  itemOperations[index-1].cycle_time,
		# 		},),
    
	@frappe.whitelist()
	def calculate_boring(self):
		for i in self.get('raw_items'):
			if(i.item == None or i.raw_item == None):
				return
			item = frappe.get_doc("Item",i.item)
			raw_item = frappe.get_doc("Item",i.raw_item)
			# frappe.msgprint(str(item.weight)+" "+str(raw_item.weight))
			i.boring_weight = raw_item.weight - item.weight
  

	def before_save(self):
		downtime_time=0.0
		for i in self.get('downtime_reason_details'):
			downtime_time=downtime_time+i.time
   
		total = getVal(self.total_earned_minutes)
		current_time_diff= getVal(self.time_difference)
		shift_time = getVal(self.required_time)
		if(current_time_diff<0):
				frappe.throw("Time diffrence is negetive!.You can not work more minutes than shit minutes")
		if(total+downtime_time<shift_time):
				frappe.throw("Mention down time reasons.")
		
		rtotal_cr_qty = 0.0
		rtotal_mr_qty = 0.0
		for i in self.get('qty_details'):
			rtotal_cr_qty += getVal(i.cr_qty)
			rtotal_mr_qty += getVal(i.mr_qty)
		
		r_cr_qty = 0
		r_mr_qty = 0
  
		for i  in self.get('rejected_items_reasons'):
			if(i.rejection_type=="CR"):
					r_cr_qty += i.qty
       
			if(i.rejection_type=="MR"):
					r_mr_qty += i.qty
		if(rtotal_cr_qty!=r_cr_qty or rtotal_mr_qty!=r_mr_qty):
				frappe.throw("Mention reasons of all rejected items")
			
		avail_qty = []
		sel_qty = []
		
		for i in self.get('raw_items'):
			avail_qty.append(i.available_qty)
   
		for i in self.get('qty_details'):
			sel_qty.append(i.total_qty)
   
		for i in range(0,len(avail_qty)):
			if(int(avail_qty[i])<int(sel_qty[i])):
				frappe.throw("Insuffeciaent Raw materials!")
		
		for i in self.get('consumable_details'):
			if(i.qty>i.available_qty):
				frappe.throw("Insuffeciaent consumable materials!")

		for i in self.get('tooling_details'):
			if(i.qty>i.available_qty):
				frappe.throw("Insuffeciaent tooling materials!")
		self.create_manufacture_stock_entry()
		self.create_transfer_stock_entry()


		
    
	def get_available_quantity(self,item_code, warehouse):
		filters = {
			"item_code": item_code,
			"warehouse": warehouse
		}
		fields = ["SUM(actual_qty) as available_quantity"]
		
		result = frappe.get_list("Stock Ledger Entry", filters=filters, fields=fields)
		
		if result and result[0].get("available_quantity"):
			return result[0].get("available_quantity")
		else:
			return 0

	@frappe.whitelist()
	def get_available_qty(self):
		for i in self.get('raw_items'):
			if(i.raw_item == None or i.source_warehouse == None):
				return
		 
			i.available_qty = self.get_available_quantity(i.raw_item , i.source_warehouse)
	
	@frappe.whitelist()
	def get_available_qtyOfCon(self):
		for i in self.get('tooling_details'):
			if(i.raw_item == None or i.source_warehouse == None):
				return
		 
			i.available_qty = self.get_available_quantity(i.raw_item , i.source_warehouse)
    #  available_quantity = get_available_quantity(item_code, warehouse)
	@frappe.whitelist()
	def get_available_qty_of_tooling(self):
		for i in self.get('tooling_details'):
			if(i.tooling_item == None or i.source_warehouse == None):
				return
		 
			i.available_qty = self.get_available_quantity(i.tooling_item , i.source_warehouse)
 
   
	@frappe.whitelist()
	def get_available_qty_of_consumables(self):
		for i in self.get('consumable_details'):
			if(i.item == None or i.source_warehouse == None):
				return
		 
			i.available_qty = self.get_available_quantity(i.item , i.source_warehouse)
#    get_rate_of_tooling
	@frappe.whitelist()
	def get_rate_of_tooling(self):
		for i in self.get('tooling_details'):
			if(i.tooling_item == None):
				return
			itemPrice = frappe.get_list("Item Price", filters={'item_name':i.tooling_item} , fields=['name','item_name','price_list_rate'], order_by='modified desc',limit = 1 )
			i.rate = itemPrice[0].price_list_rate
   
	def get_rate_of_consumable(self):
		for i in self.get('consumable_details'):
			if(i.item == None):
				return
			itemPrice = frappe.get_list("Item Price", filters={'item_name':i.item} , fields=['name','item_name','price_list_rate'], order_by='modified desc',limit = 1 )
			i.rate = itemPrice[0].price_list_rate