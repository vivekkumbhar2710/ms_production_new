quit

# Copyright (c) 2023, Nishant Shingate and contributors
# For license information, please see license.txt 
import frappe
from frappe.model.document import Document
import json

def getVal(val):
        return val if val is not None else 0

class Production(Document):
	stock_entries = []
	@frappe.whitelist()
	def get_od(self):
		pass


	@frappe.whitelist()
	def consumable_amount(self):
		for i in self.get('consumable_details'):
			i.amount  = getVal(i.qty) * getVal(i.rate)

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
				p= i.ok_qty
				# return i.ok_qty
		return p if p else 0
       
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
					"item_code" : self.getRawItemName(i.finished_item),
                    "qty": i.qty,
					"s_warehouse": self.getRawItemWareHouse(i.finished_item),
                    "t_warehouse": i.target_warehouse,
                }
            ]
			stock_entry = frappe.get_doc({
    	    "doctype": "Stock Entry",
        	"stock_entry_type": "Material Transfer",
        	"items": items,
			"production_entry": self.name,
			"company":self.company,
        	})
			stock_entry.insert()
			stock_entry.submit()
		
        
	def create_manufacture_stock_entry(self):
		for i in self.get('items'):
			wedges_for_item =0
			item_name = i.item
			items = []
			additional_costs= []
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

			for k in self.get('qty_details'):
				if k.item == i.item:
					wedges_for_item= wedges_for_item+k.wages_per_item

			additional_costs.append(
				{
                "expense_account": self.expense_account_for_wages,
                "description":  "Operation Cost",
                "amount": wedges_for_item,

				}
			)

			stock_entry = frappe.get_doc({"doctype": "Stock Entry","stock_entry_type": "Manufacture","items": items,"additional_costs":additional_costs,"production_entry": self.name,"company":self.company,})
		

			stock_entry.insert()
			stock_entry.submit()

	@frappe.whitelist()
	def set_warehouse_in_item(self):
		for mom in self.get('items'):
			mom.target_warehouse = frappe.get_value("Machine Shop Setting",self.company,"target_warehouse_p")
	
	#adding items from item table into raw table
	@frappe.whitelist()
	def update_raw_data(self,index,raw_items,item_operations):
		self.set_warehouse_in_item()
		items = self.get('items')
		s___w = frappe.get_value("Machine Shop Setting",self.company,"source_warehouse_p")
		for ind in range(len(raw_items)):
			if(index-1==ind):
				self.append("raw_items",{
					'item':items[ind].item,
					'raw_item' : frappe.get_value("Item",items[ind].item,"raw_material"),
					'item_name': frappe.get_value("Item",items[ind].item,"item_name"),
					'raw_item_name': frappe.get_value("Item",(frappe.get_value("Item",items[ind].item,"raw_material")),"item_name"),
					'source_warehouse': s___w ,
					"available_qty" : self.get_available_quantity(frappe.get_value("Item",items[ind].item,"raw_material"),s___w),
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
				'raw_item' : frappe.get_value("Item",items[index-1].item,"raw_material"),
				'item_name': frappe.get_value("Item",items[index-1].item,"item_name"),
				'raw_item_name': frappe.get_value("Item",(frappe.get_value("Item",items[index-1].item,"raw_material")),"item_name"),
				'source_warehouse': frappe.get_value("Machine Shop Setting",self.company,"source_warehouse_p"),
				"available_qty" : self.get_available_quantity(frappe.get_value("Item",items[index-1].item,"raw_material"),s___w)
				
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
		ms_setting = frappe.get_doc("Machine Shop Setting",self.company)
		for i in self.get('qty_details'):
			if(getVal(i.cr_qty)!=0):
				self.append("rejected_items_reasons",{
					'finished_item': i.item,
					'rejection_type': 'CR',
					'qty': getVal(i.cr_qty),
					'target_warehouse': ms_setting.cr_warehouse_p,
					'job_order':i.job_order,
					'operation':i.operation,

				},),
    
			if(getVal(i.mr_qty)!=0):
				self.append("rejected_items_reasons",{
					'finished_item': i.item,
					'rejection_type': 'MR',
					'qty': getVal(i.mr_qty),
					'target_warehouse': ms_setting.mr_warehouse_p,
					'job_order':i.job_order,
					'operation':i.operation,
				},),

			if(getVal(i.rw_qty)!=0):
				self.append("rejected_items_reasons",{
					'finished_item': i.item,
					'rejection_type': 'RW',
					'qty': getVal(i.rw_qty),
					'target_warehouse': ms_setting.rw_warehouse_p,
					'job_order':i.job_order,
					'operation':i.operation,
				},),
		self.calculate_qty()
		
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
   
		self.total_earned_minutes = t_total_earned_time
		self.time_difference = self.required_time - self.total_earned_minutes
		self.calculet_self_total_qty()
		self.validate_ok_qty()

	@frappe.whitelist()
	def calculet_self_total_qty(self):
		total_total_qty=0
		for item in self.get('items'):
			for ops_item in self.get('qty_details'):
				if item.item == ops_item.item:
					total_total_qty= total_total_qty + ops_item.total_qty
					break
		self.total_qty = total_total_qty

	@frappe.whitelist()
	def validate_ok_qty(self):
		for akki in self.get('qty_details'):
			for janu in self.get('qty_details'):
				if akki.idx < janu.idx and str(akki.job_order)==str(janu.job_order) and akki.item == janu.item:
					if akki.ok_qty < janu.total_qty:
						frappe.throw(f'Total Qty of operation {janu.operation} for item {janu.item} is should not be greater than the "Ok Qty" of operation {akki.operation}')



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
    
		self.validate_required_time_per_row_material()
		self.validate_qty_on_earned_min()

	def before_submit(self):
		self.setdatainitemfield()
		

    	# pass
	def on_submit(self):
		self.create_manufacture_stock_entry()
		self.create_transfer_stock_entry()
		
		pass
		

		
    
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
   
   
	@frappe.whitelist()
	def set_filters_IOM(self):
		# frappe.throw("hiiii")
		final_list =[]
		result_list =[]
		for d in self.get('items'):
			disk =frappe.get_all('Material Cycle Time', filters={'item':d.item ,'company':self.company} ,fields=['name',], order_by='modified desc',limit = 1 )
			if disk:
				for dk in disk:
					param=frappe.get_all('Machine Item', filters={'parent':dk.name} ,fields=['machine','operation'])
					for p in param:
						final_list.append(p.machine)
						result_list.append(p.operation)
			elif d.item:
				frappe.msgprint(f'There is no item {d.item} prent in "Material Cycle Time"')
		return final_list,result_list

	@frappe.whitelist()
	def set_filters_for_items(self):
		final_listed =[]
		for d in self.get('job_order'):
			final_listed.append(frappe.get_value("Job Order",str(d.job_order),"item"))
		return final_listed


	@frappe.whitelist()
	def set_cycle_time(self):
		# for do in self.get('items'):
		for v in self.get('item_operations'):
			v.cycle_time=0
			demo =frappe.get_all('Material Cycle Time', filters={'item':v.item ,'company':self.company ,"from_date" :["<=",self.date]} ,fields=['name',], order_by='from_date desc',limit = 1 )
			if demo:
				for t in demo:
					kaju=frappe.get_all('Machine Item', filters={'parent':t.name,'operation':v.operation} ,fields=['cycle_time'])
					if kaju:
						v.cycle_time=kaju[0].cycle_time
					elif v.operation :
						frappe.throw(f'There is no Operation "{v.operation}" in "Material Cycle Time" for item {v.item}')
			else:
				frappe.throw(f'There is no item {v.item} present in "Material Cycle Time" for Company {self.company}')





	@frappe.whitelist()
	def validate_required_time_per_row_material(self):
		p=0
		variable =0
		total_time =0
		for m in self.get('raw_items'):
			
			if not m.required_time:
				variable = 1
		if variable == 0:
			for f in self.get('raw_items'):
				if f.required_time:
					total_time=total_time+f.required_time
			if total_time != self.required_time:
				p=1

		if p==1:
			frappe.throw(f'Total required time per raw item  for all "Row Items" will be equal to {self.required_time} ')


	@frappe.whitelist()
	def validate_qty_on_earned_min (self):
		# frappe.throw("hi.....")
		for fo in self.get('raw_items'):
			total_earn_time = 0
			for xo in self.get('qty_details'):
				if xo.item == fo.item:
					total_earn_time = total_earn_time + xo.earned_min
			
			if  total_earn_time > fo.required_time:
				frappe.throw(f'Earned Min can not be more than { fo.required_time} for item {fo.item}')



	@frappe.whitelist()
	def calculate_total_weges(self):
		weges_per_min_of_op = 0
		# weges_per_min_of_su = 0
		total_weges =0
		cor = frappe.get_all("Wages Master",filters = {"Employee": self.operator},fields = ["name"])
		if cor:
			cos = frappe.get_all("Child Wages Master",filters = {"parent": cor[0].name ,"from_date": ['<=',self.date]},fields = ["wages_per_hour"], order_by = 'from_date DESC')
			if cos:
				weges_per_min_of_op = (cos[0].wages_per_hour)/60

		weges_per_min = weges_per_min_of_op 
		for g in self.get("qty_details"):
			g.wages_per_item = weges_per_min* g.earned_min

		for gpp in self.get("qty_details"):
			total_weges = total_weges + gpp.wages_per_item

		self.wages = total_weges
				



	@frappe.whitelist()
	def after_select_job_order(self):
		word = self.get('items')
		word.clear()
		cource = self.get('raw_items')
		cource.clear()
		conquer = self.get('item_operations')
		conquer.clear()
		fought = self.get('qty_details')
		fought.clear()

		for d in self.get('job_order'):
			item_code_for_job =frappe.get_value("Job Order",str(d.job_order),"item")
			target =frappe.get_value("Job Order",str(d.job_order),"target_warehouse")

			self.append("items",{
					'job_order': str(d.job_order) ,
					'item': item_code_for_job,
					'item_name': frappe.get_value("Item",item_code_for_job,"item_name"),
					'target_warehouse': target if target else frappe.get_value("Machine Shop Setting",self.company,"target_warehouse_p")
				},),
			
			ps = (frappe.get_value("Job Order",(d.job_order),"production_schedule"))
			mct =(frappe.get_value("Production Schedule",ps,"material_cycle_time"))
			raw_item = frappe.get_value("Material Cycle Time" ,mct,"raw_item")

			source = frappe.get_value("Job Order",str(d.job_order),"source_warehouse")
			self.append("raw_items",{
					'job_order': str(d.job_order) ,
					'item': item_code_for_job,
					'item_name': frappe.get_value("Item",item_code_for_job,"item_name"),
					'raw_item': raw_item,
					'raw_item_name': frappe.get_value("Item",raw_item,"item_name"),
					'source_warehouse': source if source else frappe.get_value("Machine Shop Setting",self.company,"source_warehouse_p"),
					'boring_weight': frappe.get_value("Item",str(raw_item),"weight") -frappe.get_value("Item",str(item_code_for_job),"weight"),
					'available_qty' : self.get_available_quantity(raw_item, source)
				},),
			vikas = frappe.get_all("Machine Item",filters = {"parent": mct },fields = ["operation","cycle_time"], order_by = 'idx ASC')
			for desh in vikas:
				self.append("item_operations",{
						'job_order': str(d.job_order) ,
						'item': item_code_for_job,
						'operation': desh.operation,
						'cycle_time': desh.cycle_time,
					},),

				self.append("qty_details",{
						'job_order': str(d.job_order) ,
						'item': item_code_for_job,
						'operation': desh.operation,
						'cycle_time': desh.cycle_time,
					},),

	@frappe.whitelist()
	def setdatainitemfield(self):
		
		list_items = []
		for item in self.get('items'):
			list_items.append(item.item_name)
		# frappe.throw(list_items)
		self.do_not_delete =str(list_items)


