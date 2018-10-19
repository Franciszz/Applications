import time
import os
import shutil
from qtt import qttconfig as QttConfig

class QttUtils:
    # 获取储存路劲
    @staticmethod
    def getStorepath(action='create'):
        localtimes = time.localtime()
        year = time.strftime('%Y', localtimes)
        month = time.strftime('%m', localtimes)
        day = time.strftime('%d', localtimes)
        store_path = QttConfig.DATA_STORE+'%s/%s/%s'%(year, month, day)

        # 删除目录
        if os.path.exists(store_path) and action == 'remove':
            shutil.rmtree(store_path)
        # 创建多级目录
        if not os.path.exists(store_path) and action == 'create':
            os.makedirs(store_path)

        return store_path
