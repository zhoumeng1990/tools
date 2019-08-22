# -*- coding: UTF-8 -*-
import zipfile
import biplist
import sys
import re
import os

dir_path = os.path.abspath('.') + '/'
ipa_path = dir_path + '688.ipa'

def analyze_ipa_with_plistlib(ipa_path):
    ipa_file = zipfile.ZipFile(ipa_path)
    plist_path = find_plist_path(ipa_file)
    plist_data = ipa_file.read(plist_path)
    # print 'plist_data: ' +plist_data
    plist_root = biplist.readPlistFromString(plist_data)
    print_ipa_info (plist_root)

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
    print ('文件名: %s' % plist_root['CFBundleDisplayName'])
    print ('包名: %s' % plist_root['CFBundleIdentifier'])
    print ('渠道号: %s' % plist_root['ChannelID'])
    print ('openInstall: %s' % plist_root['com.openinstall.APP_KEY'])
    print ('极光key: %s' % plist_root['jpush_appkey'])
    print ('微信key: %s' % plist_root['weixinAppKey'])

if __name__ == '__main__':
    analyze_ipa_with_plistlib(ipa_path)