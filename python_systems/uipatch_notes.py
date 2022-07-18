import ui
import chat
import textwrap
import event
import uiScriptLocale
import net

PATCH_DESIGN = "patch_notes/design/"
MAX_COUNT = 11
MAX_LINES = 11

class UiPatchNotes(ui.ScriptWindow):

	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.elements = {}
		self.patch_info = []
		self.page_actual = 0
		self.page_select = 0
		self.descIndex=0
		self.pos = 0
		self.desc_y = 40
		self.pos_actual = self.desc_y
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/patch_notes_windows.py")
		except:
			import exception
			exception.Abort("UiPatchNotes.LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.img_board = self.GetChild("img_board")
			self.button_prev = self.GetChild("button_prev")
			self.button_next = self.GetChild("button_next")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("UiPatchNotes.LoadWindow.LoadElements")

		self.button_prev.SetEvent(ui.__mem_func__(self.SetButtonPatch),"prev")
		self.button_next.SetEvent(ui.__mem_func__(self.SetButtonPatch),"next")

		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.SetParent(self.img_board)

		self.LoadElements()

	def LoadElements(self):
		if MAX_COUNT > 0:
			for i in xrange(0,MAX_COUNT):
				x = 38
				self.elements["button_patch_%d"%i] = ui.RadioButton()
				self.elements["button_patch_%d"%i].SetParent(self.board)
				self.elements["button_patch_%d"%i].SetUpVisual(PATCH_DESIGN+"btn_1.tga")
				self.elements["button_patch_%d"%i].SetOverVisual(PATCH_DESIGN+"btn_2.tga")
				self.elements["button_patch_%d"%i].SetDownVisual(PATCH_DESIGN+"btn_3.tga")
				self.elements["button_patch_%d"%i].SetPosition(39*i+x,33)
				self.elements["button_patch_%d"%i].SetEvent(ui.__mem_func__(self.SetButtonPatch),"select",i)
				self.elements["button_patch_%d"%i].Hide()


			self.elements["scrollBar"] = ui.ScrollBar()
			self.elements["scrollBar"].SetParent(self.board)
			self.elements["scrollBar"].SetScrollBarSize(200)
			self.elements["scrollBar"].SetPosition(475,60)
			self.elements["scrollBar"].SetScrollEvent(self.__OnScroll)
			self.elements["scrollBar"].Show()

	def ClearPatchs(self):
		self.patch_info = []
		for i in xrange(0,MAX_COUNT):
			self.elements["button_patch_%d"%i].Hide()
			
	def LoadPatchs(self,version,descript):
		self.patch_info.append([version,descript])

	def LoadingPatchs(self):

		self.descriptionBox.Show()

		self.page_actual = self.FuncPagePatch()
		self.page_select = len(self.patch_info)-1

		self.LoadButtonPatch()
		self.LoadDescript()


	def SetButtonPatch(self,func,index=0):
		if func == "prev":
			if self.page_actual-1 < 0:
				return

			self.page_actual -= 1

			self.LoadButtonPatch()

		elif func == "next":
			if self.page_actual+1 > self.FuncPagePatch():
				return

			self.page_actual += 1
			self.LoadButtonPatch()

		elif func == "select":
			self.page_select = index+self.page_actual			
			self.__ClickRadioButton(index)
			self.LoadDescript()

	def CheckImg(self,index,i):

		if len(self.patch_info)-1 == index:
			self.elements["button_patch_%d"%i].SetUpVisual(PATCH_DESIGN+"btnnew_1.tga")
			self.elements["button_patch_%d"%i].SetOverVisual(PATCH_DESIGN+"btnnew_2.tga")
			self.elements["button_patch_%d"%i].SetDownVisual(PATCH_DESIGN+"btnnew_3.tga")
		else:
			self.elements["button_patch_%d"%i].SetUpVisual(PATCH_DESIGN+"btn_1.tga")
			self.elements["button_patch_%d"%i].SetOverVisual(PATCH_DESIGN+"btn_2.tga")
			self.elements["button_patch_%d"%i].SetDownVisual(PATCH_DESIGN+"btn_3.tga")	

	def LoadButtonPatch(self):
		self.SetUpRadioButton()

		for i in xrange(0,MAX_COUNT):
			if i < len(self.patch_info):
				index = i + self.page_actual


				self.CheckImg(index,i)

				if index == self.page_select:
					self.__ClickRadioButton(i)

				version = self.patch_info[index][0]
				self.elements["button_patch_%d"%i].SetText(version)
				self.elements["button_patch_%d"%i].Show()

	def LoadDescript(self):
		event.ClearEventSet(self.descIndex)
		descript = self.patch_info[self.page_select][1]

		self.descIndex = event.RegisterEventSetFromString(descript)

		event.SetVisibleLineCount(self.descIndex, MAX_LINES)
		event.SetRestrictedCount(self.descIndex,65)
		event.AllProcessEventSet(self.descIndex)

		self.ResetPos()

	def ResetPos(self):
		event.SetVisibleStartLine(self.descIndex, 0)
		self.pos_actual = self.desc_y
		self.pos = 0
		self.elements["scrollBar"].SetPos(0.0)

	def __OnScroll(self):
		count_lines = (event.GetProcessedLineCount(self.descIndex) - MAX_LINES)+1
		if count_lines <= 0:
			return 

		pos_select = int(self.elements["scrollBar"].GetPos()*count_lines)

		line_height			= event.GetLineHeight(self.descIndex)+4
		total_line_count	= event.GetVisibleStartLine(self.descIndex)

		if self.pos != pos_select:
			if pos_select > self.pos:
				if total_line_count <= event.GetProcessedLineCount(self.descIndex) - MAX_LINES:
					self.pos = pos_select
					event.SetVisibleStartLine(self.descIndex, pos_select)

			if pos_select < self.pos:
				if total_line_count > 0:
					self.pos = pos_select
					event.SetVisibleStartLine(self.descIndex, pos_select)

		self.pos_actual = self.desc_y - (line_height * total_line_count)


	def FuncPagePatch(self):
		count=len(self.patch_info)
		if count > MAX_COUNT:
			return len(self.patch_info)-MAX_COUNT
		
		return 0

	def __ClickRadioButton(self,buttonIndex):
		selButton=self.elements["button_patch_%d"%buttonIndex]

		self.SetUpRadioButton()
		selButton.Down()	

	def SetUpRadioButton(self):
		for x in xrange(0,MAX_COUNT):
			self.elements["button_patch_%d"%x].SetUp()

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.img_board.GetGlobalPosition()


		event.UpdateEventSet(self.descIndex, xposEventSet+17, -(yposEventSet+self.pos_actual))
		self.descriptionBox.SetIndex(self.descIndex)
		self.descriptionBox.SetTop()

	def Close(self):
		event.ClearEventSet(self.descIndex)
		self.descIndex = -1
		
		if self.descriptionBox:
			self.descriptionBox.Hide()

		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

