from selenium import webdriver
import selenium
import  time
import json

def create_chrome_driver(*, headless=False):  # 创建谷歌浏览器对象，用selenium控制浏览器访问url
    options = webdriver.ChromeOptions()
    if headless:  # 如果为True，则爬取时不显示浏览器窗口
        options.add_argument('--headless')

    # 做一些控制上的优化
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # 创建浏览器对象
    browser = webdriver.Chrome(options=options,executable_path=r"chromedriver.exe")
    # 破解反爬措施
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )

    return browser

driver =  create_chrome_driver()

driver.get('https://www.douyin.com/user/MS4wLjABAAAAb8rpKxB9ARJogdeiT54H8Q5ibYwHFIIrLhB8zdtjeg8')
time.sleep(3)


# 获取cookie列表
cookie_list=driver.get_cookies()
cookie_dict={}
# 格式化打印cookie
for cookie in cookie_list:
    cookie_dict[cookie['name']]=cookie['value']
print(cookie_dict)

