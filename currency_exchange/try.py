import os.path
from datetime import datetime, timedelta
#
#
#
# date_str = '05-27-2020'
#
# dto = datetime.datetime.strptime(date_str, '%m-%d-%Y').date()
# print(type(dto))
# print(dto)
#
# # a = '15.05.2022'
# # date_time_obj = datetime.strptime(a.replace('.', '-'), '%d-%m-%Y').date()
# # print(date_time_obj)
# a = '15.05.2022'
# date_time_obj = datetime.datetime.strptime(a, '%d.%m.%Y').date()
# print(date_time_obj)
# print(datetime.datetime.today().date())
#
# print(datetime.datetime.today().date() + datetime.timedelta(days=10))
#
#
#
# class A:
#     v_1 = 1
#     v_2 = 2
#     v_3 = 3
#
#
# print([getattr(A, item) for item in dir(A) if item.startswith('v_')])
#
# from collections import OrderedDict
#
#
# d = [OrderedDict({'id': 3, 't': 5}), OrderedDict({'id': 1, 't': 5}), OrderedDict({'id': 2, 't': 5})]
#
# print(sorted(d, key=lambda item: item.get('id')))

# print(datetime.datetime.today().date())


from exchange_api.settings import BASE_DIR

print(os.path.join(BASE_DIR, 'test/my/'))