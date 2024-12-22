from environmentImage import *
from playerImage import *


class SceneSurface:
    def __init__(self, environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray):
        '''

        :param environmentImageAddress:         # 环境图片地址
        :param environmentScaleRate:            # 环境图片放大比例
        :param start_X:             # 该对象的起始位置
        :param idiomCharaArray      # [[成语], [正确文字在成语中的索引], [文字], [正确文字在文字列表中的索引]]
        '''

        self.environment = Environment(environmentImageAddress, environmentScaleRate)    # 环境图片对象
        self.environment1 = self.environment.environments[1]  # 悬空平台方块图片
        self.environment2 = self.environment.environments[0]  # 地面方块图片

        self.environment1Width = self.environment1.get_rect().width     # 地面方块图片长度
        self.environment1Height = self.environment1.get_rect().height   # 地面方块图片高度

        self.environment2Width = self.environment2.get_rect().width     # 悬空平台方块图片长度
        self.environment2Height = self.environment2.get_rect().height   # 悬空平台方块图片高度

        # 字体颜色，字体背景颜色
        self.fontColor = (0, 0, 0)
        self.fontBackcolor = (240, 135, 132)

        self.X = start_X    # X 的坐标
        self.Y = 0          # Y 的坐标

    # 更新
    def Update(self, newLength):
        '''

        :param newLength:
        :return:
        '''
        self.UpdateLocation(newLength)

    # 更新位置
    def UpdateLocation(self, newLength):
        pass

    # 场景设置
    def GetScene(self, width, height, backcolor, ground_y):
        '''

        :param width:
        :param height:
        :param backcolor:
        :param ground_y:
        :return:
        '''
        pass

    # 和玩家碰撞
    def colliderectToPlayer(self, player):
        '''

        :param player:
        :return:
        '''
        pass


class SceneInit(SceneSurface):
    def __init__(self, environmentImageAddress, environmentScaleRate, start_X):
        '''

        :param environmentImageAddress:         # 环境图片地址
        :param environmentScaleRate:            # 环境图片放大比例
        :param start_X:             # 该对象的起始位置
        '''

        # 给夫构造函数的参数
        idiomCharaArray = [[''], [0], ['', '', '', ''], [0]]

        # 继承父类构造函数
        super().__init__(environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray)

        # 横纵坐标，图片长宽
        # 顺序为 地面，悬空平台（从左到右），文字（从左到右）
        self.X_list = [0]
        self.Y_list = [0]
        self.width_list = [0]
        self.height_list = [0]

    # 场景设置（以下为 长:1200px，宽:800px，ground_y:500px 情况下设置的场景）
    def GetScene(self, width, height, backcolor, ground_y):
        scene = pygame.Surface((width, height))   # 设置场景地面大小
        scene.fill(backcolor)

        # 设计场景
        for i in range(int(width / self.environment1Width) + 1):
            scene.blit(self.environment1, (i * self.environment1Width, ground_y))      # 铺设地面
        self.X_list[0] += 0
        self.Y_list[0] += ground_y
        self.width_list[0] = width
        self.height_list[0] = self.environment1.get_rect().height

        return scene

    # 获取各个图片的碰撞面
    def Rect(self):
        # 地面
        rect1 = pygame.Rect(self.X_list[0], self.Y_list[0], self.width_list[0], self.height_list[0])

        Rect = [rect1]

        return Rect

    # 移动函数（改变 pygame.Rect() 的坐标）
    def Move(self, speed):
        self.X_list = [(x - speed) for x in self.X_list]

    # 重置函数（重置 pygame.Rect() 的坐标）
    def UpdateLocation(self, newLength):
        self.X_list = [(x + newLength) for x in self.X_list]

    # 和玩家碰撞
    def colliderectToPlayer(self, player):
        Rect = self.Rect()  # 获取 pygame.Rect() 列表

        # 判断玩家是否在下落（只有下落时才可能转移接触地）
        if player.state == 'fall':
            # 是否和地面，悬浮平台 接触/碰撞
            if Rect[0].colliderect(player.Rect()) and (player.foot <= self.Y_list[0] + 1):
                player.Y = self.Y_list[0] - player.presentHeight
                player.state = 'run'


# 场景（SceneSurface 的子类）
class Scene1(SceneSurface):
    def __init__(self, environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray):
        '''

        :param environmentImageAddress:         # 环境图片地址
        :param environmentScaleRate:            # 环境图片放大比例
        :param start_X:             # 该对象的起始位置
        '''

        # 继承父类构造函数
        super().__init__(environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray)

        # 横纵坐标，图片长宽
        # 顺序为 地面，悬空平台（从左到右），文字（从左到右）
        self.X_list = [self.X for i in range(8)]
        self.Y_list = [self.Y for i in range(8)]
        self.width_list = [0 for i in range(3)]
        self.height_list = [0 for i in range(3)]

        # 各个图片相对于整个 scene 的位置
        self.start_x = start_X
        self.relative_X = self.X_list
        self.relative_Y = self.Y_list

    # 场景设置（以下为 长:1200px，宽:800px，ground_y:500px 情况下设置的场景）
    def GetScene(self, width, height, backcolor, ground_y):
        scene = pygame.Surface((width, height))   # 设置场景地面大小
        scene.fill(backcolor)

        # 设计场景
        for i in range(int(width / self.environment1Width) + 1):
            scene.blit(self.environment1, (i * self.environment1Width, ground_y))      # 铺设地面
        self.X_list[0] += 0
        self.Y_list[0] += ground_y
        self.width_list[0] = width
        self.height_list[0] = self.environment1.get_rect().height

        # 设置悬空平台
        scene.blit(self.environment2, (135, 380))
        scene.blit(self.environment2, (350, 260))
        scene.blit(self.environment2, (565, 140))
        self.X_list[1: 4] = [135 + self.X_list[1], 350 + self.X_list[2], 565 + self.X_list[3]]
        self.Y_list[1: 4] = [380 + self.Y_list[1], 260 + self.Y_list[2], 140 + self.Y_list[3]]
        self.width_list[1] = self.environment2.get_rect().width
        self.height_list[1] = self.environment2.get_rect().height

        # 设置文字位置
        font = pygame.font.SysFont("SimHei", 30)    # 创建文字对象
        character = font.render('中', True, self.fontColor)

        # 获取字体大小
        (fontWidth, fontHeight) = character.get_size()

        self.X_list[4:] = [135 + self.environment2Width - fontWidth + self.X_list[4],
                           565 + self.X_list[5], 700 + self.X_list[6], 952 + self.X_list[7]]
        self.Y_list[4:] = [380 - fontHeight + self.Y_list[4], 300 + self.Y_list[5],
                           140 - fontHeight + self.Y_list[6], 380 + self.Y_list[7]]
        self.width_list[2] = fontWidth
        self.height_list[2] = fontHeight

        # 设置各个图片相对于整个 scene 的位置
        self.relative_X = [(X - self.start_x) for X in self.X_list]
        self.relative_Y = self.Y_list

        return scene

    # 获取各个图片的碰撞面
    def Rect(self):
        # 地面
        rect1 = pygame.Rect(self.X_list[0], self.Y_list[0], self.width_list[0], self.height_list[0])

        # 悬空平台
        rect2 = pygame.Rect(self.X_list[1], self.Y_list[1], self.width_list[1], self.height_list[1])
        rect3 = pygame.Rect(self.X_list[2], self.Y_list[2], self.width_list[1], self.height_list[1])
        rect4 = pygame.Rect(self.X_list[3], self.Y_list[3], self.width_list[1], self.height_list[1])

        # 文字
        rect5 = pygame.Rect(self.X_list[4], self.Y_list[4], self.width_list[2], self.height_list[2])
        rect6 = pygame.Rect(self.X_list[5], self.Y_list[5], self.width_list[2], self.height_list[2])
        rect7 = pygame.Rect(self.X_list[6], self.Y_list[6], self.width_list[2], self.height_list[2])
        rect8 = pygame.Rect(self.X_list[7], self.Y_list[7], self.width_list[2], self.height_list[2])

        # pygame.Rect() 列表
        Rect = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8]

        return Rect

    # 移动函数（改变 pygame.Rect() 的坐标）
    def Move(self, speed):
        self.X_list = [(x - speed) for x in self.X_list]

    # 重置函数（重置 pygame.Rect() 的坐标）
    def UpdateLocation(self, newLength):
        self.X_list = [(x + newLength) for x in self.relative_X]

    # 和玩家碰撞
    def colliderectToPlayer(self, player):
        Rect = self.Rect()  # 获取 pygame.Rect() 列表

        # 判断玩家奔跑时是否接触到了悬浮平台或地面
        # 未接触到则表明玩家已经跑出了平台或地面，则玩家下落
        count = 0
        if player.state == 'run':
            for i in range(4):
                count += 1
                if Rect[i].colliderect(player.Rect()):
                    break

        if count == 4:
            player.state = 'fall'

        # 判断玩家是否在下落（只有下落时才可能转移接触地）
        if player.state == 'fall':
            # 是否和地面，悬浮平台 接触/碰撞
            for i in range(4):
                if Rect[i].colliderect(player.Rect()) and (player.foot <= self.Y_list[i] + 1):
                    player.Y = self.Y_list[i] - player.presentHeight
                    player.state = 'run'


class Scene2(SceneSurface):
    def __init__(self, environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray):
        '''

        :param environmentImageAddress:         # 环境图片地址
        :param environmentScaleRate:            # 环境图片放大比例
        :param start_X:             # 该对象的起始位置
        '''

        # 继承父类构造函数
        super().__init__(environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray)

        # 横纵坐标，图片长宽
        # 顺序为 地面，悬空平台（从左到右），文字（从左到右）
        self.X_list = [self.X for i in range(8)]
        self.Y_list = [self.Y for i in range(8)]
        self.width_list = [0 for i in range(4)]
        self.height_list = [0 for i in range(4)]

        # 各个图片相对于整个 scene 的位置
        self.start_x = start_X
        self.relative_X = self.X_list
        self.relative_Y = self.Y_list

    # 场景设置（以下为 长:1200px，宽:800px，ground_y:500px 情况下设置的场景）
    def GetScene(self, width, height, backcolor, ground_y):
        scene = pygame.Surface((width, height))   # 设置场景地面大小
        scene.fill(backcolor)

        # 设计场景
        for i in range(int(width / self.environment1Width / 3)):
            scene.blit(self.environment1, (i * self.environment1Width, ground_y))      # 铺设地面
        self.X_list[0] += 0
        self.Y_list[0] += ground_y
        self.width_list[0] = int(width / self.environment1Width / 3) * self.environment1Width
        self.height_list[0] = self.environment1.get_rect().height

        for i in range(int(width / self.environment1Width / 3) + 1):
            scene.blit(self.environment1, (i * self.environment1Width + 800, ground_y))      # 铺设地面
        self.X_list[1] += 800
        self.Y_list[1] += ground_y
        self.width_list[1] = width - 800
        self.height_list[1] = self.environment1.get_rect().height

        # 设置悬空平台
        scene.blit(self.environment2, (350, 380))
        scene.blit(self.environment2, (560, 260))
        self.X_list[2: 4] = [350 + self.X_list[2], 560 + self.X_list[3]]
        self.Y_list[2: 4] = [380 + self.Y_list[2], 260 + self.Y_list[3]]
        self.width_list[2] = self.environment2.get_rect().width
        self.height_list[2] = self.environment2.get_rect().height

        # 设置文字位置
        font = pygame.font.SysFont("SimHei", 30)    # 创建文字对象
        character = font.render('中', True, self.fontColor)

        # 获取字体大小
        (fontWidth, fontHeight) = character.get_size()

        self.X_list[4:] = [100 + self.X_list[4], 360 + self.X_list[5],
                           900 + self.X_list[6], 850 + self.X_list[7]]
        self.Y_list[4:] = [380 - fontHeight + self.Y_list[4], 240 - fontHeight + self.Y_list[5],
                           500 - fontHeight + self.Y_list[6], 120 - fontHeight + self.Y_list[7]]
        self.width_list[3] = fontWidth
        self.height_list[3] = fontHeight

        # 设置各个图片相对于整个 scene 的位置
        self.relative_X = [(X - self.start_x) for X in self.X_list]
        self.relative_Y = self.Y_list

        return scene

    # 获取各个图片的碰撞面
    def Rect(self):
        # 地面
        rect1 = pygame.Rect(self.X_list[0], self.Y_list[0], self.width_list[0], self.height_list[0])
        rect2 = pygame.Rect(self.X_list[1], self.Y_list[1], self.width_list[1], self.height_list[1])

        # 悬空平台
        rect3 = pygame.Rect(self.X_list[2], self.Y_list[2], self.width_list[2], self.height_list[2])
        rect4 = pygame.Rect(self.X_list[3], self.Y_list[3], self.width_list[2], self.height_list[2])

        # 文字
        rect5 = pygame.Rect(self.X_list[4], self.Y_list[4], self.width_list[3], self.height_list[3])
        rect6 = pygame.Rect(self.X_list[5], self.Y_list[5], self.width_list[3], self.height_list[3])
        rect7 = pygame.Rect(self.X_list[6], self.Y_list[6], self.width_list[3], self.height_list[3])
        rect8 = pygame.Rect(self.X_list[7], self.Y_list[7], self.width_list[3], self.height_list[3])

        # pygame.Rect() 列表
        Rect = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8]

        return Rect

    # 移动函数（改变 pygame.Rect() 的坐标）
    def Move(self, speed):
        self.X_list = [(x - speed) for x in self.X_list]

    # 重置函数（重置 pygame.Rect() 的坐标）
    def UpdateLocation(self, newLength):
        self.X_list = [(x + newLength) for x in self.relative_X]

    # 和玩家碰撞
    def colliderectToPlayer(self, player):
        Rect = self.Rect()  # 获取 pygame.Rect() 列表

        # 判断玩家奔跑时是否接触到了悬浮平台或地面
        # 未接触到则表明玩家已经跑出了平台或地面，则玩家下落
        count = 0
        if player.state == 'run':
            for i in range(4):
                count += 1
                if Rect[i].colliderect(player.Rect()):
                    break

        if count == 4:
            player.state = 'fall'

        # 判断玩家是否在下落（只有下落时才可能转移接触地）
        if player.state == 'fall':
            # 是否和地面，悬浮平台 接触/碰撞
            for i in range(4):
                if Rect[i].colliderect(player.Rect()) and (player.foot <= self.Y_list[i] + 1):
                    player.Y = self.Y_list[i] - player.presentHeight
                    player.state = 'run'


class Scene3(SceneSurface):
    def __init__(self, environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray):
        '''

        :param environmentImageAddress:         # 环境图片地址
        :param environmentScaleRate:            # 环境图片放大比例
        :param start_X:             # 该对象的起始位置
        '''

        # 继承父类构造函数
        super().__init__(environmentImageAddress, environmentScaleRate, start_X, idiomCharaArray)

        # 横纵坐标，图片长宽
        # 顺序为 地面，悬空平台（从左到右），文字（从左到右）
        self.X_list = [self.X for i in range(10)]
        self.Y_list = [self.Y for i in range(10)]
        self.width_list = [0 for i in range(6)]
        self.height_list = [0 for i in range(6)]

        # 各个图片相对于整个 scene 的位置
        self.start_x = start_X
        self.relative_X = self.X_list
        self.relative_Y = self.Y_list

    # 场景设置（以下为 长:1200px，宽:800px，ground_y:500px 情况下设置的场景）
    def GetScene(self, width, height, backcolor, ground_y):
        scene = pygame.Surface((width, height))   # 设置场景地面大小
        scene.fill(backcolor)

        # 设计场景
        for i in range(2):
            scene.blit(self.environment1, (i * self.environment1Width, ground_y))      # 铺设地面
            scene.blit(self.environment1, ((i + 2) * self.environment1Width + 100, ground_y))
            scene.blit(self.environment1, ((i + 4) * self.environment1Width + 200, ground_y))
            scene.blit(self.environment1, ((i + 6) * self.environment1Width + 300, ground_y))
        self.X_list[0: 4] = [self.X_list[0],
                             2 * self.environment1Width + 100 + self.X_list[1],
                             4 * self.environment1Width + 200 + self.X_list[2],
                             6 * self.environment1Width + 300 + self.X_list[3]]
        self.Y_list[0: 4] = [ground_y for i in range(4)]
        self.width_list[0: 4] = [2 * self.environment1Width,
                                 2 * self.environment1Width,
                                 2 * self.environment1Width,
                                 width - 6 * self.environment1Width - 300]
        self.height_list[0: 4] = [self.environment1.get_rect().height for i in range(4)]

        # 设置悬空平台
        scene.blit(self.environment2, (135, 380))
        scene.blit(self.environment2, (800, 380))
        self.X_list[4: 6] = [135 + self.X_list[4], 800 + self.X_list[5]]
        self.Y_list[4: 6] = [380 + self.Y_list[4], 380 + self.Y_list[5]]
        self.width_list[4] = self.environment2.get_rect().width
        self.height_list[4] = self.environment2.get_rect().height

        # 设置文字位置
        font = pygame.font.SysFont("SimHei", 30)    # 创建文字对象
        character = font.render('中', True, self.fontColor)

        # 获取字体大小
        (fontWidth, fontHeight) = character.get_size()

        self.X_list[6:] = [230, self.X_list[1] + 100, 850, self.X_list[3]]
        self.Y_list[6:] = [380 - fontHeight, 380, 300 - fontHeight, 500 - fontHeight]
        self.width_list[5] = character.get_width()
        self.height_list[5] = character.get_height()

        # 设置各个图片相对于整个 scene 的位置
        self.relative_X = [(X - self.start_x) for X in self.X_list]
        self.relative_Y = self.Y_list

        return scene

    # 获取各个图片的碰撞面
    def Rect(self):
        # 地面
        rect1 = pygame.Rect(self.X_list[0], self.Y_list[0], self.width_list[0], self.height_list[0])
        rect2 = pygame.Rect(self.X_list[1], self.Y_list[1], self.width_list[1], self.height_list[1])
        rect3 = pygame.Rect(self.X_list[2], self.Y_list[2], self.width_list[2], self.height_list[2])
        rect4 = pygame.Rect(self.X_list[3], self.Y_list[3], self.width_list[3], self.height_list[3])

        # 悬空平台
        rect5 = pygame.Rect(self.X_list[4], self.Y_list[4], self.width_list[4], self.height_list[4])
        rect6 = pygame.Rect(self.X_list[5], self.Y_list[5], self.width_list[4], self.height_list[4])

        # 文字
        rect7 = pygame.Rect(self.X_list[6], self.Y_list[6], self.width_list[5], self.height_list[5])
        rect8 = pygame.Rect(self.X_list[7], self.Y_list[7], self.width_list[5], self.height_list[5])
        rect9 = pygame.Rect(self.X_list[8], self.Y_list[8], self.width_list[5], self.height_list[5])
        rect10 = pygame.Rect(self.X_list[9], self.Y_list[9], self.width_list[5], self.height_list[5])

        # pygame.Rect() 列表
        Rect = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9, rect10]

        return Rect

    # 移动函数（改变 pygame.Rect() 的坐标）
    def Move(self, speed):
        self.X_list = [(x - speed) for x in self.X_list]

    # 重置函数（重置 pygame.Rect() 的坐标）
    def UpdateLocation(self, newLength):
        self.X_list = [(x + newLength) for x in self.relative_X]

    # 和玩家碰撞
    def colliderectToPlayer(self, player):
        Rect = self.Rect()  # 获取 pygame.Rect() 列表

        # 判断玩家奔跑时是否接触到了悬浮平台或地面
        # 未接触到则表明玩家已经跑出了平台或地面，则玩家下落
        count = 0
        if player.state == 'run':
            for i in range(6):
                count += 1
                if Rect[i].colliderect(player.Rect()):
                    break

        if count == 6:
            player.state = 'fall'

        # 判断玩家是否在下落（只有下落时才可能转移接触地）
        if player.state == 'fall':
            # 是否和地面，悬浮平台 接触/碰撞
            for i in range(6):
                if Rect[i].colliderect(player.Rect()) and (player.foot <= self.Y_list[i] + 1):
                    player.Y = self.Y_list[i] - player.presentHeight
                    player.state = 'run'


if __name__ == "__main__":
    pygame.init()

    # 环境图片地址
    environmentAddress = "image/EnvironmentTiles.png"
    playerAddress = "image/LightBandit.png"

    # 环境图片缩放比例
    environmentScaleRate = 4
    playerScaleRate = 2

    screen = pygame.display.set_mode((1200, 800))
    screen.fill((255, 255, 255))

    clock = pygame.time.Clock()
    fps = 30

    player = Player(playerAddress, playerScaleRate)

    idiom_array = [['一二三四'], [0], ['一', '三', '器', '飒'], [0]]
    new_idiom_array = [['一二三四'], [0], ['二', '但', '个', '史'], [0]]

    scene = Scene2(environmentAddress, environmentScaleRate, 0, idiom_array)
    """scene.character1 = '我'
    scene.character2 = '是'
    scene.character3 = '个'
    scene.character4 = '人'"""

    theScene = scene.GetScene(1200, 800, (255, 255, 255), 500)

    screen.blit(theScene, (0, 0))
    a = 0
    pygame.display.flip()  # 更新画布（一般用于第一次更新，更新整个画布）

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w):
                    player.Y -= 10
                elif (event.key == pygame.K_s):
                    player.Y += 10
                elif (event.key == pygame.K_a):
                    player.X -= 10
                elif (event.key == pygame.K_d):
                    player.X += 10

        scene.Update(0, new_idiom_array)
        theScene = scene.IdiomShow(theScene)

        screen.fill((255, 255, 255))
        screen.blit(theScene, (0, 0))
        screen.blit(player.playerInit, (player.X, player.Y))

        pygame.display.update()

    pygame.quit()
