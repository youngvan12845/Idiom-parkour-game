import pygame


class Dragon:
    def __init__(self, imageAddress, scaleRate):
        '''

        :param imageAddress:        # 图片文件地址
        :param scaleRate:           # 图片缩小比例
        '''

        self.scaleRate = scaleRate      # 图片缩小比例
        self.image = pygame.image.load(imageAddress)    # 图片对象
        self.dragon = self.DragonImage()    # 恐龙运动图片

        self.dragonWidth = self.dragon[0].get_rect().width      # 图片长度
        self.dragonHeight = self.dragon[0].get_rect().height    # 图片高度

        self.X = 0      # X 坐标
        self.Y = 0      # Y 坐标

    # 获取恐龙运动图片
    def DragonImage(self):
        # 截取 image 的特定位置图片
        dragon1 = pygame.Surface.subsurface(self.image, (50, 24, 209, 105))
        dragon2 = pygame.Surface.subsurface(self.image, (308, 24, 209, 105))
        dragon3 = pygame.Surface.subsurface(self.image, (564, 22, 209, 105))
        dragon4 = pygame.Surface.subsurface(self.image, (50, 152, 209, 105))
        dragon5 = pygame.Surface.subsurface(self.image, (310, 152, 209, 105))
        dragon6 = pygame.Surface.subsurface(self.image, (564, 156, 209, 105))

        dragon = [dragon1, dragon2, dragon3, dragon4, dragon5, dragon6]
        dragon = [pygame.transform.rotozoom(dra, 0, self.scaleRate) for dra in dragon]      # 按一定比例缩小

        return dragon

    # 获取图片的碰撞面
    def Rect(self):
        return pygame.Rect(self.X, self.Y, self.dragonWidth - 20, self.dragonHeight)

# 获取子弹运动图片
class Flame:
    def __init__(self, imageAddress, scaleRate):
        '''

        :param imageAddress:        # 图片文件地址
        :param scaleRate:           # 图片缩小比例
        '''

        self.scaleRate = scaleRate  # 图片缩小比例
        self.image = pygame.image.load(imageAddress)  # 图片对象
        self.flame = self.FlameImage()      # 子弹图片

        self.X = 0  # X 坐标
        self.Y = 0  # Y 坐标

        self.flameWidth = self.flame.get_rect().width       # 图片长度
        self.flameHeight = self.flame.get_rect().height     # 图片高度

    # 子弹图片
    def FlameImage(self):
        flame = pygame.transform.rotozoom(self.image, 0, self.scaleRate)    # 按一定比例缩小

        return flame

    # 子弹的碰撞面
    def Rect(self):
        return pygame.Rect(self.X, self.Y, self.flameWidth, self.flameHeight)


# 获取药水图片
class Medicines:
    def __init__(self, imageAddress, scaleRate):
        '''

        :param imageAddress:        # 图片文件地址
        :param scaleRate:           # 图片缩小比例
        '''

        self.scaleRate = scaleRate      # 图片缩小比例
        self.image = pygame.image.load(imageAddress)        # 图片对象
        self.medicines = self.MedicinesImage()       # 药水图片列表 [速度药水，无敌药水，生命药水]

        self.X = 0  # X 坐标
        self.Y = 0  # Y 坐标

        self.imageIndex = 0        # 药水效果索引
        self.state = 'speed_up'     # 药水效果['speed_up', 'protect', 'recover']

        self.medicineWidth = self.medicines[0].get_rect().width         # 图片长度
        self.medicineHeight = self.medicines[0].get_rect().height       # 图片高度

    # 药水图片
    def MedicinesImage(self):
        medicine1 = pygame.Surface.subsurface(self.image, (0, 0, 247, 236))
        medicine2 = pygame.Surface.subsurface(self.image, (307, 0, 247, 236))
        medicine3 = pygame.Surface.subsurface(self.image, (639, 0, 247, 236))

        medicine = [medicine1, medicine2, medicine3]

        medicine = [pygame.transform.rotozoom(m, 0, self.scaleRate) for m in medicine]      # 按一定比例缩小

        return medicine

    # 药水移动
    def Move(self, speed):
        self.X -= speed

    # 获取药水的碰撞面
    def Rect(self):
        return pygame.Rect(self.X, self.Y, self.medicineWidth, self.medicineHeight)


# 获取爆炸动画图片
class Explosion:
    def __init__(self, imageAddress, scaleRate):
        '''

        :param imageAddress:        # 图片文件地址
        :param scaleRate:           # 图片缩小比例
        '''

        self.scaleRate = scaleRate  # 图片缩小比例
        self.image = pygame.image.load(imageAddress)  # 图片对象
        self.explosion = self.ExplosionImage()      # 爆炸图片

        self.explosionWidth = self.explosion[0].get_rect().width    # 爆炸图片的长度
        self.explosionHeight = self.explosion[0].get_rect().height  # 爆炸图片的高度

        self.X = 0      # X 的坐标
        self.Y = 0      # Y 的坐标

    def ExplosionImage(self):
        explosion = []      # 爆炸图片集合
        (width, height) = self.image.get_rect().size    # 整合的图片大小

        # 单张图片大小
        w = width / 6
        h = height / 5

        # 截取图片
        for j in range(5):
            exp = pygame.Surface.subsurface(self.image, (0, h * j, w, h))
            exp = pygame.transform.rotozoom(exp, 0, self.scaleRate)
            explosion.append(exp)

        return explosion


# 正确，错误 图片
class WrongRight:
    def __init__(self, imageAddress, scaleRate):
        self.scaleRate = scaleRate  # 图片缩小比例
        self.imageAddress = imageAddress  # 图片对象

        self.X = 0
        self.Y = 0

    def WRImage(self):
        image = pygame.image.load(self.imageAddress)
        image = pygame.transform.rotozoom(image, 0, self.scaleRate)

        return image


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    pygame.display.flip()  # 更新画布（一般用于第一次更新，更新整个画布）

    clock = pygame.time.Clock()
    fps = 30

    dragon = Dragon("image/dragon.png", 1)
    flame = Flame("image/flame.png", 1)
    medicines = Medicines("image/medicines.png", 0.2)
    explosion = Explosion("image/explosion.png", 1)

    dragonIndex = 0.0
    explosionIndex = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(dragon.dragon[int(dragonIndex)], (0, 0))
        screen.blit(flame.flame, (300, 0))
        screen.blit(medicines.medicines[0], (0, 150))
        screen.blit(medicines.medicines[1], (200, 150))
        screen.blit(medicines.medicines[2], (400, 150))
        screen.blit(explosion.explosion[int(explosionIndex)], (0, 400))

        dragonIndex = (dragonIndex + 0.01) % 6
        explosionIndex = (explosionIndex + 0.008) % 5

        pygame.display.update()

    pygame.quit()
