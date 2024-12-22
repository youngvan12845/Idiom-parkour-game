import pygame


class IdiomFrame:
    def __init__(self, frameAddress, backcolor, font_color):
        self.frameAddress = frameAddress
        self.backcolor = backcolor
        self.fontColor = font_color

        self.X = 0
        self.Y = 0
        self.fontLocation = [0, 0]

    # 设置文字相对于的 成语框 所在界面 的位置
    def updateFontLocation(self):
        pygame.init()
        font = pygame.font.SysFont("SimHei", 45)  # 创建文字对象
        character = font.render('中', True, self.fontColor)
        font_size = character.get_size()    # 获取单字大小

        font_x = self.X + (100 - font_size[0]) / 2     # 文字的 X 坐标
        font_y = self.Y + (100 - font_size[1]) / 2     # 文字的 Y 坐标

        self.fontLocation = [font_x, font_y]

    # 设置位置
    def setLocation(self, location):
        self.X = location[0]
        self.Y = location[1]

    # 获取 idiomFrame 的 Surface 类型对象
    def frameRect(self):
        # 获取 Surface 对象
        rect = pygame.Surface((100, 100))
        rect.fill(self.backcolor)

        # 成语框图片
        image = pygame.image.load(self.frameAddress)

        # 将 idiomFrame 图片绘制到 Surface 对象上
        rect.blit(image, (0, 0))

        return rect


# 设置 所有 idiomFrame 对象的位置
def SetFramesLocation(frames, screen_width, locate_y):
    frame_num = len(frames)     # idiomFrame 对象的个数
    x1 = (screen_width - frame_num * 100) / 2   # 第一个 idiomFrame 的 左上角的 X 坐标

    for i, fr in enumerate(frames):
        xi = x1 + i * 100       # 第 i 个 idiomFrame 的 左上角的 X 坐标
        fr.setLocation((xi, locate_y))      # 设置第 i 个 idiomFrame 的 坐标
        fr.updateFontLocation()     # 设置文字相对于的 成语框 所在界面 的位置


# 设置 所有 idiomFrame 对象的文字，并获取 idiomFrame 图像
def UpdateFramesCharacter(frames):
    # idiomFrame 的图像
    frame_rect = []

    # 设置文字
    for i, fr in enumerate(frames):
        frame_rect.append(fr.frameRect())

    return frame_rect
