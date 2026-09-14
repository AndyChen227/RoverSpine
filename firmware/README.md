# Firmware

Code that runs on the microcontrollers in this project.

## The language is not decided yet

It is an **end-of-month-1 decision, made from a measurement**: buy two ¥25 Picos,
write the same `blink` in each candidate, and pick the one that makes you want to
write a second program.

| Candidate | What it gives | What it costs |
|---|---|---|
| **C** on the Pico SDK | The language every chip datasheet's reference code is written in | CMake, and the steepest toolchain of the three |
| **C++** on arduino-pico | No CMake, `setup()`/`loop()`, one-click upload, `Serial.println()` that works. Exposes PIO, so Stage 3 is still reachable | You still have to *read* C — the vendor examples are C |
| **MicroPython** | A REPL. Change a line, see it immediately | Vendor examples must be translated by hand; high-speed work goes through PIO |

**C++ is not the easier one.** It is a superset of C: pointers, memory layout,
fixed-width integers, bit manipulation and manual resource handling are all still
there. On a microcontroller most of what makes C++ convenient is unavailable —
`std::string` and `std::vector` need the heap, exceptions and RTTI are disabled,
`new`/`delete` fragment memory over a long run. Embedded C++ means learning all of
C **plus** a list of C++ features that must not be used.

What is usually painful is the **toolchain**, not the language: CMake,
environment variables, dragging a `.uf2`, no REPL, a crash that presents as a
silent hang. Changing language does not fix that; changing *framework* does.

The evaluation protocol is in [the roadmap](../docs/roadmap.md#lang-eval).

## How much of this project needs firmware

**The microcontroller has exactly one irreplaceable job here: four-channel
high-speed quadrature decode** — roughly 28 000 edges/s across four wheels at
full speed, which Python drops silently.

Everything else has a no-firmware path: battery voltage through an I2C ADC
(ADS1115), current through an I2C monitor (INA226), and the heartbeat watchdog
through a retriggerable monostable or a dedicated watchdog IC — the last is
preferable, since a pure-hardware watchdog has no firmware that can itself hang.

## This directory starts filling in month 1

Not at Stage 3. The firmware track runs on a breadboard Pico from the beginning,
so by the time a board is drawn for this firmware, the firmware has already run.

| Expected contents | From |
|---|:---:|
| `blink/` — the same program in each candidate language | Month 1 |
| The language decision, with its reason, in a devlog entry | End of month 1 |
| Other learning exercises | Month 1–2 |
| Quadrature decode in PIO | Month 3–4 |
| Heartbeat watchdog | Month 3–4 |
| UART message format shared with the Pi | Month 3–4 |
| The assembled Stage 3 firmware | Month 5–7 |

**Stage 1 needs none of this.** The first board is passive with no
microcontroller on it, so the firmware track and the hardware track do not meet
until Stage 3.

## What does not live here

The Pi-side control code belongs to
[RoverPi](https://github.com/AndyChen227/RoverPi) and stays in Python. It is
already written and already physically verified; rewriting it would discard
verified work for unverified work, which this project's one rule forbids. Facts
about the rover live there; facts about the boards live here.

## Status

Empty. Nothing has been written yet, and no Pico has been bought yet.

---

# 固件 / 中文

本项目中运行在单片机上的代码。

## 语言尚未决定

它是**第 1 个月末、根据实测做的决定**：买两块 ¥25 的 Pico，用每个候选各写一遍同一个
`blink`，选那个让你想写第二个程序的。

| 候选 | 给你什么 | 代价 |
|---|---|---|
| **C**，原生 Pico SDK | 芯片手册的参考代码都是用它写的 | CMake，三者里工具链最陡 |
| **C++**，arduino-pico | 不用 CMake，`setup()`/`loop()`，一键烧录，`Serial.println()` 直接能用。开放 PIO，第 3 阶段仍然够得着 | 你仍然得**能读** C——厂家例程都是 C |
| **MicroPython** | 有 REPL，改一行立刻看到结果 | 厂家例程要手工翻译；高速部分仍要走 PIO |

**C++ 不是更简单的那个。** 它是 C 的超集：指针、内存布局、定长整数、位运算、手动管理资源，
一个都不会消失。而在单片机上，C++ 里那些让它显得好用的东西基本都用不了——`std::string`
和 `std::vector` 要堆内存，异常和 RTTI 关掉，`new`/`delete` 长期运行会内存碎片化。
嵌入式 C++ 是"既要学 C 的全部，又要额外背一张不能用的清单"。

**真正折磨人的通常不是语言，是工具链**：CMake、环境变量、拖 `.uf2`、没有 REPL、
崩溃表现为静默死机。换语言解决不了，换**框架**才解决。

评估方法见[路线图](../docs/roadmap.md#lang-eval)。

## 这个项目到底有多少部分需要固件

**单片机在这里只有一个真正不可替代的用途：四路高速正交解码**——满速四轮约 28000 边沿/秒，
Python 会悄无声息地丢计数。

其余功能都有不写固件的路：电压用 I2C 的 ADC（ADS1115）、电流用 I2C 的电流监测芯片
（INA226）、心跳看门狗用可重触发单稳态或专用看门狗芯片——最后这个更可取，因为纯硬件看门狗
没有固件可以自己死机。

## 这个目录从第 1 个月就开始有内容

不是等到第 3 阶段。固件线一开始就在面包板上的 Pico 上跑，这样等到真的为这份固件画板子的
时候，固件已经跑过了。

| 预期内容 | 时间 |
|---|:---:|
| `blink/`——每个候选语言各写一遍 | 第 1 个月 |
| 语言决定及其理由，写在开发日志里 | 第 1 个月末 |
| 其他入门练习 | 第 1–2 个月 |
| PIO 正交解码 | 第 3–4 个月 |
| 心跳看门狗 | 第 3–4 个月 |
| 与 Pi 约定的 UART 报文格式 | 第 3–4 个月 |
| 第 3 阶段整合固件 | 第 5–7 个月 |

**第 1 阶段完全不需要这里的任何东西**：第一块板是被动板，上面没有单片机。固件线和硬件线
要到第 3 阶段才交汇。

## 不放在这里的东西

Pi 端的控制代码属于 [RoverPi](https://github.com/AndyChen227/RoverPi)，继续用 Python。
它已经写好、也已经实测验证过；重写等于丢掉已验证的东西去换未验证的东西，这是本项目铁律
所禁止的。关于车的事实住在那边，关于板子的事实住在这边。

## 当前状态

空的。还没有写任何代码，Pico 也还没买。

---

Licensed under MIT. See [`../LICENSE.md`](../LICENSE.md).
