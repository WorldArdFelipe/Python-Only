import ui
import uiToolTip
import mouseModule
import player
import item
import chat
import net
import localeInfo
import wndMgr
import grp
import ime
import nonplayer
ITEM_LIST=item.GetNames()


class UiCofresLoader(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.curPage 	= 1
		self.MaxPage 	= 2
		self.search_vnum=0
		self.items 		=[]
		self.s_n 		={}
		self.vnum 		= None
		self.index 		= None
		self.pos 		= None
		self.slotpos 	= None

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "System/Cofres/boxcofres_new.py")
		except:
			import exception
			exception.Abort("UiCofresLoader.LoadWindow")

		try:
			self.bg 			= self.GetChild("board")
			self.slot 			= self.GetChild("ItemSlot")
			self.item_name 		= self.GetChild("ItemName")
			self.item_name_edit = self.GetChild("ItemNameEdit")
			self.aceptar 		= self.GetChild("AceptButton")
			self.abrir 			= self.GetChild("AbrirButton")
			self.limpiar 		= self.GetChild("LimpiarButton")
			self.scrollbar 		=  self.GetChild("contentScrollbar")
			self.scrollbar.SetScrollEvent(ui.__mem_func__(self.OnScrollResultList))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("UiCofresElements.LoadWindow")

		self.Box = UiCofresBox()
		self.Box.Open(self.bg,28,210)
		self.Box.Show()

		self.slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))

		self.limpiar.SetEvent(self.__OnLimpiar)
		self.aceptar.SetEvent(self.__OnAcept)
		self.abrir.SetEvent(self.__OnAbrir)

		self.s_n["list_names"] = DropDown(self)
		self.s_n["list_names"].OnChange=self.OnChange
		self.s_n["list_names"].SetPosition(0,0)
		self.s_n["list_names"].Hide()

		self.s_n["nameEdit"]=self.item_name_edit
		self.s_n["nameEdit"].OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.s_n["nameEdit"].SetReturnEvent(ui.__mem_func__(self.__OnHideList))
		self.s_n["nameEdit"].SetEscapeEvent(ui.__mem_func__(self.__OnHideList))

	def Information(self,type,vnums,counts):
		self.items.append([int(type),int(vnums),int(counts)])

	def Page(self):
		self.Box.Hide()		
		self.Box.ClearList()

		for a in xrange(min(self.MaxPage, len(self.items) - self.curPage * self.MaxPage +self.MaxPage)):
			type_item 	= self.items[a + (self.curPage - 1)*self.MaxPage][0]
			vnum_item 	= self.items[a + (self.curPage - 1)*self.MaxPage][1]
			count_item 	= self.items[a + (self.curPage - 1)*self.MaxPage][2]
			self.Box.SetContent(type_item,vnum_item,count_item,a)
			self.Box.Show()


	def __OnSelectEmptySlot(self, selectedSlotPos):
		if self.search_vnum != 0:
			chat.AppendChat(1,"[SearchBox] No puede colocar items si tiene la busqueda por nombre.")
			return

		self.index,self.pos=None,None
		self.__OnLimpiar()
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			mouseModule.mouseController.DeattachObject()
			if player.SLOT_TYPE_INVENTORY != attachedSlotType:
				return

		item.SelectItem(player.GetItemIndex(attachedSlotPos))

		if app.ENABLE_SEARCH_BOX_GACHA_SYSTEM:
			if item.ITEM_TYPE_TREASURE_BOX == item.GetItemType() or item.ITEM_TYPE_GIFTBOX == item.GetItemType() or item.ITEM_TYPE_GACHA == item.GetItemType():
				self.slot.ClearSlot(selectedSlotPos)
				self.slot.SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
				self.index = player.GetItemIndex(attachedSlotPos)
				self.pos = attachedSlotPos
				self.slotpos=selectedSlotPos
				self.vnum = player.GetItemIndex(attachedSlotPos)
				self.item_name.SetText(item.GetItemName())

				self.s_n["nameEdit"].Hide()
				self.search_vnum = 0
				self.__OnHideList()
		else:
			if item.ITEM_TYPE_TREASURE_BOX == item.GetItemType() or item.ITEM_TYPE_GIFTBOX == item.GetItemType():
				self.slot.ClearSlot(selectedSlotPos)
				self.slot.SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
				self.index = player.GetItemIndex(attachedSlotPos)
				self.pos = attachedSlotPos
				self.slotpos=selectedSlotPos
				self.vnum = player.GetItemIndex(attachedSlotPos)
				self.item_name.SetText(item.GetItemName())

				self.s_n["nameEdit"].Hide()
				self.search_vnum = 0
				self.__OnHideList()

	def __OnSelectItemSlot(self, selectedSlotPos):
		self.__OnLimpiar()	

	def OnChange(self):
		self.search_vnum=self.s_n["list_names"].DropList.GetSelectedItem().value
		name=""
		for it in ITEM_LIST:
			if int(it["vnum"]) == self.search_vnum:
				name=it["name"]
				break
		self.s_n["nameEdit"].SetText(str(name))
		self.s_n["list_names"].Clear()
		self.s_n["list_names"].Hide()
		self.pos = None
		ime.SetCursorPosition(len(name)+1)

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.s_n["nameEdit"])
		val=self.s_n["nameEdit"].GetText()
		if len(val) >0:
			self.s_n["list_names"].Clear()
			f=0
			n=[]
			for it in ITEM_LIST:
				vnum,name=it["vnum"],it["name"]
				if f==10:
					break
				if len(name)>=len(val) and name[:len(val)].lower() == val.lower():
					item.SelectItem(vnum)
					if app.ENABLE_SEARCH_BOX_GACHA_SYSTEM:
						if item.ITEM_TYPE_TREASURE_BOX == item.GetItemType() or item.ITEM_TYPE_GIFTBOX == item.GetItemType() or item.ITEM_TYPE_GACHA == item.GetItemType():
							self.s_n["list_names"].AppendItem(name,vnum)
							f+=1
					else:
						if item.ITEM_TYPE_TREASURE_BOX == item.GetItemType() or item.ITEM_TYPE_GIFTBOX == item.GetItemType():
							self.s_n["list_names"].AppendItem(name,vnum)
							f+=1
			if f>0:
				if self.s_n["list_names"].dropped==0:
					self.s_n["list_names"].Clear()
					self.s_n["list_names"].ExpandMe()
					self.search_vnum = 0
				self.s_n["list_names"].Show()
				return
		self.__OnHideList()

	def __OnHideList(self):
		self.s_n["list_names"].dropped=0
		self.s_n["list_names"].Clear()
		self.s_n["list_names"].Hide()
		self.search_vnum = 0

	def OnScrollResultList(self):
		if self.GetCountItem() < 3:
			return

		count = 2
		scrollLineCount = self.WFunction(float(len(self.items))/float(self.MaxPage))
		startIndex = int(scrollLineCount * self.scrollbar.GetPos()+1)

		if startIndex > scrollLineCount:
			return

		self.curPage = startIndex
		self.Page()

	def __OnAcept(self):
		if self.pos == None and self.search_vnum == 0 :
			chat.AppendChat(1, "Ingrese un item en el slot o coloque el nombre.")
			return

		self.ClearBox()
		vnum = 0
		if self.pos != None:
			#chat.AppendChat(1,"Type Item: vnum:%d"%self.vnum)
			vnum = self.vnum
		if self.search_vnum != 0:
			#chat.AppendChat(1,"Type Name: vnum:%d"%self.search_vnum)
			vnum = self.search_vnum

		net.SearchBoxSearch(vnum)

	def __OnAbrir(self):
		if self.pos == None:
			chat.AppendChat(1, "Ingrese un item en el slot")
			return

		if self.search_vnum != 0:
			chat.AppendChat(1, "No tiene ningun cofre en el slot")
			return

		net.SearchBoxOpen(int(self.pos))

	def RefreshOpen(self):
		self.slot.SetItemSlot(self.slotpos, player.GetItemIndex(self.pos), player.GetItemCount(self.pos))
		if player.GetItemCount(self.pos) == 0:
			self.__OnLimpiar()

	def __OnLimpiar(self):
		self.items=[]
		self.curPage = 1
		self.index,self.pos,self.vnum=None,None,None
		self.Box.Hide()		
		self.Box.ClearList()
		self.slot.ClearSlot(0)	
		self.item_name.SetText("")
		self.s_n["nameEdit"].Show()
		self.s_n["nameEdit"].SetText("")
		self.search_vnum=0

	def ClearBox(self):
		self.items=[]
		self.curPage = 1
		self.Box.Hide()		
		self.Box.ClearList()
		self.scrollbar.SetPos(0)

	def GetCountItem(self):
		return len(self.items)

	def WFunction(self, num):
		if (num + 1) != int(num+1):
			return int(num+1)
		else:
			return int(num)

	def Close(self):
		self.__OnLimpiar()
		wndMgr.Hide(self.hWnd)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class UiCofresBox(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = False
		self.list = {}
		self.list_items = []

		self.tooltipItem = uiToolTip.ItemToolTip()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "System/Cofres/boxitems.py")

		except:
			import exception
			exception.Abort("UiCofresBox.LoadWindow")

		try:
			for i in xrange(0,2):
				self.list["bg_items_%d"%i] 		= self.GetChild("CofresBoxItemsBg%s"%i)
				self.list["name_items_%d"%i] 	= self.GetChild("CofresBoxItemsName%s"%i)
				self.list["icon_items_%d"%i] 	=  self.GetChild("CofresBoxItemsIcon%s"%i)
				self.list["icon_items_%d"%i].Hide()
				self.list["icon_items_%d"%i].OnMouseOverIn= lambda selfArg = self, index = i: selfArg.OverInItem(index)
				self.list["icon_items_%d"%i].OnMouseOverOut = lambda selfArg = self, index = i: selfArg.OverOutItem(index)
				self.list["count_items_%d"%i] 	= self.GetChild("CofresBoxItemsCount%s"%i)
				self.list["bg_items_%d"%i].Hide()
		except:
			import exception
			exception.Abort("UiCofresBoxElement.LoadWindow")

	def SetContent(self, type, vnum, count, index):
		if type != 3:
			item.SelectItem(vnum)
			self.list["icon_items_%d"%index].LoadImage(item.GetIconImageFileName())
			self.list["icon_items_%d"%index].Show()
			self.list_items.append([vnum,type])
		else:
			self.list["icon_items_%d"%index].Hide()
		
		if type == 1:
			self.list["name_items_%d"%index].SetText(str(localeInfo.NumberToMoneyStringWorld(count))+" Yang")
			self.list["count_items_%d"%index].SetText("1")
		elif type == 2:
			self.list["name_items_%d"%index].SetText(str(localeInfo.NumberToMoneyStringWorld(count))+" Exp")
			self.list["count_items_%d"%index].SetText("1")
		elif type == 3:
			self.list["name_items_%d"%index].SetText("Mob: "+nonplayer.GetMonsterName(count))
			self.list["count_items_%d"%index].SetText("1")

		else:
			self.list["name_items_%d"%index].SetText(item.GetItemName())
			self.list["count_items_%d"%index].SetText(str(count))


		self.list["bg_items_%d"%index].Show()

	def Open(self, parent, x, y):
		if False == self.isLoaded:
			self.LoadWindow()

		self.SetParent(parent)
		self.SetPosition(x,y)
		self.Show()

	def OverInItem(self,index):
		if int(self.list_items[index][1]) >= 1 and int(self.list_items[index][1]) <= 3:
			return

		self.tooltipItem.ClearToolTip()
		self.tooltipItem.AddItemDataSearchBox(int(self.list_items[index][0]))
			
	def OverOutItem(self,index):
		self.tooltipItem.Hide()

	def ClearList(self):
		self.list_items=[]
		for i in xrange(0,2):
			self.list["bg_items_%d"%i].Hide()

class DropDown(ui.Window):
	dropped  = 0
	dropstat = 0
	width = 0
	height = 0
	maxh = 30
	OnChange = None
	class Item(ui.Window):
		TEMPORARY_PLACE = 0
		width = 0
		height = 0
		def __init__(self,parent, text,value=0,skill=0):
			ui.Window.__init__(self)
			self.textBox=ui.MakeTextLine(self)
			self.textBox.SetText(text)
			self.value = int(value)
			self.skill = int(skill)

		def __del__(self):
			ui.Window.__del__(self)

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent=parent

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def SetSize(self,w,h):
			w = w-110
			ui.Window.SetSize(self,w,h)
			self.width = w
			self.height = h
		def OnUpdate(self):	
			if self.IsIn():
				self.isOver = True
			else:
				self.isOver = False
		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(ui.BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(ui.DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.SetColor(ui.BRIGHT_COLOR)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			if self.isOver:
				grp.SetColor(ui.HALF_WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

	
	def __init__(self,parent):
		ui.Window.__init__(self,"TOP_MOST")
		self.down = 1
		self.parent=parent
	
		self.DropList = ui.ListBoxEx()
		self.DropList.SetParent(self)
		self.DropList.itemHeight = 20
		self.DropList.itemWidth = 220
		self.DropList.itemStep = 18
		self.DropList.SetPosition(0,0)
		self.DropList.SetSize(200,2) 
		self.DropList.SetSelectEvent(self.SetTitle)
		self.DropList.SetViewItemCount(0)
		self.DropList.Show()
		self.selected = self.DropList.GetSelectedItem()
		
		self.SetSize(220-110,95)
	
	def __del__(self): 
		ui.Window.__del__(self)
		
	def AppendItem(self,text,value=0,skill=0):  
		self.DropList.AppendItem(self.Item(self,text,value,skill))
	
	def OnPressEscapeKey(self):		
		self.Hide()
		self.Clear()
				
	def SetTitle(self,item):
		self.dropped = 0
		self.selected = item
		if self.OnChange:
			self.OnChange()
		self.Clear()		
		
	def SetSize(self,w,h):
		ui.Window.SetSize(self,w,h+10)
		self.width = w
		self.height = h
		self.DropList.SetSize(w,h)

	def Clear(self):
		for x in self.DropList.itemList:
			x.Hide()
		self.DropList.RemoveAllItems()

	def ExpandMe(self):
		if self.dropped == 1:
			self.dropped = 0
		else:
			self.dropped = 1
			
	def OnUpdate(self):
		(w,h) = self.parent.GetLocalPosition()
		self.maxh =self.DropList.itemStep*len(self.DropList.itemList)
		self.SetPosition(w+35,h+80)
		if self.dropped == 0 or not self.parent.IsShow() or len(self.DropList.itemList)==0:
			self.SetSize(self.GetWidth(),0)
			self.DropList.SetViewItemCount(0)
			self.Hide()
		elif self.dropped == 1:
			self.Show()
			self.SetTop()
			height = self.maxh+5 if int(self.maxh/self.DropList.itemStep) <2 else self.maxh
			self.SetSize(self.GetWidth(),height)
			self.DropList.SetViewItemCount(self.maxh/self.DropList.itemStep)