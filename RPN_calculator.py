#!usr/bin/env python3
#-*- coding: utf-8 -*-

"""
guanzizhan RPN calculator interview test
"""
import functools
import time
import math
import re
import copy

def retry(func, tries = 3, delay = 3):
    """ retry to do some operation """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper"""
        for r in range(tries - 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                print(f"请检查，并在{delay}秒后重新输入：")
                time.sleep(delay)
        return func(*args, **kwargs)
    return wrapper


class RPN_Calculator(object):
    """ rpn calculator mode """

    def __init__(self):
        """ init something """
        self.history_stack = dict()  # 初始化历史记录
        self.number_of_operations = 0  # 历史记录key版本
        self.current_stack = list()  # 初始化堆栈

    def rpn_switch(self, switch):
        """ rpn计算开关 """
        self.rpn_switch = switch  # 计算开关
        while self.rpn_switch:
            self.rpn_mode()

    @retry
    def input_check(self):
        """ check input """
        self.input_stack = input("input stack > ")  # 请输入
        if self.input_stack == "exit":
            exit(0)
        self.check_input_stack = list()  # 初始化检查后列表
        for item in self.input_stack.split(" "):  # 逐个检查
            if item:  # 去空格
                if item in ("+", "-", "*", "/", "sqrt", "undo", "clear"):  # 判断是操作符
                    self.check_input_stack.append(item)  # 加入结果列表
                    continue
                item = round(float(item), 15)  # 不是操作符则改为15位小数
                self.check_input_stack.append(item)  # 加入结果列表
        return self.check_input_stack  # 返回结果

    def rpn_mode(self):
        """ rpn_mode """
        self.check_input_stack = self.input_check()  # 检查初始化输入
        self.copy_input_stack = copy.deepcopy(self.check_input_stack)  # 备份输入数据
        while self.check_input_stack:  # 输入不为空则进行运算
            current_item = self.check_input_stack.pop(0)  # 逐个弹出
            self.operation_model(current_item)  # 对弹出对象进行操作
            self.number_of_operations += 1  # 历史记录自增
            self.history_stack[self.number_of_operations] = list(self.current_stack)  # 记录本次操作
            if current_item == "undo":  # 遇到undo则退回上个版本
                del self.history_stack[self.number_of_operations]
                del self.history_stack[self.number_of_operations - 1]
                self.number_of_operations -= 2
                self.current_stack = self.history_stack[self.number_of_operations]  # 将当前进度更新为上个版本
        print("stack:", " ".join([str("%.10f" % x) for x in self.history_stack[self.number_of_operations]]))  # 打印结果保留10位小数


    def operation_model(self, current_item):
        """ operation model """
        if current_item == "clear":
            self.current_stack = list()
        if current_item not in ("+", "-", "*", "/", "sqrt", "undo", "clear"):
            self.current_stack.append(current_item)  # 数字加入堆栈
        if current_item in ("+", "-", "*", "/") and len(self.current_stack) >= 2:
            last_num = self.current_stack.pop()
            penultimate_num = self.current_stack.pop()
            if current_item == "+":
                self.current_stack.append(round(penultimate_num + last_num, 15))
            if current_item == "-":
                self.current_stack.append(round(penultimate_num - last_num, 15))
            if current_item == "*":
                self.current_stack.append(round(penultimate_num * last_num, 15))
            if current_item == "/":
                self.current_stack.append(round(penultimate_num / last_num, 15))
        elif current_item in ("+", "-", "*", "/"):
            position = 2 * (len(self.copy_input_stack) - len(self.check_input_stack)) - 1  # 计算报错位置
            print(f"operator {current_item}(position:{position}):insucient parameters")  # 打印错误位置
            print("stack:", " ".join([str("%.10f" % x) for x in self.current_stack]))  # 打印堆栈当前状态
            exit(0)
        if current_item == "sqrt" and len(self.current_stack) >= 1:  # 业务疑问：sqrt对堆栈顶部进行平方根之后插入顶部还是底部？
            self.current_stack.insert(0, round(math.sqrt(self.current_stack.pop(0)), 15))  # 当前模式为插入顶部
        elif current_item == "sqrt":
            position = 2(len(self.copy_input_stack) - len(self.check_input_stack)) - 1  # 计算报错位置
            print(f"operator sqrt(position:{position}):insucient parameters")  # 打印错误位置
            print("stack:", " ".join([str("%.10f" % x) for x in self.current_stack]))  # 打印堆栈当前状态
            exit(0)


if __name__ == "__main__":
    rpn_calculator = RPN_Calculator()  # 实例化
    rpn_calculator.rpn_switch(switch=True)