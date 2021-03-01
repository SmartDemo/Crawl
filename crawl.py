import requests
from urllib.parse import urlparse
import json


class DouBan:
    # 初始化爬取得url,以及请求头信息
    def __init__(self):
        self.url = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=20&page_start={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }

    # 构造一个链接
    def get_url_list(self, page_start):
        return self.url.format(page_start)

    # 请求这个接口，返回一个json
    def parse_html(self, url):
        try:
            print(url)
            res = requests.get(url, headers=self.headers)
            assert res.status_code == 200
            res = res.content.decode()
        except:
            res = None
        return res

    # 按分数排序
    def sort_by_rate(self):
        l = []
        with open("douban.txt", "r", encoding="utf-8") as f:
            for line in f:
                l.append((line[0:3], line[3:-1]))
            l = sorted(l, key=lambda x: x[0], reverse=True)
        # print(l)
        with open("douban.txt", "w", encoding="utf-8") as f:
            for line in l:
                f.writelines(line)
                f.writelines("\n")

    # 保存爬取的数据
    def save(self, json_str):
        re = json.loads(json_str)
        for i in range(len(re["subjects"])):
            title = re["subjects"][i]["title"]
            rate = re["subjects"][i]["rate"]
            url = re["subjects"][i]["url"]
            with open("douban.txt", "a", encoding="utf-8") as f:
                f.write(rate + "   " + title + "    " + url + "  \n")

    def run(self):
        pagestart = 0;
        count = True
        while (count):
            url = self.get_url_list(pagestart)
            pagestart += 20
            # 返回的是json字符串
            json_str = self.parse_html(url)
            # 转换成python的dict类型
            re = json.loads(json_str)
            # 保存
            self.save(json_str)
            # 判断返回的数据量是否大于20，是就继续，否就终止爬虫
            count = True if len(re["subjects"]) == 20 else False


if __name__ == "__main__":
    D = DouBan()
    D.run()
    D.sort_by_rate()
