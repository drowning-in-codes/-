import os.path
import tqdm
import requests
from lxml import etree
import sys


class Article:
    def __init__(self):
        self.__url = None
        self.title = None
        self.__header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
        }
        self.filepathList = set()
        self.getUpdated()

    def getUpdated(self):
        url = 'https://www.pixivision.net/zh/c/illustration'
        res = requests.get(url,headers=self.__header)
        selector = etree.HTML(res.text)
        lastUpdatedNumber = selector.xpath("//li[@class='article-card-container'][1]/article/div[@class='arc__thumbnail-container']/a[1]/@href")[0]
        lastUpdatedNumber = lastUpdatedNumber.split('/')[-1]
        print('最新的图文号为',lastUpdatedNumber)

    def getarticle(self):
        self.__url = input('输入网站链接(仅限pixvision:https://www.pixivision.net/zh/a/number):')
        if self.__url.isnumeric():
            self.__url = 'https://www.pixivision.net/zh/a/' + self.__url
        try:
            res = requests.get(self.__url, headers=self.__header)
        except requests.exceptions.ProxyError as e:
            print('网络出现问题', e)
            sys.exit(-1)
            return
        except Exception as e:
            print('出错', e)
            sys.exit(-1)
            return
        selector = etree.HTML(res.text)
        imgLinks = selector.xpath(
            "////div[@class='_feature-article-body']/div[@class='article-item _feature-article-body__pixiv_illust']//div[@class='am__work__main']//img/@src")  # 返回为一列表
        self.title = selector.xpath("//h1[@class='am__title']/text()")
        self.download(imgLinks)

    def download(self, imgLinks):
        filepath = input('输入下载的目录路径(默认F:\公众号\图片):')
        if filepath == "":
            filepath = 'F:\\公众号\\图片'
        if not os.path.exists(filepath):
            print('目录输入错误')
            return
        if self.title:
            absfilepath = filepath + f'\\{self.title}'
            if os.path.exists(absfilepath):
                # 清空文件夹中的文件
                print('清空文件夹中的文件')
                del_list = os.listdir(absfilepath)
                for f in del_list:
                    file_path = os.path.join(absfilepath, f)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            else:
                print('生成文件夹')
                os.mkdir(absfilepath)
            self.filepathList.add(absfilepath)
            self.__header['Referer'] = 'https://www.pixiv.net/'
            pbar = tqdm.tqdm(imgLinks)
            total = len(imgLinks)
            for index, link in enumerate(pbar):
                filename = link.split('/')[-1]
                pbar.set_description("正在下载%s," % filename)
                pbar.set_postfix({'current': index + 1, 'total': total})
                try:
                    res = requests.get(link, headers=self.__header)
                    with open(absfilepath + f'\\{filename}', 'wb+') as f:
                        f.write(res.content)
                except Exception as e:
                    print('需要设置代理', e)
        else:
            print('不存在该文章,请继续...')
            self.getarticle()
