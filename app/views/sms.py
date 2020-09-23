import string
import time

import random
from flask import Blueprint, current_app, request
from redis.utils import pipeline

sms = Blueprint('sms', __name__, url_prefix='/sms')

CODE_LENGTH = 6  # 验证码长度
CODE_LIFETIME = 60 * 5  # 验证码有效时间
CODE_INTERVAL = 60  # 发送验证码的时间间隔
CODE_VALID_TIMES = 3  # 验证码可以被测试的次数
SINGLE_IP_TIMES = 3  # 单个IP可以调用接口的次数，超过之后需要输入验证码
ONE_HOUR = 3600
ONE_DAY = 3600 * 24


def random_digits(length):
    return ''.join(random.choice(string.digits) for _ in range(length))


def random_captcha():
    return ''.join(random.choice(string.ascii_letters) for _ in range(6))


def sms_api(phone, msg):
    print(msg)
    return True


def captch_required():
    """装饰器，用来修饰在某些情况下需要通过图形验证码才能调用的函数"""
    pass


def redis_get_int(redis, key, default=None):
    n = redis.get(key)
    if n is not None:
        return int(n)

    return default


@sms.route('/<phone>', methods=['POST'])
# 适用 flask-limiter 对同一个来源 IP 做调用次数限制，一分钟内只能调用一次
def send_sms(phone):
    # 短信验证码有效期 5 分钟
    # 验证码为 6 为纯数字
    # 每个手机号 60s 内只能发送一次短信
    # 同一手机号在同一时间内可以有多个有效的验证码
    # 保存于服务端的验证码，至多可被适用3次（无论是否匹配，3次后立即作废）
    # 发送短信验证码前，先验证图形或第三方验证程序

    sms_sent_key = 'sms_sent:' + phone
    sms_codes_key = 'sms_codes:' + phone
    sms_used_times_key = 'sms_codes:{}:times'.format(phone)
    ip_sms_times = 'ip:{}:sms'.format(request.remote_addr)

    redis = current_app.redis
    if redis.exists(sms_sent_key):
        raise ValueError('Only once sms can be sent in one minute')
    if redis_get_int(redis, ip_sms_times, 0) > SINGLE_IP_TIMES:
        raise ValueError('Need captcha')

    code = random_digits(CODE_LENGTH)
    if sms_api(phone, code):
        # 添加一个有效的验证码
        now = int(time.time())
        redis.zadd(sms_codes_key, now + CODE_LIFETIME, code)
        redis.zadd(sms_used_times_key, 0, code)
        # 将过期的验证码剔除
        # 这个也必须加到一个后台的定时任务中，避免内存占用过多
        redis.zremrangebyscore(sms_codes_key, 0, now)
        redis.set(sms_sent_key, 1, CODE_INTERVAL)
        redis.incr(ip_sms_times)
        redis.expire(ip_sms_times, ONE_HOUR)
    else:
        raise ValueError('Send sms failed')


def check_sms_code(phone, code):
    sms_codes_key = 'sms_codes:' + phone
    # 用来记录各个验证码已使用的次数，每次不匹配则现有的全部都+1
    sms_used_times_key = 'sms_codes:{}:times'.format(phone)
    now = int(time.time())
    redis = current_app.redis

    # 将过期的验证码剔除
    redis.zremrangebyscore(sms_codes_key, 0, now)
    # 判断 code 是否存在于集合中
    valid = redis.zscore(sms_codes_key, code) is not None
    if valid:
        # 删除多个 key
        redis.delete(sms_codes_key,
                     sms_used_times_key)
        return True
    else:
        # 对所有当前有效的验证码的使用次数都+1
        with pipeline(redis) as p:
            # range 的范围左右都是包含的
            # 如果要使用不包含的范围，可以使用 (1 (10 表示开区间
            # 0 表示第一个元素，-1 表示最后一个元素，-2 表示倒数第二个元素
            for code in p.zrange(sms_used_times_key, 0, -1):
                p.zincrby(sms_used_times_key, 1, code)
            # 删除超过次数的验证码，上限为 +inf
            p.zremrangebyscore(sms_used_times_key, CODE_VALID_TIMES, '+inf')
        return False


def generate_captcha(captcha):
    return 'image'


@sms.route('/captcha', methods=['GET'])
def new_captcha():
    current_app.session['captch'] = captcha = random_captcha()
    return generate_captcha(captcha)


@sms.route('/captcha/<captcha>', methods=['POST'])
def check_captcha(captcha):
    pass
