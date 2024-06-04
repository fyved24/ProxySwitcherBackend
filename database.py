# database.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Proxies(Base):
    __tablename__ = 'proxies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    select = Column(Integer, default=0)  # 默认值为0，表示未选择
    matched_urls = relationship("MatchedURLs", back_populates="proxy")


class MatchedURLs(Base):
    __tablename__ = 'matched_urls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    matched_url = Column(String)
    proxy_id = Column(Integer, ForeignKey('proxies.id'))
    proxy = relationship("Proxies", back_populates="matched_urls")


class Database:
    def __init__(self, db_url='sqlite:///proxies.db'):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_proxy(self, name):
        new_proxy = Proxies(name=name)
        self.session.add(new_proxy)
        self.session.commit()
        print(f'Added proxy: {new_proxy}')

    def query_proxies(self):
        return self.session.query(Proxies).all()

    def delete_proxy(self, proxy_id):
        proxy = self.session.query(Proxies).filter(Proxies.id == proxy_id).first()
        if proxy:
            self.session.delete(proxy)
            self.session.commit()
            print(f'Deleted proxy with id: {proxy_id}')
        else:
            print(f'Proxy with id: {proxy_id} not found')

    def set_selected_proxy(self, proxy_id):
        proxies = self.session.query(Proxies).all()
        for proxy in proxies:
            if proxy.id == proxy_id:
                proxy.select = 1
            else:
                proxy.select = 0
        self.session.commit()

    def get_selected_proxy(self):
        selected_proxy = self.session.query(Proxies).filter(Proxies.select == 1).first()
        return selected_proxy.id if selected_proxy else None

    def add_matched_url(self, matched_url, proxy_id):
        new_url = MatchedURLs(matched_url=matched_url, proxy_id=proxy_id)
        self.session.add(new_url)
        self.session.commit()
        print(f'Added matched URL: {new_url}')

    def query_matched_urls(self):
        return self.session.query(MatchedURLs).all()

    def delete_matched_url(self, url_id):
        url = self.session.query(MatchedURLs).filter(MatchedURLs.id == url_id).first()
        if url:
            self.session.delete(url)
            self.session.commit()
            print(f'Deleted matched URL with id: {url_id}')
        else:
            print(f'Matched URL with id: {url_id} not found')

    def query_matched_urls_by_proxy_id(self, proxy_id):
        proxy = self.session.query(Proxies).filter(Proxies.id == proxy_id).first()
        if proxy:
            return [url.matched_url for url in proxy.matched_urls]
        else:
            print(f'Proxy with id: {proxy_id} not found')
            return []
