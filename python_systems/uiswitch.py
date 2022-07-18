import ui
import app
import net
import chat
import wndMgr
import time
import uiToolTip
import mouseModule
import player
import item
import get_attr_items
import grp

class SwitchAutomatic(ui.ScriptWindow):

	VNUM_ITEM_CHANGE = 49390
	SPEED_CHANGE = 0.3
	
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		self.get_affect = uiToolTip.ItemToolTip().AFFECT_DICT
		self.info_get_bonus = get_attr_items.info_get_bonus

		self.elements = {}

		self.list_get_bonus_id = []
		self.list_get_value_bonus_repeat = []

		self.list_get_bonus_id_m_h = [[72,10,40],[71,5,20]] #Media - Habilidad [id,give_value,max_value]

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self):
		self.Show()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "system/switchwindows.py")
		except:
			import exception
			exception.Abort("SwitchAutomatic.LoadWindow.LoadObject")

		self.TitleBar = self.GetChild("TitleBar")

		self.elements["slot_active_item"] = 0
		self.elements["func_start_automatic"] = False

		for i in xrange(1,6):

			self.elements["m_h_activate_item_%d"%i] = -1

			self.elements["id_page_bonus_%d"%i] = -1
			self.elements["id_value_bonus_%d"%i] = -1

			self.elements["id_bonus_select_%d"%i] = -1
			self.elements["value_bonus_select_%d"%i] = -1

			self.elements["thinboard_bonus_%d"%i] = self.GetChild("thinboard_bonus_%d"%i)
			self.elements["bonus_text_%d"%i] = self.GetChild("thinboard_bonus_line_%d"%i)
			self.elements["slot_board_%d"%i] = self.GetChild("slot_bonus_%d"%i)
			self.elements["slot_board_%d"%i].Hide()
			self.elements["slot_edit_%d"%i] = self.GetChild("slot_page_%d"%i)
			self.elements["button_change_bonus_%d"%i] = self.GetChild("button_change_%d"%i)
			self.elements["button_change_bonus_%d"%i].SetEvent(self.SelectBonusValor,i)
			self.elements["button_change_bonus_%d"%i].Hide()
			self.elements["button_next_bonus_%d"%i] = self.GetChild("next_bonus_%d"%i)
			self.elements["button_next_bonus_%d"%i].SetEvent(self.SelectBonus,i,1)
			self.elements["button_next_bonus_%d"%i].Hide()
			self.elements["button_prev_bonus_%d"%i] = self.GetChild("prev_button_%d"%i)
			self.elements["button_prev_bonus_%d"%i].SetEvent(self.SelectBonus,i,0)
			self.elements["button_prev_bonus_%d"%i].Hide()

		self.elements["slot_item"] = self.GetChild("ItemSlot")

		self.elements["windows_buttons"] = self.GetChild("window_buttons")

		self.elements["button_change"] = self.GetChild("button_change")

		self.elements["id_slot_items"]=None
		self.elements["button_change"].SetEvent(self.ChangeBonus)

		self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))


	def SelectBonusValor(self,index):

		if self.elements["func_start_automatic"] == True:
			return

		if self.elements["id_page_bonus_%d"%index] == -1:
			return

		if self.elements["m_h_activate_item_%d"%index] == -1:
			self.elements["id_value_bonus_%d"%index] += 1
			if self.elements["id_value_bonus_%d"%index] >= len(self.list_get_bonus_id[self.elements["id_page_bonus_%d"%index]][2]):
				self.elements["id_value_bonus_%d"%index] = 0
		else:

			for i in xrange(0,len(self.list_get_bonus_id_m_h)):
				if self.elements["id_bonus_select_%d"%index] == self.list_get_bonus_id_m_h[i][0]:
					self.elements["id_value_bonus_%d"%index] = self.elements["id_value_bonus_%d"%index] + self.list_get_bonus_id_m_h[i][1]
					if self.elements["id_value_bonus_%d"%index] > self.list_get_bonus_id_m_h[i][2]:
						self.elements["id_value_bonus_%d"%index] -= self.list_get_bonus_id_m_h[i][2]

		self.LoadTextBonus(index)

	def SelectBonus(self,index,page):
		if self.elements["func_start_automatic"] == True:
			return
		#prev
		if page == 0:
			self.elements["id_page_bonus_%d"%index] -= 1
			if self.elements["id_page_bonus_%d"%index] <= 0:
				self.elements["id_page_bonus_%d"%index] = 0

		#next
		else:

			if self.elements["m_h_activate_item_%d"%index] == -1:
				list_bonus = self.list_get_bonus_id
			else:
				list_bonus = self.list_get_bonus_id_m_h

			self.elements["id_page_bonus_%d"%index] += 1
			if self.elements["id_page_bonus_%d"%index] >= len(list_bonus):
				self.elements["id_page_bonus_%d"%index] -= 1

		self.elements["id_value_bonus_%d"%index] = 0

		self.LoadTextBonus(index)

	def LoadTextBonus(self,index):
		if self.elements["m_h_activate_item_%d"%index] == -1:
			id_bonus = self.list_get_bonus_id[self.elements["id_page_bonus_%d"%index]][1]
			value_bonus = self.list_get_bonus_id[self.elements["id_page_bonus_%d"%index]][2][self.elements["id_value_bonus_%d"%index]]
		else:
			id_bonus = self.list_get_bonus_id_m_h[self.elements["id_page_bonus_%d"%index]][0]
			value_bonus = self.elements["id_value_bonus_%d"%index]

		self.elements["bonus_text_%d"%index].SetText(str(self.get_affect[id_bonus](int(value_bonus))))

		self.elements["id_bonus_select_%d"%index] = int(id_bonus)
		self.elements["value_bonus_select_%d"%index] = int(value_bonus)

	def func_set_pos_item(self,attachedSlotPos):
		itemIndex = player.GetItemIndex(attachedSlotPos)
		itemCount = player.GetItemCount(attachedSlotPos)
		item.SelectItem(itemIndex)
		itemType = item.GetItemType()
		if item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType :
			self.elements["id_slot_items"]=attachedSlotPos
			self.elements["slot_item"].SetItemSlot(1, itemIndex, 1)
			self.func_elements_item("ADD_ITEM")

	def func_check_item_slot(self):
		if self.elements["id_slot_items"]==None:
			chat.AppendChat(1,"[ChangeAutomatic] Coloque un item en el slot.")
			return False

		return True

	def func_check_bonus_select_repeat(self):
		count_bonus_repeat,list_bonus_repeat,get_bonus_repeat = 0,[],[]

		for i in xrange(1,6):
			if self.elements["id_bonus_select_%d"%i] != -1:
				list_bonus_repeat.append([self.elements["id_bonus_select_%d"%i]])

		count = 0
		for i in list_bonus_repeat:
			if i not in get_bonus_repeat:
				get_bonus_repeat.append(list_bonus_repeat[count])
			else:
				count_bonus_repeat = 1
			count += 1

		return count_bonus_repeat

	def func_select_all_bonus(self):
		count_bonus_selects = 0

		for i in xrange(1,6):
			if self.elements["id_bonus_select_%d"%i] != -1:
				count_bonus_selects += 1

		return count_bonus_selects

	def func_slots_activate(self):
		return self.elements["slot_active_item"]	

	def func_get_bonus_select(self,index):
		if self.elements["id_bonus_select_%d"%index] == -1:
			return False
		return True

	def func_get_id_bonus(self,index):
		return int(self.elements["id_bonus_select_%d"%index])

	def func_get_value_bonus(self,index):
		return int(self.elements["value_bonus_select_%d"%index])

	def func_check_select_bonus(self):
		count_bonus_actives_slots = self.elements["slot_active_item"]
		
		if count_bonus_actives_slots <= 0:
			chat.AppendChat(1,"[ChangeAutomatic] El item no contiene bonus.")
			return False
		
		#All bonus slot select
		if self.func_select_all_bonus() <= 0:
			chat.AppendChat(1,"[ChangeAutomatic] Seleccione al menos 1 bonus")
			return False

		#Bonus select repeat
		if self.func_check_bonus_select_repeat() == 1:
			chat.AppendChat(1,"[ChangeAutomatic] No puede tener el mismo bonus en otro slot.")
			return False

		return True

	def ChangeBonus(self):
		if self.func_check_item_slot():
			if self.func_check_select_bonus():
				if self.elements["func_start_automatic"] == False:
					self.elements["func_start_automatic"] = True
					self.func_elements_item("START")
					self.StartEvent()
				else:
					self.func_elements_item("STOP")
					#self.elements["func_start_automatic"] = False


	def StartEvent(self):
		val,bon = {},{}

		if self.elements["func_start_automatic"] == True:
			val[1], bon[1] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 0) 
			val[2], bon[2] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 1) 
			val[3], bon[3] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 2) 
			val[4], bon[4] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 3) 
			val[5], bon[5] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 4) 

			count = 0

			for a in xrange(1,self.func_slots_activate()+1):
				if self.func_get_bonus_select(a) == True:
					for i in xrange(1,self.func_slots_activate()+1):
						if (val[i] == self.func_get_id_bonus(a) and bon[i] >= self.func_get_value_bonus(a)):
							count += 1

			if count == self.func_select_all_bonus():
				self.func_elements_item("FINISH")
				return

			if player.GetItemCountByVnum(int(self.VNUM_ITEM_CHANGE)) <= 0:
				self.Close()
				return

			self.WaitingDelay = WaitingDialog()
			self.WaitingDelay.Open(float(self.SPEED_CHANGE))
			self.WaitingDelay.SAFE_SetTimeOverEvent(self.StartEvent)

			net.SwitchChange()

	def get_item_type(self,index):
		itemIndex = player.GetItemIndex(self.elements["id_slot_items"])
		item.SelectItem(itemIndex)
		if item.IsWearableFlag(item.WEARABLE_BODY):	
			return self.get_valor_body(index)
		elif  item.IsWearableFlag(item.WEARABLE_HEAD):
			return self.get_valor_head(index)
		elif item.IsWearableFlag(item.WEARABLE_FOOTS):
			return self.get_valor_foots(index)
		elif item.IsWearableFlag(item.WEARABLE_WRIST):
			return self.get_valor_wrist(index)
		elif item.IsWearableFlag(item.WEARABLE_WEAPON):
			return self.get_valor_weapon(index)
		elif item.IsWearableFlag(item.WEARABLE_NECK):
			return self.get_valor_neck(index)
		elif item.IsWearableFlag(item.WEARABLE_EAR):
			return self.get_valor_ear(index)
		elif item.IsWearableFlag(item.WEARABLE_SHIELD):
			return self.get_valor_shield(index)

		return -1
	
	def func_elements_item(self,status):
		if status == "ADD_ITEM":

			self.get_list_func()

			val,bon = {},{}

			val[1], bon[1] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 0) #(itemposition, atrribute)
			val[2], bon[2] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 1) #(itemposition, atrribute)
			val[3], bon[3] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 2) #(itemposition, atrribute)
			val[4], bon[4] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 3) #(itemposition, atrribute)
			val[5], bon[5] = player.GetItemAttribute((int(self.elements["id_slot_items"])), 4) #(itemposition, atrribute)

			for i in xrange(1,6):
				if val[i] == 0:
					self.elements["button_next_bonus_%d"%i].Hide()
					self.elements["button_prev_bonus_%d"%i].Hide()
					self.elements["button_change_bonus_%d"%i].Hide()
				else:
					self.elements["button_next_bonus_%d"%i].Show()
					self.elements["button_prev_bonus_%d"%i].Show()
					self.elements["button_change_bonus_%d"%i].Show()


					if val[i] == self.list_get_bonus_id_m_h[0][0] or val[i] == self.list_get_bonus_id_m_h[1][0]:
						self.elements["m_h_activate_item_%d"%i] = val[i]
					else:
						self.elements["m_h_activate_item_%d"%i] = -1

					self.elements["slot_active_item"] += 1


				self.elements["windows_buttons"].Show()

		elif status == "DELETE_ITEMS":
			for i in xrange(1,6):
				self.elements["button_next_bonus_%d"%i].Hide()
				self.elements["button_prev_bonus_%d"%i].Hide()
				self.elements["button_change_bonus_%d"%i].Hide()
				self.elements["bonus_text_%d"%i].SetText("~")
				self.elements["id_page_bonus_%d"%i] = -1
				self.elements["id_value_bonus_%d"%i] = -1
				self.elements["slot_active_item"] = 0
				self.elements["id_bonus_select_%d"%i] = -1
				self.elements["value_bonus_select_%d"%i] = -1
				self.elements["m_h_activate_item_%d"%i] = -1
				self.elements["func_start_automatic"] = False
				self.elements["bonus_text_%d"%i].SetPackedFontColor(self.NORMAL_COLOR)

			self.list_get_bonus_id = []
			self.elements["id_slot_items"]=None

		elif status == "START":
			self.elements["button_change"].SetText("Stop")
			for i in xrange(1,6):
				self.elements["bonus_text_%d"%i].SetPackedFontColor(self.NORMAL_COLOR)

		elif status == "FINISH":
			chat.AppendChat(1,"[ChangeAutomatic]Bonus Agregado exitosamente.")
			self.elements["button_change"].SetText("Start")
			for i in xrange(1,6):
				self.elements["bonus_text_%d"%i].SetPackedFontColor(self.POSITIVE_COLOR)

			self.elements["func_start_automatic"] = False

		elif status == "STOP":
			self.elements["button_change"].SetText("Start")
			self.elements["func_start_automatic"] = False


	def get_list_func(self):
		count,count1 = 1,0
		self.list_get_bonus_id = []

		for a in xrange(1,len(self.get_affect)+1):
			if  (a <= 25) or (a >= 27 and a <= 39) or a == 41 or (a >= 43 and a <= 45) or (a >= 48 and a <= 49) or a == 53 or a == 92:
				if self.get_item_type(count) != 0:
					self.list_get_bonus_id.append([count1,a,self.func_get_repeat_bonus(count)])
					count1 += 1
				count += 1

	def func_get_repeat_bonus(self,count):
		get_bonus = [self.get_valor_bonus(count,1),self.get_valor_bonus(count,2),self.get_valor_bonus(count,3),self.get_valor_bonus(count,4),self.get_valor_bonus(count,5)]
		list_new_bonus = []

		for key in get_bonus:
			if key not in list_new_bonus:
				list_new_bonus.append(key)	

		return  list_new_bonus

	def get_valor_bonus(self,index,valor): #linea - columna
		if valor > 5:
			return
		index = index - 1
		valor = valor - 1
		if valor < 0:
			return
		if index < 0:
			return
		if index > 0:
			index = index*13
		return int(self.info_get_bonus[index+valor])

	def get_valor_weapon(self,index,weapon_index = 5):
		if index < 0:
			return
		if index > 1:
			weapon_index = weapon_index + (13*(index-1))
		return int(self.info_get_bonus[weapon_index])

	def get_valor_body(self,index,body_index = 6):
		if index < 0:
			return
		if index > 1:
			body_index = body_index + (13*(index-1))
		return int(self.info_get_bonus[body_index])

	def get_valor_wrist(self,index,wrist_index = 7):
		if index < 0:
			return
		if index > 1:
			wrist_index = wrist_index + (13*(index-1))

		return int(self.info_get_bonus[wrist_index])

	def get_valor_foots(self,index,foots_index = 8):
		if index < 0:
			return
		if index > 1:
			foots_index = foots_index + (13*(index-1))
		return int(self.info_get_bonus[foots_index])

	def get_valor_neck(self,index,neck_index = 9):
		if index < 0:
			return
		if index > 1:
			neck_index = neck_index + (13*(index-1))
		return int(self.info_get_bonus[neck_index])

	def get_valor_head(self,index,head_index= 10):
		if index < 0:
			return
		if index > 1:
			head_index = head_index + (13*(index-1))
		return int(self.info_get_bonus[head_index])

	def get_valor_shield(self,index,shield_index = 11):
		if index < 0:
			return
		if index > 1:
			shield_index = shield_index + (13*(index-1))
		return int(self.info_get_bonus[shield_index])

	def get_valor_ear(self,index,ear_index = 12):
		if index < 0:
			return
		if index > 1:
			ear_index = ear_index + (13*(index-1))
		return int(self.info_get_bonus[ear_index])

	def Close(self):
		self.func_elements_item("DELETE_ITEMS")
		net.SwitchClose()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE


class WaitingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Show()		

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)
		
	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			return
		
	def OnPressExitKey(self):
		self.Close()
		return TRUE