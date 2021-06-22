#coding:utf-8
import pandas as pd
import re

#读取表格内容到data
data = pd.read_excel(r'51job.xls',sheet_name='Job')
result = pd.DataFrame(data)

a = result.dropna(axis=0,how='any')
pd.set_option('display.max_rows',None)     #输出全部行，不省略

#清洗职位中的异常数据
b = u'数据'
number = 1
li = a['职位']
for i in range(0,len(li)):
    try:
        if b in li[i]:
            #print(number,li[i])
            number+=1
        else:
            a = a.drop(i,axis=0)  #删除整行
    except:
        pass
#清洗学历要求的异常数据
b2 = '人'
li2 = a['学历要求']
for i in range(0,len(li2)):
    try:
        if b2 in li2[i]:
            # print(number,li2[i])
            number += 1
            a = a.drop(i, axis=0)
    except:
        pass

#转换薪资单位
b3 =u'万/年'
b4 =u'千/月'
li3 = a['薪资']
#注释部分的print都是为了调试用的
for i in range(0,len(li3)):
    try:
        if b3 in li3[i]:
            x = re.findall(r'\d*\.?\d+',li3[i])
            #print(x)
            min_ = format(float(x[0])/12,'.2f')              #转换成浮点型并保留两位小数
            max_ = format(float(x[1])/12,'.2f')
            li3[i][1] = min_+'-'+max_+u'万/月'
        if b4 in li3[i]:
            x = re.findall(r'\d*\.?\d+',li3[i])
            #print(x)
            #input()
            min_ = format(float(x[0])/10,'.2f')
            max_ = format(float(x[1])/10,'.2f')
            li3[i][1] = str(min_+'-'+max_+'万/月')
        print(i,li3[i])

    except:
        pass

#保存成另一个excel文件
a.to_excel('51job2.xlsx', sheet_name='Job', index=False)

########################################数据可视化################################################
import pandas as pd
import re
from pyecharts.charts import Funnel,Pie,Geo
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.datasets import register_url


file = pd.read_excel(r'51job2.xlsx',sheet_name='Job')
f = pd.DataFrame(file)
pd.set_option('display.max_rows',None)

add = f['公司地点']
sly = f['薪资']
edu = f['学历要求']
exp = f['工作经验']
address =[]
salary = []
education = []
experience = []


for i in range(0,len(f)):
    try:
        a = add[i].split('-')
        address.append(a[0])
        #print(address[i])
        s = re.findall(r'\d*\.?\d+',sly[i])
        s1= float(s[0])
        s2 =float(s[1])
        salary.append([s1,s2])
        #print(salary[i])
        education.append(edu[i])
        #print(education[i])
        experience.append(exp[i])
        #print(experience[i])
    except:
       pass

min_s=[]							#定义存放最低薪资的列表
max_s=[]							#定义存放最高薪资的列表
for i in range(0,len(experience)):
    min_s.append(salary[i][0])
    max_s.append(salary[i][0])

#matplotlib模块如果显示不了中文字符串可以用以下代码。
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

my_df = pd.DataFrame({'experience':experience, 'min_salay' : min_s, 'max_salay' : max_s})				#关联工作经验与薪资
data1 = my_df.groupby('experience').mean()['min_salay'].plot(kind='line')
plt.show()
my_df2 = pd.DataFrame({'education':education, 'min_salay' : min_s, 'max_salay' : max_s})				#关联学历与薪资
data2 = my_df2.groupby('education').mean()['min_salay'].plot(kind='line')
plt.show()

def get_edu(list):
    education2 = {}
    for i in set(list):
        education2[i] = list.count(i)
    return education2
dir1 = get_edu(education)
# print(dir1)

attr= dir1.keys()
value = dir1.values()

# 旧版pyecharts
# pie = Pie("学历要求")
# pie.add("", attr, value, center=[50, 50], is_random=False, radius=[30, 75], rosetype='radius',
#         is_legend_show=False, is_label_show=True,legend_orient='vertical')
# pie.render('学历要求玫瑰图.html')

# 新版pyecharts
c = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(attr, value)],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-Radius"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("学历要求玫瑰图.html")
)

def get_address(list):
    address2 = {}
    for i in set(list):
        address2[i] = list.count(i)
    try:
        address2.pop('异地招聘')
        # 有些地名可能不合法或者地图包里没有可以自行删除，之前以下名称都会报错，现在好像更新了
        # address2.pop('山东')
        # address2.pop('怒江')
        # address2.pop('池州')
    except:
        pass
    return address2
dir2 = get_address(address)
#print(dir2)
attr2 = dir2.keys()
value2 = dir2.values()

# 旧版pyecharts
# geo = Geo("大数据人才需求分布图", title_color="#2E2E2E",
#           title_text_size=24,title_top=20,title_pos="center", width=1300,height=600)

# geo.add("",attr2, value2, type="effectScatter", is_random=True, visual_range=[0, 1000], maptype='china',symbol_size=8, effect_scale=5, is_visualmap=True)
# geo.render('大数据城市需求分布图.html')

# 新版pyecharts
c = (
    Geo()
    .add_schema(maptype="china")
    .add("geo", [list(z) for z in zip(attr2, value2)])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="Geo-基本示例")
    )
    .render("大数据城市需求分布图.html")
)

def get_experience(list):
    experience2 = {}
    for i in set(list):
         experience2[i] = list.count(i)
    return experience2
dir3 = get_experience(experience)
#print(dir3)

attr3= dir3.keys()
value3 = dir3.values()

# 旧版pyecharts
# funnel = Funnel("工作经验漏斗图",title_pos='center')
# funnel.add("", attr3, value3,is_label_show=True,label_pos="inside", label_text_color="#fff",legend_orient='vertical',legend_pos='left')
# funnel.render('工作经验要求漏斗图.html')

# 新版pyecharts
c = (
    Funnel()
    .add(
        "",
        [list(z) for z in zip(attr3, value3)],
        label_opts=opts.LabelOpts(position="inside"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Funnel-Label（inside)"))
    .render("工作经验要求漏斗图.html")
)
