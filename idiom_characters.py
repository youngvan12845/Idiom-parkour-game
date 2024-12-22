import random


# 生成成语和需要填的字
class Idiom:
    def __init__(self, idiomAddress):
        self.idiomAddress = idiomAddress            # 成语文件的位置
        self.idiom_array = self.IdiomArray()[0]     # 成语数组
        self.characters = self.IdiomArray()[1]      # 文字数组
        self.idiomNum = len(self.idiom_array)       # 总成语数
        self.charaNum = len(self.characters)        # 总文字数

    # 成语数组
    def IdiomArray(self):
        with open(self.idiomAddress, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]

        # 获取所有的文字
        characters = []
        for line in lines:
            characters += line

        return lines, characters

    # 随机获取一定数量的成语
    def IdiomPre(self, idiom_num):
        # 需要的成语
        pre_array = []
        for i in range(idiom_num):
            random_idiom = random.randint(0, self.idiomNum - 1)
            pre_array.append(self.idiom_array[random_idiom])

        return pre_array

    # 获取所有正确文字和干扰文字
    def Characters_all(self, idiom_num, pre_array):
        # 正确文字[0]，干扰文字[1] [2] [3]
        # 二维数组
        charaAll_array = []

        # 需要缺少的汉字的索引
        chara_index_array = []

        for i in range(idiom_num):
            # 缺字位置，和缺少的字
            chara_index = random.randint(0, 3)
            chara_Right = pre_array[i][chara_index]

            chara_array = self.Getcharacters(chara_Right, 3)

            charaAll_array.append(chara_array)
            chara_index_array.append(chara_index)

        # 正确文字在 charaAll_array 中的每一行的第一个
        return charaAll_array, chara_index_array

    # 获取正确文字和干扰文字
    def Getcharacters(self, chara_Right, chara_num):
        # 保存正确文字和干扰文字的列表
        chara_array = [chara_Right]

        for i in range(chara_num):
            other_chara_index = random.randint(0, self.charaNum - 1)
            other_chara = self.characters[other_chara_index]

            # 保证文字不会重到
            while other_chara in chara_array:
                other_chara_index = random.randint(0, self.charaNum - 1)
                other_chara = self.characters[other_chara_index]

            chara_array.append(other_chara)

        return chara_array

    # 只生成一个成语 格式: [[成语], [正确文字在成语中的索引], [文字], [正确文字在文字列表中的索引]]
    def IdiomCharacters(self):
        # 预设的成语
        pre_array = self.IdiomPre(1)

        # 文字，正确文字索引
        charaAll_array, chara_index_array = self.Characters_all(1, pre_array)
        chara_array = charaAll_array[0]

        # 正确文字在 文字列表中的索引
        right_index = random.randint(0, 3)

        # 改变正确文字的位置
        temp = chara_array[0]
        chara_array[0] = chara_array[right_index]
        chara_array[right_index] = temp

        return [pre_array, chara_index_array, chara_array, [right_index]]


if __name__ == "__main__":
    idiom = Idiom('idiom/idiom.txt')
    array = idiom.IdiomCharacters()

    print(array)
