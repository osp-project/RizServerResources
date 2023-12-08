import requests
import os
import json

res_version = "v1_0_15_4561e57133"

# 设置请求头，模拟游戏访问
headers = {
    'User-Agent': 'Rizline/5 CFNetwork/1408.0.4 Darwin/22.5.0',
    "X-Unity-Version": "2021.3.15f1c1"
}

downlist = []

catalog_file = open("HotUpdateResources/catalog_catalog.json","r")
catalog = catalog_file.read()
catalog_file.close()
catalog = json.loads(catalog)

# 筛选catalog中的可下载资源至列表
for InternalId in catalog["m_InternalIds"]:
    if "http://" in InternalId:
        downlist.append(InternalId)
        print(f'InternalId {InternalId} 为可下载资源，已添加至下载列表')

# 将下载列表中的下载链接替换为可用链接
for i in range(len(downlist)):
    downlist[i] = str(downlist[i]).replace("http://rizastcdn.pigeongames.cn/default/iOS/","https://rizlineassetstore.pigeongames.cn/versions/" + res_version + "/iOS/")
    if "/cridata_assets_criaddressables/" in str(downlist[i]):
        downlist[i] = str(downlist[i]).replace(".bundle","") #如果是音乐资源则移除bundle后缀，因为游戏请求音乐资源不会带Bundle

for fileurl in downlist:

    # 设置要下载的文件的url
    url = fileurl

    filename = os.path.basename(url)

    if not (os.path.exists("MusicResources/" + filename) or os.path.exists("HotUpdateResources/" + filename)):

        # 发送GET请求，获取文件的响应内容
        response = requests.get(url, headers=headers)

        if "/cridata_assets_criaddressables/" in url:
            filename = "MusicResources/" + filename
        else:
            filename = "HotUpdateResources/" + filename

        # 保存文件到本地，使用二进制写入模式
        with open(filename, 'wb') as f:
            f.write(response.content)

        # 打印文件名和大小
        print(f'文件{filename}已下载，大小为{os.path.getsize(filename)}字节。')
    else:
        print(f'文件{filename}已存在，跳过不下载。')