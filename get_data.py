from elasticsearch import Elasticsearch


def get_everyday_avg_price():
    es = Elasticsearch([{"host":"124.223.110.36","port":9200}], timeout=60)
    result = es.search(index='bkzf_data', doc_type='_doc')
    total = result['hits']['total']['value']
    body = {
        'from': 0,
        'size': total
    }
    result = es.search(index='bkzf_data', doc_type='_doc', body=body)
    day_jiage = {}
    data_count = 0
    for i in result['hits']['hits']:
        i = i['_source']
        if day_jiage.get(i['create_time']) == None:
            day_jiage[i['create_time']] = []
        day_jiage[i['create_time']].append(int(str(i['unitPriceStr']).strip('元/平')))
        data_count += 1
    print(f'已获取{data_count}条数据')
    # return list(day_jiage.keys()), [round(sum(i)/len(i), 2) for i in day_jiage.values()]
    return list(day_jiage.keys()), list(day_jiage.values())


def get_xiaoqu_avg_price():
    es = Elasticsearch([{"host": "124.223.110.36", "port": 9200}], timeout=60)
    result = es.search(index='bkzf_data', doc_type='_doc')
    total = result['hits']['total']['value']
    body = {
        'from': total-1000,
        'size': 1000
    }
    result = es.search(index='bkzf_data', doc_type='_doc', body=body)
    day_jiage = {}
    data_count = 0
    for i in result['hits']['hits']:
        i = i['_source']
        xiaoqu_name = str(i['desc']).split('/')[-1]
        if day_jiage.get(xiaoqu_name) == None:
            day_jiage[xiaoqu_name] = []
        day_jiage[xiaoqu_name].append(int(str(i['unitPriceStr']).strip('元/平')))
        data_count += 1
    print(f'已获取{data_count}条数据')
    for k, v in day_jiage.items():
        day_jiage[k] = round(sum(v) / len(v), 2)
    day_jiage_sorted = sorted(day_jiage.items(), key=lambda x: x[1], reverse=True)
    return [i[0] for i in day_jiage_sorted], [i[1] for i in day_jiage_sorted]


# get_xiaoqu_avg_price()