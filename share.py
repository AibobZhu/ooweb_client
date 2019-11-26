from flask import make_response, request, jsonify
from flask_restful import abort, Api
from flask_httpauth import HTTPBasicAuth
import json, zlib
import random
import binascii
import uuid
from dateutil.relativedelta import relativedelta
import datetime

#TODO(haibo.zhu@hotmail.com): Check HTTPBasicAuth thread safe

APIs = {
    'render': '/api/{}/render'
}

auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized():
    print(request.base_url)
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_password
def verify_password(username, password):
    print('username:{}, password:{}'.format(username, password))
    if username != 'haibo' or password != 'python':
        return False
    return True


def abort_if_task_doesnt_exist(task_id, tasks):
    if task_id not in tasks:
        abort(404, message="Task {} doesn't exist".format(task_id))

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    else:
        print("Error: Type not support:",type(obj))
        raise TypeError

def create_payload(data_input, compress=True):
    if not isinstance(data_input, str):
        data_json = json.dumps(data_input, default=set_default)
    else:
        data_json = data_input
    print('len of data_input:{}, data_json:{}'.format(len(data_input), len(data_json)))
    if compress:
        data_bytes_com = zlib.compress(data_json.encode('utf8'))
        data_str = data_bytes_com.hex()
        print('len of compressed data:{}'.format(len(data_str)))
    else:
        data_str = data_json

    return {'data': data_str}


def extract_data(data_str_com, compressed=True):
    if compressed:
        rd_bytes_com = bytes.fromhex(data_str_com)
        rd = zlib.decompress(rd_bytes_com)
        rd = rd.decode('utf8')
    else:
        rd = data_str_com
    #rd = json.loads(rd_json)
    return rd


def _getGBK2312():
  head = random.randint(0xb0,0xc0)
  body = random.randint(0xa1,0xc9)
  val = (head << 8) | body
  val = binascii.unhexlify(hex(val)[2:].encode('ascii')).decode('gb2312')
  return val


def _getStr(leng):
  s = ''
  for _ in range(leng):
    s += _getGBK2312()
  return s


def _getSUUID():
	return str(uuid.uuid4()).split("-")[0]

def getDatetimeStr(years=(2019,2019),months=(1,12),days=(1,28),delta_days=None):
  year = random.randint(years[0],years[1])
  month = random.randint(months[0],months[1])
  day = random.randint(days[0],days[1])
  dd=str(year)+"-"+str(month)+"-"+str(day)
  fmt="%Y-%m-%d"
  start = datetime.datetime.strptime(dd, fmt)
  if not delta_days:
    delta_days = random.randint(3,15)
  end = start + relativedelta(days=delta_days)
  return start.strftime(fmt), end.strftime(fmt)

def randDatetimeRange(delta_days_range=(0,30)):
    today = datetime.datetime.today()
    before_days = random.randint(delta_days_range[0],delta_days_range[1])
    after_days = random.randint(delta_days_range[0], delta_days_range[1])
    fmt = "%Y-%m-%d %H:%M:%S"
    start = today - relativedelta(days=before_days)
    end = today + relativedelta(days=after_days)
    return start.strftime(fmt), end.strftime(fmt)

def day_2_week_number(self, date, first_day=0):
    import numpy as np
    calendar.setfirstweek(first_day) # first_day 0 for monday, 6 for sunday
    year = date.year
    month = date.month
    day = date.day
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x == day)[0][0] + 1
    return week_of_month

def week_2_dates(week_str, first_day=0):
    import numpy as np
    def _week_end(week):
        for i in range(0, week.__len__())[::-1]:
            if week[i] != 0:
                return week[i]

    calendar.setfirstweek(first_day) # 0 for monday, 6 for sunday
    year = int(week_str.split('年')[0])
    month = int(week_str.split('月')[0].split(' ')[-1])
    week_num = int(week_str.split('周')[0].split('第')[-1])

    weeks = np.array(calendar.monthcalendar(year,month))
    week = weeks[week_num]
    return (datetime.datetime(year,month,week[0]),datetime.datetime(year,month,_week_end(week)))
