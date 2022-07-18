import ui
import uitooltip
import net
import wndMgr

class UiChangeBonus(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()

		self.index_page = -1
		self.index_slot = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "System/ChangeBonus/changebonus_0.py")
		except:
			import exception
			exception.Abort("UiChangeBonus.LoadWindow")

		self.Board = self.GetChild("board")
		self.Next = self.GetChild("next_button")
		self.Next.SetEvent(self.Page,1)
		self.Prev = self.GetChild("prev_button")
		self.Prev.SetEvent(self.Page,2)
		self.Slot_Bg = self.GetChild("slot_bonus")
		self.Slot_Page = self.GetChild("slot_page")
		self.ChangeButton = self.GetChild("ChangeButton")
		self.ChangeButton.SetEvent(self.Change)
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		self.tooltipItem.SetParent(self.Board)
		self.tooltipItem.SetInventoryItem(int(self.index_slot))
		self.tooltipItem.SetPosition(20,40)
		self.tooltipItem.Show()

	def Destroy(self):
		self.ClearDictionary()
		self.index_page = -1
		self.index_slot = 0
		self.Hide()

	def Close(self):
		net.SendChatPacket("/change_bonus_items close %s"%self.index_slot)
		self.tooltipItem.Hide()
		wndMgr.Hide(self.hWnd)

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def Change(self):
		import chat
		net.SendChatPacket("/change_bonus_items change %s %s"%(self.index_slot,self.index_page))

	def IndexSlot(self,slot):
		self.index_page = -1
		self.Page(1)
		self.index_slot = slot


	def Page(self,index):
		bones_items = self.tooltipItem.GetBones()
		if bones_items >= 0:
			if index == 1:
				self.index_page = self.index_page+1
			else:
				if self.index_page > 0:
					self.index_page = self.index_page-1
		if self.index_page > bones_items:
			self.index_page = 0

		self.Slot_Page.SetText(str(self.index_page))
		self.tooltipItem.WIndexColor(self.index_page)

	def OnUpdate(self):
		self.tooltipItem.ClearToolTip()
		self.tooltipItem.SetInventoryItem(int(self.index_slot))
		self.SetSize(230,self.tooltipItem.GetHeightW()+120)
		self.Board.SetSize(230,self.tooltipItem.GetHeightW()+120)
		self.Next.SetPosition(142+5,self.tooltipItem.GetHeightW()+49)
		self.Prev.SetPosition(70+5,self.tooltipItem.GetHeightW()+49)
		self.Slot_Bg.SetPosition(85+5,self.tooltipItem.GetHeightW()+45)
		self.ChangeButton.SetPosition(73,self.tooltipItem.GetHeightW()+75)
