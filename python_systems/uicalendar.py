import ui
import uiCommon
import app
import net
import os
import chat
import grp
import wndMgr
import localeInfo
import time
import ime

PATCH_IMG = "rework_calendario/"
DAY_TITLE = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]


class CalendarItems(ui.Window):
	def __init__(self, getParentEvent):
		ui.Window.__init__(self)
		self.SetParent(getParentEvent().GetBoard())

		self.day = -1
		self.isOpen = False

		self.barra_dia = ui.Button()
		self.barra_dia.SetParent(self)
		self.barra_dia.SetUpVisual(PATCH_IMG+"barra_dia.png")
		self.barra_dia.SetOverVisual(PATCH_IMG+"barra_dia.png")
		self.barra_dia.SetDownVisual(PATCH_IMG+"barra_dia.png")
		self.barra_dia.SetEvent(self.Select)
		self.barra_dia.Show()


		self.expand = ui.Button()
		self.expand.SetParent(self.barra_dia)
		self.expand.SetUpVisual(PATCH_IMG+"slide_down_1.png")
		self.expand.SetOverVisual(PATCH_IMG+"slide_down_2.png")
		self.expand.SetDownVisual(PATCH_IMG+"slide_down_3.png")
		self.expand.SetPosition(427,5)
		self.expand.SetEvent(self.Select)
		self.expand.Show()

		
		self.cuadro_desplegado = ui.ImageBox()
		self.cuadro_desplegado.SetParent(self)
		self.cuadro_desplegado.LoadImage(PATCH_IMG+"cuadro_desplegado.png")
		self.cuadro_desplegado.SetPosition(12,25)
		self.cuadro_desplegado.Hide()

		self.event_descrip = ui.TextLine()
		self.event_descrip.SetParent(self.cuadro_desplegado)
		self.event_descrip.SetPosition(100,17)
		self.event_descrip.SetMultiLine()
		self.event_descrip.SetLimitWidth(320)
		self.event_descrip.Show()

		self.icon = ui.ImageBox()
		self.icon.SetParent(self.cuadro_desplegado)
		self.icon.SetPosition(17,12)
		self.icon.Show()

		self.day_title = ui.TextLine()
		self.day_title.SetParent(self)
		self.day_title.SetPosition(10,6)
		self.day_title.SetPackedFontColor(0xffffb937)
		self.day_title.Show()

		self.name_event = ui.TextLine()
		self.name_event.SetParent(self)
		self.name_event.SetPosition(90,6)
		self.name_event.SetLimitWidth(170)
		self.name_event.Show()

		self.hora_go_1 = ui.TextLine()
		self.hora_go_1.SetParent(self)
		self.hora_go_1.SetPosition(276,6)
		self.hora_go_1.Show()

		self.hora_go_2 = ui.TextLine()
		self.hora_go_2.SetParent(self)
		self.hora_go_2.SetPosition(355,6)
		self.hora_go_2.Show()

		self.getParentEvent = getParentEvent

		self.SetSize(450, 26)	

	def GetDay(self):
		return self.day

	def SetInfo(self,dia,event,descrip,banner,horario_go,horario_end,horario_2_go,horario_2_end):
		self.day = dia
		self.day_title.SetText(DAY_TITLE[dia-1])
		self.name_event.SetText(event)
		self.event_descrip.SetText(descrip)
		self.icon.LoadImage(PATCH_IMG+"%s.png"%(banner))

		self.hora_go_1.SetText("{} - {}".format(horario_go,horario_end))
		self.hora_go_2.SetText("{} - {}".format(horario_2_go,horario_2_end))

	def Open(self):
		self.isOpen = True
		self.cuadro_desplegado.Show()
		self.ExpandImage(1)

	def Close(self):
		self.isOpen = False
		self.cuadro_desplegado.Hide()
		self.ExpandImage(0)


	def ExpandImage(self,index):
		image = ["slide_down_","slide_up_"]
		self.expand.SetUpVisual(PATCH_IMG+"{}1.png".format(image[index]))
		self.expand.SetOverVisual(PATCH_IMG+"{}2.png".format(image[index]))
		self.expand.SetDownVisual(PATCH_IMG+"{}3.png".format(image[index]))


	def IsOpen(self):
		return self.isOpen

	def Select(self):
		self.getParentEvent().OnSelectItem(self)

class UiCalendar(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.days_list = []
		self.event_info = []
		self.startLine = 0
		self.count_days = 7
		self.pais_select = 0

		self.flag = [["es","Espana",0],["ar","Argentina",-4],["ec","Colombia",-6],["mx","Mexico",-7],["ve","Venezuela",-5],["cl","Chile",-4],["cr","Costa Rica",-8],["ro","Romania",+1],["gb","United Kingdom",-1],["tr","Turkish",+1],["pt","Portugal",-1],["de","Deutschland",0]]


	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/calendar.py")
		except:
			import exception
			exception.Abort("UiCalendar.LoadWindow.LoadObject")

		self.base_transparente = self.GetChild("base_transparente")
		#self.flag_icon 		   = self.GetChild("flag_icon")
		#self.prev_button       = self.GetChild("prev_button")
		#self.next_button	   = self.GetChild("next_button")
		self.TitleBar		   = self.GetChild("TitleBar")

		for i in xrange(0,self.count_days):
			days_items = CalendarItems(ui.__mem_func__(self.GetSelf))
			days_items.Show()
			self.days_list.append(days_items)

		yPos = 0
		for item in self.days_list:
			item.SetPosition(4,20+yPos)
			yPos += 28

		#self.prev_button.SetEvent(self.SelectPais,0)
		#self.next_button.SetEvent(self.SelectPais,1)
		self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		#self.SelectPais(0)

	def ClearEventos(self):
		self.event_info = []

	def LoadEventos(self,dia,event,descrip,banner,horario_go,horario_end,horario_2_go,horario_2_end):
		self.event_info.append([int(dia),event,descrip,banner,horario_go,horario_end,horario_2_go,horario_2_end])

	def LoadingEventos(self):
		for i in xrange(0,len(self.event_info)):
			dia 		= self.event_info[i][0]
			event 		= self.event_info[i][1]
			descrip 	= self.event_info[i][2]
			banner 		= self.event_info[i][3]
			horario_go 	= self.event_info[i][4]
			horario_end = self.event_info[i][5]
			horario_2_go = self.event_info[i][6]
			horario_2_end = self.event_info[i][7]

			self.days_list[dia-1].SetInfo(dia,event,descrip,banner,self.ConverTotal(horario_go),self.ConverTotal(horario_end),self.ConverTotal(horario_2_go),self.ConverTotal(horario_2_end))

	#def SelectPais(self,index):

		#if index == 1:
		#	if self.pais_select < len(self.flag)-1:
		#		self.pais_select = self.pais_select + 1
		#else:
			#if self.pais_select > 0:
			#	self.pais_select = self.pais_select - 1

		#self.flag_icon.LoadImage(PATCH_IMG+"banderas/"+self.flag[self.pais_select][0]+".tga")
		
		#self.LoadingEventos()


	def ConverTotal(self,hora):
		time_actual = self.FormtTime(hora,self.pais_select)
		return "%s:%s"%(self.GetHour(time_actual),self.GetMin(time_actual))

	def FormtTime(self,time_re,pais):
		conver = time_re.split(":")
		return time.strptime(str(self.CalcTiempo(conver[0],pais))+":"+conver[1], "%H:%M")

	def Time24Hours(self,time):
		if int(time) < 10:
			return "0"+str(time)
		else:
			return str(time)

	def GetHour(self,time):
		return self.Time24Hours(time.tm_hour)

	def GetMin(self,time):
		return self.Time24Hours(time.tm_min)

	def CalcTiempo(self,hora,pais):
		tiempo_enviando = int(hora)
		#tiempo_valor = self.CalcHPais(pais)
		tiempo_valor = 0

		valor = 1

		if tiempo_enviando+tiempo_valor > 24:
			valor = (tiempo_enviando+tiempo_valor)-24
		else:
			if tiempo_enviando+tiempo_valor < 1:
				valor = (tiempo_enviando+tiempo_valor)+24
			else:
				valor = tiempo_enviando+tiempo_valor

		if valor == 24:
			valor = 0

		return valor

	def CalcHPais(self,pais):
		return self.flag[pais][2]

	def OnSelectItem(self, item):
		self.selectedDay = item

		if self.selectedDay:
			map(ui.Window.Hide, self.days_list)

			yPos = 0
			iIndex = 1
			yOpen = 100
			for item in self.days_list:
				item.SetPosition(4,20+yPos)
				if iIndex != self.selectedDay.GetDay():
					item.Close()
				item.Show()
				
				yPos += 28
				if iIndex == self.selectedDay.GetDay() and not self.selectedDay.IsOpen():
					yPos += 77

				iIndex+=1

			if self.selectedDay.IsOpen():
				self.selectedDay.Close()
			else:
				self.selectedDay.Open()

	def GetBoard(self):
		return self.base_transparente

	def GetSelf(self):
		return self

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		net.CalendarClose()
		wndMgr.Hide(self.hWnd)



class CalendarIngameWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "Modulo/calendariowindows.py")
		except:
			import exception
			exception.Abort("CalendarIngameWindow.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.gameButton = GetObject("calendar_button")

		except:
			import exception
			exception.Abort("CubeWindow.LoadDialog.BindObject")

		self.gameButton.SetEvent(ui.__mem_func__(self.__OnClickGame))

	def __OnClickGame(self):
		net.CalendarOpen()
		
	def Destroy(self):
		self.ClearDictionary()

