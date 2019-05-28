import asyncio
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from config import headers, logger
import os

ip = 'www.fly****.cn'  # 写入爬取信息的数据库服务器地址, 我已经爬过，你们可以直接找我要数据
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
engine = create_engine(f'oracle+cx_oracle://Zoe:Zoe@{ip}:1521/orcl')


def create_table():
    tables = engine.table_names()
    if 't_info' not in tables:
        sql = "CREATE TABLE t_info(id_ number, info varchar2(100),tel varchar2(100),url varchar2(100))"
        engine.execute(sql)


async def get_phone(sem, id_):
    sql = f'select count(1) from t_info where id_ = {id_}'
    result = engine.execute(sql).fetchmany()[0][0]
    if result != 0:
        return True
    url = f'http://lxbjs.baidu.com/cb/url/show?f=55&id={id_}'
    async with ClientSession() as session:
        async with sem:
            try:
                async with session.get(url, headers=headers, timeout=10) as respone:
                    text = await respone.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    info = soup.find('div', class_='cpy-info').text
                    tel = soup.find('div', class_='cpy-info cpy-tel').text
                    url = soup.find('div', class_='cpy-info cpy-url').find('a').text
                    sql = f"insert into t_info values({id_}, '{info}', '{tel}', '{url}')"
                    engine.execute(sql)
                    logger.info(f'爬取信息成功: [{id_}] {info}')
                return True
            except Exception as e:
                logger.error(f'爬取信息失败: [{id_}] {type(e)}: {str(e)}')
                return False


def main():
    sessionCount = 10  # 同时启动协程数量
    sem = asyncio.Semaphore(sessionCount)
    loop = asyncio.get_event_loop()  # 启动异步首要语句
    for page_num in range(1, 1001):  # 为了避免同时创建太多task,这里分1000页，每页100条
        start_id = (page_num - 1) * 100 + 1
        end_id = page_num * 100
        tasks = [asyncio.ensure_future(get_phone(sem, id_)) for id_ in range(start_id, end_id)]  # 创建任务列表
        # tasks = [asyncio.ensure_future(get_phone(sem, id_)) for id_ in range(1, 2)]  # 创建任务列表
        loop.run_until_complete(asyncio.wait(tasks))  # 执行任务
        # break
    loop.close()


if __name__ == '__main__':
    create_table()
    main()
