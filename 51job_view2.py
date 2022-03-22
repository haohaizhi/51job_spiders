#coding:utf-8
import pandas as pd
import xlwt
import re

def read_excel():
    #读取表格内容到data
    pd.set_option('display.max_rows',None)     #输出全部行，不省略
    pd.set_option('display.max_columns',None)   #输出全部列，不省略
    data = pd.read_excel(r'51job.xls',sheet_name='Job')

    result = pd.DataFrame(data)

    result.dropna(axis=0,how='any',inplace=True)
    return result
def main():
    # 新建表格空间
    excel1 = xlwt.Workbook()
    # 设置单元格格式
    sheet1 = excel1.add_sheet('Job', cell_overwrite_ok=True)
    sheet1.write(0, 0, '序号')
    sheet1.write(0, 1, '职位')
    sheet1.write(0, 2, '公司名称')
    sheet1.write(0, 3, '公司地点')
    sheet1.write(0, 4, '公司性质')
    sheet1.write(0, 5, '薪资')
    sheet1.write(0, 6, '学历要求')
    sheet1.write(0, 7, '工作经验')
    sheet1.write(0, 8, '公司规模')
    sheet1.write(0, 9, '公司福利')
    sheet1.write(0, 10, '发布时间')
    number = 1

    a = read_excel()
#清洗异常数据,替换某些数据
    for i in range(0,len(a)):
        id = a["序号"].values[i]
        jobs = a["职位"].values[i]
        companys = a["公司名称"].values[i]
        location = a["公司地点"].values[i]
        company_v = a["公司性质"].values[i]
        moneys = a["薪资"].values[i]
        edu = a["学历要求"].values[i]
        exp = a["工作经验"].values[i]
        size = a["公司规模"].values[i]
        welfare = a["公司福利"].values[i]
        date = a["发布时间"].values[i]
        if 'Python' not in jobs and 'python' not in jobs:
            continue
        if '人' in edu or '人' in exp:
            continue
        if '万/年' in moneys:
            x = re.findall(r'\d*\.?\d+', moneys)
            min_ = format(float(x[0])/12,'.2f')              #转换成浮点型并保留两位小数
            max_ = format(float(x[1])/12,'.2f')
            moneys = min_+'-'+max_+u'万/月'
        if '千/月' in moneys:
            x = re.findall(r'\d*\.?\d+', moneys)
            min_ = format(float(x[0])/10,'.2f')
            max_ = format(float(x[1])/10,'.2f')
            moneys = str(min_+'-'+max_+'万/月')
        print(id,jobs,companys,location,company_v,moneys,edu,exp,size,welfare,date)
        sheet1.write(number, 0, int(id))
        sheet1.write(number, 1, jobs)
        sheet1.write(number, 2, companys)
        sheet1.write(number, 3, location)
        sheet1.write(number, 4, company_v)
        sheet1.write(number, 5, moneys)
        sheet1.write(number, 6, edu)
        sheet1.write(number, 7, exp)
        sheet1.write(number, 8, size)
        sheet1.write(number, 9, welfare)
        sheet1.write(number, 10,date)
        number += 1
    excel1.save("51job2.xls")

if __name__ == '__main__':
    main()
