import time

from dodp_new.client_v1 import DODPClientV1

start_time = time.time()
client_v1 = DODPClientV1('https://do.av3715.ru')
print(client_v1.login('motorina@ia-group.ru', '23610'))
end_time = time.time()
print(f'Delta time: {end_time - start_time}')
