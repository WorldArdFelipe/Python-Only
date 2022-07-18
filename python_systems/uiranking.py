
import ui
import uiCommon
import app
import alrnet as net
import os
import chat
import grp
import wndMgr
import alrchr as chr
import item

ROOT_PATH = "d:/ymir work/ui/public/"

CATEGORIAS = [
[1,"Armadura"],
[2,"Armas"],
[3,"Accesorios"],
[4,"Peinados"]
]

IS_BUY = FALSE ## Do not change

class UiRanking(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.PAGES_VIEW 	= 15
		self.PAGE_ACTUAL 	= 1

		self.list_world = []

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Modulo/dragonlairranking.py")
		except:
			import exception
			exception.Abort("UiRanking.LoadWindow")

		try:
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.scrollBar = self.GetChild("GuildDragonLairScrollBar")
		except:
			import exception
			exception.Abort("UiRanking.LoadDialog.BindObject")

		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScrollResultList))
		self.LoadElements()

	def Destroy(self):
		self.ClearList()
		
	def LoadElements(self):
		self.elements = {}

		for i in xrange(0,self.PAGES_VIEW):
			self.elements["image_box_%d"%i] = ui.MakeImageBox(self, "d:/ymir work/ui/game/guild/dragonlairranking/line_down.sub", 22, 25*i+70)
			self.elements["image_box_%d"%i].Show()

			self.elements["slot_background_0_%d"%i] = ui.Bar("TOP_MOST")
			self.elements["slot_background_0_%d"%i].SetParent(self.elements["image_box_%d"%i])
			self.elements["slot_background_0_%d"%i].SetPosition(6, 3)
			self.elements["slot_background_0_%d"%i].SetSize(31, 16)
			self.elements["slot_background_0_%d"%i].SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
			self.elements["slot_background_0_%d"%i].Show()

			self.elements["slot_background_1_%d"%i] = ui.Bar("TOP_MOST")
			self.elements["slot_background_1_%d"%i].SetParent(self.elements["image_box_%d"%i])
			self.elements["slot_background_1_%d"%i].SetPosition(55, 3)
			self.elements["slot_background_1_%d"%i].SetSize(114, 16)
			self.elements["slot_background_1_%d"%i].SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
			self.elements["slot_background_1_%d"%i].Show()


			self.elements["slot_background_2_%d"%i] = ui.Bar("TOP_MOST")
			self.elements["slot_background_2_%d"%i].SetParent(self.elements["image_box_%d"%i])
			self.elements["slot_background_2_%d"%i].SetPosition(192, 3)
			self.elements["slot_background_2_%d"%i].SetSize(22, 16)
			self.elements["slot_background_2_%d"%i].SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
			self.elements["slot_background_2_%d"%i].Show()

			self.elements["slot_background_3_%d"%i] = ui.Bar("TOP_MOST")
			self.elements["slot_background_3_%d"%i].SetParent(self.elements["image_box_%d"%i])
			self.elements["slot_background_3_%d"%i].SetPosition(239, 3)
			self.elements["slot_background_3_%d"%i].SetSize(61, 16)
			self.elements["slot_background_3_%d"%i].SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
			self.elements["slot_background_3_%d"%i].Show()

			self.elements["id_%d"%i] = ui.MakeTextLine(self.elements["slot_background_0_%d"%i])
			self.elements["id_%d"%i].SetPosition(0,-3)
			self.elements["id_%d"%i].SetText("")
			self.elements["id_%d"%i].Hide()

			self.elements["name_%d"%i] = ui.MakeTextLine(self.elements["slot_background_1_%d"%i])
			self.elements["name_%d"%i].SetPosition(0,-3)
			self.elements["name_%d"%i].SetText("")
			self.elements["name_%d"%i].Hide()

			self.elements["empire_%d"%i] = ui.MakeImageBox(self.elements["slot_background_2_%d"%i], "d:/ymir work/ui/game/rank/empire_1.sub", -2, -1)
			self.elements["empire_%d"%i].Hide()

			self.elements["muertes_%d"%i] = ui.MakeTextLine(self.elements["slot_background_3_%d"%i])
			self.elements["muertes_%d"%i].SetPosition(0,-3)
			self.elements["muertes_%d"%i].SetText("")
			self.elements["muertes_%d"%i].Hide()

		self.elements["button_shop"] = ui.MakeButton(self,20,450,"Shop",ROOT_PATH ,"public_intro_btn/plus_btn_01.sub","public_intro_btn/plus_btn_02.sub","public_intro_btn/plus_btn_03.sub")
		self.elements["button_shop"].SetEvent(self.OpenGuiShop)
		self.elements["button_shop"].Show()

	def ClearList(self):
		self.PAGE_ACTUAL = 1
		self.list_world = []

	def AddList(self,nombre,reino,muertes):
		self.list_world.append([nombre,reino,muertes])

	def LoadList(self):
		for a in xrange(min(self.PAGES_VIEW, self.GetListCount() - self.PAGE_ACTUAL * self.PAGES_VIEW +self.PAGES_VIEW)):

			name 	= self.list_world[a + (self.PAGE_ACTUAL - 1)*self.PAGES_VIEW][0]
			reino	= self.list_world[a + (self.PAGE_ACTUAL - 1)*self.PAGES_VIEW][1]
			muertes = self.list_world[a + (self.PAGE_ACTUAL - 1)*self.PAGES_VIEW][2]

			self.SetId(a)
			self.SetName(a,name)
			self.SetReino(a,reino)
			self.SetMuertes(a,muertes)

	def SetId(self,value):
		self.elements["id_%d"%value].SetText(str(value+1))
		self.elements["id_%d"%value].Show()

	def SetName(self,value,name):
		self.elements["name_%d"%value].SetText(name)
		self.elements["name_%d"%value].Show()

	def SetReino(self,value,reino):
		self.elements["empire_%d"%value].LoadImage("d:/ymir work/ui/game/rank/empire_%s.sub" % reino)
		self.elements["empire_%d"%value].Show()

	def SetMuertes(self,value,muertes):
		self.elements["muertes_%d"%value].SetText(muertes)
		self.elements["muertes_%d"%value].Show()

	def OnScrollResultList(self):
		if self.GetListCount() < self.PAGES_VIEW+1:
			return

		scrollLineCount = self.WFunction(float(len(self.list_world))/float(self.PAGES_VIEW))
		startIndex = int(scrollLineCount * self.scrollBar.GetPos()+1)

		if startIndex > scrollLineCount:
			return

		self.PAGE_ACTUAL = startIndex
		self.LoadList()

	def WFunction(self, num):
		if (num + 1) != int(num+1):
			return int(num+1)
		else:
			return int(num)

	def GetListCount(self):
		return len(self.list_world)

	def OpenGuiShop(self):
		net.SendChatPacket("/ranking_duel open_ranking_shop")

	def Close(self):
		net.SendChatPacket("/ranking_duel close_ranking_list")
		self.ClearList()
		self.Hide()

			
class UiRankingShop(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.PT = 4
		self.CP = 1
		self.CATEGORIAS_A = 1
		self.info_items = []
		self.info_items_c = []
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Modulo/rankingshop.py")
		except:
			import exception
			exception.Abort("UiRankingShop.LoadWindow")

		try:
			self.board = self.GetChild("board")
			self.thinboard_0 = self.GetChild("thinboard_0")

			self.prev_button = self.GetChild("prev_button")
			self.last_prev_button = self.GetChild("last_prev_button")
			self.next_button = self.GetChild("next_button")
			self.last_next_button = self.GetChild("last_next_button")

			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("UiRankingShopElements.LoadWindow")

		self.prev_button.SetEvent(self.__OnClickArrow, 'MOSTBOUGHT_RIGHT')
		self.last_prev_button.SetEvent(self.__OnClickArrow, 'MOSTBOUGHT_RIGHT_LAST')
		self.next_button.SetEvent(self.__OnClickArrow, 'MOSTBOUGHT_LEFT')
		self.last_next_button.SetEvent(self.__OnClickArrow, 'MOSTBOUGHT_LEFT_LAST')

		self.elements_box = {}
		self.LoadingBox()
		self.LoadingCategoria()

	def LoadingCategoria(self):
		count = 0
		for i in xrange(0,len(CATEGORIAS)):
			self.elements_box["categoria_%d"%count] = ui.MakeButton(self.thinboard_0,10,25*count+20,"","d:/ymir work/ui/public/" ,"Large_Button_01.sub","Large_Button_02.sub","Large_Button_03.sub")
			self.elements_box["categoria_%d"%count].SetText(CATEGORIAS[count][1])
			self.elements_box["categoria_%d"%count].SetEvent(self.SelectCategoria,count)
			self.elements_box["categoria_%d"%count].Show()
			count +=1

	def LoadingBox(self):
		self.elements_box["box_items"] = UiRankingShopBox()
		self.elements_box["box_items"].Open(self.board,145,50)
		self.elements_box["box_items"].Hide()

	def ClearItems(self):
		self.info_items = []

	def LoadItems(self,categoria,id,vnum,count,price):
		self.info_items.append([int(categoria),int(id),int(vnum),int(count),int(price)])

	def Page(self):
		self.elements_box["box_items"].Hide()
		self.elements_box["box_items"].ClearList()

		self.SetItemCategoria()

		for a in xrange(min(self.PT, len(self.info_items_c) - self.CP * self.PT + self.PT)):
			categoria 	= self.info_items_c[a + (self.CP - 1)*self.PT][0]
			id 			= self.info_items_c[a + (self.CP - 1)*self.PT][1]
			vnum 		= self.info_items_c[a + (self.CP - 1)*self.PT][2]
			count 		= self.info_items_c[a + (self.CP - 1)*self.PT][3]
			price 		= self.info_items_c[a + (self.CP - 1)*self.PT][4]

			self.elements_box["box_items"].SetContent(a,id,vnum,count,price)
			self.elements_box["box_items"].Show()

		if self.CP *self.PT >=  len(self.info_items_c):
			self.next_button.Hide()
			self.last_next_button.Hide()
		else:
			self.next_button.Show()
			self.last_next_button.Show()

		if self.CP > 1:
			self.prev_button.Show()
			self.last_prev_button.Show()
		else:
			self.prev_button.Hide()
			self.last_prev_button.Hide()

	def SetItemCategoria(self):
		self.info_items_c = []
		for a in xrange(0,len(self.info_items)):
			categoria = self.info_items[a][0]
			if categoria == self.CATEGORIAS_A:
				self.info_items_c.append(self.info_items[a])

	def __OnClickArrow(self, arrow):
		Left_Last = self.WFunction(float(len(self.info_items_c))/float(self.PT))

		if arrow == 'MOSTBOUGHT_LEFT':
			self.CP += 1
			self.Page()
		elif arrow == 'MOSTBOUGHT_LEFT_LAST':
			self.CP = Left_Last
			self.Page()
		elif arrow == 'MOSTBOUGHT_RIGHT':
			self.CP -= 1
			self.Page()
		elif arrow == 'MOSTBOUGHT_RIGHT_LAST':
			self.CP = 1
			self.Page()

	def WFunction(self, num):
		if (num + 1) != int(num+1):
			return int(num+1)
		else:
			return int(num)

	def SelectCategoria(self,index):
		self.CATEGORIAS_A = index+1
		self.CP = 1
		self.Page()

	def Close(self):
		net.SendChatPacket("/ranking_duel close_ranking_shop")
		self.elements_box["box_items"].Hide()		
		self.elements_box["box_items"].ClearList()
		self.Hide()

class UiRankingShopBox(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = FALSE
		self.elements = {}
		self.list_items = []
		self.buy_item = []

		self.itemBuyQuestionDialog = ItemBuyDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Modulo/rankingshopbox.py")
		except:
			import exception
			exception.Abort("UiRankingShopBox.LoadWindow")

		try:
			for i in xrange(0,4):
				self.elements["item_name_%d"%i] = self.GetChild("ItemName_%d"%i)


				self.elements["item_icon_%d"%i] = self.GetChild("ItemIcon_%d"%i)
				self.elements["item_price_%d"%i] = self.GetChild("ItemPrice_%d"%i)
				self.elements["item_count_bg_%d"%i] = self.GetChild("ItemAmountSlot_%d"%i)
				self.elements["item_count_%d"%i] = self.GetChild("ItemAmount_%d"%i)
				self.elements["item_buy_%d"%i] = self.GetChild("AceptButton_%d"%i)
				self.elements["item_buy_%d"%i].SetEvent(self.BuyItem, i)
				self.elements["item_bg_%d"%i] = self.GetChild("board_%d"%i)
				self.elements["item_bg_%d"%i].Hide()

		except:
			import exception
			exception.Abort("UiRankingShopBoxElements.LoadWindow")

		self.isLoaded = TRUE
		self.itemBuyQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerBuyItem(arg))
		self.itemBuyQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerBuyItem(arg))

	def Open(self, parent, x, y):
		if FALSE == self.isLoaded:
			self.LoadWindow()

		self.SetParent(parent)
		self.SetPosition(x,y)
		self.Show()

	def BuyItem(self, index):
		if int(self.elements["item_count_%d"%index].GetText()) > 200:
			chat.AppendChat(1,"No puede poner una cantidad mayor a 200.")
			return

		if int(self.elements["item_count_%d"%index].GetText()) <= 0:
			chat.AppendChat(1,"No puede poner una cantidad menor o igual a 0.")
			return

		self.buy_item = []
		self.buy_item.append([self.list_items[index][0],self.elements["item_count_%d"%index].GetText()])

		self.itemBuyQuestionDialog.SetText("Deseas compras %s x%d por la cantidad de %d Muertes?"%(self.elements["item_name_%d"%index].GetText(),int(self.elements["item_count_%d"%index].GetText()),self.GetPrice(index)))
		self.itemBuyQuestionDialog.Open()

	def GetPrice(self,index):
		return self.list_items[index][1] * int(self.elements["item_count_%d"%index].GetText())

	def SetContent(self, index, id, vnum, count, price):
		item.SelectItem(int(vnum))

		self.list_items.append([id,price,count])

		self.elements["item_name_%d"%index].SetText(item.GetItemName())
		self.elements["item_icon_%d"%index].LoadImage(item.GetIconImageFileName())
		self.elements["item_price_%d"%index].SetText(str(price)+" Muertes")
		self.elements["item_count_%d"%index].SetText(str(count))

		if item.IsFlag(4) == 1:
			self.elements["item_count_bg_%d"%index].Show()
		else:
			self.elements["item_count_bg_%d"%index].Hide()

		self.elements["item_bg_%d"%index].Show()

	def AnswerBuyItem(self, arg):
		if arg:
			net.SendChatPacket("/ranking_duel buy_ranking_shop %s %s"%(self.buy_item[0][0],self.buy_item[0][1]))

		self.itemBuyQuestionDialog.Close()	
	def ClearList(self):
		for i in xrange(0,4):
			self.elements["item_bg_%d"%i].Hide()
			self.list_items = []


class ItemBuyDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		global IS_BUY
		if IS_BUY == TRUE:
			return
		IS_BUY = TRUE
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		

	def Close(self):
		global IS_BUY
		IS_BUY = FALSE
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE