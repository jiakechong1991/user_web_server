# -*- coding:utf-8 -*-

import datetime



class TimeBase(object):
    """一个程序中，控制时间的来源，应该只有一处，否则遇见时区问题，将非常麻烦"""
    pass

    @staticmethod
    def get_now_str():
        """获得当前时间戳"""
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        return time_str
    
    @staticmethod
    def time_str2int(time_str:str):
        """时间字符串转int"""
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    
    @staticmethod
    def time_int2str(time_int:int):
        """int转时间字符串"""
        dt = datetime.datetime.fromtimestamp(time_int)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def datetime_diff(in_datetime, diff_seconds:int):
        """比较in_datetite + diff_seconds(秒) >= now"""
        pass
        #a = datetime.datetime(2025, 8, 9, 15, 36, 58)

        # 比较a加60秒是否大于当前时间
        if in_datetime + datetime.timedelta(seconds=diff_seconds) >= datetime.datetime.now():
            return True
        else:
            return False

    




if __name__ == "__main__":
    pass

    print("当前时间:{a}".format(a=TimeBase.get_now_str()))
    print("2025-06-11 15:06:12  和  1749625572 互相转化")
    print(TimeBase.time_str2int("2025-06-11 15:06:12"))
    print(TimeBase.time_int2str(1749625572))





















