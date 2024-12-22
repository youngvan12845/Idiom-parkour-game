from CharacterRect import *
import random

# 更新成语框中的文字
def UpdateFrameCharacter(frame_character_list, present_idiom, present_index):
    present_idiom = [chara for chara in present_idiom]
    present_idiom[present_index] = ''
    frame_character = UpdateCharaWithoutBack(frame_character_list, present_idiom)
    change_frame = False

    return frame_character, change_frame


# 玩家和文字的碰撞检测
def ColliderectPlayerChara(character_list1, character_list2, player_rect, col_chara1, col_chara2):
    col_chara_index = [-1, -1]

    # 检测 玩家是否和 characters1 中的文字发生碰撞
    for i, char1 in enumerate(character_list1):
        if char1.Rect().colliderect(player_rect):
            col_chara1 = True
            col_chara_index = [1, i]
            break

    # 如果玩家和 characters1 发生碰撞，则不必和 characters2 做碰撞检测
    if col_chara_index[0] == -1:
        # 检测 玩家是否和 characters2 中的文字发生碰撞
        for j, char2 in enumerate(character_list2):
            if char2.Rect().colliderect(player_rect):
                col_chara2 = True
                col_chara_index = [2, j]
                break

    return col_chara_index, col_chara1, col_chara2


# 清除碰撞的文字，将碰撞的文字填到文本框中
def UpdateColCharacter(chara_index, character_list, frame_character_list, present_idiom, present_index):
    # 碰撞到的文字
    col_character = character_list[int(chara_index)].character

    # 清除碰撞到的文字
    characters = UpdateCharacters(character_list, ['', '', '', ''])

    # 将碰撞的文字填到文本框中
    present_idiom = [chara for chara in present_idiom]
    present_idiom[present_index] = col_character
    frame_character = UpdateCharaWithoutBack(frame_character_list, present_idiom)

    return characters, frame_character, col_character


# 生成药水
def UpdateMedicine(medicine, wall_rect, limit_x, limit_y):
    get_medicine = False    # 是否生成药水

    # 药水生成率为 0.2
    if random.randint(1, 5) == 1:
        get_medicine = True

    # 如果未生成药水
    if not get_medicine:
        return False, medicine

    # 如果生成了药水
    # 确保药水不会和平台重合
    change_locate = True

    while change_locate:
        change_locate = False

        medicine.X = random.randint(limit_x[0], limit_x[1])
        medicine.Y = random.randint(limit_y[0], limit_y[1])
        medicine_rect = medicine.Rect()

        for rect in wall_rect:
            if rect.colliderect(medicine_rect):
                change_locate = True

    # 设置药水效果
    medicine.imageIndex = random.randint(0, 2)
    medicine.state = ['speed_up', 'protect', 'recover'][medicine.imageIndex]

    return True, medicine
