import pandas as pd
import matplotlib.pyplot as plt

from pyecharts.charts import Pie,Funnel,Geo
from pyecharts import options as opts

file = pd.read_excel(r'51job2.xls',sheet_name='Job')

pd.set_option('display.max_rows', None)  # 输出全部行，不省略
pd.set_option('display.max_columns', None)  # 输出全部列，不省略

f = pd.DataFrame(file)

add = f['公司地点']
sly = f['薪资']
edu = f['学历要求']
exp = f['工作经验']

address =[]             # 存放公司地点
salary = []             # 存放薪资
education = []          # 存放学历要求
experience = []         # 存放工作经验

for i in range(0,len(f)):
    try:
        address.append(add[i])
        salary.append(sly[i])
        education.append(edu[i])
        experience.append(exp[i])
        # print(add[i],sly[i],edu[i],exp[i])
    except:
       pass

#matplotlib模块如果显示不了中文字符串可以用以下代码。

plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

my_df = pd.DataFrame({'experience':experience, 'salary': salary})				#关联工作经验与薪资
data1 = my_df.groupby('experience').mean()['salary'].plot(kind='line')
plt.show()

my_df2 = pd.DataFrame({'education':education, 'salary': salary})				#关联学历与薪资
data2 = my_df2.groupby('education').mean()['salary'].plot(kind='line')
plt.show()

### 动态图

def get_edu(list):       # 储存 不同学历要求及其数量
    education_dir = {}
    for i in set(list):
        education_dir[i] = list.count(i)
    return education_dir

education_dir = get_edu(education)

attr= education_dir.keys()
value = education_dir.values()

# 旧版pyecharts 0.5.9
# pie = Pie("学历要求")
# pie.add("", attr, value, center=[50, 50], is_random=False, radius=[30, 75], rosetype='radius',
#         is_legend_show=False, is_label_show=True,legend_orient='vertical')
# pie.render('学历要求动态饼图.html')

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
    .render("学历要求动态饼图.html")
)

def get_experience(list):           # 储存 工作经验要求及其数量
    experience_dir = {}
    for i in set(list):
         experience_dir[i] = list.count(i)
    return experience_dir
experience_dir = get_experience(experience)


attr2 = experience_dir.keys()
value2 = experience_dir.values()

# 旧版pyecharts 0.5.9
# funnel = Funnel("工作经验漏斗图",title_pos='center')
# funnel.add("", attr3, value3,is_label_show=True,label_pos="inside", label_text_color="#fff",legend_orient='vertical',legend_pos='left')
# funnel.render('工作经验要求漏斗图.html')

# 新版pyecharts
c = (
    Funnel()
    .add(
        "",
        [list(z) for z in zip(attr2, value2)],
        label_opts=opts.LabelOpts(position="inside"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Funnel-Label（inside)"))
    .render("工作经验要求漏斗图.html")
)

def get_address(list):          # 储存 城市名及其数量
    address_dir = {}
    for i in set(list):
        address_dir[i] = list.count(i)
    try:
        address_dir.pop('异地招聘')
        # 有些地名可能不合法或者地图包里没有可以自行删除，之前以下名称都会报错，现在好像更新了没报错了
        # address_dir.pop('山东')
        # address_dir.pop('怒江')
        # address_dir.pop('池州')
    except:
        pass
    return address_dir

address_dir = get_address(address)

attr3 = address_dir.keys()
value3 = address_dir.values()

# 旧版pyecharts 0.5.9
# geo = Geo("大数据人才需求分布图", title_color="#2E2E2E",
#           title_text_size=24,title_top=20,title_pos="center", width=1300,height=600)

# geo.add("",attr2, value2, type="effectScatter", is_random=True, visual_range=[0, 1000], maptype='china',symbol_size=8, effect_scale=5, is_visualmap=True)
# geo.render('大数据城市需求分布图.html')

# 新版pyecharts
c = (
    Geo()
    .add_schema(maptype="china")
    .add("geo", [list(z) for z in zip(attr3, value3)])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="Geo-基本示例")
    )
    .render("大数据城市需求分布图.html")
)