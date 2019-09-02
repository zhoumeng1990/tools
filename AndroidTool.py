# -*- coding: UTF-8 -*-

import os
import shutil
import xml.dom.minidom as XmlDocument

dir_path = os.path.abspath('.') + '/'
channel_path = ''    # 写入渠道号
app_name = ''

def readInfo():
    if os.path.exists(channel_path):
        f = open(channel_path, 'r+')
        print (u'渠道号: ' + f.read()).strip('\n')
        f.close()
    # 使用minidom解析器打开 XML 文档
    DOMTree = XmlDocument.parse(dir_path + '/' + app_name + '/AndroidManifest.xml')
    manifestNode = DOMTree.getElementsByTagName('manifest')[0]
    print u'包名: ' + manifestNode.getAttribute('package')
    collection = DOMTree.documentElement
    applicationNode = collection.getElementsByTagName("application")[0]
    if applicationNode.hasAttribute('android:label'):
        print u'文件名: ' + applicationNode.getAttribute("android:label")

    meta_datas = applicationNode.getElementsByTagName('meta-data')

    for metaData in meta_datas:
        if metaData.getAttribute('android:name') == 'com.openinstall.APP_KEY':
            print 'openInstall: ' + metaData.getAttribute('android:value')
        elif metaData.getAttribute('android:name') == 'WX_APP_KEY':
            print u'微信key:' + metaData.getAttribute('android:value')
        elif metaData.getAttribute('android:name') == 'JPUSH_APPKEY':
            print u'极光key: ' + metaData.getAttribute('android:value')

    if os.path.exists(dir_path + app_name):
        shutil.rmtree(dir_path + app_name)
    pass

if __name__ == '__main__':

    files = os.listdir(dir_path)
    for file in files:
        if os.path.splitext(file)[-1][1:] == 'apk':
            app_name = os.path.splitext(file)[0]
            channel_path = dir_path + '/' + app_name + '/assets/channel.ini'
            if os.path.exists(dir_path + app_name):
                shutil.rmtree(dir_path + app_name)
            # 反编译
            decode_cmd = 'apktool d ' + app_name + '.apk'
            os.system('cd ' + dir_path)
            os.system(decode_cmd)
            readInfo()