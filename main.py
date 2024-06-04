from typing import Union

from fastapi import FastAPI

app = FastAPI()


# 切换代理
@app.get("/switch")
def switch_proxy(proxy_id: int):
    print(proxy_id)
    return {'code': 0}


# 将match url 添加到被代理列表
@app.get("/add")
def switch_proxy(matched_url: str):
    print(matched_url)
    return {'code': 0}


# 获取所有代理
@app.get("/proxies")
def data():
    return {'code': 0,
            "data": [
                {'name': "直接连接", 'select': 0, 'id': 0},
                {'name': "Proxy1", 'select': 1, 'id': 1},
                {'name': "Proxy2", 'select': 0, 'id': 2},
                {'name': "Proxy3", 'select': 0, 'id': 3},
            ]}
