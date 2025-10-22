# my_se.py
# Customized Gem5 configuration for architectural exploration
# Based on the standard se.py from gem5/configs/example/

import argparse
import sys

import m5
from m5.objects import *

# 创建系统
system = System()

# 设置时钟和电压域
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# 设置内存模式
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# 创建CPU
# 可在此处切换 CPU 类型：AtomicSimpleCPU() 或 TimingSimpleCPU()
system.cpu = TimingSimpleCPU()

# 创建内存总线
system.membus = SystemXBar()

# 连接CPU缓存端口等
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# 创建中断控制器等
system.cpu.createInterruptController()

# 创建一个进程，运行测试程序
process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello'] # 指定要运行的测试程序
system.cpu.workload = process
system.cpu.createThreads()

# 连接系统端口
system.system_port = system.membus.cpu_side_ports

# 创建内存控制器
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.port = system.membus.mem_side_ports

# 启动系统
root = Root(full_system = False, system = system)
m5.instantiate()

# 开始模拟
print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
