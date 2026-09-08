# Firmware / 固件

Code that runs on the microcontrollers in this project, written in **C** against
the Raspberry Pi Pico SDK.

本项目中运行在单片机上的代码，用 **C** 编写，基于 Raspberry Pi Pico SDK。

## Why C, and why not C++ / 为什么是 C，为什么不是 C++

The full reasoning is in
[the roadmap](../docs/roadmap.md#the-parallel-c-track--并行的-c-语言线). The short
version: C is the language embedded work is actually done in — every chip
datasheet's reference code is C — and it teaches what Python and Java hide, which
is exactly what register-level work consists of. C++ is deliberately deferred:
its embedded dialect comes with a long list of features that must not be used,
and stacking it on top of learning PCB design and embedded systems at the same
time is one steep curve too many.

完整理由见[路线图](../docs/roadmap.md#the-parallel-c-track--并行的-c-语言线)。
简短版：C 是嵌入式实际使用的语言——每一颗芯片数据手册的参考代码都是 C——而且它教的
正是 Python 和 Java 藏起来的那些东西，那恰恰就是寄存器级工作的内容。C++ 是刻意推迟
的：它的嵌入式方言带着一长串"不能用"的特性，而在同时学 PCB 设计和嵌入式的时候再叠
一条陡峭曲线，是多余的一条。

## This directory starts filling in month 1 / 这个目录从第 1 个月就开始有内容

Not at Stage 3. The C track runs on a breadboard Pico from the beginning, so that
by the time a board is drawn for this firmware, the firmware has already run.

**不是等到第 3 阶段。** C 语言线一开始就在面包板上的 Pico 上跑，这样等到真的为这份
固件画板子的时候，固件已经跑过了。

| Expected contents | 预期内容 | From / 时间 |
|---|---|:---:|
| `blink/` and other learning exercises | 入门练习 | Month 1 |
| Quadrature decode in PIO | PIO 正交解码 | Month 3–4 |
| Heartbeat watchdog | 心跳看门狗 | Month 3–4 |
| UART message format shared with the Pi | 与 Pi 约定的 UART 报文格式 | Month 3–4 |
| The assembled Stage 3 firmware | 第 3 阶段整合固件 | Month 5–7 |

## What does not live here / 不放在这里的东西

The Pi-side control code belongs to
[RoverPi](https://github.com/AndyChen227/RoverPi) and stays in Python. It is
already written and already physically verified; rewriting it in C would discard
verified work to make room for unverified work, which this project's one rule
forbids. This is also the boundary rule from the [README](../README.md): facts
about the rover live there, facts about the boards live here.

Pi 端的控制代码属于 [RoverPi](https://github.com/AndyChen227/RoverPi)，继续用
Python。它已经写好、也已经实测验证过；用 C 重写等于丢掉已验证的东西去换未验证的
东西，这是本项目铁律所禁止的。这同时也是 [README](../README.md) 里的分工规矩：
关于车的事实住在那边，关于板子的事实住在这边。

## Status / 当前状态

Empty. Nothing has been written yet.

空的，还没有写任何代码。

---

Licensed under MIT. See [`../LICENSE.md`](../LICENSE.md).
