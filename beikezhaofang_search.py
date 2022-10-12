import time
import requests
import datetime
from elasticsearch import Elasticsearch
import schedule

es = Elasticsearch([{"host": "124.223.110.36", "port": 9200}], timeout=60)


def search():
    """
    十梅庵
    :return:
    """
    try:
        session = requests.session()
        all_count = 0
        for page in range(1, 150):
            url = f'https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/houselist?cityId=370200&dataSource=ESF&curPage={page}&condition=&type=&resblockId=&maxLatitude=36.19938884697075&minLatitude=36.18258202960425&maxLongitude=120.43441802672942&minLongitude=120.39309597327043'
            resp = session.get(url).json()
            for i in resp['data']['list']:
                i['area'] = '十梅庵'
                i['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d')
                del i['tags']
                es.index(index='bkzf_data', doc_type='_doc', body=i)
                all_count += 1
            if not resp['data']['hasMore']:
                break
        print(f'本次获取{all_count}条数据', datetime.datetime.now())
    except Exception as e:
        print(e)


def search_xq_cjjl(xqid, page=1):
    """
    获取小区成交记录
    :return:
    """
    print(xqid, page)
    session = requests.session()
    session.headers = {
        'cookie': 'lianjia_uuid=44e1391b-489c-4c0a-a327-6e245aa88d36; crosSdkDT2019DeviceId=-x9q3no--5mdcvr-f9kzxya5es48pbd-jx7pp1cqo; hy_data_2020_id=182193f7789584-0f868125df5e09-26021a51-921600-182193f778a160f; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%22182193f7789584-0f868125df5e09-26021a51-921600-182193f778a160f%22%2C%22site_id%22%3A341%2C%22user_company%22%3A236%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%22182193f7789584-0f868125df5e09-26021a51-921600-182193f778a160f%22%7D; _ga=GA1.2.771328723.1658281096; ke_uuid=347ddfd2d2a158c6e7e42fa80de9b80a; __xsptplus788=788.6.1663656166.1663656338.6%234%7C%7C%7C%7C%7C%23%23PAOid8MvNTnzaW7MN1-jtwaYRKI5ApUL%23; select_city=370200; lianjia_ssid=b5f934ba-07ba-4c8e-a303-e933fa047e0b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218215bb5d8498d-03458b5f0566ca-26021a51-921600-18215bb5d8512a0%22%2C%22%24device_id%22%3A%2218215bb5d8498d-03458b5f0566ca-26021a51-921600-18215bb5d8512a0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%E6%89%BE%E6%88%BF%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyqingdao%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; login_ucid=2000000267987290; lianjia_token=2.001071df017ae19bb701dcf63000b9d978; lianjia_token_secure=2.001071df017ae19bb701dcf63000b9d978; security_ticket=VrJY/JbqCARn4UxQ745xoVRA/8kaogmiZ8Ws/9oDGehanmZgkPcD/6Mx9gkmAB0MWNDdre/wCpujZxyz9LrDxL8x4c7w99gU4OrPwAooh9EPE96ZDnG69ASsMURg9/JQhF71Zo5LJD5+keo07gpsvNP0NW75qGAMhNGSGpagq3k=; digData=%7B%22key%22%3A%22m_pages_chengjiaoSearch%22%7D; beikeBaseData=%7B%22parentSceneId%22%3A%226314282828215173377%22%7D',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    }
    url = f'https://m.ke.com/liverpool/api/chengjiao/getList?cityId=370200&condition=%252Fc{xqid}pg{page}'
    resp = session.get(url).json()
    for i in resp['data']['data']['getChengjiaoList']['list']:
        print(i['signTime'])
        query2 = {
            "query": {
                "match": {
                    "houseCode": str(i['houseCode'])
                }
            }
        }
        res2 = es.search(index="bkzf_data_xq_cjjl", body=query2)
        if int(res2['hits']['total']['value']) == 0:
            es.index(index='bkzf_data_xq_cjjl', doc_type='_doc', body=i)
        else:
            print('已存在')
            return 0
    if resp['data']['data']['getChengjiaoList']['hasMoreData']:
        page += 1
        search_xq_cjjl(xqid, page)
        time.sleep(2)


def search_xq():
    for xqid in [
        '1520061020486796',  # 湖山美地一期
        '1520061020478558',  # 湖山美地二期
        '1511041749946',    # 春和景明一期
        '1511043475286',  # 春和景明二期
    ]:
        search_xq_cjjl(xqid)


if __name__ == '__main__':
    # print('贝壳找房信息正在监控中')
    # schedule.every().day.at("08:00").do(search)
    # while 1:
    #     schedule.run_pending()
    #     time.sleep(10)
    search_xq()
