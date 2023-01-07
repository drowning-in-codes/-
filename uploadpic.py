import tqdm
import requests
import os


class upload:
    def __init__(self, ACCESS_TOKEN, FILEPATHLIST):
        self.url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={ACCESS_TOKEN}&type' \
                   f'=image'
        self.filepath = FILEPATHLIST
        self.uploadPics()

    def uploadPics(self):

        if isinstance(self.filepath, str):
            self.uploadPic(self.filepath)
        else:
            for f in self.filepath:
                self.uploadPic(f)

    def uploadPic(self, filepath):
        if os.path.isdir(filepath):
            filelist = os.listdir(filepath)
            total = len(filelist)
            pbar = tqdm.tqdm(filelist)
            for index, f in enumerate(pbar):
                file_path = os.path.join(filepath, f)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        files = {
                            'media': file
                        }
                        res = requests.post(self.url, files=files)
                        pbar.set_description('正在上传' + f)
                        pbar.set_postfix({'current': index + 1, 'total': total})
        else:
            print('文件夹错误', filepath)
