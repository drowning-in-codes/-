import time
from user import User
from getpic import Article
from uploadpic import upload

if __name__ == "__main__":
    uploadDownloadpic = '0'
    if input('直接上传图片?0表示直接上传,1表示下载\n') == '1':
        article = Article()
        while True:
            article.getarticle()
            doContinue = input('是否继续下载图片？1表示继续,0表示退出\n')
            if doContinue == '0':
                break
        uploadDownloadpic = input('是否上传刚才的图片?1表示是,0表示自己选择\n')
    u = User()
    continueUpload = '0'
    while True:
        if continueUpload == '1':
            filepath = input('输入需要上传的文件目录(单个):\n')
            upload(u.access_token, filepath)
        else:
            if uploadDownloadpic == '1':
                upload(u.access_token, article.filepathList)
            else:
                filepath = input('输入需要上传的文件目录(单个):\n')
                upload(u.access_token, filepath)
        continueUpload = input('是否继续上传?1表示是,0表示退出\n')
        if '0' == continueUpload:
            break
