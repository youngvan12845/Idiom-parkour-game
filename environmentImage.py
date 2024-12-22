import pygame


class Environment:
    def __init__(self, imageAddress, scaleRate):
        '''

        :param imageAddress:        # 图片文件地址
        :param scaleRate:           # 图片放大比例
        '''
        self.scaleRate = scaleRate      # 图片放大比例
        self.image = pygame.image.load(imageAddress)        # 图片对象

        self.environments = self.EnvironmentImage()         # 图片集合

        self.X = 0  # X 坐标
        self.Y = 0  # Y 坐标

    # 获取环境图片
    def EnvironmentImage(self):
        environment1 = pygame.Surface.subsurface(self.image, (25, 25, 6, 37))
        environment2 = pygame.Surface.subsurface(self.image, (32, 0, 30, 30))
        environment3 = pygame.Surface.subsurface(self.image, (54, 30, 9, 33))

        environment1 = pygame.transform.rotozoom(environment1, 90, self.scaleRate)
        environment2 = pygame.transform.rotozoom(environment2, 0, self.scaleRate)
        environment3 = pygame.transform.rotozoom(environment3, 0, self.scaleRate)

        environments = [environment1, environment2, environment3]

        return environments


if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))

    environment = Environment("image/EnvironmentTiles.png", 3)

    screen.blit(environment.environments[0], (0, 0))
    screen.blit(environment.environments[1], (0, 150))
    screen.blit(environment.environments[2], (0, 300))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
