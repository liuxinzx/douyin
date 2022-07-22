from selenium import webdriver
import pprint
import  time
import  requests

import  re
import json
from queue import Queue
from threading import Thread


def get_url():
    def drop_down():
        for x in range(1, 8, 4):
            time.sleep(1)
            j = x/9
            js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight'
            driver.execute_script(js)


    driver =  webdriver.Chrome()
    driver.get('https://www.douyin.com/user/MS4wLjABAAAAb8rpKxB9ARJogdeiT54H8Q5ibYwHFIIrLhB8zdtjeg8')
    time.sleep(5)
    drop_down()
    urls = []
    lis = driver.find_elements_by_css_selector('#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div:nth-child(2) > ul > li')
    for li in lis:
        href = li.find_element_by_css_selector('a').get_attribute("href")
        urls.append(href)
    return  urls;


def queue_url(urls,in_q):
    for url in urls:
            in_q.put(url)



def get_data(in_q):
    try:
        headers = {
            'cookie': 'douyin.com; __ac_nonce=062da5b90001e1bdbe53; __ac_signature=_02B4Z6wo00f01u10bxAAAIDDjn6vesY6M4rtVEuAANmUda; ttwid=1%7CL3EWH_o0INmOXlRoir27MuGc9qM2jYHO7tPuKQETJBg%7C1658477456%7Cfe14be209c9fb22d265983cd01cbc4793408a988764274b3fbfa3315ca9519c2; strategyABtestKey=1658477457.973; s_v_web_id=verify_l5w6nop9_lzr7h8Ay_D4CQ_4kin_A5qR_c9neXkue0eB1; passport_csrf_token=fcc8e969a97f6df8bdba562c825e5621; passport_csrf_token_default=fcc8e969a97f6df8bdba562c825e5621; msToken=N6elszJa5_JNNmsfcwxDr6ycMfiFEGnWcC79PKgxs4HgVZMBLNNE7nxfPPJQctnvsXpOm9wZ5cbHKPoHz_B80a5jry4YFgmO8kY3t2AwwQTa; home_can_add_dy_2_desktop=%221%22; msToken=VKeYLpL3pGX_2WO6H3H6a3Ls79z0wXLsHltHeVbyE5Wk-ygd88qbdo6r0VgZsWSb0QuCWcCWrquf6zXd4dDbMIs5QgQ-zVT-yqAE4BiP4pMjSPGNdgIJH6oN-dIXypw=; ttcid=3e618b04bb07425fbe2555c7fc79856e28; tt_scid=nZhQ8KKG4fsX9H1xwr5GZkIWlILZ0reg2oMP6.2eubur90BHoxoAdJe3PHV1MWYP17b4; THEME_STAY_TIME=%2213501%22',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        while in_q.empty() is not True:

            response = requests.get(url=in_q.get(), headers=headers)
            title = re.findall('<title data-react-helmet="true">(.*?)</title>', response.text)[0]
            title = re.sub(r'[\\\?\/\:\*\"\<\>\|]', '_', title)
            print(title)

            html_data = re.findall('type="application/json">(.*?)</script>', response.text)[0]
            html_data = requests.utils.unquote(html_data)
            # print(html_data)
            json_data = json.loads(html_data)
            # print(json_data)
            # pprint.pprint(json_data)  # 把json字典格式化
            video_url = 'https:' + json_data['73']['aweme']['detail']['video']['bitRateList'][0]['playAddr'][0]['src']
            # print(video_url)
            video_content = requests.get(url=video_url,headers= headers).content
            with open('video\\' + title + '.mp4',mode='wb') as f :
                f.write(video_content)

            content_list = [i['text'] for i in json_data['73']['comment']['comments']]
            content = '\n'.join(content_list)
            # print(content)
            with open('data\\' + title + '.txt', mode='w', encoding='utf-8') as f:
                f.write(content)
            in_q.task_done()




    except Exception as e:
        print(e)


if __name__ == '__main__':
    start = time.time()
    urls = get_url()
    print(urls)
    queue = Queue(maxsize=8)

    print('queue 开始大小 %d' % queue.qsize())


    data_thread = Thread(target=queue_url, args=(urls , queue,))
    data_thread.daemon = True
    data_thread.start()
    print(queue.qsize())
    for index in range(8):
        data_thread = Thread(target=get_data, args=(queue,))
        data_thread.daemon = True
        data_thread.start()

    queue.join()


    end = time.time()
    print('总耗时：%s' % (end - start))
    print('queue 结束大小 %d' % queue.qsize())


