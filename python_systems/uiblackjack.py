import ui
import chat
from _weakref import proxy
import app
import blackjack
import item
import uiToolTip
import localeInfo

PATCH_DESIGN = "d:/ymir work/ui/minigame/blackjack/blackjack/cards/"
EFFECT_PATCH = "d:/ymir work/ui/minigame/blackjack/blackjack/effect/"
GOLD = 2000000

class BlackJackWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		blackjack.SetBlackJackHandler(self)
		self.ItemToolTip 	= uiToolTip.ItemToolTip()

		self.elements = {}
		
		for i in xrange(blackjack.MAX_PLAYER):
			self.elements["count_cards_%d"%(i)] = 0
			self.elements["total_count_cards_%d"%(i)] = []
			self.elements["list_cards_%d"%(i)] = []
			self.elements["list_cards_dealer_%d"%(i)] = []

			self.elements["temp_count_cards_%d"%(i)] = 0
			self.elements["temp_list_cards_%d"%(i)] = []

		self.elements["status"] = 0
		self.elements["item_reward"] = 0
		self.elements["animation_blackjack"] = None

		self.LoadWindow()

	def __del__(self):
		blackjack.SetBlackJackHandler(None)
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "System/black_jack.py")
		except:
			import exception
			exception.Abort("UiBlackJack.LoadWindow.LoadObject")

		self.board = self.GetChild("board")
		self.TitleBar = self.GetChild("TitleBar")
		self.hit_button = self.GetChild("hit_button")
		self.play_button = self.GetChild("play_button")
		self.stand_button = self.GetChild("stand_button")
		self.slot_item = self.GetChild("slot_item")
		self.text_yang = self.GetChild("text_yang")
		
		self.slot_item.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.slot_item.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.play_button.SetEvent(ui.__mem_func__(self.FuncBlackJack),2)
		self.hit_button.SetEvent(ui.__mem_func__(self.FuncBlackJack),4)
		self.stand_button.SetEvent(ui.__mem_func__(self.FuncBlackJack),3)

		for players in xrange(1,blackjack.MAX_PLAYER+1):
			self.elements["count_player_%d"%(players)] = self.GetChild("count_player_%d"%(players))

		self.TitleBar.SetCloseEvent(self.Close)

		self.elements["move_card"] = ui.MoveImageBox()
		self.elements["move_card"].AddFlag("float")
		self.elements["move_card"].SetParent(proxy(self.board))
		self.elements["move_card"].SetPosition(320,55)
		self.elements["move_card"].Hide()

		self.text_yang.SetText(localeInfo.NumberToMoneyString(GOLD))

	def FuncBlackJack(self,index):
		if self.elements["move_card"].GetMove():
			return

		if (index == 3 or index == 4) and self.GetStatus() == blackjack.GAME_NONE and self.play_button.IsShow():
			return

		blackjack.SendBlackJack(index)

	def ClearGame(self):
		for i in xrange(blackjack.MAX_PLAYER):
			self.elements["count_cards_%d"%(i)] = 0
			self.elements["total_count_cards_%d"%(i)] = []

			self.elements["temp_count_cards_%d"%(i)] = 0
			self.elements["temp_list_cards_%d"%(i)] = []

			if len(self.elements["list_cards_%d"%(i)]) > 0:
				for elements_cards in self.elements["list_cards_%d"%(i)]:
					elements_cards.Hide()

			if len(self.elements["list_cards_dealer_%d"%(i)]) > 0:
				for elements_cards in self.elements["list_cards_dealer_%d"%(i)]:
					elements_cards.Hide()

			self.elements["count_player_%d"%(i+1)].SetText("0")

			self.elements["list_cards_%d"%(i)] = []	
			self.elements["list_cards_dealer_%d"%(i)] = []	

		self.elements["status"] = 0
		self.elements["item_reward"] = 0
		self.slot_item.ClearSlot(0)

		self.play_button.Hide()

	def EndGame(self,status,vnum,count):
		self.elements["status"] = int(status)
		self.elements["item_reward"] = int(vnum)

		self.play_button.Show()
		self.slot_item.SetItemSlot(0,int(vnum),int(count),(1.0, 1.0, 1.0, 0.8))

	def GetStatus(self):
		return self.elements["status"]

	def CreateCard(self,index_player,index_card_color,index_card_number):
		self.elements["temp_count_cards_%d"%(index_player)] += 1
		self.elements["temp_list_cards_%d"%(index_player)].append([index_card_color,index_card_number])

	def CreateAnimation(self):
		self.elements["animation_blackjack"] = ui.AniImageBox()
		self.elements["animation_blackjack"].SetParent(self.board)
		self.elements["animation_blackjack"].SetDelay(5)
		self.elements["animation_blackjack"].SetEndFrameEvent(ui.__mem_func__(self.EndAnimation))
		self.elements["animation_blackjack"].Hide()

		func = self.GetStatus()

		list_effect = ["push","lose","win","blackjack"]
		effect = list_effect[int(func)-1]

		if self.elements["animation_blackjack"]:
			self.elements["animation_blackjack"].Clear()
			for i in xrange(1,10):
				self.elements["animation_blackjack"].AppendImage(EFFECT_PATCH+"{}/{}{}.sub".format(effect,effect,i-10))

			for i in xrange(0,8):
				self.elements["animation_blackjack"].AppendImage(EFFECT_PATCH+"{}/{}{}.sub".format(effect,effect,1))

			for i in xrange(1,10):
				self.elements["animation_blackjack"].AppendImage(EFFECT_PATCH+"{}/{}{}.sub".format(effect,effect,i))
			self.elements["animation_blackjack"].SetPosition(109,116)
			self.elements["animation_blackjack"].ResetFrame()
			self.elements["animation_blackjack"].Show()

	def SetCards(self):
		index_player = -1
		if len(self.elements["temp_list_cards_%d"%(blackjack.PLAYER_ME)]) > 0:
			index_player = 1
		else:
			if len(self.elements["temp_list_cards_%d"%(blackjack.PLAYER_DEALER)]) > 0:
				index_player = 0

		if index_player < 0:
			return

		(x_pos,y_pos) = self.FuncPosCards(index_player)


		index_card_color = self.elements["temp_list_cards_%d"%(index_player)][0][0]
		index_card_number = self.elements["temp_list_cards_%d"%(index_player)][0][1]

		self.CreateNormalCards(x_pos,y_pos,index_player,index_card_color,index_card_number)
		self.CreateNormalCardsDealer(x_pos,y_pos,index_player,index_card_color,index_card_number)
		self.CreateAnimationCard(x_pos,y_pos,index_player,index_card_color,index_card_number)
		self.FuncCardsCount(index_player,index_card_number)

	def CreateCardNormal(self,index_player,index_card_color,index_card_number):
		(x_pos,y_pos) = self.FuncPosCards(index_player)

		self.CreateNormalCards(x_pos,y_pos,index_player,index_card_color,index_card_number)		

		self.FuncCardsCount(index_player,index_card_number)

	def FuncPosCards(self,index_player):
		y_pos = 79
		if index_player:
			y_pos = 184
		x_pos = self.elements["count_cards_%d"%(index_player)]

		return (x_pos,y_pos)

	def FuncCardsCount(self,index_player,index_card_number):
		self.elements["count_cards_%d"%(index_player)] += 1
		self.elements["total_count_cards_%d"%(index_player)].append(index_card_number)

	def CountCards(self,index_player):
		count_cards = self.elements["total_count_cards_%d"%(index_player)]
		card_as = 0
		card_normal = 0
		
		for cards_index in count_cards:
			if cards_index >= 10:
				cards_index = 10
			card_normal += cards_index

			if cards_index == 1:
				card_as += 10

		count_total = str(card_normal)
		count_sum = card_as+card_normal

		if card_as != 0 and count_sum <= 21:
			count_total += "/" + str(count_sum)
		
		self.elements["count_player_%d"%(index_player+1)].SetText(count_total)

	def CreateNormalCards(self,x_pos,y_pos,index_player,index_card_color,index_card_number):
		(x_p , y_p) = self.board.GetLocalPosition()
		card_img = PATCH_DESIGN + "card_%d_%d.sub"%(index_card_color,index_card_number)

		if index_player == blackjack.PLAYER_DEALER and len(self.elements["list_cards_%d"%(blackjack.PLAYER_DEALER)])+1 >= 2:
			card_img = PATCH_DESIGN + "card_back.dds"

		self.elements["cards_%d_%d_%d"%(index_player,index_card_color,index_card_number)] = ui.ImageBox()
		self.elements["cards_%d_%d_%d"%(index_player,index_card_color,index_card_number)].SetParent(proxy(self.board))
		self.elements["cards_%d_%d_%d"%(index_player,index_card_color,index_card_number)].SetPosition(15*x_pos+(x_p+170),y_p+y_pos)
		self.elements["cards_%d_%d_%d"%(index_player,index_card_color,index_card_number)].LoadImage(card_img)
		self.elements["cards_%d_%d_%d"%(index_player,index_card_color,index_card_number)].Hide()

		self.elements["list_cards_%d"%(index_player)].append(self.elements["cards_%d_%d_%d"%(index_player,index_card_color,index_card_number)])

	def CreateNormalCardsDealer(self,x_pos,y_pos,index_player,index_card_color,index_card_number):
		(x_p , y_p) = self.board.GetLocalPosition()
		card_img = PATCH_DESIGN + "card_%d_%d.sub"%(index_card_color,index_card_number)

		self.elements["cards_d_%d_%d_%d"%(index_player,index_card_color,index_card_number)] = ui.ImageBox()
		self.elements["cards_d_%d_%d_%d"%(index_player,index_card_color,index_card_number)].SetParent(proxy(self.board))
		self.elements["cards_d_%d_%d_%d"%(index_player,index_card_color,index_card_number)].SetPosition(15*x_pos+(x_p+170),y_p+y_pos)
		self.elements["cards_d_%d_%d_%d"%(index_player,index_card_color,index_card_number)].LoadImage(card_img)
		self.elements["cards_d_%d_%d_%d"%(index_player,index_card_color,index_card_number)].Hide()

		self.elements["list_cards_dealer_%d"%(index_player)].append(self.elements["cards_d_%d_%d_%d"%(index_player,index_card_color,index_card_number)])

	def CreateAnimationCard(self,x_pos,y_pos,index_player,index_card_color,index_card_number):
		(x_p , y_p) = self.board.GetGlobalPosition()
		card_img = PATCH_DESIGN + "card_%d_%d.sub"%(index_card_color,index_card_number)

		if index_player == blackjack.PLAYER_DEALER and len(self.elements["list_cards_%d"%(blackjack.PLAYER_DEALER)]) >= 2:
			card_img = PATCH_DESIGN + "card_back.dds"

		self.elements["move_card"].LoadImage(card_img)
		self.elements["move_card"].SetMoveSpeed(8.0)
		self.elements["move_card"].SetMovePosition(15*x_pos+(x_p+170),y_p+y_pos)
		self.elements["move_card"].SetEndMoveEvent(ui.__mem_func__(self.__OnMoveEnd), index_player )
		self.elements["move_card"].MoveStart()
		self.elements["move_card"].Show()

	def EndAnimation(self):
		if self.elements["animation_blackjack"]:
			self.elements["animation_blackjack"].Hide()
			del self.elements["animation_blackjack"]

	def __OnMoveEnd(self, index_player):
		self.elements["move_card"].Hide()

		index_card = self.elements["count_cards_%d"%(index_player)]
		self.elements["list_cards_%d"%(index_player)][index_card-1].Show()
		if index_player == blackjack.PLAYER_DEALER:

			if len(self.elements["list_cards_%d"%(blackjack.PLAYER_DEALER)]) < 2:
				self.CountCards(index_player)
		else:
			self.CountCards(index_player)

		if self.elements["temp_count_cards_%d"%(index_player)] - 1 <= 0:
			self.elements["temp_list_cards_%d"%(index_player)] = []
			self.elements["temp_count_cards_%d"%(index_player)] = 0

			if index_player == blackjack.PLAYER_ME:
				if self.elements["temp_count_cards_%d"%(blackjack.PLAYER_DEALER)] > 0:
					self.SetCards()
			else:
				if self.elements["temp_count_cards_%d"%(blackjack.PLAYER_ME)] > 0:
					self.SetCards()

		else:
			self.elements["temp_count_cards_%d"%(index_player)] -= 1
			self.elements["temp_list_cards_%d"%(index_player)].pop(0)
			self.SetCards()

	def OnUpdate(self):
		if self.elements:
			#end animation and end game
			if False == self.elements["move_card"].GetMove() and self.GetStatus() != blackjack.GAME_NONE:
				if len(self.elements["list_cards_%d"%(blackjack.PLAYER_DEALER)]) > 0:
					self.CountCards(blackjack.PLAYER_DEALER)
					for elements_cards in self.elements["list_cards_dealer_%d"%(blackjack.PLAYER_DEALER)]:
						elements_cards.Show()
					for elements_cards in self.elements["list_cards_%d"%(blackjack.PLAYER_DEALER)]:
						elements_cards.Hide()

				self.CreateAnimation()
				self.elements["status"] = 0

	def OverInItem(self,index):
		if self.ItemToolTip:
			self.ItemToolTip.ClearToolTip()
			self.ItemToolTip.SetItemToolTip(self.elements["item_reward"])

	def OverOutItem(self):
		self.ItemToolTip.HideToolTip()


	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE


# = UiBlackJack()
#x.LoadWindow()

#x.Show()


#blackjack.SendBlackJack(2)