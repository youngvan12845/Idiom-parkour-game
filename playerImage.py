import pygame


class Player():
    def __init__(self, imageAddress, scaleRate):
        '''

        :param imageAddress:    # 图片文件地址
        :param scaleRate:       # 图片放大比例
        '''

        self.scaleRate = scaleRate      # 图片放大比例
        self.image = pygame.image.load(imageAddress)    # 图片对象

        self.playerInit = self.InitImage()      # 初始动作（一张图片）
        self.run = self.RunImage()          # 奔跑动作（图片集合）
        self.attack = self.AttackImage()    # 攻击动作（图片集合）
        self.hurt = self.HurtImage()        # 受伤动作（图片集合）
        self.jump = self.JumpImage()        # 跳跃动作（一张图片）
        self.die = self.DieImage()          # 死亡动作（一张图片）

        self.initWidth = self.playerInit.get_rect().width       # 初始图片长度
        self.initHeight = self.playerInit.get_rect().height     # 初始图片高度
        self.runWidth = self.run[0].get_rect().width            # 奔跑图片长度
        self.runHeight = self.run[0].get_rect().height          # 奔跑图片高度
        self.attackWidth = self.attack[4].get_rect().width      # 攻击图片长度
        self.attackHeight = self.attack[0].get_rect().height    # 攻击图片高度
        self.hurtWidth = self.hurt[0].get_rect().width          # 受伤图片长度
        self.hurtHeight = self.hurt[0].get_rect().height        # 受伤图片高度
        self.jumpWidth = self.jump.get_rect().width             # 跳跃图片长度
        self.jumpHeight = self.jump.get_rect().height           # 跳跃图片高度
        self.dieWidth = self.die.get_rect().width               # 死亡图片长度
        self.dieHeight = self.die.get_rect().height             # 死亡图片高度

        self.X = 0.0      # X 坐标
        self.Y = 0.0     # Y 坐标
        self.presentImage = self.playerInit     # 现在应加载的图片
        self.presentWidth = self.initWidth      # 现在应加载的图片的长度
        self.presentHeight = self.initHeight    # 现在应加载的图片的高度
        self.foot = self.Y + self.presentHeight     # 图片的底端的 Y 坐标

        self.state = 'run'  # 玩家的状态 （['run', 'jump', 'fall', 'attack', 'hit']）
        self.buff = ''  # 玩家获得的特殊效果（['protect', 'speed_up']）

    # 获取初始动作图片（一张图片）
    def InitImage(self):
        playerInit = pygame.Surface.subsurface(self.image, (14, 9, 26, 37))           # 截取 image 的特定位置图片
        playerInit = pygame.transform.flip(playerInit, True, False)        # 图片水平翻转
        playerInit = pygame.transform.rotozoom(playerInit, 0, self.scaleRate)   # 图片缩放

        return playerInit

    # 获取奔跑动作图片（图片集合）
    def RunImage(self):
        # 截取 image 的特定位置图片
        run1 = pygame.Surface.subsurface(self.image, (14, 59, 25, 35))
        run2 = pygame.Surface.subsurface(self.image, (58, 59, 29, 35))
        run3 = pygame.Surface.subsurface(self.image, (105, 59, 32, 35))
        run4 = pygame.Surface.subsurface(self.image, (158, 59, 25, 35))
        run5 = pygame.Surface.subsurface(self.image, (209, 59, 20, 35))
        run6 = pygame.Surface.subsurface(self.image, (247, 59, 31, 35))
        run7 = pygame.Surface.subsurface(self.image, (294, 59, 31, 35))
        run8 = pygame.Surface.subsurface(self.image, (343, 59, 31, 35))

        run = [run1, run2, run3, run4, run5, run6, run7, run8]
        run = [pygame.transform.flip(r, True, False) for r in run]         # 图片水平翻转
        run = [pygame.transform.rotozoom(r, 0, self.scaleRate) for r in run]    # 图片缩放

        return run

    # 获取攻击动作图片（图片集合）
    def AttackImage(self):
        # 截取 image 的特定位置图片
        attack1 = pygame.Surface.subsurface(self.image, (12, 96, 24, 46))
        attack2 = pygame.Surface.subsurface(self.image, (59, 96, 25, 46))
        attack3 = pygame.Surface.subsurface(self.image, (107, 96, 25, 46))
        attack4 = pygame.Surface.subsurface(self.image, (155, 96, 24, 46))
        attack5 = pygame.Surface.subsurface(self.image, (192, 96, 38, 46))
        attack6 = pygame.Surface.subsurface(self.image, (242, 96, 36, 46))
        attack7 = pygame.Surface.subsurface(self.image, (293, 96, 33, 46))
        attack8 = pygame.Surface.subsurface(self.image, (350, 96, 24, 46))

        attack = [attack1, attack2, attack3, attack4, attack5, attack6, attack7, attack8]
        attack = [pygame.transform.flip(at, True, False) for at in attack]         # 图片水平翻转
        attack = [pygame.transform.rotozoom(at, 0, self.scaleRate) for at in attack]    # 图片缩放

        return attack

    # 获取受伤动作图片（图片集合）
    def HurtImage(self):
        # 截取 image 的特定位置图片
        hurt1 = pygame.Surface.subsurface(self.image, (14, 203, 24, 35))
        hurt2 = pygame.Surface.subsurface(self.image, (62, 203, 26, 35))

        hurt = [hurt1, hurt2]
        hurt = [pygame.transform.flip(h, True, False) for h in hurt]           # 图片水平翻转
        hurt = [pygame.transform.rotozoom(h, 0, self.scaleRate) for h in hurt]      # 图片缩放

        return hurt

    # 获取死亡动作图片（一张图片）
    def DieImage(self):
        die = pygame.Surface.subsurface(self.image, (145, 230, 43, 8))      # 截取 image 的特定位置图片
        die = pygame.transform.flip(die, True, False)            # 图片水平翻转
        die = pygame.transform.rotozoom(die, 0, self.scaleRate)       # 图片缩放

        return die

    # 获取跳跃动作图片（一张图片）
    def JumpImage(self):
        jump = pygame.Surface.subsurface(self.image, (110, 203, 24, 35))    # 截取 image 的特定位置图片
        jump = pygame.transform.flip(jump, True, False)          # 图片水平翻转
        jump = pygame.transform.rotozoom(jump, 0, self.scaleRate)     # 图片缩放

        return jump

    # 获取现在的图片的碰撞面
    def Rect(self):
        return pygame.Rect(self.X, self.Y, self.presentWidth, self.presentHeight + 1)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    pygame.display.flip()       # 更新画布（一般用于第一次更新，更新整个画布）

    clock = pygame.time.Clock()
    fps = 30

    player = Player("image/LightBandit.png", 2)

    runIndex = 0.0
    attackIndex = 0.0
    hurtIndex = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(player.playerInit, (0, 100 - player.initHeight))
        screen.blit(player.jump, (100, 100 - player.jumpHeight))
        screen.blit(player.die, (200, 100 - player.dieHeight))
        screen.blit(player.run[int(runIndex)], (0, 300 - player.runHeight))
        screen.blit(player.attack[int(attackIndex)], (100, 300 - player.attackHeight))
        screen.blit(player.hurt[int(hurtIndex)], (200, 300 - player.hurtHeight))

        # 切换图片
        runIndex = (runIndex + 0.005) % 8
        attackIndex = (attackIndex + 0.005) % 8
        hurtIndex = (hurtIndex + 0.005) % 2

        # 更新（一般用于第二次开始的更新，更新画布中更改的区域）
        pygame.display.update()

    pygame.quit()
