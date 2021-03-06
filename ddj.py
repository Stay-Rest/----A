import time,re
from selenium import webdriver
sougouwenwen = webdriver.Chrome()
wenwen_url = 'https://wenwen.sogou.com'
sougouwenwen.get(wenwen_url)
question = None
hinder_data = None
original_label = None
custom_lable_data = None
question_numbers = [1,2,3,4,5,6,7,8,9,10]
lable_numbers = [1,2,3]

custom_array = [1,2,3]
lable_really =0

temporary_data = 0

qty = 0


def zhuanyi():
    try:
        with open('./障碍数据库.txt', 'r') as fp:
            hinder_data = str.split(fp.read())
            fp.close()
            # print('障碍数据库:',hinder_data)

        with open('./自定义数据库.txt', 'r')as fp:
            custom_lable_data = str.split(fp.read())
            print('自定义数据库:',custom_lable_data)
            fp.close()
        #10个问题
        lable_really = 0
        for i in question_numbers:
            time.sleep(1)
            question =sougouwenwen.find_element_by_xpath('//*[@id="userList_talent_2"]/ul/li[%d]/div/div[1]/a'%(i)).text
            print('当前问题：',question)
            jump_qusetion = 0
            #判断当前问题是否为障碍数据
            try:
                for ii in hinder_data:
                    # print(ii)
                    if re.search(question,ii) :
                        print('当前问题属于障碍数据:',question,ii)
                        jump_qusetion = 1#障碍数据标志 赋1
                    else:
                        pass
                        # print('不属于障碍数据:',question,ii)
            except:
                print('正在判断当前问题是否属于障碍数据')
            if jump_qusetion == 0:#当前问题不在障碍数据中后 开始进行判断
                custom_array = ['','','']
                temporary_data = 0
                #自定义数据库搜索
                try:
                    for iii in custom_lable_data:#根据数据库中的自定义数据的数量进行对比
                        keywords = str.split(iii,'|')[0]#将当前数据分割为关键字和所属标签
                        keywords_lable = str.split(iii,'|')[1]
                        temporary_data = temporary_data+1
                        try:
                            re_back = re.search(keywords,question)#对比  在当前问题中寻找关键字
                            if re_back == None:#在问题中成功找到关键字
                                print(temporary_data,'未找到关键字',keywords,'当前问题：',question)
                                pass
                            else:
                                print('当前关键字:', keywords,'所属标签:',keywords_lable, '当前结果：', re_back)
                                custom_lable_repeat = 0
                                # print(len(custom_array))
                                try:
                                    if  custom_array[2]=="" :
                                        print('正在判断当前标签是否已拥有')
                                        try:
                                            for iiii in lable_numbers:
                                                if  re.search(keywords_lable,custom_array[iiii-1]) != None:
                                                    custom_lable_repeat = 1
                                                    print('该标签已拥有')
                                                    break
                                        except:
                                            pass
                                        if custom_lable_repeat == 0:
                                            try:
                                                for xx in lable_numbers:
                                                    if custom_array[xx-1]=="":
                                                        custom_array[xx-1]=keywords_lable
                                                        break
                                                # print('当前需要加入的标签:',custom_array)
                                            except:
                                                pass
                                    else:
                                        print('当前自定义标签已满')
                                except:
                                    print('标签对比中')
                        except:
                            print('关键字寻找中')
                except:
                    print('数据处理中')
                #判断标签数据与原标签数据是否相同
                original_label_array=[]
                try:
                    for xx in lable_numbers:
                        #//*[@id="userList_talent_2"]/ul/li[1]/div/div[2]/div/div[1]/a
                        original_label =   sougouwenwen.find_element_by_xpath('//*[@id="userList_talent_2"]/ul/li[%d]/div/div[2]/div/div[1]/a[%d]'%(i,xx)).text
                        if original_label != None:
                            original_label_array.append(original_label)
                            # print(original_label)
                        else:
                            print('original_label未找到')
                except:
                    print("数组排序中")
                custom_array.sort(reverse=True)#排序自定义标签数组
                original_label_array.sort(reverse=True)#排序原标签数组

                print('原标签：',original_label_array)

                print('需要加入的自定义标签:',custom_array)
                shuju = 0
                temporary_data = 0
                try:
                    for xxx in original_label_array:
                        xxxx =re.sub(pattern=' ',string=xxx,repl='')#删除标签内的空格 as:QQ 空间   QQ空间
                        custom_data=re.sub(pattern=' ',string=custom_array[temporary_data],repl='')
                        if xxxx != custom_data:
                            shuju =1#数据不同
                            break
                        temporary_data = temporary_data+1

                except:
                    print('正在检查数组是否相同')
                # print('是否相同',shuju)

                #当有自定义标签数据且标签数据与原标签数据不同
                try:
                    if  custom_array[0] !="":
                        #点击转移标签
                        # print('有数据')
                        if  shuju == 1:
                            sougouwenwen.find_element_by_xpath('//*[@id="userList_talent_2"]/ul/li[%d]/div/div[2]/div/div[2]/a[2]'%(i)).click()
                            #删除原标签
                            for iii in lable_numbers:
                                try:
                                    original_label_search=sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[3]/div[1]/span').text
                                    if original_label_search != None:
                                        sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[3]/div[1]/a').click()
                                    else:
                                        break
                                except:
                                    # print('删除原标签中')
                                    pass
                            # print('已删除完原标签')
                            time.sleep(0.1)
                            #点击搜索框
                            sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[4]/div[1]/div[2]/div/input').clear()
                            print('已删除搜索框内容')
                            time.sleep(0.1)
                            #加入自定义标签
                            try:
                                for x in custom_array:
                                    sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[4]/div[1]/div[2]/div/input').send_keys(x)
                                    time.sleep(0.1)
                                    #点击空白处
                                    sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[3]/div').click()
                                    time.sleep(0.1)
                                    #重新点击输入框刷新索引标签
                                    sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[4]/div[1]/div[2]/div/input').click()
                                    time.sleep(1)
                                    #//*[@id="popup_wrap"]/div/div/div[2]/div[4]/div[1]/div[2]/div/ul/li[1]
                                    sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[4]/div[1]/div[2]/div/ul/li[1]').click()
                            except:
                                pass
                            print('已加入自定义标签')
                            #点击确认
                            sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[5]/div/a[2]').click()
                            lable_really = 1
                            #点击取消
                            # sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[5]/div/a[1]').click()
                except:
                    print('转移动作')
                print(custom_array[0])
                if shuju ==0:
                    print('数据相同，直接正确')                                   #//*[@id="userList_talent_2"]/ul/li[1]/div/div[2]/div/div[2]/a[1]
                    lable_really = 1
                    sougouwenwen.find_element_by_xpath('//*[@id="userList_talent_2"]/ul/li[%d]/div/div[2]/div/div[2]/a[1]'%(i)).click()
                    time.sleep(0.2)
                    sougouwenwen.find_element_by_xpath('//*[@id="scroll-nav"]/div[2]/a[1]').click()
                elif  custom_array[0] =="":
                    print('数据空，直接正确')  # //*[@id="userList_talent_2"]/ul/li[1]/div/div[2]/div/div[2]/a[1]
                    lable_really = 1
                    sougouwenwen.find_element_by_xpath('//*[@id="userList_talent_2"]/ul/li[%d]/div/div[2]/div/div[2]/a[1]'%(i)).click()
                    time.sleep(0.2)
                    sougouwenwen.find_element_by_xpath('//*[@id="scroll-nav"]/div[2]/a[1]').click()
            else:
                print('当前第%d个问题为障碍数据'%(i),question)

            # break  # 只转移第一个
            if lable_really == 1:
                break

    except:
        print('数据处理中')

kaishi = input('输入任意值开始转移标签')

while 1:

    try:
        cancel = sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[5]/div/a[1]').text
        if cancel == '取消':
            print('已存在取消界面')
            cancel = sougouwenwen.find_element_by_xpath('//*[@id="popup_wrap"]/div/div/div[2]/div[5]/div/a[1]').click()
            sougouwenwen.refresh()
    except:
        pass
    #//*[@id="scroll-nav"]/div[2]/a[1]
    sougouwenwen.find_element_by_xpath('//*[@id="scroll-nav"]/div[2]/a[1]').click()
    zhuanyi()
    qty=qty+1
    if qty >= 1000:
        sougouwenwen.refresh()
        qty = 0
    #     break
    #     print('已工作完成')
    #     qty = 0
    time.sleep(5)
