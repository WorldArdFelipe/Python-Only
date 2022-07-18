import ui
import wndMgr
import player
import item
import chat
import mouseModule
import item
import uiToolTip
import net

ITEM_W = [30340,30341,30342]

class UiUsePanel(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.posicion_in = {}
		for i in xrange(0,2):
			self.posicion_in[i] = -1

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Modulo/weary/weary_windows.py")
		except:
			import exception
			exception.Abort("UiWearyPanel.LoadWindow")

		try:
			self.board = self.GetChild("board")
			self.slot = {}
			for i in xrange(0,2):
				self.slot[i] = self.GetChild("AddSlot_%d"%i)
				self.slot[i].SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
				self.slot[i].SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
				self.slot[i].SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				self.slot[i].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.acept_button = self.GetChild("acept_button")
			self.cancel_button = self.GetChild("cancel_button")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("UiWearyPanel.LoadWindow")

		self.acept_button.SetEvent(self.__OnAcept)

	def __OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			mouseModule.mouseController.DeattachObject()
			if player.SLOT_TYPE_INVENTORY != attachedSlotType:
				return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			count = player.GetItemCount(attachedInvenType, attachedSlotPos)
				
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)
			itemType = item.GetItemType()

		if selectedSlotPos == 0 and item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType:
			self.slot[selectedSlotPos].ClearSlot(selectedSlotPos)
			self.slot[selectedSlotPos].SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
			self.posicion_in[selectedSlotPos] = attachedSlotPos

		if selectedSlotPos == 1 and itemVNum == ITEM_W[0] or itemVNum == ITEM_W[1] or itemVNum == ITEM_W[2]:		
			self.slot[selectedSlotPos].ClearSlot(selectedSlotPos)
			self.slot[selectedSlotPos].SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
			self.posicion_in[selectedSlotPos] = attachedSlotPos

	def __OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			mouseModule.mouseController.DeattachObject()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			count = player.GetItemCount(attachedInvenType, attachedSlotPos)
				
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)
			itemType = item.GetItemType()

		else:
			self.posicion_in[selectedSlotPos] = -1
			self.slot[selectedSlotPos].ClearSlot(selectedSlotPos)

		if selectedSlotPos == 0 and item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType:
			self.slot[selectedSlotPos].ClearSlot(selectedSlotPos)
			self.slot[selectedSlotPos].SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
			self.posicion_in[selectedSlotPos] = attachedSlotPos

		if selectedSlotPos == 1 and itemVNum == ITEM_W[0] or itemVNum == ITEM_W[1] or itemVNum == ITEM_W[2]:
			self.slot[selectedSlotPos].ClearSlot(selectedSlotPos)
			self.slot[selectedSlotPos].SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
			self.posicion_in[selectedSlotPos] = attachedSlotPos

	

	def OverInItem(self, slotIndex):
		if (mouseModule.mouseController.isAttached()):
			return
			
		if (self.tooltipItem != 0):
			self.tooltipItem.SetInventoryItem(self.posicion_in[slotIndex])
			
	def OverOutItem(self):
		if (self.tooltipItem != 0):
			self.tooltipItem.HideToolTip()

	def __OnAcept(self):
		if player.GetItemCount(self.posicion_in[1]) == 0:
			self.posicion_in[1] = -1
			self.slot[1].ClearSlot(0)	

		for i in xrange(0,2):
			if self.posicion_in[i] == -1:
				self.Chat_W("[Error]Los slots estan vacios.")
				return

		net.SendChatPacket("/use_items r_w %d %d"%(self.posicion_in[0],self.posicion_in[1]))

	def RefreshPanel(self):
		self.slot[1].SetItemSlot(1, player.GetItemIndex(self.posicion_in[1]), player.GetItemCount(self.posicion_in[1]))
		if player.GetItemCount(self.posicion_in[1]) == 0:
			self.slot[1].ClearSlot(0)	
			self.posicion_in[1] = -1
	
	def Chat_W(self,arg):
		chat.AppendChat(1,arg)

	def Close(self):
		wndMgr.Hide(self.hWnd)


class UiUsePanelSlot(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.slots = {
		'0' : '0',
		'1' : '0',
		'2' : '0',
		'3' : '0',
		'4' : '0',
		'5' : '0',
		'6' : '0',
		'10' : '0',
		}

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Modulo/weary/weary_slot.py")
		except:
			import exception
			exception.Abort("UiUsePanelSlot.LoadWindow")

		self.wndEquip  = self.GetChild("EquipmentSlot")
		self.wndEquip .SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

	def SelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			return
		else:
			net.SendChatPacket("/use_items s_w %d"%selectedSlotPos)	

	def UseItem(self,vnum,slotNumber):
		self.slots[slotNumber] = vnum
		self.wndEquip.SetItemSlot(int(slotNumber), int(vnum), 0)

	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddUseItemInventary(int(self.slots[str(slotIndex)]))

	def UseItemRefresh(self,pos):
		self.slots[pos] = "0"
		self.wndEquip.ClearSlot(int(pos))

	def Close(self):
		self.Hide()