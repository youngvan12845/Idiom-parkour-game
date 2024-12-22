from sundryImage import *
from sceneSurface import *
from idiom_characters import *
from idiomFrame import *
from function import *
import random
import time
import concurrent.futures

# 屏幕大小，背景颜色
mainWidth = 1200
mainHeight = 800
mainBackColor = (22, 65, 124)       # 主界面的背景颜色
groundBackColor = (255, 255, 255)   # 地面的背景颜色
ground_X1 = 0                       # 第一个地面场景的 X 坐标
ground_X2 = ground_X1 + mainWidth   # 第二个地面场景的 X 坐标
fontColor = (0, 0, 0)               # 文字的字体颜色
fontBackcolor = (115, 151, 253)     # 文字的背景颜色
frameLocate_y = 650                 # 成语框的 y 坐标
font1 = 30          # 屏幕上移动的文字的字体大小
font2 = 45          # 成语框中的文字的字体大小
mask = 0            # 游戏分数

# 图片地址
environmentAddress = "dist/image/EnvironmentTiles.png"
playerAddress = "dist/image/LightBandit.png"
dragonAddress = "dist/image/dragon.png"
flameAddress = "dist/image/flame.png"
explosionAddress = "dist/image/explosion.png"
idiomAddress = "dist/idiom/idiom.txt"
idiomFrameAddress = "dist/image/idiomFrame2.png"
wrongAddress = "dist/image/wrongIdiom2.png"
rightAddress = "dist/image/rightIdiom2.png"
medicineAddress = "dist/image/medicines.png"
buttonUpAddress = "dist/image/game_start_up.png"
buttonDownAddress = "dist/image/game_start_down.png"

# 图片缩放比例
environmentScaleRate = 4
playerScaleRate = 1.5
dragonScaleRate = 1
flameScaleRate = 1
explosionScaleRate = 0.5
wrongScaleRate = 1
rightScaleRate = 1
medicineScaleRate = 0.2

# 生成对象
environment = Environment(environmentAddress, environmentScaleRate)
player = Player(playerAddress, playerScaleRate)
dragon = Dragon(dragonAddress, dragonScaleRate)
flameList = [Flame(flameAddress, flameScaleRate), Flame(flameAddress, flameScaleRate)]
explosion = [Explosion(explosionAddress, explosionScaleRate) for ex in range(2)]

# 成语框对象
idiomFrameList = [IdiomFrame(idiomFrameAddress, mainBackColor, fontColor) for fr in range(4)]

# 文字对象
characterList1 = [CharacterRect(fontColor, fontBackcolor, font1) for ch1 in range(4)]

characterList2 = [CharacterRect(fontColor, fontBackcolor, font1) for ch2 in range(4)]

frameCharacterList = [CharacterRect(fontColor, fontBackcolor, font2) for fc in range(4)]

# 药水对象
medicine = Medicines(medicineAddress, medicineScaleRate)

# 生成成语对象
idiom1 = Idiom(idiomAddress)
idiom2 = Idiom(idiomAddress)

# 正确，错误图片对象
wrong = WrongRight(wrongAddress, wrongScaleRate)
right = WrongRight(rightAddress, rightScaleRate)

wrong.X, wrong.Y = (300, frameLocate_y)
right.X, right.Y = (300, frameLocate_y)

# 生成成语及 正确/错误 的缺字 及 它们的索引，目前该显示的成语
idiom_chara1 = [[['', '', '', '']], [0], ['', '', '', ''], [0]]
idiom_chara2 = idiom2.IdiomCharacters()
present_idiom = idiom_chara2[0][0]
present_index = idiom_chara2[1][0]

# 缺少的字，接触到的字
right_chara = idiom_chara2[2][idiom_chara2[3][0]]
col_chara = ''

sceneInit = SceneInit(environmentAddress, environmentScaleRate, ground_X1)  # 初始场景对象
sceneList1 = [Scene1(environmentAddress, environmentScaleRate, ground_X1, idiom_chara1),  # 场景对象列表
              Scene2(environmentAddress, environmentScaleRate, ground_X1, idiom_chara1),
              Scene3(environmentAddress, environmentScaleRate, ground_X1, idiom_chara1),
              sceneInit]
sceneList2 = [Scene1(environmentAddress, environmentScaleRate, ground_X2, idiom_chara2),  # 场景对象列表
              Scene2(environmentAddress, environmentScaleRate, ground_X2, idiom_chara2),
              Scene3(environmentAddress, environmentScaleRate, ground_X2, idiom_chara2)]

# 显示的图片的索引
condition = 0       # 索引累加的条件
environmentIndex = 0
playerIndex = 0
dragonIndex = 0
explosionIndex1 = 0
explosionIndex2 = 0
randomIndex1 = -1
randomIndex2 = random.randint(0, 1)

# 各种基础属性
player_lives = 3    # 玩家生命值（程序开始前设定，不在程序中修改）
groundSpeed = 2     # 地面移动速度
addSpeed = 1        # 额外速度
dragonSpeed = 1     # 恐龙速度
jumpSpeed = 2       # 跳跃速度（程序开始前设定，不在程序中修改）
jumpTime = 60       # 跳跃的时间（循环遍历次数）（程序开始前设定，不在程序中修改）
jumpingHeight = 0   # 已经跳跃的高度
jumpingTime = 300   # 已经跳跃的时间 (循环遍历次数)
attackIndex = 0.    # 玩家攻击图片索引
attackSpeed = 0.15   # 玩家攻击速度（程序开始前设定，不在程序中修改）
hurtIndex = 0.      # 玩家受伤图片索引
hurtSpeed = 0.08    # 玩家受伤图片更新速度（程序开始前设定，不在程序中修改）
attackStopSpeed = groundSpeed    # 玩家攻击停止移动，限制屏幕的速度（程序开始前设定，不在程序中修改）
flameSpeed = 2      # 子弹相对于地面的速度（程序开始前设定，不在程序中修改）
sceneId = 1      # 玩家目前所在的场景的编号
buff_speed_up_time = 1000   # 加速 buff 的时间（程序开始前设定，不在程序中修改）
buff_protect_time = 1000    # 保护 buff 的时间（程序开始前设定，不在程序中修改）
buffing_time = 0      # buff 的剩余时间
flameLocateList1 = [450, 330]    # 子弹位置列表
flameLocate2 = 0    # 子弹位置

# 人物状态
player.stateArray = ['run', 'jump', 'fall', 'attack', 'hit', 'fly', 'speed_up']
formerState = 'run'     # 玩家之前状态（主要用于其他状态转换为 hit 时使用）

# 判断类型变量
flameHitting1 = False   # 子弹是否击中
flameHitting2 = False   # 子弹是否击中
col_chara_index = [-1, -1]      # 碰撞文字所在的场景编号，碰撞文字的索引
col_chara1 = False      # 是否和 scene1 中的文字发生碰撞
col_chara2 = False      # 是否和 scene2 中的文字发生碰撞
changeFrame = True      # 是否更换成语框中的成语
changeScene = False     # 是否更换了场景
scene_to_1 = False      # 由 2 到 1
scene_to_2 = False      # 由 1 到 2
rightCharacter = None   # 成语是否填对
get_medicine = False    # 是否获得药水
col_medicine = False    # 是否碰到药水

# 地面，人物，子弹的位置（X， Y 分开写可以方便对坐标进行更改）
scene_X1 = ground_X1
scene_X2 = ground_X2
groundLocationY = 500

player.X = 600
player.Y = groundLocationY - player.initHeight

dragon.X = 20
dragon.Y = groundLocationY - dragon.dragonHeight

flameList[0].X = mainWidth
flameList[0].Y = flameLocateList1[random.randint(0, 1)]

# 设置成语框的位置
SetFramesLocation(idiomFrameList, mainWidth, frameLocate_y)

# 初始化
pygame.init()

# 设置屏幕大小，背景颜色，玩家状态图片
screen = pygame.display.set_mode((mainWidth, mainHeight))
pygame.display.set_caption('里奥学成语')
screen.fill(mainBackColor)
player.presentImage = player.run[playerIndex]

# 绘制人物，场景，成语框，药水
screen.blit(player.presentImage, (player.X, player.Y))
screen.blit(dragon.dragon[dragonIndex], (dragon.X, dragon.Y))

the_sceneInit = sceneInit.GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY)   # 初始场景图片
the_sceneList1 = [sceneList1[0].GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY),    # 场景图片
                  sceneList1[1].GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY),
                  sceneList1[2].GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY),
                  the_sceneInit]
the_sceneList2 = [sceneList2[0].GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY),    # 场景图片
                  sceneList2[1].GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY),
                  sceneList2[2].GetScene(mainWidth, mainHeight, mainBackColor, groundLocationY)]

frame_rectList = UpdateFramesCharacter(idiomFrameList)      # 成语框图片

# scene1 上的文字
# 由于第一轮的时候，scene1 是 初始场景，不需要显示文字，所以把character1初始化为没有任何内容的 Surface 对象集
characters1 = [pygame.Surface((0, 0)) for ch in range(4)]

# scene2 上的文字
rect = sceneList2[randomIndex2].Rect()
characters_rect = GetCharactersRect(rect)
UpdateCharactersLocation(characterList2, characters_rect)
characters2 = UpdateCharacters(characterList2, idiom_chara2[2])

# 成语框中的文字
frame_rect = [idiomFrameList[fr].fontLocation for fr in range(4)]
UpdateCharactersLocation(frameCharacterList, frame_rect)
frameCharacter = UpdateCharaWithoutBack(frameCharacterList, present_idiom)

# 药水图片
medicineImage = medicine.MedicinesImage()[random.randint(0, 2)]

screen.blit(the_sceneInit, (scene_X1, 0))
screen.blit(the_sceneList2[randomIndex2], (scene_X2, 0))

# 显示 scene2 和 成语框 上的文字
for i in range(4):
    screen.blit(characters2[i], (characterList2[i].X, characterList2[0].Y))
    screen.blit(frameCharacter[i], idiomFrameList[i].fontLocation)

# 更新画布（一般用于第一次更新，更新整个画布）
pygame.display.flip()

starting = True     # 开始（代表是否运行开始界面）
running = False     # 运行（代表是否运行游戏程序）
ending = False      # 结束（代表是否运行游戏结算界面）

# -------------等待开始界面---------------------
start_screen = pygame.display.set_mode((mainWidth, mainHeight))     # 等待开始界面
pygame.display.set_caption('里奥学成语')
start_screen.fill(mainBackColor)

npc_index = 0
npc_speed = 3

npc = Player(playerAddress, 2.4)
npc.X = 550
npc.Y = 300 - npc.presentHeight

start_scene1 = SceneInit(environmentAddress, environmentScaleRate, 0)  # 初始场景对象
start_the_scene1 = start_scene1.GetScene(mainWidth, mainHeight, mainBackColor, 300)

start_scene2 = SceneInit(environmentAddress, environmentScaleRate, mainWidth)  # 初始场景对象
start_the_scene2 = start_scene2.GetScene(mainWidth, mainHeight, mainBackColor, 300)

button_down = False
buttonUp = pygame.image.load(buttonUpAddress)
buttonDown = pygame.image.load(buttonDownAddress)

btn_width, btn_height = buttonUp.get_rect().size
btn_X = (mainWidth - btn_width) / 2
btn_Y = 550

buttonRect = pygame.Rect(btn_X, btn_Y, btn_width, btn_height)

while starting:
    time.sleep(0.01)

    # 事件检测
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting = False

    mouse_pos = pygame.mouse.get_pos()      # 获取鼠标位置
    button_down = buttonRect.collidepoint(mouse_pos)    # 判断鼠标是否悬停在开始游戏按钮上

    npc_index = (npc_index + 0.08) % 8   # 索引递增

    # 地面移动
    start_scene1.X -= npc_speed
    start_scene2.X -= npc_speed

    if start_scene1.X <= -mainWidth:
        start_scene1.X = mainWidth

    if start_scene2.X <= -mainWidth:
        start_scene2.X = mainWidth

    # 点击开始游戏按钮
    if button_down and pygame.mouse.get_pressed()[0]:
        starting = False
        running = True

    # 绘制各个图像
    start_screen.fill(mainBackColor)
    start_screen.blit(start_the_scene1, (start_scene1.X, start_scene1.Y))
    start_screen.blit(start_the_scene2, (start_scene2.X, start_scene2.Y))
    start_screen.blit(npc.run[int(npc_index)], (npc.X, npc.Y))
    if not button_down:
        start_screen.blit(buttonUp, (btn_X, btn_Y))
    else:
        start_screen.blit(buttonDown, (btn_X, btn_Y))

    pygame.display.update()

# 如果要开始游戏，则先显示空白，用来过度游戏的开始
if running:
    screen.fill(mainBackColor)
    pygame.display.update()
    time.sleep(0.6)

# ---------------开始游戏----------------------
while running:
    time.sleep(0.004)

    # 停止当前正在进行的文本输入
    # 使用 key.stop_text_input() 和 key.start_text_input() 解决 按下 j 后没有反应的问题
    pygame.key.stop_text_input()

    # 事件监测
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 空格键被按下（跳跃）
            if (event.key == pygame.K_SPACE) and (player.state == 'run'):
                player.state = 'jump'
                jumpingTime = 0     # 重置跳跃时间
            # j键被按下（攻击）
            elif (event.key == pygame.K_j) and (player.state == 'run'):
                player.state = 'attack'

    # 开始文本输入
    pygame.key.start_text_input()

    # 游戏结束
    if player_lives < 0:    # 角色生命值低于 0
        running = False
        ending = True
    if player.Y >= groundLocationY:     # 角色掉入悬崖
        running = False
        ending = True

    # 碰撞事件
    # 判断玩家是否和恐龙发生碰撞
    if player.Rect().colliderect(dragon.Rect()):
        running = False
        ending = True
    # 判断恐龙是否和子弹碰撞
    elif dragon.Rect().colliderect(flameList[0].Rect()):
        flameHitting1 = True  # 子弹击中 -- True
        explosionIndex1 = 0  # 爆炸图片索引从 0 开始
        explosion[0].X = flameList[0].X  # 爆炸图片的位置 -- X
        explosion[0].Y = flameList[0].Y  # 爆炸图片的位置 -- Y
        flameList[0].X = mainWidth + 500  # 重置子弹位置
    elif dragon.Rect().colliderect(flameList[1].Rect()):
        flameHitting2 = True  # 子弹击中 -- True
        explosionIndex2 = 0  # 爆炸图片索引从 0 开始
        explosion[1].X = flameList[1].X  # 爆炸图片的位置 -- X
        explosion[1].Y = flameList[1].Y  # 爆炸图片的位置 -- Y
        flameList[1].Y = -100  # 重置子弹位置
    # 判断玩家是否和子弹碰撞
    elif player.Rect().colliderect(flameList[0].Rect()):
        # 假如玩家未砍中子弹
        if (player.state != 'attack') and (player.buff != 'protect'):
            player_lives -= 1   # 玩家生命值 -1
            formerState = player.state   # 记录玩家此时状态
            player.state = 'hit'     # 玩家状态改为被击中（hit）
            flameHitting1 = True     # 子弹击中 -- True
            explosionIndex1 = 0      # 爆炸图片索引从 0 开始
            explosion[0].X = flameList[0].X   # 爆炸图片的位置 -- X
            explosion[0].Y = flameList[0].Y   # 爆炸图片的位置 -- Y
        # 假如玩家砍中了子弹
        else:
            pass
        flameList[0].X = mainWidth + 500  # 重置子弹位置

    elif player.Rect().colliderect(flameList[1].Rect()):
        # 假如玩家未砍中子弹
        if (player.state != 'attack') and (player.buff != 'protect'):
            player_lives -= 1  # 玩家生命值 -1
            formerState = player.state  # 记录玩家此时状态
            player.state = 'hit'  # 玩家状态改为被击中（hit）
            flameHitting2 = True  # 子弹击中 -- True
            explosionIndex2 = 0  # 爆炸图片索引从 0 开始
            explosion[1].X = flameList[1].X  # 爆炸图片的位置 -- X
            explosion[1].Y = flameList[1].Y  # 爆炸图片的位置 -- Y
        # 假如玩家砍中了子弹
        else:
            pass
        flameList[1].Y = -100  # 重置子弹位置

    # 玩家状态更改
    # 玩家跳跃
    if player.state == 'jump':
        if jumpingTime < jumpTime:
            jumpingHeight += jumpSpeed
            jumpingTime += 1
        else:
            player.state = 'fall'
    # 玩家下落
    elif player.state == 'fall':
        jumpingHeight -= jumpSpeed
    # 玩家攻击
    elif player.state == 'attack':
        # 累加玩家攻击索引
        attackIndex += attackSpeed

        # 玩家攻击时，相对与地面停止移动
        # 即：界面停止移动，恐龙向前移动
        groundSpeed = 0
        dragon.X += attackStopSpeed
        # 当遍历完所有的攻击图片，更改玩家状态，攻击索引改为 0
        if attackIndex >= 8.:
            player.state = 'run'
            attackIndex = 0.
            # 由于攻击时界面停止移动，所以攻击停止后，界面需恢复，恢复原速度
            groundSpeed = attackStopSpeed
    # 玩家受伤
    elif player.state == 'hit':
        # 累加玩家受伤索引
        hurtIndex += hurtSpeed
        # 当遍历完所有的受伤图片，还原玩家状态，受伤索引改为 0
        if hurtIndex >= 2.:
            player.state = formerState   # 还原受伤前的状态
            hurtIndex = 0.

    # 场景改变
    if scene_X1 <= -mainWidth:
        get_medicine = False    # 生成药水 -> false
        scene_X1 = mainWidth
        sceneList1[randomIndex1].UpdateLocation(mainWidth)
        randomIndex1 = random.randint(0, 2)
        sceneList1[randomIndex1].Update(mainWidth)

        # 更新文字
        '''idiom_chara1 = idiom1.IdiomCharacters()
        rect = sceneList1[randomIndex1].Rect()
        characters_rect = GetCharactersRect(rect)
        UpdateCharactersLocation(characterList1, characters_rect)
        characters1 = UpdateCharacters(characterList1, idiom_chara1[2])'''

    if scene_X2 <= -mainWidth:
        scene_X2 = mainWidth
        sceneList2[randomIndex2].UpdateLocation(mainWidth)
        randomIndex2 = random.randint(0, 1)
        sceneList2[randomIndex2].Update(mainWidth)

        # 更新文字
        changeFrame = True
        idiom_chara2 = idiom2.IdiomCharacters()
        rect = sceneList2[randomIndex2].Rect()
        characters_rect = GetCharactersRect(rect)
        UpdateCharactersLocation(characterList2, characters_rect)
        characters2 = UpdateCharacters(characterList2, idiom_chara2[2])
        present_idiom = idiom_chara2[0][0]
        present_index = idiom_chara2[1][0]
        right_chara = idiom_chara2[2][idiom_chara2[3][0]]
        rightCharacter = None

    # 多线程运行
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 更改成语框中的文字（这一步花的时间较长，所以放在线程里）
        if changeFrame:
            # 和文字发生碰撞改为 False
            future1 = executor.submit(UpdateFrameCharacter, frameCharacterList, present_idiom, present_index)
            # 获取线程函数的返回值
            frameCharacter, changeFrame = future1.result()

        # 检测玩家是否和文字发生碰撞
        future2 = executor.submit(ColliderectPlayerChara, characterList1, characterList2,
                                  player.Rect(), col_chara1, col_chara2)
        # 获取线程函数的返回值
        # 碰撞文字所在的场景编号和碰撞文字的索引，是否和文字发生碰撞
        col_chara_index, col_chara1, col_chara2 = future2.result()

        '''# 玩家和 character1 中的文字发生碰撞
        if col_chara_index[0] == 1:
            index = col_chara_index[1]
            future3 = executor.submit(UpdateColCharacter, index, characterList1,
                                      frameCharacterList, present_idiom, present_index)
            characters1, frameCharacter = future3.result()'''
        # 玩家和 character2 中的文字发生碰撞
        if col_chara_index[0] == 2:
            index = col_chara_index[1]
            future4 = executor.submit(UpdateColCharacter, index, characterList2,
                                      frameCharacterList, present_idiom, present_index)
            characters2, frameCharacter, col_chara = future4.result()

            # 判断碰到的字是否正确
            if col_chara == right_chara:
                rightCharacter = True
                mask += 1   # 游戏分数 +1
            else:
                rightCharacter = False
                flameList[1].X = mainWidth
                flameList[1].Y = player.Y + 20

        # 设置药水
        if not get_medicine and (scene_X1 == mainWidth):
            future5 = executor.submit(UpdateMedicine, medicine, sceneList1[randomIndex1].Rect(),
                                      (mainWidth, mainWidth * 2), (200, groundLocationY))
            get_medicine, medicine = future5.result()

    # 地面移，药水移动
    scene_X1 -= groundSpeed
    sceneList1[randomIndex1].Move(groundSpeed)

    scene_X2 -= groundSpeed
    sceneList2[randomIndex2].Move(groundSpeed)

    if get_medicine:    # 移动药水（前提是生成了药水）
        medicine.Move(groundSpeed)

        # 如果玩家碰到了药水，设置 get_medicine 为 false，药水则会消失
        if medicine.Rect().colliderect(player.Rect()):
            get_medicine = False
            col_medicine = True

    # 更新玩家信息（药水效果）
    if col_medicine:
        col_medicine = False

        if medicine.state == 'recover':     # 恢复药水
            player_lives += 1
        elif medicine.state == 'speed_up':  # 加速药水
            player.buff = 'speed_up'
            buffing_time = buff_speed_up_time
            groundSpeed += addSpeed
        elif medicine.state == 'protect':   # 保护药水
            player.buff = 'protect'
            buffing_time = buff_protect_time

    # 玩家 buff 时间减少
    if player.buff == 'speed_up':
        buffing_time -= 1
        dragon.X -= dragonSpeed     # 恐龙后退
    elif player.buff == 'protect':
        buffing_time -= 1

    # 如果 获得了 buff 且 buff 时间结束，则清除 buff
    if (player.buff != '') and (buffing_time <= 0):
        player.buff = ''
        groundSpeed = attackStopSpeed

    # 文字移动
    MoveCharacters(characterList1, groundSpeed)
    MoveCharacters(characterList2, groundSpeed)

    # 子弹移动
    flameList[0].X -= groundSpeed + flameSpeed
    flameList[1].X -= groundSpeed + flameSpeed
    if flameList[0].X <= -100:
        flameList[0].X = mainWidth
        flameList[0].Y = flameLocateList1[random.randint(0, 10) % 2]

    # 人物运动，子弹爆炸显示
    condition += 1
    if flameHitting1 and (condition % 8 == 0):
        explosionIndex1 = (explosionIndex1 + 1) % 5

        # 如果已经遍历完了所有爆炸图片，则 爆炸显示（flameHitting1）不为真
        if explosionIndex1 == 4:
            flameHitting1 = False

    if flameHitting2 and (condition % 8 == 0):
        explosionIndex2 = (explosionIndex2 + 1) % 5

        # 如果已经遍历完了所有爆炸图片，则 爆炸显示（flameHitting1）不为真
        if explosionIndex2 == 4:
            flameHitting2 = False

    if condition % 16 == 0:
        playerIndex = (playerIndex + 1) % 8
        dragonIndex = (dragonIndex + 1) % 6
        condition = 0

    # 玩家图片更新
    if player.state == 'run':
        player.presentImage = player.run[playerIndex]   # 更新目前图片
        player.presentHeight = player.runHeight         # 更新目前图片高度
    elif player.state == 'jump':
        player.presentImage = player.jump               # 更新目前图片
        player.presentHeight = player.jumpHeight        # 更新目前图片高度
    elif player.state == 'fall':
        player.presentImage = player.jump               # 更新目前图片
        player.presentHeight = player.jumpHeight        # 更新目前图片高度
    elif player.state == 'attack':
        player.presentImage = player.attack[int(attackIndex)]       # 更新目前图片
        player.presentHeight = player.attackHeight      # 更新目前图片高度
    elif player.state == 'hit':
        player.presentImage = player.hurt[int(hurtIndex)]
        player.presentHeight = player.hurtHeight

    # 调整玩家的 Y 坐标 和 玩家图片底端的 Y 坐标
    player.Y = groundLocationY - player.presentHeight - jumpingHeight
    player.foot = player.Y + player.presentHeight

    # 调整恐龙位置
    if (dragon.X < 20) and (player.buff != 'speed_up'):
        dragon.X += dragonSpeed

    # 如果玩家在 randomScene1 中，则判断是否和 randomScene1 中的 pygame.Rect() 发生碰撞
    if (scene_X1 - 10 <= player.X) and (player.X <= scene_X1 + mainWidth - 10):
        sceneList1[randomIndex1].colliderectToPlayer(player)
        '''present_idiom = idiom_chara1[0][0]
        present_index = idiom_chara1[1][0]
        # 如果玩家从 场景2 到了 场景1 并且 在此过程中玩家未和文字碰撞，则 changeScene 变为 True
        if sceneId == 2:
            scene_to_1 = True
        sceneId = 1         # 更改玩家所在场景的编号'''
    # 否则，判断是否和 randomScene2 中的 pygame.Rect() 发生碰撞
    else:
        sceneList2[randomIndex2].colliderectToPlayer(player)
        '''present_idiom = idiom_chara2[0][0]
        present_index = idiom_chara2[1][0]
        # 如果玩家从 场景1 到了 场景2  并且 在此过程中玩家未和文字碰撞，则 changeScene 变为 True
        if sceneId == 1:
            scene_to_2 = True
        sceneId = 2         # 更改玩家所在场景的编号'''

    # 绘制各种图片
    screen.fill(mainBackColor)
    screen.blit(the_sceneList1[randomIndex1], (scene_X1, 0))
    screen.blit(the_sceneList2[randomIndex2], (scene_X2, 0))
    screen.blit(flameList[0].flame, (flameList[0].X, flameList[0].Y))
    screen.blit(flameList[1].flame, (flameList[1].X, flameList[1].Y))
    screen.blit(player.presentImage, (player.X, player.Y))
    screen.blit(dragon.dragon[dragonIndex], (dragon.X, dragon.Y))

    # 显示药水
    if get_medicine:
        screen.blit(medicine.MedicinesImage()[medicine.imageIndex], (medicine.X, medicine.Y))

    # 如果子弹有击中，则绘制爆炸图片
    if flameHitting1:
        screen.blit(explosion[0].explosion[explosionIndex1], (explosion[0].X - 20, explosion[0].Y - 20))

    if flameHitting2:
        screen.blit(explosion[1].explosion[explosionIndex2], (explosion[1].X - 20, explosion[1].Y - 20))

    # 显示文字，成语框
    for i in range(4):
        screen.blit(characters1[i], (characterList1[i].X, characterList1[i].Y))
        screen.blit(characters2[i], (characterList2[i].X, characterList2[i].Y))
        screen.blit(frame_rectList[i], (idiomFrameList[i].X, idiomFrameList[i].Y))
        screen.blit(frameCharacter[i], idiomFrameList[i].fontLocation)

    # 正确，错误 图片显示
    if rightCharacter is not None:
        if rightCharacter:
            screen.blit(right.WRImage(), (right.X, right.Y))
        else:
            screen.blit(wrong.WRImage(), (wrong.X, wrong.Y))

    # 玩家状态类信息显示
    font = pygame.font.SysFont('SimHei', 25)
    title1 = font.render("生命", True, (255, 255, 255))
    title2 = font.render("状态", True, (255, 255, 255))
    title3 = font.render("buff", True, (255, 255, 255))
    title4 = font.render("分数", True, (255, 255, 255))

    result1 = font.render(str(player_lives), True, (255, 255, 255))
    result2 = font.render(str(player.state), True, (255, 255, 255))
    result3 = font.render(str(player.buff) + '(' + str(buffing_time)[0] + 's' + ')',
                          True, (255, 255, 255))
    result4 = font.render(str(mask), True, (255, 255, 255))

    screen.blit(title1, (0, 0))
    screen.blit(title2, (0, 40))
    screen.blit(title3, (0, 80))
    screen.blit(title4, (0, 120))
    screen.blit(result1, (100, 0))
    screen.blit(result2, (100, 40))
    screen.blit(result3, (100, 80))
    screen.blit(result4, (100, 120))

    pygame.display.update()

# 如果要打开结算界面，则先显示空白，用来过度
if ending:
    screen.fill((255, 255, 255))
    pygame.display.update()
    time.sleep(0.6)

# -----------------------游戏结算界面-----------------------
ending_backcolor = (255, 255, 255)      # 背景颜色
font_color = (0, 0, 0)      # 字体颜色

with open("grade/grade.txt", 'r') as file:
    best_grade = file.read()

if int(best_grade) < mask:
    with open("grade/grade.txt", 'w+') as file:
        file.write(str(mask))

screen = pygame.display.set_mode((mainWidth, mainHeight))
pygame.display.set_caption('里奥学成语')
screen.fill(ending_backcolor)

font = pygame.font.SysFont('SimHei', 50)
title1 = font.render("你的分数是 : ", True, font_color)
title2 = font.render("此前最佳分数是 : ", True, font_color)

result1 = font.render(str(mask), True, font_color)
result2 = font.render(best_grade, True, font_color)

screen.blit(title1, (200, 150))
screen.blit(title2, (200, 500))
screen.blit(result1, (800, 150))
screen.blit(result2, (800, 500))

if ending:
    pygame.display.flip()

running_time = 5

while ending:
    time.sleep(1)

    # 事件监测
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ending = False

    running_time -= 1

    # 一定时间后自动关闭
    if running_time <= 0:
        ending = False

    pygame.display.flip()

pygame.quit()
