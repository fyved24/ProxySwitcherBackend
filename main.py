from typing import Union
from database import Database

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()
db = Database()


# 切换代理
@app.get("/switch")
def switch_proxy(proxy_id: int):
    print(proxy_id)
    db.set_selected_proxy(proxy_id)
    return {'code': 0}


# 将match url 添加到被代理列表
@app.get("/add")
def switch_proxy(matched_url: str):
    print(matched_url)
    selected_proxy_id = db.get_selected_proxy()
    db.add_matched_url(matched_url=matched_url, proxy_id=selected_proxy_id)
    return {'code': 0}


# 获取所有代理
@app.get("/proxies")
def data():
    proxies = db.query_proxies()
    print(proxies)
    return {'code': 0,
            "data": proxies}


@app.get("/rules.pac", response_class=PlainTextResponse)
def rules_pac():
    # 获取当前选定的代理 ID
    proxy_id = db.get_selected_proxy()
    if proxy_id is None:
        raise HTTPException(status_code=404, detail="No proxy selected")

    # 根据当前选定的代理 ID 查询匹配的 URL 列表
    matched_urls = db.query_matched_urls_by_proxy_id(proxy_id)

    # 构建 PAC 规则
    pac_content = """ FindProxyForURL(url, host) {
"""

    if matched_urls:
        pac_content += "\n" + "\n".join(
            [f'    if (shExpMatch(url, "{url}")) return "SOCKS5 127.0.0.1:7890";' for url in matched_urls])

    pac_content += """

    return "DIRECT"; 
}"""

    return pac_content
