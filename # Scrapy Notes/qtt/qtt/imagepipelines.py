# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import os
from qtt.qttutils import QttUtils

#封面图下载
class CoverImagePipeline(ImagesPipeline):
    #获取settings中的常量
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')
    #下载图片
    def get_media_requests(self, item, info):
        cover_images = item['cover']
        if cover_images:
            for image_url in cover_images:
                yield scrapy.Request(url=image_url)

    def item_completed(self, results, item, info):
        # print('*'*20,results,item,info)
        image_path = [x['path'] for ok, x in results if ok]
        # 获取自定义存储路径
        store_path = QttUtils.getStorepath()
        coverImages = []
        # 将图片移动到新的路径
        if image_path:
            for image_url in image_path:
                file_name = os.path.split(str(image_url))
                new_image = store_path + "/" + file_name[1]
                coverImages.append(new_image)
                os.rename(self.IMAGES_STORE + "/" + image_url, new_image)
        item['cover'] = coverImages
        return item


# 内容图片下载
class ContentImagePipeline(ImagesPipeline):
    # 获取settings中的常量
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    # 下载图片
    def get_media_requests(self, item, info):
        content_images = item['content_images']
        if content_images:
            for image_url in content_images:
                yield scrapy.Request(image_url)

        # 下载完成
        def item_completed(self, results, item, info):
            image_info = [(x['path'], x['url']) for ok, x in results if ok]
            # 获取自定义存储路径
            store_path = QttUtils.getStorepath()
            contentImages = []
            # 将图片移动到新的路径
            if image_info:
                for value in image_info:
                    image_url = value[0]
                    image_source = value[1]
                    file_name = os.path.split(str(image_url))
                    new_image = store_path + "/" + file_name[1]
                    contentImages.append((new_image, image_source))
                    os.rename(self.IMAGES_STORE + "/" + image_url, new_image)
            item['content_images'] = contentImages
            return item