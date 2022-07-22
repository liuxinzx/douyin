import pprint

import  requests
import  selenium
import  re
import json
url = 'https://www.douyin.com/video/7117577191218515203'
headers = {
    'cookie': 'douyin.com; __ac_nonce=062da5b90001e1bdbe53; __ac_signature=_02B4Z6wo00f01u10bxAAAIDDjn6vesY6M4rtVEuAANmUda; ttwid=1%7CL3EWH_o0INmOXlRoir27MuGc9qM2jYHO7tPuKQETJBg%7C1658477456%7Cfe14be209c9fb22d265983cd01cbc4793408a988764274b3fbfa3315ca9519c2; strategyABtestKey=1658477457.973; s_v_web_id=verify_l5w6nop9_lzr7h8Ay_D4CQ_4kin_A5qR_c9neXkue0eB1; passport_csrf_token=fcc8e969a97f6df8bdba562c825e5621; passport_csrf_token_default=fcc8e969a97f6df8bdba562c825e5621; msToken=N6elszJa5_JNNmsfcwxDr6ycMfiFEGnWcC79PKgxs4HgVZMBLNNE7nxfPPJQctnvsXpOm9wZ5cbHKPoHz_B80a5jry4YFgmO8kY3t2AwwQTa; home_can_add_dy_2_desktop=%221%22; msToken=VKeYLpL3pGX_2WO6H3H6a3Ls79z0wXLsHltHeVbyE5Wk-ygd88qbdo6r0VgZsWSb0QuCWcCWrquf6zXd4dDbMIs5QgQ-zVT-yqAE4BiP4pMjSPGNdgIJH6oN-dIXypw=; ttcid=3e618b04bb07425fbe2555c7fc79856e28; tt_scid=nZhQ8KKG4fsX9H1xwr5GZkIWlILZ0reg2oMP6.2eubur90BHoxoAdJe3PHV1MWYP17b4; THEME_STAY_TIME=%2213501%22',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
response = requests.get(url=url,headers=headers)
title = re.findall('<title data-react-helmet="true">(.*?)</title>',response.text)[0]
title =  re.sub(r'[\\\?\/\:\*\"\<\>\|]','_',title)
print(title)

html_data = re.findall('type="application/json">(.*?)</script>',response.text)[0]
html_data =  requests.utils.unquote(html_data)
print(html_data)
json_data = json.loads(html_data)
# print(json_data)
pprint.pprint(json_data) # 把json字典格式化
video_url = 'https:' + json_data['73']['aweme']['detail']['video']['bitRateList'][0]['playAddr'][0]['src']
print(video_url)
# video_content = requests.get(url=video_url,headers= headers).content
# with open('video\\' + title + '.mp4',mode='wb') as f :
#     f.write(video_content)

content_list=[ i ['text'] for i in json_data['73']['comment']['comments']]
content = '\n'.join(content_list)
print(content)
with open('data\\' + title + '.txt',mode='w',encoding='utf-8') as f:
    f.write(content)

