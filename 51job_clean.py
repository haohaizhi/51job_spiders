import pandas as pd
import re

import xlwt
#除此之外还要安装xlrd包

def read_excel():
    #读取表格内容到data
    pd.set_option('display.max_rows', None)  # 输出全部行，不省略
    pd.set_option('display.max_columns', None)  # 输出全部列，不省略

    data = pd.read_excel(r'51job.xls', sheet_name='Job')

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
    sheet1.write(0, 9, '发布时间')

    number = 1

    result = read_excel()

    for i in range(0, len(result)):
        try:
            id = result["序号"].values[i]
            job_name = result["职位"].values[i]
            companys = result["公司名称"].values[i]
            location = result["公司地点"].values[i]
            company_v = result["公司性质"].values[i]
            moneys = result["薪资"].values[i]
            edu = result["学历要求"].values[i]
            exp = result["工作经验"].values[i]
            size = result["公司规模"].values[i]
            date = result["发布时间"].values[i]

            if u'数据' not in job_name:
                continue

            tmp = moneys.split('-')
            if u'薪' in tmp[1]:
                tmp = tmp[1].split('·')
                tmp[1] = tmp[0]
            if u'万' in tmp[1]:
                moneys= re.findall(r'\d*\.?\d+', tmp[1])
                moneys = format(float(moneys[0]), '.2f')
            if u'千' in tmp[1]:
                moneys = re.findall(r'\d*\.?\d+', tmp[1])
                moneys = format(float(moneys[0]) / 10, '.2f')
            if u'万/年' in tmp[1]:
                moneys = re.findall(r'\d*\.?\d+', tmp[1])
                moneys = format(float(moneys[0]) / 12, '.2f')

            print(id, job_name, companys, location, company_v, moneys, edu, exp, size, date)
            sheet1.write(number, 0, int(id))
            sheet1.write(number, 1, job_name)
            sheet1.write(number, 2, companys)
            sheet1.write(number, 3, location)
            sheet1.write(number, 4, company_v)
            sheet1.write(number, 5, moneys)
            sheet1.write(number, 6, edu)
            sheet1.write(number, 7, exp)
            sheet1.write(number, 8, size)
            sheet1.write(number, 9, date)
            number += 1
        except:
            pass

    excel1.save("51job2.xls")


if __name__ == '__main__':
    main()
