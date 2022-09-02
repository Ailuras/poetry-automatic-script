import os
import pandas as pd
import re
from langconv import *
import pyperclip
import pyautogui
import time
import platform
from cnocr import CnOcr

class quantangshi:
    imageInfo = {'keywords':(422, 222, 230, 33), 'room1':(422, 222, 230, 33), 'room2':(422, 222, 230, 33), 'money':(422, 222, 230, 33), 'strength':(422, 222, 230, 33)}
    # room = {1:[1, 2], 2:[1, 2]}
    
    def __init__(self):
        path = '../chinesePoetry/quan_tang_shi/json'
        file_list = os.listdir(path)
        # self.df = pd.DataFrame(columns=['no#', 'title', 'paragraphs'])
        self.df = pd.DataFrame(columns=['paragraphs'])
        for filename in file_list:
            df1 = pd.read_json(path + '/' + filename)
            # df1 = df1[['no#', 'title', 'paragraphs']]
            df1 = df1[['paragraphs']]
            self.df = pd.concat([self.df, df1], axis=0)
        for index, row in self.df.iterrows():
            data = []
            # print(row['paragraphs'])
            for s in row['paragraphs']:
                s = self.traditional_to_simplified(s)
                sentence = re.split('，|。|、|？', s)[:-1]
                data += sentence
            # print(data)
            row['paragraphs'] = data

    def traditional_to_simplified(self, sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence

    def get_info(self, filename):
        if not self.imageInfo.has_key(filename):
            return ''
        pyautogui.screenshot(filename+'.png', region=self.imageInfo[filename])
        ocr = CnOcr() 
        res = ocr.ocr_for_single_line(filename)
        if len(res[0] > 0):
            return ''.join(res[0])
        elif filename == 'room1' or filename == 'room2':
            return '0个'
        else:
            raise Exception('图片有误！')

    def get_keyword(self):
        try:
            self.fw.activate()
        except:
            self.fw.minimize()
            self.fw.restore()
        time.sleep(0.5)
        res = self.get_info('keywords')
        self.keywords = res[1]
        if res[2] != '】':
            self.keywords += res[2]
        self.location = int(res[-1])  
    
    def has_strength(self):
        try:
            self.fw.activate()
        except:
            self.fw.minimize()
            self.fw.restore()
        time.sleep(0.5)
        pyautogui.moveTo(370, 915)
        pyautogui.click()
        res = self.get_info('strength')
        if res[0] == '0':
            return False
        else:
            return True

    def has_money(self):
        try:
            self.fw.activate()
        except:
            self.fw.minimize()
            self.fw.restore()
        time.sleep(0.5)
        pyautogui.moveTo(370, 915)
        pyautogui.click()
        res = self.get_info('money')
        return int(res) > 200

    def which_room(self):
        try:
            self.fw.activate()
        except:
            self.fw.minimize()
            self.fw.restore()
        time.sleep(0.5)
        pyautogui.moveTo(370, 915)
        pyautogui.click()
        res1 = self.get_info('room1')[:-1]
        res2 = self.get_info('room2')[:-1]
        return 1 if int(res1) < int(res2) else 2

    def start(self):
        try:
            self.fw.activate()
        except:
            self.fw.minimize()
            self.fw.restore()
        time.sleep(0.5)
        index = self.which_room()
        pyautogui.moveTo(self.room[index][0], self.room[index][1])
        if index == 1:
            pyautogui.moveTo(1, 2)
        else:
            pyautogui.moveTo(1, 2)
        pyautogui.click()
        try:
            res = self.get_info('keywords')
            if res[0] != ['【']:
                raise Exception()
        except:
            if index == 1:
                pyautogui.moveTo(1, 1)
            else:
                pyautogui.moveTo(1, 1)
            pyautogui.click()

    def exit(self):
        try:
            self.fw.activate()
        except:
            self.fw.minimize()
            self.fw.restore()
        time.sleep(0.5)
        pyautogui.moveTo(1, 2)
        pyautogui.click()

    def run(self, times, numbers):
        fw = pyautogui.getWindowsWithTitle('火') 
        if len(fw) > 0:
            self.fw = fw[0]
            self.fw.width = 518
            self.fw.height = 920
            self.fw.topleft = (340, 40)
        else:
            raise Exception('没有打开小程序！')
        for i in range(times):
            self.start()
            self.get_keywords()
            self.serach()
            self.paste(numbers)
            self.exit()
            if not self.has_strength():
                if self.has_money():
                    self.gain_strength()
                else:
                    print('结束！')
                    return

    def serach(self):
        self.flag = 0
        keywords = self.keywords
        location = self.location-1
        ans = []
        if self.location == -1:
            for index, row in self.df.iterrows():
                # l = [item for item in row['paragraphs'] if (len(item) > location) and (keywords == item[location])]
                l = [item for item in row['paragraphs'] if keywords in item]
                ans += l
                # print(len(ans))
        elif len(keywords) == 1:
            for index, row in self.df.iterrows():
                l = [item for item in row['paragraphs'] if (len(item) > location) and (keywords == item[location])]
                ans += l
                # print(len(ans))
        elif len(keywords) > 1:
            end = len(keywords)+location
            for index, row in self.df.iterrows():
                # l = [item for item in row['paragraphs'] if keywords == item[location])]
                l = [item for item in row['paragraphs'] if (len(item) >= end) and (keywords == item[location:end])]
                ans += l
        # ans.sort(key = lambda i:len(i), reverse=True)
        print(len(ans), 'best solutions found!')
        self.length = len(ans)
        self.ans = ans

    def serach_one(self, keywords, location):
        self.flag = 0
        ans = []
        location -= 1
        if location == -1:
            for index, row in self.df.iterrows():
                # l = [item for item in row['paragraphs'] if (len(item) > location) and (keywords == item[location])]
                l = [item for item in row['paragraphs'] if keywords in item]
                ans += l
                # print(len(ans))
        elif len(keywords) == 1:
            for index, row in self.df.iterrows():
                l = [item for item in row['paragraphs'] if (len(item) > location) and (keywords == item[location])]
                ans += l
                if len(ans) > 10:
                    self.ans = ans[:10]
                    break
    # Deprecated
    def clip(self):
        sys = platform.system()
        if sys == "Windows":
            # windows recommend
            pyperclip.copy(self.ans[self.flag])
            self.flag += 1
        else:
            # linux only
            ans = self.ans[self.flag*10 : (self.flag+1)*10]
            self.flag += 1
            for i in ans:
                pyperclip.copy(i)
                pyperclip.paste()

    def output(self, number):
        if self.flag+number <= self.length:
            for i in range(number):
                print(self.ans[self.flag+i])
            self.flag += number
            
    def paste(self, number):
        if self.flag+number <= self.length: 
            try:
                self.fw.activate()
            except:
                self.fw.minimize()
                self.fw.restore()
            pyautogui.moveTo(370, 915)
            pyautogui.click()
            for i in range(number):
                pyperclip.copy(self.ans[self.flag+i])
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(0.5)
            self.flag += number
a = quantangshi()