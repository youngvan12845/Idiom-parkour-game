import pygame


class CharacterRect:
    def __init__(self, font_color, font_backcolor, font_size):
        self.X = 0
        self.Y = 0

        self.font_width = 0
        self.font_height = 0

        self.character = ''

        self.fontColor = font_color
        self.fontBackcolor = font_backcolor
        self.fontSize = font_size

    def Rect(self):
        return pygame.Rect(self.X, self.Y, self.font_width, self.font_height)

    def Move(self, speed):
        self.X -= speed

    def updateLocation(self, location):
        self.X = location[0]
        self.Y = location[1]

    # 改变文字（显示的文字会带有有色矩形框）（用于屏幕中移动的文字）
    def updateCharacter(self, character):
        self.character = character      # 记录文字

        font = pygame.font.SysFont("SimHei", self.fontSize)  # 创建文字对象
        character = font.render(character, True, self.fontColor)

        (self.font_width, self.font_height) = character.get_size()

        surface = pygame.Surface((self.font_width, self.font_height))
        surface.fill(self.fontBackcolor)

        surface.blit(character, (0, 0))

        return surface

    # 改变文字（显示的文字会带有有色矩形框）（用于成语框中的文字）
    def updateCharaWithoutBack(self, character):
        font = pygame.font.SysFont("SimHei", self.fontSize)  # 创建文字对象
        character = font.render(character, True, self.fontColor)

        return character


# 更新文字位置
def UpdateCharactersLocation(character_rects, rect):
    for i, cha in enumerate(character_rects):
        cha.updateLocation(rect[i])


# 文字移动
def MoveCharacters(character_rects, speed):
    for cha in character_rects:
        cha.Move(speed)


# 改变文字（显示的文字会带有有色矩形框）（用于屏幕中移动的文字）
def UpdateCharacters(character_rects, idiom_chara):
    characters = []

    for i, cha in enumerate(character_rects):
        characters.append(cha.updateCharacter(idiom_chara[i]))

    return characters


# 改变文字（显示的文字会带有有色矩形框）（用于成语框中的文字）
def UpdateCharaWithoutBack(character_rects, idiom_chara):
    characters = []

    for i, cha in enumerate(character_rects):
        characters.append(cha.updateCharaWithoutBack(idiom_chara[i]))

    return characters


# 获取文字所在的位置
def GetCharactersRect(rect):
    characters_rect = []

    for i in range(4):
        characters_rect.append(rect[i - 4][0: 2])

    return characters_rect
