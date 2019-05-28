attack_config = {
        'phone': '1331883****',  # 攻击的电话号码
        'name': '刘**',  # 攻击的人姓名
        'email': '137419****@qq.com',  # 攻击的人邮箱(未做此功能)
        'address': '广州市天河区',  # 地址(未做次功能)
        "content": "你好, 我想与贵公司进行业务洽谈, 请尽快与我联系! 我的微信是: ",  # 留言信息
        'attack_num': 10,  # 攻击次数(是访问网站的次数，并不代表成功攻击次数)
        'attack_type': ('sq', 'lxb'),  # sq: 留言， lxb: 网页回呼
        'wechat': '1331883****'  # 微信
    }
attack_config['content'] += attack_config['wechat']
