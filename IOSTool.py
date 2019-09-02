# -*- coding: UTF-8 -*-
import zipfile
import biplist
import sys
import re
import os

dir_path = os.path.abspath('.') + '/'

def analyze_ipa_with_biplist(ipa_path):
    # 先解压
    ipa_file = zipfile.ZipFile(ipa_path)
    # 拿到plist文件
    plist_path = find_plist_path(ipa_file)
    # 读取
    plist_data = ipa_file.read(plist_path)
    # print 'plist_data: ' +plist_data
    # 转字典
    plist_root = biplist.readPlistFromString(plist_data)
    # 读取字典
    print_ipa_info(plist_root)


def find_plist_path(zip_file):
    name_list = zip_file.namelist()
    pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
    for path in name_list:
        m = pattern.match(path)
        if m is not None:
            return m.group()


def print_ipa_info(plist_root):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # print ('文件名: %s' % plist_root['CFBundleDisplayName'])
    if 'ChannelID' in plist_root:
        print (u'渠道号: %s' % plist_root['ChannelID'])
    if 'CFBundleIdentifier' in plist_root:
        print (u'包名: %s' % plist_root['CFBundleIdentifier'])
    if 'com.openinstall.APP_KEY' in plist_root:
        print (u'openInstall: %s' % plist_root['com.openinstall.APP_KEY'])
    if 'CFBundleDisplayName' in plist_root:
        print (u'文件名: %s' % plist_root['CFBundleDisplayName'])
    if 'jpush_appkey' in plist_root:
        print (u'极光key: %s' % plist_root['jpush_appkey'])
    if 'weixinAppKey' in plist_root:
        print (u'微信key: %s' % plist_root['weixinAppKey'])


if __name__ == '__main__':
    files = os.listdir(dir_path)
    for file in files:
        if os.path.splitext(file)[-1][1:] == 'ipa':
            app_name = os.path.splitext(file)[0]
            ipaPath = dir_path + app_name + '.ipa'
            analyze_ipa_with_biplist(ipaPath)
