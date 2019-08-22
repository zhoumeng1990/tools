# -*- coding: UTF-8 -*-

import os
import shutil
import xml.dom.minidom as XmlDocument

dir_path = os.path.abspath('.') + '/'
manifest_path = dir_path + '/app/AndroidManifest.xml'  # AndroidManifest路径
apk_path = dir_path + '/app.apk'  # apk路径
channel_path = dir_path + '/app/assets/channel.ini'    # 写入渠道号

def readInfo():
    f = open(channel_path, 'r+')
    print 'channel: ' + f.read()
    # 使用minidom解析器打开 XML 文档
    DOMTree = XmlDocument.parse(manifest_path)
    manifestNode = DOMTree.getElementsByTagName('manifest')[0]
    print 'packageName: '+manifestNode.getAttribute('package')
    collection = DOMTree.documentElement
    applicationNode = collection.getElementsByTagName("application")[0]
    if applicationNode.hasAttribute('android:label'):
        print 'appName: '+applicationNode.getAttribute("android:label")

    metaDatas = applicationNode.getElementsByTagName('meta-data')

    for metaData in metaDatas:
        if metaData.getAttribute('android:name') == 'com.openinstall.APP_KEY':
            print 'openInstall: ' + metaData.getAttribute('android:value')
        elif metaData.getAttribute('android:name') == 'WX_APP_KEY':
            print 'wxKey:' + metaData.getAttribute('android:value')
        elif metaData.getAttribute('android:name') == 'JPUSH_APPKEY':
            print 'jpushKey: ' + metaData.getAttribute('android:value')

    pass

if __name__ == '__main__':

    files = os.listdir(dir_path)
    for file in files:
        if os.path.splitext(file)[0] == 'app' and os.path.splitext(file)[-1][1:] == 'apk':
            if os.path.exists(dir_path + 'app'):
                shutil.rmtree(dir_path + 'app')
            decode_cmd = 'apktool d app.apk'
            os.system('cd ' + dir_path)
            os.system(decode_cmd)
            readInfo()

            pass