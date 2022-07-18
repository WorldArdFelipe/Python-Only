import dbg
import app
import net
import ui
import ime
import snd
import wndMgr
import musicInfo
import serverInfo
import systemSetting
import ServerStateChecker
import localeInfo
import constInfo
import uiCommon
import time
import ServerCommandParser
import ime
import uiScriptLocale

RUNUP_MATRIX_AUTH = FALSE
NEWCIBN_PASSPOD_AUTH = FALSE

LOGIN_DELAY_SEC = 0.0
SKIP_LOGIN_PHASE = FALSE
SKIP_LOGIN_PHASE_SUPPORT_CHANNEL = FALSE
FULL_BACK_IMAGE = FALSE

PASSPOD_MSG_DICT = {}

VIRTUAL_KEYBOARD_NUM_KEYS = 1
VIRTUAL_KEYBOARD_RAND_KEY = TRUE

def Suffle(src):
	if VIRTUAL_KEYBOARD_RAND_KEY:
		items = [item for item in src]

		itemCount = len(items)
		for oldPos in xrange(itemCount):
			newPos = itemCount-1
			items[newPos], items[oldPos] = items[oldPos], items[newPos]

		return "".join(items)
	else:
		return src

if localeInfo.IsNEWCIBN() or localeInfo.IsCIBN10():
	LOGIN_DELAY_SEC = 20.0
	FULL_BACK_IMAGE = TRUE
	NEWCIBN_PASSPOD_AUTH = TRUE
	PASSPOD_MSG_DICT = {
		"PASERR1"	: localeInfo.LOGIN_FAILURE_PASERR1,
		"PASERR2"	: localeInfo.LOGIN_FAILURE_PASERR2,
		"PASERR3"	: localeInfo.LOGIN_FAILURE_PASERR3,
		"PASERR4"	: localeInfo.LOGIN_FAILURE_PASERR4,
		"PASERR5"	: localeInfo.LOGIN_FAILURE_PASERR5,
	}

elif localeInfo.IsYMIR() or localeInfo.IsCHEONMA():
	FULL_BACK_IMAGE = TRUE

elif localeInfo.IsHONGKONG():
	FULL_BACK_IMAGE = TRUE
	RUNUP_MATRIX_AUTH = TRUE 
	PASSPOD_MSG_DICT = {
		"NOTELE"	: localeInfo.LOGIN_FAILURE_NOTELEBLOCK,
	}

elif localeInfo.IsJAPAN():
	FULL_BACK_IMAGE = TRUE

def IsFullBackImage():
	global FULL_BACK_IMAGE
	return FULL_BACK_IMAGE

def IsLoginDelay():
	global LOGIN_DELAY_SEC
	if LOGIN_DELAY_SEC > 0.0:
		return TRUE
	else:
		return FALSE

def IsRunupMatrixAuth():
	global RUNUP_MATRIX_AUTH
	return RUNUP_MATRIX_AUTH	

def IsNEWCIBNPassPodAuth():
	global NEWCIBN_PASSPOD_AUTH
	return NEWCIBN_PASSPOD_AUTH

def GetLoginDelay():
	global LOGIN_DELAY_SEC
	return LOGIN_DELAY_SEC

app.SetGuildMarkPath("test")

class ConnectingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()		

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("%.0f%s" % (waitTime, localeInfo.SECOND))

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
			self.SetCountDownMessage(self.endTime - time.clock())

	def OnPressExitKey(self):
		#self.eventExit()
		return TRUE

class LoginWindow(ui.ScriptWindow):

	IS_TEST = net.IsTest()

	def __init__(self, stream):
		print "NEW LOGIN WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		self.matrixInputChanceCount = 0
		self.lastLoginTime = 0
		self.inputDialog = None
		self.connectingDialog = None
		self.stream=stream
		self.isNowCountDown=FALSE
		self.isStartError=FALSE

		self.xServerBoard = 0
		self.yServerBoard = 0
		
		self.loadingImage = None

		self.virtualKeyboard = None
		self.virtualKeyboardMode = "ALPHABET"
		self.virtualKeyboardIsUpper = FALSE
		
	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE LOGIN WINDOW"

	def Open(self):
		ServerStateChecker.Create(self)

		print "LOGIN WINDOW OPEN ----------------------------------------------------------------------------"

		self.loginFailureMsgDict={
			#"DEFAULT" : locale.LOGIN_FAILURE_UNKNOWN,

			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: self.__DisconnectAndInputPassword,
			"WRONGMAT"	: self.__DisconnectAndInputMatrix,
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		if not self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "LoginWindow.py"):
			dbg.TraceError("LoginWindow.Open - __LoadScript Error")
			return
		
		self.__LoadLoginInfo("loginInfo.py")
		
		if app.loggined:
			self.loginFailureFuncDict = {
			"WRONGPWD"	: app.Exit,
			"WRONGMAT"	: app.Exit,
			"QUIT"		: app.Exit,
			}

		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		# pevent key "[" "]"
		ime.AddExceptKey(91)
		ime.AddExceptKey(93)
			
		self.Show()

		global SKIP_LOGIN_PHASE
		if SKIP_LOGIN_PHASE:
			if self.isStartError:
				self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.__ExitGame)
				return

			if self.loginInfo:
				return
			else:
				self.__RefreshServerList()
				self.__OpenServerBoard()
		else:
			connectingIP = self.stream.GetConnectAddr()
			if connectingIP:
				if app.USE_OPENID and not app.OPENID_TEST :
					self.__RefreshServerList()
					self.__OpenServerBoard()
				else:
					self.__OpenLoginBoard()
					if IsFullBackImage():
						self.GetChild("bg1").Hide()
						self.GetChild("bg2").Show()

			else:
				self.__RefreshServerList()
				self.__OpenServerBoard()

		app.ShowCursor()

	def Close(self):

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		ServerStateChecker.Initialize(self)

		print "---------------------------------------------------------------------------- CLOSE LOGIN WINDOW "
		#
		# selectMusicÀÌ ¾øÀ¸¸é BGMÀÌ ²÷±â¹Ç·Î µÎ°³ ´Ù Ã¼Å©ÇÑ´Ù. 
		#
		if musicInfo.loginMusic != "" and musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.loginMusic)

		## NOTE : idEditLine¿Í pwdEditLineÀº ÀÌº¥Æ®°¡ ¼­·Î ¿¬°á µÇ¾îÀÖ¾î¼­
		##        Event¸¦ °­Á¦·Î ÃÊ±âÈ­ ÇØÁÖ¾î¾ß¸¸ ÇÕ´Ï´Ù - [levites]
		self.idEditLine.SetTabEvent(0)
		self.idEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetTabEvent(0)

		self.idEditLine = None
		self.pwdEditLine = None
		self.inputDialog = None
		self.connectingDialog = None
		self.loadingImage = None
		self.serverList					= None
		self.channelList = None


		# RUNUP_MATRIX_AUTH
		self.matrixQuizBoard	= None
		self.matrixAnswerInput	= None
		self.matrixAnswerOK	= None
		self.matrixAnswerCancel	= None
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		self.passpodBoard	= None
		self.passpodAnswerInput	= None
		self.passpodAnswerOK	= None
		self.passpodAnswerCancel = None
		# NEWCIBN_PASSPOD_AUTH_END

		self.VIRTUAL_KEY_ALPHABET_LOWERS = None
		self.VIRTUAL_KEY_ALPHABET_UPPERS = None
		self.VIRTUAL_KEY_SYMBOLS = None
		self.VIRTUAL_KEY_NUMBERS = None

		# VIRTUAL_KEYBOARD_BUG_FIX
		if self.virtualKeyboard:
			for keyIndex in xrange(0, VIRTUAL_KEYBOARD_NUM_KEYS+1):
				key = self.GetChild2("key_%d" % keyIndex)
				if key:
					key.SetEvent(None)

			self.GetChild("key_space").SetEvent(None)
			self.GetChild("key_backspace").SetEvent(None)
			self.GetChild("key_enter").SetEvent(None)
			self.GetChild("key_shift").SetEvent(None)
		

			self.virtualKeyboard = None

		self.KillFocus()
		self.Hide()

		self.stream.popupWindow.Close()
		self.loginFailureFuncDict=None

		ime.ClearExceptKey()

		app.HideCursor()

	def __SaveChannelInfo(self):
		try:
			file=open("channel.inf", "w")
			file.write("%d %d %d" % (self.__GetServerID(), self.__GetChannelID(), self.__GetRegionID()))
		except:
			print "LoginWindow.__SaveChannelInfo - SaveError"

	def __LoadChannelInfo(self):
		try:
			file=open("channel.inf")
			lines=file.readlines()
			
			if len(lines)>0:
				tokens=lines[0].split()

				selServerID=int(tokens[0])
				selChannelID=int(tokens[1])
				
				if len(tokens) == 3:
					regionID = int(tokens[2])

				return regionID, selServerID, selChannelID

		except:
			print "LoginWindow.__LoadChannelInfo - OpenError"
			return -1, -1, -1

	def __ExitGame(self):
		app.Exit()

	def SetIDEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetFocus()

	def SetPasswordEditLineFocus(self):
		if localeInfo.IsEUROPE():
			if self.idEditLine != None: #0000862: [M2EU] ·Î±×ÀÎÃ¢ ÆË¾÷ ¿¡·¯: Á¾·á½Ã ¸ÕÀú None ¼³Á¤µÊ
				self.idEditLine.SetText("")
				self.idEditLine.SetFocus() #0000685: [M2EU] ¾ÆÀÌµð/ºñ¹Ð¹øÈ£ À¯Ãß °¡´É ¹ö±× ¼öÁ¤: ¹«Á¶°Ç ¾ÆÀÌµð·Î Æ÷Ä¿½º°¡ °¡°Ô ¸¸µç´Ù

			if self.pwdEditLine != None: #0000862: [M2EU] ·Î±×ÀÎÃ¢ ÆË¾÷ ¿¡·¯: Á¾·á½Ã ¸ÕÀú None ¼³Á¤µÊ
				self.pwdEditLine.SetText("")
		else:
			if self.pwdEditLine != None:
				self.pwdEditLine.SetFocus()								

	def OnEndCountDown(self):
		self.isNowCountDown = FALSE
		self.OnConnectFailure()

	def OnConnectFailure(self):

		if self.isNowCountDown:
			return

		snd.PlaySound("sound/ui/loginfail.wav")

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		if app.loggined:
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.__ExitGame)
		else:
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.SetPasswordEditLineFocus)

	def OnHandShake(self):
		if not IsLoginDelay():
			snd.PlaySound("sound/ui/loginok.wav")
			self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		if not IsLoginDelay():
			self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			if PASSPOD_MSG_DICT:
				try:
					loginFailureMsg = PASSPOD_MSG_DICT[error]
				except KeyError:
					loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN + error
			else:
				loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN  + error


		#0000685: [M2EU] ¾ÆÀÌµð/ºñ¹Ð¹øÈ£ À¯Ãß °¡´É ¹ö±× ¼öÁ¤: ¹«Á¶°Ç ÆÐ½º¿öµå·Î Æ÷Ä¿½º°¡ °¡°Ô ¸¸µç´Ù
		loginFailureFunc=self.loginFailureFuncDict.get(error, self.SetPasswordEditLineFocus)

		if app.loggined:
			self.PopupNotifyMessage(loginFailureMsg, self.__ExitGame)
		else:
			self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)

		snd.PlaySound("sound/ui/loginfail.wav")

	def __DisconnectAndInputID(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetIDEditLineFocus()
		net.Disconnect()

	def __DisconnectAndInputPassword(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetPasswordEditLineFocus()
		net.Disconnect()

	def __DisconnectAndInputMatrix(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.stream.popupWindow.Close()
		self.matrixInputChanceCount -= 1

		if self.matrixInputChanceCount <= 0:
			self.__OnCloseInputDialog()

		elif self.inputDialog:
			self.inputDialog.Show()

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "LoginWoG/loginwindow.py")
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")


		try:
			GetObject=self.GetChild
			self.BoardGuardado()
			self.channelboard = ui.BoardWithTitleBar()
			self.channelboard.SetParent(self)
			self.channelboard.SetSize(245, 80)
			self.channelboard.SetPosition((wndMgr.GetScreenWidth()- 290) / 2,(wndMgr.GetScreenHeight() -470)/2)
			self.channelboard.AddFlag("movable")
			self.channelboard.AddFlag("float")
			self.channelboard.SetTitleName("Seleccion Channel")
			self.channelboard.Hide()

			self.serverList = ui.ListBox2()
			self.serverList.SetParent(self.channelboard)
			self.serverList.SetPosition(10,40)
			self.serverList.SetSize(112, 171 + 180)
			self.serverList.SetRowCount(15)
			self.serverList.Show()

			self.channelList = ui.ListBox()
			self.channelList.SetParent(self.channelboard)
			self.channelList.SetPosition(125,40)
			self.channelList.SetSize(109, 171 + 180)
			self.channelList.Show()

			self.autoguardado = self.GetChild("auto_guardado") 
			self.autoguardado.SetEvent(ui.__mem_func__(self.AutoGuardado))


			self.selectConnectButton	= self.GetChild("start_button")
			self.closeConnectButton		= self.GetChild("Close")
			self.virtualKeyboard		= self.GetChild("VirtualKeyboard")
			self.idEditLine				= self.GetChild("name_input")
			self.button_teclado 		= self.GetChild("open_teclado")
			self.buttonchannel         	= self.GetChild	("select_channel")
			self.pwdEditLine			= self.GetChild("pass_input")

			self.idEditLine.SetFocus()			


			self.button_teclado.SetEvent(ui.__mem_func__(self.OpenTeclado))
			self.buttonchannel.SetEvent(ui.__mem_func__(self.OpenChannel))
			self.serverList.SetEvent(ui.__mem_func__(self.__OnSelectServer)) 
			self.selectConnectButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))
			self.closeConnectButton.SetEvent(ui.__mem_func__(self.__OnClickExitButton))
			self.virtualKeyboard.Hide()

			if localeInfo.IsVIETNAM():
				self.checkButton = GetObject("CheckButton")				
				self.checkButton.Down()
			
			# RUNUP_MATRIX_AUTH
			if IsRunupMatrixAuth():
				self.matrixQuizBoard	= GetObject("RunupMatrixQuizBoard")
				self.matrixAnswerInput	= GetObject("RunupMatrixAnswerInput")
				self.matrixAnswerOK	= GetObject("RunupMatrixAnswerOK")
				self.matrixAnswerCancel	= GetObject("RunupMatrixAnswerCancel")
			# RUNUP_MATRIX_AUTH_END

			# NEWCIBN_PASSPOD_AUTH
			if IsNEWCIBNPassPodAuth():
				self.passpodBoard	= GetObject("NEWCIBN_PASSPOD_BOARD")
				self.passpodAnswerInput	= GetObject("NEWCIBN_PASSPOD_INPUT")
				self.passpodAnswerOK	= GetObject("NEWCIBN_PASSPOD_OK")
				self.passpodAnswerCancel= GetObject("NEWCIBN_PASSPOD_CANCEL")
			# NEWCIBN_PASSPOD_AUTH_END

			self.virtualKeyboard		= self.GetChild2("VirtualKeyboard")

			

			if self.virtualKeyboard:
				self.VIRTUAL_KEY_ALPHABET_UPPERS = Suffle(localeInfo.VIRTUAL_KEY_ALPHABET_UPPERS)
				self.VIRTUAL_KEY_ALPHABET_LOWERS = "".join([localeInfo.VIRTUAL_KEY_ALPHABET_LOWERS[localeInfo.VIRTUAL_KEY_ALPHABET_UPPERS.index(e)] for e in self.VIRTUAL_KEY_ALPHABET_UPPERS])
				if localeInfo.IsBRAZIL():
					self.VIRTUAL_KEY_SYMBOLS_BR = Suffle(localeInfo.VIRTUAL_KEY_SYMBOLS_BR)
				else:
					self.VIRTUAL_KEY_SYMBOLS = Suffle(localeInfo.VIRTUAL_KEY_SYMBOLS)
				self.VIRTUAL_KEY_NUMBERS = Suffle(localeInfo.VIRTUAL_KEY_NUMBERS)
				self.__VirtualKeyboard_SetAlphabetMode()
			
				self.GetChild("key_space").SetEvent(lambda : self.__VirtualKeyboard_PressKey(' '))
				self.GetChild("key_backspace").SetEvent(lambda : self.__VirtualKeyboard_PressBackspace())
				self.GetChild("key_enter").SetEvent(lambda : self.__VirtualKeyboard_PressReturn())
				self.GetChild("key_shift").SetToggleDownEvent(lambda : self.__VirtualKeyboard_SetUpperMode())
				self.GetChild("key_shift").SetToggleUpEvent(lambda : self.__VirtualKeyboard_SetLowerMode())
				
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

	
		
		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))

		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))

		# RUNUP_MATRIX_AUTH
		if IsRunupMatrixAuth():			
			self.matrixAnswerOK.SAFE_SetEvent(self.__OnClickMatrixAnswerOK)
			self.matrixAnswerCancel.SAFE_SetEvent(self.__OnClickMatrixAnswerCancel)
			self.matrixAnswerInput.SAFE_SetReturnEvent(self.__OnClickMatrixAnswerOK)
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		if IsNEWCIBNPassPodAuth():
			self.passpodAnswerOK.SAFE_SetEvent(self.__OnClickNEWCIBNPasspodAnswerOK)
			self.passpodAnswerCancel.SAFE_SetEvent(self.__OnClickNEWCIBNPasspodAnswerCancel)
			self.passpodAnswerInput.SAFE_SetReturnEvent(self.__OnClickNEWCIBNPasspodAnswerOK)

		# NEWCIBN_PASSPOD_AUTH_END


		if IsFullBackImage():
			self.GetChild("bg1").Show()
			self.GetChild("bg2").Hide()
		return 1

	def BoardGuardado(self):
		self.BoardG = ui.BoardWithTitleBar()
		self.BoardG.SetParent(self)
		self.BoardG.SetSize(245, 140)
		self.BoardG.SetPosition((wndMgr.GetScreenWidth()- 290) / 2,(wndMgr.GetScreenHeight() -570)/2)
		self.BoardG.AddFlag("movable")
		self.BoardG.AddFlag("float")
		self.BoardG.SetTitleName("Auto Guardado")
		self.BoardG.Hide()

		self.Count,Number = {},1
		position = [[20,35],[20,35+25],[20,35+25+25],[20,35+25+25+25]]
		for i in position:
			self.Count[str(Number)] = ui.TextLine()
			self.Count[str(Number)].SetParent(self.BoardG)
			self.Count[str(Number)].SetPosition(i[0],i[1])
			self.Count[str(Number)].Show()
			Number +=1

		self.ButtonAceptar,Number1 = {},1
		position = [[133,33],[133,33+25],[133,33+25+25],[133,33+25+25+25]]
		for i1 in position:
			self.ButtonAceptar[str(Number1)] = ui.Button()
			self.ButtonAceptar[str(Number1)].SetParent(self.BoardG)
			self.ButtonAceptar[str(Number1)].SetPosition(i1[0],i1[1])
			self.ButtonAceptar[str(Number1)].SetUpVisual("d:/ymir work/ui/game/windows/tab_button_small_01.sub")
			self.ButtonAceptar[str(Number1)].SetOverVisual("d:/ymir work/ui/game/windows/tab_button_small_02.sub")
			self.ButtonAceptar[str(Number1)].SetDownVisual("d:/ymir work/ui/game/windows/tab_button_small_03.sub")
			self.ButtonAceptar[str(Number1)].SetText("OK")
			self.ButtonAceptar[str(Number1)].SetEvent(self.__AceptarG,str(Number1))
			self.ButtonAceptar[str(Number1)].Show()
			Number1 +=1

		self.ButtonEdit,Number3 = {},1
		position3 = [[153+12,33],[153+12,33+25],[153+12,33+25+25],[153+12,33+25+25+25]]
		for i3 in position3:
			self.ButtonEdit[str(Number3)] = ui.Button()
			self.ButtonEdit[str(Number3)].SetParent(self.BoardG)
			self.ButtonEdit[str(Number3)].SetPosition(i3[0],i3[1])
			self.ButtonEdit[str(Number3)].SetUpVisual("d:/ymir work/ui/game/windows/tab_button_small_01.sub")
			self.ButtonEdit[str(Number3)].SetOverVisual("d:/ymir work/ui/game/windows/tab_button_small_02.sub")
			self.ButtonEdit[str(Number3)].SetDownVisual("d:/ymir work/ui/game/windows/tab_button_small_03.sub")
			self.ButtonEdit[str(Number3)].SetText("Edit")
			self.ButtonEdit[str(Number3)].SetEvent(self.__EditSave,str(Number3))
			self.ButtonEdit[str(Number3)].Show()
			Number3 +=1

		self.ButtonBorrar,Number2 = {},1
		position1 = [[153+32+12,33],[153+32+12,33+25],[153+32+12,33+25+25],[153+32+12,33+25+25+25]]
		for i2 in position1:
			self.ButtonBorrar[str(Number2)] = ui.Button()
			self.ButtonBorrar[str(Number2)].SetParent(self.BoardG)
			self.ButtonBorrar[str(Number2)].SetPosition(i2[0],i2[1])
			self.ButtonBorrar[str(Number2)].SetUpVisual("d:/ymir work/ui/game/windows/tab_button_small_01.sub")
			self.ButtonBorrar[str(Number2)].SetOverVisual("d:/ymir work/ui/game/windows/tab_button_small_02.sub")
			self.ButtonBorrar[str(Number2)].SetDownVisual("d:/ymir work/ui/game/windows/tab_button_small_03.sub")
			self.ButtonBorrar[str(Number2)].SetText("Borrar")
			self.ButtonBorrar[str(Number2)].SetEvent(self.__Borrar,str(Number2))
			self.ButtonBorrar[str(Number2)].Show()
			Number2 +=1

		self.__accdata()

	def __AceptarG(self,number312):
		import dbg
		fo = open("Save/login"+str(number312), "r") 
		liste = fo.readlines() 
		iD = liste[0].replace("id:","").replace("\n","")
		PW = liste[1].replace("pw:","")
		self.idEditLine.SetText(iD) 
		self.pwdEditLine.SetText(PW)
		self.__OnClickLoginButton()
		fo.close()

	def __accdata(self): 
		for i in xrange(1,5):
			fo = open("Save/login"+str(i), "r") 
			liste = fo.readlines() 
			ID = liste[0].replace("id:","").replace("\n","") 
			PW = liste[1].replace("pw:","") 
			self.Count[str(i)].SetText(ID) 
			fo.close()

	def __Borrar(self,number1):
		fo = open("Save/login"+str(number1), "w") 
		fo.write("id:"+""+"\npw:"+"")
		fo.close() 

	def __EditSave(self,number2):
		self.BoardG.Hide()
		self.BoardEdit = ui.BoardWithTitleBar()
		self.BoardEdit.SetParent(self)
		self.BoardEdit.SetSize(185, 140)
		self.BoardEdit.SetPosition((wndMgr.GetScreenWidth()- 230) / 2,(wndMgr.GetScreenHeight() -570)/2)
		self.BoardEdit.AddFlag("movable")
		self.BoardEdit.AddFlag("float")
		self.BoardEdit.SetTitleName("Edit Guardado "+str(number2))
		self.BoardEdit.Show()

		self.SlotEdit = ui.ImageBox()
		self.SlotEdit.SetParent(self.BoardEdit)
		self.SlotEdit.LoadImage("d:/ymir work/ui/public/Parameter_Slot_04.sub")
		self.SlotEdit.SetPosition(16, 32)
		self.SlotEdit.Show()

		self.EditLineAccount = ui.EditLine()
		self.EditLineAccount.SetParent(self.SlotEdit)
		self.EditLineAccount.SetPosition(3,2)
		self.EditLineAccount.SetSize(111, 40)
		self.EditLineAccount.SetMax(17)
		self.EditLineAccount.SetText("Account")
		self.EditLineAccount.Show()

		self.SlotEdit1 = ui.ImageBox()
		self.SlotEdit1.SetParent(self.BoardEdit)
		self.SlotEdit1.LoadImage("d:/ymir work/ui/public/Parameter_Slot_04.sub")
		self.SlotEdit1.SetPosition(16, 32+32)
		self.SlotEdit1.Show()

		self.EditLinePass = ui.EditLine()
		self.EditLinePass.SetParent(self.SlotEdit1)
		self.EditLinePass.SetPosition(3,2)
		self.EditLinePass.SetSize(111, 40)
		self.EditLinePass.SetMax(17)
		self.EditLinePass.SetText("Password")
		self.EditLinePass.SetSecret(1)
		self.EditLinePass.Show()

		self.ButtonAcepEdit = ui.Button()
		self.ButtonAcepEdit.SetParent(self.BoardEdit)
		self.ButtonAcepEdit.SetPosition(11+131, 32+17)
		self.ButtonAcepEdit.SetUpVisual("d:/ymir work/ui/game/windows/tab_button_small_01.sub")
		self.ButtonAcepEdit.SetOverVisual("d:/ymir work/ui/game/windows/tab_button_small_02.sub")
		self.ButtonAcepEdit.SetDownVisual("d:/ymir work/ui/game/windows/tab_button_small_03.sub")
		self.ButtonAcepEdit.SetText("OK")
		self.ButtonAcepEdit.SetEvent(self.__OkEdit,number2)
		self.ButtonAcepEdit.Show()

	def __OkEdit(self,number32):
		fo = open("Save/login"+str(number32), "w") 
		fo.write("id:"+self.EditLineAccount.GetText()+"\npw:"+self.EditLinePass.GetText())
		fo.close()  
		self.BoardG.Show()
		self.BoardEdit.Hide()

	def AutoGuardado(self):
		if self.BoardG.IsShow():
			self.BoardG.Hide()
		else:
			if self.channelboard.IsShow():
				self.channelboard.Hide()
			if self.virtualKeyboard.IsShow():
				self.virtualKeyboard.Hide()
			self.BoardG.Show()

	def OpenTeclado(self):
		if self.virtualKeyboard.IsShow():
			self.virtualKeyboard.Hide()
		else:
			if self.channelboard.IsShow():
				self.channelboard.Hide()
			if self.BoardG.IsShow():
				self.BoardG.Hide()
			self.virtualKeyboard.Show()

	def OpenChannel(self):
		self.__RefreshServerStateList()
		if self.channelboard.IsShow():
			self.channelboard.Hide()
		else:
			if self.virtualKeyboard.IsShow():
				self.virtualKeyboard.Hide()
			if self.BoardG.IsShow():
				self.BoardG.Hide()
			self.channelboard.Show()

	def __VirtualKeyboard_SetKeys(self, keyCodes):
		uiDefFontBackup = localeInfo.UI_DEF_FONT
		localeInfo.UI_DEF_FONT = localeInfo.UI_DEF_FONT_LARGE

		keyIndex = 1
		for keyCode in keyCodes:					
			key = self.GetChild2("key_%d" % keyIndex)
			if key:
				key.SetEvent(lambda x=keyCode: self.__VirtualKeyboard_PressKey(x))
				key.SetText(keyCode)
				key.ButtonText.SetFontColor(1, 1, 1)
				keyIndex += 1
			
		for keyIndex in xrange(keyIndex, VIRTUAL_KEYBOARD_NUM_KEYS+1):
			key = self.GetChild2("key_%d" % keyIndex)
			if key:
				key.SetEvent(lambda x=' ': self.__VirtualKeyboard_PressKey(x))
				key.SetText(' ')
		
		localeInfo.UI_DEF_FONT = uiDefFontBackup

	def __VirtualKeyboard_PressKey(self, code):
		ime.PasteString(code)
		
		#if self.virtualKeyboardMode == "ALPHABET" and self.virtualKeyboardIsUpper:
		#	self.__VirtualKeyboard_SetLowerMode()
			
	def __VirtualKeyboard_PressBackspace(self):
		ime.PasteBackspace()
		
	def __VirtualKeyboard_PressReturn(self):
		ime.PasteReturn()		

	def __VirtualKeyboard_SetUpperMode(self):
		self.virtualKeyboardIsUpper = TRUE
		
		if self.virtualKeyboardMode == "ALPHABET":
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_ALPHABET_UPPERS)
		elif self.virtualKeyboardMode == "NUMBER":
			if localeInfo.IsBRAZIL():
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS_BR)
			else:	
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS)
		else:
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_NUMBERS)
			
	def __VirtualKeyboard_SetLowerMode(self):
		self.virtualKeyboardIsUpper = FALSE
		
		if self.virtualKeyboardMode == "ALPHABET":
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_ALPHABET_LOWERS)
		elif self.virtualKeyboardMode == "NUMBER":
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_NUMBERS)			
		else:
			if localeInfo.IsBRAZIL():
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS_BR)
			else:	
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS)
			
	def __VirtualKeyboard_SetAlphabetMode(self):
		self.virtualKeyboardIsUpper = FALSE
		self.virtualKeyboardMode = "ALPHABET"		
		self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_ALPHABET_LOWERS)	

	def __VirtualKeyboard_SetNumberMode(self):			
		self.virtualKeyboardIsUpper = FALSE
		self.virtualKeyboardMode = "NUMBER"
		self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_NUMBERS)
					
	def __VirtualKeyboard_SetSymbolMode(self):		
		self.virtualKeyboardIsUpper = FALSE
		self.virtualKeyboardMode = "SYMBOL"
		if localeInfo.IsBRAZIL():
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS_BR)
		else:	
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS)
				
	def Connect(self, id, pwd):

		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()

		if IsLoginDelay():
			loginDelay = GetLoginDelay()
			self.connectingDialog = ConnectingDialog()
			self.connectingDialog.Open(loginDelay)
			self.connectingDialog.SAFE_SetTimeOverEvent(self.OnEndCountDown)
			self.connectingDialog.SAFE_SetExitEvent(self.OnPressExitKey)
			self.isNowCountDown = TRUE

		else:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, self.SetPasswordEditLineFocus, localeInfo.UI_CANCEL)

		self.stream.SetLoginInfo(id, pwd)
		self.stream.Connect()

	def __OnClickExitButton(self):
		self.stream.SetPhaseWindow(0)

	def __SetServerInfo(self, name):
		net.SetServerInfo(name.strip())


	def __LoadLoginInfo(self, loginInfoFileName):

		try:
			loginInfo={}
			execfile(loginInfoFileName, loginInfo)
		except IOError:
			print(\
				"ÀÚµ¿ ·Î±×ÀÎÀ» ÇÏ½Ã·Á¸é" + loginInfoFileName + "ÆÄÀÏÀ» ÀÛ¼ºÇØÁÖ¼¼¿ä\n"\
				"\n"\
				"³»¿ë:\n"\
				"================================================================\n"\
				"addr=ÁÖ¼Ò\n"\
				"port=Æ÷Æ®\n"\
				"id=¾ÆÀÌµð\n"\
				"pwd=ºñ¹Ð¹øÈ£\n"\
				"slot=Ä³¸¯ÅÍ ¼±ÅÃ ÀÎµ¦½º (¾ø°Å³ª -1ÀÌ¸é ÀÚµ¿ ¼±ÅÃ ¾ÈÇÔ)\n"\
				"autoLogin=ÀÚµ¿ Á¢¼Ó ¿©ºÎ\n"
				"autoSelect=ÀÚµ¿ Á¢¼Ó ¿©ºÎ\n"
				"localeInfo=(ymir) LC_Ymir ÀÏ°æ¿ì ymir·Î ÀÛµ¿. ÁöÁ¤ÇÏÁö ¾ÊÀ¸¸é korea·Î ÀÛµ¿\n"
			);

		id=loginInfo.get("id", "")
		pwd=loginInfo.get("pwd", "")

		if self.IS_TEST:
			try:
				addr=loginInfo["addr"]
				port=loginInfo["port"]
				account_addr=addr
				account_port=port

				net.SetMarkServer(addr, port)
				self.__SetServerInfo(localeInfo.CHANNEL_TEST_SERVER_ADDR % (addr, port))
			except:
				try:
					addr=serverInfo.TESTADDR["ip"]
					port=serverInfo.TESTADDR["tcp_port"]

					net.SetMarkServer(addr, port)
					self.__SetServerInfo(localeInfo.CHANNEL_TEST_SERVER)
				except:
					import exception
					exception.Abort("LoginWindow.__LoadLoginInfo - Å×½ºÆ®¼­¹ö ÁÖ¼Ò°¡ ¾ø½À´Ï´Ù")

		else:
			addr=loginInfo.get("addr", "")
			port=loginInfo.get("port", 0)
			account_addr=loginInfo.get("account_addr", addr)
			account_port=loginInfo.get("account_port", port)

			localeInfo = loginInfo.get("localeInfo", "")

			if addr and port:
				net.SetMarkServer(addr, port)

				if localeInfo == "ymir" :
					net.SetServerInfo("Ãµ¸¶ ¼­¹ö")
				else:
					net.SetServerInfo(addr+":"+str(port))

		slot=loginInfo.get("slot", 0)
		isAutoLogin=loginInfo.get("auto", 0)
		isAutoLogin=loginInfo.get("autoLogin", 0)
		isAutoSelect=loginInfo.get("autoSelect", 0)

		self.stream.SetCharacterSlot(slot)
		self.stream.SetConnectInfo(addr, port, account_addr, account_port)
		self.stream.isAutoLogin=isAutoLogin
		self.stream.isAutoSelect=isAutoSelect

		self.id = None
		self.pwd = None		
		self.loginnedServer = None
		self.loginnedChannel = None			
		app.loggined = FALSE

		self.loginInfo = loginInfo

		if self.id and self.pwd:
			app.loggined = TRUE

		if isAutoLogin:
			self.Connect(id, pwd)
			
			print "=================================================================================="
			print "ÀÚµ¿ ·Î±×ÀÎ: %s - %s:%d %s" % (loginInfoFileName, addr, port, id)
			print "=================================================================================="

		
	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	# RUNUP_MATRIX_AUTH
	def BINARY_OnRunupMatrixQuiz(self, quiz):
		if not IsRunupMatrixAuth():
			return

		id		= self.GetChild("RunupMatrixID")
		id.SetText(self.idEditLine.GetText())
		
		code	= self.GetChild("RunupMatrixCode")
		
		code.SetText("".join(["[%c,%c]" % (quiz[i], quiz[i+1]) for i in xrange(0, len(quiz), 2)]))

		self.stream.popupWindow.Close()
		self.matrixQuizBoard.Show()
		self.matrixAnswerInput.SetFocus()

	def __OnClickMatrixAnswerOK(self):
		answer = self.matrixAnswerInput.GetText()

		print "matrix_quiz.ok"
		net.SendRunupMatrixCardPacket(answer)
		self.matrixQuizBoard.Hide()	

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open("WAITING FOR MATRIX AUTHENTICATION", 
			self.__OnClickMatrixAnswerCancel, 
			localeInfo.UI_CANCEL)

	def __OnClickMatrixAnswerCancel(self):
		print "matrix_quiz.cancel"

		if self.matrixQuizBoard:
			self.matrixQuizBoard.Hide()	



	# RUNUP_MATRIX_AUTH_END

	# NEWCIBN_PASSPOD_AUTH
	def BINARY_OnNEWCIBNPasspodRequest(self):
		if not IsNEWCIBNPassPodAuth():
			return

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.stream.popupWindow.Close()
		self.passpodBoard.Show()
		self.passpodAnswerInput.SetFocus()

	def BINARY_OnNEWCIBNPasspodFailure(self):
		if not IsNEWCIBNPassPodAuth():
			return

	def __OnClickNEWCIBNPasspodAnswerOK(self):
		answer = self.passpodAnswerInput.GetText()

		print "passpod.ok"
		net.SendNEWCIBNPasspodAnswerPacket(answer)
		self.passpodAnswerInput.SetText("")
		self.passpodBoard.Hide()	

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.WAIT_FOR_PASSPOD, 
			self.__OnClickNEWCIBNPasspodAnswerCancel, 
			localeInfo.UI_CANCEL)

	def __OnClickNEWCIBNPasspodAnswerCancel(self):
		print "passpod.cancel"

		if self.passpodBoard:
			self.passpodBoard.Hide()	
	


	# NEWCIBN_PASSPOD_AUTH_END


	def OnMatrixCard(self, row1, row2, row3, row4, col1, col2, col3, col4):

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.matrixInputChanceCount = 3

		self.stream.popupWindow.Close()

		# CHINA_MATRIX_CARD_BUG_FIX
		## A~Z ±îÁö 26 ÀÌ³»ÀÇ °ªÀÌ µé¾îÀÖ¾î¾ß¸¸ ÇÑ´Ù.
		## Python Exception Log ¿¡¼­ ±× ÀÌ»óÀÇ °ªÀÌ µé¾îÀÖ¾î¼­ ¿¡·¯ ¹æÁö
		## Çåµ¥ ¿Ö ÇÑ±¹ÂÊ ·Î±×¿¡¼­ ÀÌ°Ô È°¿ëµÇ´ÂÁö´Â ¸ð¸£°ÚÀ½
		row1 = min(30, row1)
		row2 = min(30, row2)
		row3 = min(30, row3)
		row4 = min(30, row4)
		# END_OF_CHINA_MATRIX_CARD_BUG_FIX

		row1 = chr(row1 + ord('A'))
		row2 = chr(row2 + ord('A'))
		row3 = chr(row3 + ord('A'))
		row4 = chr(row4 + ord('A'))
		col1 = col1 + 1
		col2 = col2 + 1
		col3 = col3 + 1
		col4 = col4 + 1

		inputDialog = uiCommon.InputDialogWithDescription2()
		inputDialog.SetMaxLength(8)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.__OnAcceptMatrixCardData))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.__OnCancelMatrixCardData))
		inputDialog.SetTitle(localeInfo.INPUT_MATRIX_CARD_TITLE)
		inputDialog.SetDescription1(localeInfo.INPUT_MATRIX_CARD_NUMBER)
		inputDialog.SetDescription2("%c%d %c%d %c%d %c%d" % (row1, col1,
															row2, col2,
															row3, col3,
															row4, col4))

		inputDialog.Open()
		self.inputDialog = inputDialog

	def __OnAcceptMatrixCardData(self):
		text = self.inputDialog.GetText()
		net.SendChinaMatrixCardPacket(text)
		if self.inputDialog:
			self.inputDialog.Hide()
		self.PopupNotifyMessage(localeInfo.LOGIN_PROCESSING)
		return TRUE

	def __OnCancelMatrixCardData(self):
		self.SetPasswordEditLineFocus()
		self.__OnCloseInputDialog()
		self.__DisconnectAndInputPassword()
		return TRUE

	def __OnCloseInputDialog(self):
		if self.inputDialog:
			self.inputDialog.Close()
		self.inputDialog = None
		return TRUE

	def OnPressExitKey(self):
		self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return TRUE

	def OnExit(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE, app.Exit, localeInfo.UI_OK)

	def OnUpdate(self):
		ServerStateChecker.Update()
		for i in xrange(1,5):
			fo = open("Save/login"+str(i), "r") 
			liste = fo.readlines() 
			ID = liste[0].replace("id:","").replace("\n","") 
			PW = liste[1].replace("pw:","") 
			self.Count[str(i)].SetText(ID) 
			fo.close()

			x = self.Count[str(i)].GetText()
			if len(x) ==0:
				self.ButtonBorrar[str(i)].Hide()
				self.ButtonAceptar[str(i)].Hide()
				self.Count[str(i)].SetText("Vacio")
			else:
				self.ButtonBorrar[str(i)].Show()
				self.ButtonAceptar[str(i)].Show()

	def EmptyFunc(self):
		pass

	#####################################################################################

	def __ServerBoard_OnKeyUp(self, key):
		return TRUE

	def __GetRegionID(self):
		return 0

	def __GetServerID(self):
		return self.serverList.GetSelectedItem()
	def __GetChannelID(self):
		return self.channelList.GetSelectedItem()

	# SEVER_LIST_BUG_FIX
	def __ServerIDToServerIndex(self, regionID, targetServerID):
		try:
			regionDict = serverInfo.REGION_DICT[regionID]
		except KeyError:
			return -1

		retServerIndex = 0
		for eachServerID, regionDataDict in regionDict.items():
			if eachServerID == targetServerID:
				return retServerIndex

			retServerIndex += 1		
		
		return -1

	def __ChannelIDToChannelIndex(self, channelID):
		return channelID - 1
	# END_OF_SEVER_LIST_BUG_FIX

	def __OpenServerBoard(self):

		loadRegionID, loadServerID, loadChannelID = self.__LoadChannelInfo()
		
		serverIndex = self.__ServerIDToServerIndex(loadRegionID, loadServerID)
		channelIndex = self.__ChannelIDToChannelIndex(loadChannelID)
		
		# RUNUP_MATRIX_AUTH
		if IsRunupMatrixAuth():
			self.matrixQuizBoard.Hide()
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		if IsNEWCIBNPassPodAuth():
			self.passpodBoard.Hide()
		# NEWCIBN_PASSPOD_AUTH_END

		self.serverList.SelectItem(serverIndex)

		if localeInfo.IsEUROPE():
			self.channelList.SelectItem(app.GetRandom(0, self.channelList.GetItemCount()))
		else:
			if channelIndex >= 0:
				self.channelList.SelectItem(channelIndex)

		
		## Show/Hide ÄÚµå¿¡ ¹®Á¦°¡ ÀÖ¾î¼­ ÀÓ½Ã - [levites]

		if self.virtualKeyboard:
			self.virtualKeyboard.Hide()

		if app.loggined and not SKIP_LOGIN_PHASE_SUPPORT_CHANNEL:
			self.serverList.SelectItem(self.loginnedServer-1)
			self.channelList.SelectItem(self.loginnedChannel-1)
			self.__OnClickSelectServerButton()


	def __OpenLoginBoard(self):


		# RUNUP_MATRIX_AUTH
		if IsRunupMatrixAuth():
			self.matrixQuizBoard.Hide()
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		if IsNEWCIBNPassPodAuth():
			self.passpodBoard.Hide()
		# NEWCIBN_PASSPOD_AUTH_END


		## if users have the login infomation, then don't initialize.2005.9 haho
		if self.idEditLine == None:
			self.idEditLine.SetText("")
		if self.pwdEditLine == None:
			self.pwdEditLine.SetText("")

		self.idEditLine.SetFocus()

	

	def __OnSelectRegionGroup(self):
		self.__RefreshServerList()

	def __OnSelectSettlementArea(self):
		# SEVER_LIST_BUG_FIX
		regionID = self.__GetRegionID()
		serverID = self.serverListOnRegionBoard.GetSelectedItem()

		serverIndex = self.__ServerIDToServerIndex(regionID, serverID)
		self.serverList.SelectItem(serverIndex)
		
		self.__OnSelectServer()

	def __RefreshServerList(self):
		regionID = self.__GetRegionID()
		
		if not serverInfo.REGION_DICT.has_key(regionID):
			return

		self.serverList.ClearItem()


		regionDict = serverInfo.REGION_DICT[regionID]

		visible_index = 1
		for id, regionDataDict in regionDict.items():
			name = regionDataDict.get("name", "noname")
			if localeInfo.IsBRAZIL() or localeInfo.IsCANADA():
				self.serverList.InsertItem(id, "%s" % (name))
			else:
				if localeInfo.IsCIBN10():			
					if name[0] == "#":
						self.serverList.InsertItem(-1, "  %s" % (name[1:]))
					else:
						self.serverList.InsertItem(id, "  %s" % (name))
						visible_index += 1
				else:
					try:
						server_id = serverInfo.SERVER_ID_DICT[id]
					except:
						server_id = visible_index

					self.serverList.InsertItem(id, "  %02d. %s" % (int(server_id), name))
					
					visible_index += 1

		

	def __OnSelectServer(self):
		self.__OnCloseInputDialog()
		self.__RequestServerStateList()
		self.__RefreshServerStateList()

	def __RequestServerStateList(self):
		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except:
			print " __RequestServerStateList - serverInfo.REGION_DICT(%d, %d)" % (regionID, serverID)
			return

		ServerStateChecker.Initialize();
		for id, channelDataDict in channelDict.items():
			key=channelDataDict["key"]
			ip=channelDataDict["ip"]
			udp_port=channelDataDict["udp_port"]
			ServerStateChecker.AddChannel(key, ip, udp_port)

		ServerStateChecker.Request()

	def __RefreshServerStateList(self):

		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()
		bakChannelID = self.channelList.GetSelectedItem()

		self.channelList.ClearItem()


		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except:
			print " __RequestServerStateList - serverInfo.REGION_DICT(%d, %d)" % (regionID, serverID)
			return

		for channelID, channelDataDict in channelDict.items():
			channelName = channelDataDict["name"]
			channelState = channelDataDict["state"]
			self.channelList.InsertItem(channelID, " %s %s" % (channelName, channelState))

		self.channelList.SelectItem(bakChannelID-1)


	def __GetChannelName(self, regionID, selServerID, selChannelID):
		try:
			return serverInfo.REGION_DICT[regionID][selServerID]["channel"][selChannelID]["name"]
		except KeyError:
			if 9==selChannelID:
				return localeInfo.CHANNEL_PVP
			else:
				return localeInfo.CHANNEL_NORMAL % (selChannelID)

	def NotifyChannelState(self, addrKey, state):
		try:
			stateName=serverInfo.STATE_DICT[state]
		except:
			stateName=serverInfo.STATE_NONE

		regionID=int(addrKey/1000)
		serverID=int(addrKey/10) % 100
		channelID=addrKey%10

		try:
			serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["state"] = stateName
			#self.__RefreshServerStateList()

		except:
			import exception
			exception.Abort(localeInfo.CHANNEL_NOT_FIND_INFO)

	def __OnClickExitServerButton(self):
		print "exit server"
		self.__OpenLoginBoard()			

		if IsFullBackImage():
			self.GetChild("bg1").Hide()
			self.GetChild("bg2").Show()
			

	def __OnClickSelectRegionButton(self):
		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()

		if (not serverInfo.REGION_DICT.has_key(regionID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_REGION)
			return

		if (not serverInfo.REGION_DICT[regionID].has_key(serverID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_SERVER)
			return		

		self.__SaveChannelInfo()


		self.__RefreshServerList()
		self.__OpenServerBoard()

	def __OnClickSelectServerButton(self):
		if IsFullBackImage():
			self.GetChild("bg1").Hide()
			self.GetChild("bg2").Show()

		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()
		channelID = self.__GetChannelID()

		if (not serverInfo.REGION_DICT.has_key(regionID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_REGION)
			return

		if (not serverInfo.REGION_DICT[regionID].has_key(serverID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_SERVER)
			return

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except KeyError:
			return

		try:
			state = channelDict[channelID]["state"]
		except KeyError:
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_CHANNEL)
			return

		# »óÅÂ°¡ FULL °ú °°À¸¸é ÁøÀÔ ±ÝÁö
		if state == serverInfo.STATE_DICT[3]: 
			self.PopupNotifyMessage(localeInfo.CHANNEL_NOTIFY_FULL)
			return

		self.__SaveChannelInfo()

		try:
			serverName = serverInfo.REGION_DICT[regionID][serverID]["name"]
			channelName = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["name"]
			addrKey = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["key"]
			
			if "Ãµ¸¶ ¼­¹ö" == serverName:			
				app.ForceSetlocaleInfo("ymir", "localeInfo/ymir")
			elif "Äèµµ ¼­¹ö" == serverName:			
				app.ForceSetlocaleInfo("we_korea", "localeInfo/we_korea")				
				
		except:
			print " ERROR __OnClickSelectServerButton(%d, %d, %d)" % (regionID, serverID, channelID)
			serverName = localeInfo.CHANNEL_EMPTY_SERVER
			channelName = localeInfo.CHANNEL_NORMAL % channelID

		self.__SetServerInfo("%s, %s " % (serverName, channelName))

		try:
			ip = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["ip"]
			tcp_port = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["tcp_port"]
		except:
			import exception
			exception.Abort("LoginWindow.__OnClickSelectServerButton - ¼­¹ö ¼±ÅÃ ½ÇÆÐ")

		try:
			account_ip = serverInfo.REGION_AUTH_SERVER_DICT[regionID][serverID]["ip"]
			account_port = serverInfo.REGION_AUTH_SERVER_DICT[regionID][serverID]["port"]
		except:
			account_ip = 0
			account_port = 0

		try:
			markKey = regionID*1000 + serverID*10
			markAddrValue=serverInfo.MARKADDR_DICT[markKey]
			net.SetMarkServer(markAddrValue["ip"], markAddrValue["tcp_port"])
			app.SetGuildMarkPath(markAddrValue["mark"])
			# GUILD_SYMBOL
			app.SetGuildSymbolPath(markAddrValue["symbol_path"])
			# END_OF_GUILD_SYMBOL

		except:
			import exception
			exception.Abort("LoginWindow.__OnClickSelectServerButton - ¸¶Å© Á¤º¸ ¾øÀ½")


		if app.USE_OPENID and not app.OPENID_TEST :
			## 2012.07.19 OpenID : ±è¿ë¿í
			# Ã¤³Î ¼±ÅÃ È­¸é¿¡¼­ "È®ÀÎ"(SelectServerButton) À» ´­·¶À»¶§,
			# ·Î±×ÀÎ È­¸éÀ¸·Î ³Ñ¾î°¡Áö ¾Ê°í ¹Ù·Î ¼­¹ö¿¡ OpenID ÀÎÁõÅ°¸¦ º¸³»µµ·Ï ¼öÁ¤
			self.stream.SetConnectInfo(ip, tcp_port, account_ip, account_port)
			self.Connect(0, 0)
		else :
			self.stream.SetConnectInfo(ip, tcp_port, account_ip, account_port)
			self.__OpenLoginBoard()
		

	def __OnClickSelectConnectButton(self):
		if IsFullBackImage():
			self.GetChild("bg1").Show()
			self.GetChild("bg2").Hide()
		self.__RefreshServerList()
		self.__OpenServerBoard()

	def __OnClickLoginButton(self):
		self.__OnClickSelectServerButton()
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()
		

		if self.channelList.GetSelectedItem() == 0:	
			self.PopupNotifyMessage("Elige Channel")
			return	

		if len(id)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, self.SetIDEditLineFocus)
			return

		if len(pwd)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, self.SetPasswordEditLineFocus)
			return

		self.Connect(id, pwd)
