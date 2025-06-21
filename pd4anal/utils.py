import numpy as np
import pandas as pd
import importlib.util
from typing import Any, Tuple, Union
import sys
if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata
from contextlib import contextmanager


def spend_time(func):
    import time
    start = time.time()
    def warpper(*args, **kwargs):
        res = func(*args, **kwargs)
        end = time.time()
        consume = end - start
        start1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
        end1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))

        print(f'{start1} ~ {end1}\tspent {consume:.2f}s')
        return res
    return warpper

def cal_month_delta(start_dt, end_date='202301'):
    '''计算两个日期之间差的月份数, 支持series和str的输入
    '''
    if isinstance(start_dt, pd.Series):
        year_delta = int(end_date[:4]) - start_dt.astype('str').str[:4].astype(int)
        month_delta = int(end_date[4:6]) - start_dt.astype('str').str[4:6].astype(int)
    elif isinstance(start_dt, str):
        year_delta = int(end_date[:4]) - int(start_dt[:4])
        month_delta = int(end_date[4:6]) - int(start_dt[4:6])
    return 12 * year_delta + month_delta + 1


def cal_dt_by_month_delta(dt, month_delta):
    '''根据固定日期和offset的月份，计算月份, dt是int或者str类型的输入
    '''
    year = int(str(dt)[:4])
    month = int(str(dt)[4:6])
    dt = str(dt)[6:8]
    
    a = (month + month_delta) // 12
    b = (month + month_delta) % 12
    if (a==0) and (b==0):
        a = -1
        b = 12
    year_new = year + a
    month_new = b
    dt_new = str(year_new) + str(month_new).zfill(2)
    if dt != '':
        dt_new += dt
    return int(dt_new)

def is_dtype_numberic(sr):
    ''' 判断一个series的dtype是否是数值型 '''
    if is_dtype_float(sr) or is_dtype_int(sr):
        return True
    return False

def is_dtype_float(sr):
    ''' 判断一个series的dtype是否是float '''
    dtype = sr.dtype if isinstance(sr, pd.Series) else sr
    if (dtype == float) or (dtype == np.float32) or (dtype == 'float'):
        return True
    return False

def is_dtype_int(sr):
    ''' 判断一个series的dtype是否是int '''
    dtype = sr.dtype if isinstance(sr, pd.Series) else sr
    if (dtype == int) or (dtype == np.int32) or (dtype == 'int'):
        return True
    return False

def is_package_available(pkg_name: str, return_version: bool = False) -> Union[Tuple[bool, str], bool]:
    # Check we're not importing a "pkg_name" directory somewhere but the actual library by trying to grab the version
    package_exists = importlib.util.find_spec(pkg_name) is not None
    package_version = "N/A"
    if package_exists:
        try:
            package_version = importlib.metadata.version(pkg_name)
            package_exists = True
        except importlib.metadata.PackageNotFoundError:
            package_exists = False
        # print(f"Detected {pkg_name} version {package_version}")
    if return_version:
        return package_exists, package_version
    else:
        return package_exists

@contextmanager
def safe_import(pkg_name: str = None):
    '''import some module safely
    - 部分包中使用到某些函数，import出错也不影响其他函数的运行
    - 如果下面函数入参类型声明使用到了这个包，这种方式也会报错，比如定义`def func(df:pd.DataFrame)`，但是不存在pandas包

    :param pkg_name: str, 包名，用于检查module是否存在，默认为None表示不检查

    ### Example
    ```python
    from torch4keras.snippets import safe_import
    with safe_import('pptx') as si:
        if si:  # 包存在才执行
            from pptx import Presentation

    # 不验证包是否存在, import出错不影响运行
    with safe_import():
        import fitz
    '''
    try:
        if pkg_name is None:  # 未指定包名
            yield True
        elif not is_package_available(pkg_name): # 指定包名但不存在
            log_warn_once(f"No module named '{pkg_name}'")
            yield False
        else:  # 指定报名且存在
            yield True
    except Exception as e:
        log_warn_once(f"{e}")