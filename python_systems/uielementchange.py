import app
import net
import player
import item
import ui
import uiToolTip
import mouseModule
import localeInfo
import uiCommon
import constInfo
import chat

class ElementsSpellChange(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False

		self.toolTip = uiToolTip.ItemToolTip()

	def __Initialize(self):
		self.itemPos = 0
		self.cost = 0
		self.itemType = 0
		self.typeSelect = -1

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refineelementchange.py")

		except:
			import exception
			exception.Abort("ElementsSpellChange.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.CancelChangeElements))

			self.ButtonsElements = []
			self.ButtonsElements.append([self.GetChild("FireButton"),item.APPLY_ATTBONUS_FIRE])
			self.ButtonsElements.append([self.GetChild("IceButton"),item.APPLY_ATTBONUS_ICE])
			self.ButtonsElements.append([self.GetChild("WindButton"),item.APPLY_ATTBONUS_WIND])
			self.ButtonsElements.append([self.GetChild("ElectButton"),item.APPLY_ATTBONUS_ELEC])
			self.ButtonsElements.append([self.GetChild("EarthButton"),item.APPLY_ATTBONUS_EARTH])
			self.ButtonsElements.append([self.GetChild("DarkButton"),item.APPLY_ATTBONUS_DARK])
			self.costText = self.GetChild("Cost")

		except:
			import exception
			exception.Abort("ElementsSpellChange.__LoadScript.BindObject")


		for i in xrange(0,len(self.ButtonsElements)):
			self.ButtonsElements[i][0].SetEvent(self.FuncSelect,i)

		self.GetChild("AcceptButton").SetEvent(self.AcceptChangeElements)
		self.GetChild("CancelButton").SetEvent(self.CancelChangeElements)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.itemPos = 0
		self.cost = 0
		self.itemType = 0
		self.typeSelect = -1

		self.board = 0

	def Close(self):
		self.Hide()

	def Open(self, itemPos, cost):

		if False == self.isLoaded:
			self.__LoadScript()

		self.__Initialize()

		self.itemPos = itemPos
		self.itemType = player.GetItemElementType(itemPos)
		self.cost = int(cost)
		self.typeSelect = self.itemType
		
		for i in xrange(0,len(self.ButtonsElements)):
			if self.ButtonsElements[i][1] == self.itemType:
				self.ButtonsElements[i][0].Disable()

		self.costText.SetText(localeInfo.DottedNumber(cost))

		self.SetTop()
		self.Show()

	def FuncSelect(self,index):
		self.__ClickRadioButton(index)

	def __ClickRadioButton(self, buttonIndex):
		selButton=self.ButtonsElements[buttonIndex][0]

		self.typeSelect = self.ButtonsElements[buttonIndex][1]

		for i in xrange(0,len(self.ButtonsElements)):
			if self.ButtonsElements[i][1] != self.itemType:
				self.ButtonsElements[i][0].SetUp()

		selButton.Down()


	def AcceptChangeElements(self):
		if  player.GetElk() < self.cost :
			chat.AppendChat(1,"Sorry, you don't have enough Yang.")
			self.CancelChangeElements()
			return

		if self.typeSelect <= 0:
			return

		if self.itemPos < 0:
			return

		if self.typeSelect == self.itemType:
			return

		net.ElementsSpellChange(self.itemPos,self.typeSelect)
		self.Close()

	def CancelChangeElements(self):
		net.ElementsSpellClose()
		self.Close()

	def OnPressEscapeKey(self):
		self.CancelChangeElements()
		return True