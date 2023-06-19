from selenium import webdriver
from selenium.webdriver import ActionChains
import time

import re
import xlwt
import urllib.parse

def get_html(url):
    options = webdriver.ChromeOptions()

    # selenium静默执行（无浏览器界面）
    options.add_argument('headless')

    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")

    chrome_driver = './chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options,executable_path=chrome_driver)

    # webdriver防屏蔽
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false
        })
      """
    })

    driver.get(url)

    time.sleep(1)
    # 找到需要滑动的滑块元素
    slider = driver.find_element_by_xpath('//div[@class="nc_bg"]')

    # 创建操作链
    action_chains = ActionChains(driver)

    # 将鼠标移动到滑块上
    action_chains.move_to_element(slider)

    # 模拟按下鼠标左键并保持不松开
    action_chains.click_and_hold()

    # 移动鼠标使滑块达到目标位置
    action_chains.move_by_offset(300, 0)

    # 松开鼠标左键
    action_chains.release()

    # 执行操作链
    action_chains.perform()

    time.sleep(10)

    html = driver.page_source
    driver.quit()

    return html


def get_msg(excel1, sheet1):
    number = 0
    job_type = input("请输入你想要搜索的职位：")
    for i in range(1, 10):  # 页数自己随便改
        try:
            print("正在爬取第" + str(i) + "页数据...")
            result = urllib.parse.quote(job_type)
            url_start = 'https://we.51job.com/api/job/search-pc?api_key=51job&keyword=' + result

            # 删除&timestamp参数，修改&pageSize=500
            url_end = '&searchType=2&function=&industry=&jobArea=000000&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum=' \
                      + str(i) + '&requestId=&pageSize=500&source=1&accountId=&pageCode=sou%7Csou%7Csoulb'
            url = url_start + url_end
            # print(url)

            msg = get_html(url)
            msg = msg.replace('\\', '')  # 将用于转义的"\"替换为空

            # print(msg)

            # 匹配规则如下,里面匹配项一定不能写错，不然运行结果就会是空
            # `(.*?)`表示任意我们想要的内容
            # `.*?`表示任意其他字符串

            reg = re.compile(r'"jobName":"(.*?)".*?"cityString":"(.*?)".*?"provideSalaryString":"(.*?)","issueDateString":"(.*?)".*?'
                             r'"workYearString":"(.*?)","degreeString":"(.*?)".*?"companyName":"(.*?)".*?"companyTypeString":"(.*?)","companySizeString":"(.*?)"',re.S)

            items = reg.findall(msg)

            for item in items:
                number = number + 1
                print(number,item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])

                sheet1.write(number, 0, number)
                sheet1.write(number, 1, item[0])
                sheet1.write(number, 2, item[6])
                sheet1.write(number, 3, item[1])
                sheet1.write(number, 4, item[7])
                sheet1.write(number, 5, item[2])
                sheet1.write(number, 6, item[5])
                sheet1.write(number, 7, item[4])
                sheet1.write(number, 8, item[8])
                sheet1.write(number, 9, item[3])

                # 表格文件保存是可以选择两种情况，
                # 一种在for循环里面，每写一行保存一次，这样可以放在程序中途出现异常后，文件内容啥也没有
                # 另一种是在for循环之外，所有内容写完再保存
                excel1.save("51job.xls")
                time.sleep(0.3)  # 休息间隔
        except:
            pass

def creat_xls(excel1):
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
    return sheet1

def main():
    # 新建表格空间
    excel1 = xlwt.Workbook()
    sheet1 = creat_xls(excel1)
    get_msg(excel1, sheet1)

if __name__ == '__main__':
    main()


