import ui
import app
import battlepass
import chat 
import localeinfo
import wndMgr
import item
import nonplayer

RUTA_IMGS = "battlepass/"
MISION_INFO_DESCRIPT = {}
COLOR_PORCENTAJE = [
	0xffc9f06b,
	0XFFF0BE6B,
	0xffF06B6B
]
class UiBattlePassButton(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.elements = {}
		self.SetPosition(wndMgr.GetScreenWidth() - 105, 205)
		self.SetSize(78, 23)

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):

		self.elements["button_battlepass"] = ui.Button()
		self.elements["button_battlepass"].SetParent(self)
		self.elements["button_battlepass"].SetPosition(0, 0)
		self.elements["button_battlepass"].SetUpVisual(RUTA_IMGS + "bp_boton_1.png")
		self.elements["button_battlepass"].SetOverVisual(RUTA_IMGS + "bp_boton_2.png")
		self.elements["button_battlepass"].SetDownVisual(RUTA_IMGS + "bp_boton_3.png")
		self.elements["button_battlepass"].SetEvent(ui.__mem_func__(self.OpenBattlePass))
		self.elements["button_battlepass"].Hide()

	def ShowButton(self):
		if self.elements:
			if self.elements["button_battlepass"]:
				self.elements["button_battlepass"].Show()

	def HideButton(self):
		if self.elements:
			if self.elements["button_battlepass"]:
				self.elements["button_battlepass"].Hide()

	def OpenBattlePass(self):
		battlepass.Open()

class UiBattlePass(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		battlepass.SetBattlePassHandler(self)

		import uiToolTip
		self.toolTip = uiToolTip.ToolTip(260)
		self.toolTip.HideToolTip()

		self.tooltipItem = uiToolTip.ItemToolTip()

		self.pages_view = 10

		self.LoadMisionesDescript()

		self.elements = {}

		self.elements["index_select_mision"] = -1

		self.LoadWindow()

	def __del__(self):
		battlepass.SetBattlePassHandler(None)
		ui.ScriptWindow.__del__(self)

	def LoadMisionesDescript(self):
		try:
			lines = open(app.GetLocalePath()+"/battle_pass.txt", "r").readlines()
		except:
			import exception
			exception.Abort("LoadMisionesDescript")
		
		
		for line in lines:
			tokens = line[:-1].split("\t")
			if len(tokens) == 0 or not tokens[0]:
				continue
				
			if tokens[0] == "#":
				continue
			
			type = int(tokens[0])
			
			MISION_INFO_DESCRIPT[type] = [tokens[1],tokens[2],tokens[3]]

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/battlepass_windows.py")
		except:
			import exception
			exception.Abort("UiBattlePass.LoadWindow.LoadObject")

		try:
			self.marco_img	= self.GetChild("marco_img")
			self.slot 		= self.GetChild("slot")
			self.time_r		= self.GetChild("time_r")
			self.mision_complete_total = self.GetChild("mision_complete_total")
			self.recibir_recompensa_button = self.GetChild("recibir_recompensa_button")
			self.TitleBar		= self.GetChild("titlebar")


		except:
			import exception
			exception.Abort("UiBattlePass.LoadWindow.LoadElements")

		self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.recibir_recompensa_button.SetEvent(self.FuncRecibirMision)
		self.LoadElements()

	def OverInItem(self,index):
		if None != self.tooltipItem:
			index = 3-index
			(vnum,count) = self.GetDateItemStruc(self.elements["index_select_mision"]-1,index)

			self.tooltipItem.ClearToolTip()
			self.tooltipItem.ShowRender(False)
			self.tooltipItem.AddItemData(int(vnum),0)


	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def LoadElements(self):
		for i in xrange(0,self.pages_view):
			i+=1

			x = 5
			y = 173

			if i >= 1 and i <=5:
				y += 28*i
			else:
				x = 203
				y += 28*(i-5)

			self.elements["select_mision_%d"%i] = ui.RadioButton()
			self.elements["select_mision_%d"%i].SetParent(self.marco_img)
			self.elements["select_mision_%d"%i].SetUpVisual(RUTA_IMGS+"boton_mision_1.png")
			self.elements["select_mision_%d"%i].SetOverVisual(RUTA_IMGS+"boton_mision_2.png")
			self.elements["select_mision_%d"%i].SetDownVisual(RUTA_IMGS+"boton_mision_3.png")
			self.elements["select_mision_%d"%i].SetPosition(x,y)
			self.elements["select_mision_%d"%i].SetEvent(self.FuncSelectMision,i)
			self.elements["select_mision_%d"%i].Hide()

			self.elements["corona_plata_img_%d"%i] = ui.ImageBox()
			self.elements["corona_plata_img_%d"%i].SetParent(self.elements["select_mision_%d"%i])
			self.elements["corona_plata_img_%d"%i].LoadImage(RUTA_IMGS+"corona_plata_new.png")
			self.elements["corona_plata_img_%d"%i].SetPosition(5,8)
			self.elements["corona_plata_img_%d"%i].Show()

			self.elements["mision_name_%d"%i] = ui.TextLine()
			self.elements["mision_name_%d"%i].SetParent(self.elements["select_mision_%d"%i])
			self.elements["mision_name_%d"%i].SetPosition(29,5)
			self.elements["mision_name_%d"%i].SetHorizontalAlignLeft()
			self.elements["mision_name_%d"%i].Hide()

			self.elements["porcentaje_mision_%d"%i] = ui.TextLine()
			self.elements["porcentaje_mision_%d"%i].SetParent(self.elements["select_mision_%d"%i])
			self.elements["porcentaje_mision_%d"%i].SetPosition(158,5)
			self.elements["porcentaje_mision_%d"%i].SetText("")
			self.elements["porcentaje_mision_%d"%i].SetPackedFontColor(0xffc9f06b)
			self.elements["porcentaje_mision_%d"%i].SetHorizontalAlignCenter()
			self.elements["porcentaje_mision_%d"%i].Hide()

			self.elements["info_mision_%d"%i] = ui.ImageBox()
			self.elements["info_mision_%d"%i].SetParent(self.elements["select_mision_%d"%i])
			self.elements["info_mision_%d"%i].LoadImage(RUTA_IMGS+"info_icon.png")
			self.elements["info_mision_%d"%i].SetPosition(175,7)
			self.elements["info_mision_%d"%i].OnMouseOverIn = lambda index = i :self.OnMouseOverIn(index)
			self.elements["info_mision_%d"%i].OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOut)
			self.elements["info_mision_%d"%i].Hide()

	def BINARY_BATTLEPASS_LOADING(self,subheader):
		if subheader == 4:
			self.LoadDateInfo()
		else:
			self.LoadDateUpdateCount()


	def GetColorPorcentaje(self,porcentaje):
		if porcentaje >= 0 and porcentaje <= 25:
			return COLOR_PORCENTAJE[2]
		elif porcentaje >= 26 and porcentaje <= 99:
			return COLOR_PORCENTAJE[1]

		return COLOR_PORCENTAJE[0]


	def LoadDateUpdateCount(self):
		count_mision = battlepass.CountDates()
		for x in range(count_mision):
			(count_total,count_actual,reward_status) = self.GetDatesCountStruc(x)
			index = x+1
			self.elements["porcentaje_mision_%d"%index].SetText("%d%%"%(self.CalcPorcentaje(count_actual,count_total)))
			self.elements["porcentaje_mision_%d"%index].SetPackedFontColor(self.GetColorPorcentaje(self.CalcPorcentaje(count_actual,count_total)))

		self.CheckButtonRecompensa(self.elements["index_select_mision"])
		self.CountCompleteMisiones()


	def LoadDateInfo(self):
		count_mision = battlepass.CountDates()

		for x in range(count_mision):
			(type_mision,vnum_extra) = self.GetDatesStruc(x)
			(count_total,count_actual,reward_status) = self.GetDatesCountStruc(x)

			index = x+1
			self.elements["mision_name_%d"%index].SetText("%d. %s"%(index,self.GetTextMisions(0,type_mision,count_total,vnum_extra)))
			self.elements["mision_name_%d"%index].Show()
			self.elements["porcentaje_mision_%d"%index].SetText("%d%%"%(self.CalcPorcentaje(count_actual,count_total)))
			self.elements["porcentaje_mision_%d"%index].SetPackedFontColor(self.GetColorPorcentaje(self.CalcPorcentaje(count_actual,count_total)))
			self.elements["porcentaje_mision_%d"%index].Show()
			self.elements["select_mision_%d"%index].Show()
			self.elements["info_mision_%d"%index].Show()


		self.FuncSelectMision(1)
		self.SetTime()
		self.CountCompleteMisiones()

	def GetDatesStruc(self,index):
		func_dates 		= battlepass.GetDates(index)
		type_mision 	= func_dates[0]
		vnum_extra 		= func_dates[1]

		return (type_mision,vnum_extra)

	def GetDatesCountStruc(self,index):
		func_dates		= battlepass.GetDatesCount(index)
		count_total 	= func_dates[0]
		count_actual 	= func_dates[1]
		reward_status	= func_dates[2]

		return (count_total,count_actual,reward_status)

	def GetCounts(self,index):
		(count_total,count_actual,reward_status) = self.GetDatesCountStruc(index-1)
		return (count_total,count_actual)

	def GetDateItemStruc(self,index,index1):
		func_dates = battlepass.GetDatesItems(index,index1)
		vnum_item  = func_dates[0]
		count_item = func_dates[1]

		return(vnum_item,count_item)

	def SetTime(self):
		time  = battlepass.GetTime() + app.GetGlobalTimeStamp() 
		self.time_r.SetText("Tiempo Restante: {}".format(localeinfo.SecondOfflineToDHM(time-app.GetGlobalTimeStamp() )))

	def CountCompleteMisiones(self):
		count_complete_mision = 0
		count_mision = battlepass.CountDates()
		for x in range(count_mision):
			(count_total,count_actual) = self.GetCounts(x+1)

			if count_actual >= count_total:
				count_complete_mision += 1

		self.mision_complete_total.SetText("Misiones completadas: %d / %d"%(count_complete_mision,count_mision))


	def SetInfoMision(self,index):
		(type_mision,vnum_extra) = self.GetDatesStruc(index-1)
		(count_total,count_actual,reward_status) = self.GetDatesCountStruc(index-1)
		if count_actual > count_total:
			count_actual = count_total
			
		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.GetTextMisions(1,type_mision,count_total,vnum_extra))
		self.toolTip.AppendDescription(self.GetTextMisions(2,type_mision,count_total,vnum_extra),100)
		self.toolTip.AppendSpace(20)
		self.toolTip.AppendTextLine("Cantidad Restante: %d / %d"%(count_actual,count_total))

	def GetTextMisions(self,type_m,type,count = 0, vnum = 0):
		"""
		1.Count
		2.Count + NameMob
		3.Count + NameItem

		"""
		list = {
			1 : [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,21],
			2 : [2],
			3 : [20],
			4 : [18]
		}

		if type_m > 0:
			for i in list:
				for a in range(len(list[i])):
					if list[i][a] == type:
						if i == 1:
							return MISION_INFO_DESCRIPT[type][type_m]%(count)
						if i == 2:
							name_mob = nonplayer.GetMonsterName(vnum)
							return MISION_INFO_DESCRIPT[type][type_m]%(count,name_mob)
						if i == 3:
							item.SelectItem(vnum)	
							name_item = item.GetItemName()
							return MISION_INFO_DESCRIPT[type][type_m]%(count,name_item)
						if i == 4:
							return MISION_INFO_DESCRIPT[type][type_m]

		return MISION_INFO_DESCRIPT[type][type_m]

	def CalcPorcentaje(self,count_actual,count_total):
		cal = float(count_actual) / max(1, float(count_total)) * 100
		if cal > 100:
			cal = 100
		return cal

	def FuncSelectMision(self,index):
		self.ShowItemSlotMision(index)
		self.CheckButtonRecompensa(index)

		self.__ClickRadioButton(index)
		self.elements["index_select_mision"] = index

	def __ClickRadioButton(self, buttonIndex):
		selButton=self.elements["select_mision_%d"%buttonIndex]

		for i in xrange(0,self.pages_view):
			i+=1
			self.elements["select_mision_%d"%i].SetUp()

		selButton.Down()

	def ShowItemSlotMision(self,index):
		for x in range(4):
			index_new = 3-x
			(vnum,count) = self.GetDateItemStruc(index-1,x)
			self.slot.SetItemSlot(index_new, vnum,count)		

	def CheckCompleteMision(self,index):
		(count_total,count_actual) = self.GetCounts(index)
		if count_actual >= count_total:
			return True
		return False

	def CheckRewardStatus(self,index):
		(count_total,count_actual,reward_status) = self.GetDatesCountStruc(index-1)
		if reward_status == 1:
			return True
		return False

	def CheckButtonRecompensa(self,index):
		if self.CheckCompleteMision(index) and not self.CheckRewardStatus(index):
			self.recibir_recompensa_button.SetUpVisual(RUTA_IMGS+"reward_1.png")
			self.recibir_recompensa_button.SetOverVisual(RUTA_IMGS+"reward_2.png")
			self.recibir_recompensa_button.SetDownVisual(RUTA_IMGS+"reward_3.png")
		else:
			self.recibir_recompensa_button.SetUpVisual(RUTA_IMGS+"no_reward.png")
			self.recibir_recompensa_button.SetOverVisual(RUTA_IMGS+"no_reward.png")
			self.recibir_recompensa_button.SetDownVisual(RUTA_IMGS+"no_reward.png")

		if self.CheckCompleteMision(index) and self.CheckRewardStatus(index):
			self.recibir_recompensa_button.SetText("Recompensa entregada")
		else:
			self.recibir_recompensa_button.SetText("Recibir Recompensa")

	def FuncRecibirMision(self):
		index = self.elements["index_select_mision"]
		if self.CheckCompleteMision(index):
			battlepass.Reward(index)

	def OnMouseOverIn(self,index):
		self.SetInfoMision(index)
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
