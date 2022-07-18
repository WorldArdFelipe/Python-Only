import item
import player
import mouseModule

VNUM_CHANGE = 71097

def GetChangeItemAttrList(dstItemVNum, srcItemVNum):
	item.SelectItem(dstItemVNum)

	if item.GetItemType() == item.ITEM_TYPE_DS and srcItemVNum != VNUM_CHANGE:
		return False

	elif srcItemVNum == VNUM_CHANGE and item.GetItemType() != item.ITEM_TYPE_DS:
		return False

	elif not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR) and srcItemVNum != VNUM_CHANGE:
		return False

	return True


def CanUseSrcItemToDstItem(srcItemVNum, srcSlotPos, dstSlotPos):
	dstItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY,dstSlotPos)

	if dstItemVNum == 0:
		return False

	item.SelectItem(dstItemVNum)

	if srcItemVNum != VNUM_CHANGE:
		return False

	if item.GetItemType() != item.ITEM_TYPE_DS:
		return False

	for i in xrange(player.METIN_SOCKET_MAX_NUM):
		if player.GetItemAttribute(dstSlotPos, i) != 0:
			return True

	return False


def FuncOverInItem(overSlotPos):
	attachedItemType = mouseModule.mouseController.GetAttachedType()
	if player.SLOT_TYPE_INVENTORY == attachedItemType:
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
		if CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
			return True

	return False


def CanChangeItemAttrList(self, dstSlotPos, srcItemVNum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if GetChangeItemAttrList(dstItemVNum,srcItemVNum) == False:
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False
			