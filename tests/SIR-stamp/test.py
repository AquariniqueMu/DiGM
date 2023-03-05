'''
Description: 
Author: Junwen Yang
Date: 2023-03-05 14:03:33
LastEditTime: 2023-03-05 14:17:30
LastEditors: Junwen Yang
'''
from tqdm import tqdm, trange

# # 设置外部循环的进度条
for i in trange(2000, desc='Overall Progress'):
    # 设置内部循环的进度条
    for j in tqdm(range(7000000), desc='Inner Progress', leave=False):
        # 你的代码
        pass

# from alive_progress import alive_bar, config_handler


# config_handler.set_global(length=50, spinner='fish2')


# for i in range(20):
#     with alive_bar(700, title=f'Outer loop {i}') as bar1:
#         for j in range(700):
#             # Do some work here
#             bar1()