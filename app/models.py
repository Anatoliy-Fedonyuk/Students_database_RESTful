from datetime import datetime

num = 1000000000000000001000
now = datetime.now()

print(f'{num = :_}')
print(f'Now it`s - {now:%d.%m.%Y %H:%M:%S}')