# Firmware / 固件

Code that runs on the microcontrollers in this project.

本项目中运行在单片机上的代码。

## The language is not decided yet / 语言尚未决定

**Revised 2026-09-12.** An earlier version of this file said the firmware was
written in **C** against the Raspberry Pi Pico SDK, decided 2026-09-08. That
commitment has been **withdrawn** — not because C was the wrong answer, but
because it was decided from reading rather than from writing code. This directory
was empty and no Pico had been bought.

By this project's own rule, a value fixed before the measurement is a guess
wearing a footprint. So the language is now an explicit **end-of-month-1
decision, made from a measurement**: buy two ¥25 Picos, write the same `blink` in
each candidate, and pick the one that makes you want to write a second program.

**2026-09-12 修订。** 这个文件早先的版本写的是"固件用 C 编写，基于 Raspberry Pi Pico
SDK，2026-09-08 决定"。那个决定已经**撤回**——不是因为 C 是错的答案，而是因为它是读来的
判断，不是写出来的结论：当时这个目录是空的，Pico 也还没买。

按这个项目自己的规矩，测量之前定下来的数值只是一个套着封装的猜测。所以语言现在变成
**第 1 个月末、根据实测做的决定**：买两块 ¥25 的 Pico，用每个候选各写一遍同一个 `blink`，
选那个让你想写第二个程序的。

### The candidates / 候选

| Candidate | 候选 | What it gives | What it costs |
|---|---|---|---|
| **C** on the Pico SDK | 原生 Pico SDK 的 C | The language every chip datasheet's reference code is written in | CMake and the steepest toolchain of the three |
| **C++** on arduino-pico | arduino-pico 的 C++ | No CMake, `setup()`/`loop()`, one-click upload, `Serial.println()` that just works. Exposes PIO, so Stage 3 is still reachable | You still have to *read* C, because the vendor examples are C |
| **MicroPython** | MicroPython | A REPL. Change a line, see it immediately | Vendor examples must be translated by hand; high-speed work has to go through PIO |

### One fact, recorded so it is not re-argued / 记下一个事实，免得以后再争

**C++ is not the easier one.** It is a superset of C: pointers, memory layout,
fixed-width integers, bit manipulation and manual resource handling are all still
there. On a microcontroller most of what makes C++ feel convenient is
unavailable — `std::string` and `std::vector` need the heap, exceptions and RTTI
are disabled, `new`/`delete` fragment memory over a long run. So embedded C++
means learning all of C **plus** carrying a list of C++ features that must not be
used.

What is usually painful is not the language but the **toolchain**: CMake,
environment variables, dragging a `.uf2`, no REPL, a crash that presents as a
silent hang. Changing language does not fix that. Changing *framework* does — which
is what arduino-pico is doing in the table above.

**C++ 不是更简单的那个。** 它是 C 的超集：指针、内存布局、定长整数、位运算、手动管理
资源，一个都不会消失；而在单片机上，C++ 里那些让它显得好用的东西基本都用不了（`std::string`
和 `std::vector` 要堆内存，异常和 RTTI 关掉，`new`/`delete` 长期运行会内存碎片化）。所以
嵌入式 C++ 是"既要学 C 的全部，又要额外背一张不能用的清单"。

**真正折磨人的通常不是语言，是工具链**：CMake、环境变量、拖 `.uf2`、没有 REPL、崩溃表现为
静默死机。换语言解决不了，换**框架**才解决——上表里 arduino-pico 就是在换框架。

The full reasoning and the evaluation protocol are in
[the roadmap](../docs/roadmap.md#c-track).
完整理由和评估方法见[路线图](../docs/roadmap.md#c-track)。

## How much of this project actually needs firmware / 这个项目到底有多少部分需要固件

Less than it looks. **The microcontroller has exactly one irreplaceable job here:
four-channel high-speed quadrature decode** — roughly 28 000 edges/s across four
wheels at full speed, which Python drops silently.

Everything else has a no-firmware path: battery voltage through an I2C ADC
(ADS1115), current through an I2C monitor (INA226), and the heartbeat watchdog
through a retriggerable monostable or a dedicated watchdog IC — which is arguably
*better*, since a pure-hardware watchdog has no firmware that can itself hang.

See [the capability menu](../docs/roadmap.md#menu).

比看起来少。**单片机在这里只有一个真正不可替代的用途：四路高速正交解码**（满速四轮约
28000 边沿/秒，Python 会悄无声息地丢计数）。其余功能都有不写固件的路：电压用 I2C 的 ADC、
电流用 I2C 的电流监测芯片、心跳看门狗用可重触发单稳态或专用看门狗芯片——后者甚至**更好**，
因为纯硬件看门狗没有固件可以自己死机。见[功能清单](../docs/roadmap.md#menu)。

## This directory starts filling in month 1 / 这个目录从第 1 个月就开始有内容

Not at Stage 3. The firmware track runs on a breadboard Pico from the beginning,
so that by the time a board is drawn for this firmware, the firmware has already
run.

**不是等到第 3 阶段。** 固件线一开始就在面包板上的 Pico 上跑，这样等到真的为这份
固件画板子的时候，固件已经跑过了。

| Expected contents | 预期内容 | From / 时间 |
|---|---|:---:|
| `blink/` — the same program in each candidate language | 每个候选语言各写一遍的 blink | Month 1 |
| The language decision, with its reason, in a devlog entry | 语言决定及其理由，写在开发日志里 | End of month 1 |
| Other learning exercises | 其他入门练习 | Month 1–2 |
| Quadrature decode in PIO | PIO 正交解码 | Month 3–4 |
| Heartbeat watchdog | 心跳看门狗 | Month 3–4 |
| UART message format shared with the Pi | 与 Pi 约定的 UART 报文格式 | Month 3–4 |
| The assembled Stage 3 firmware | 第 3 阶段整合固件 | Month 5–7 |

Note that **Stage 1 needs none of this.** The first board is passive copper with
no microcontroller on it, so the firmware track and the hardware track do not
meet until Stage 3.

注意**第 1 阶段完全不需要这里的任何东西**：第一块板是纯铜被动板，上面没有单片机。
固件线和硬件线要到第 3 阶段才真正交汇。

## What does not live here / 不放在这里的东西

The Pi-side control code belongs to
[RoverPi](https://github.com/AndyChen227/RoverPi) and stays in Python. It is
already written and already physically verified; rewriting it would discard
verified work to make room for unverified work, which this project's one rule
forbids. This is also the boundary rule from the [README](../README.md): facts
about the rover live there, facts about the boards live here.

Pi 端的控制代码属于 [RoverPi](https://github.com/AndyChen227/RoverPi)，继续用
Python。它已经写好、也已经实测验证过；重写等于丢掉已验证的东西去换未验证的
东西，这是本项目铁律所禁止的。这同时也是 [README](../README.md) 里的分工规矩：
关于车的事实住在那边，关于板子的事实住在这边。

## Status / 当前状态

Empty. Nothing has been written yet, and no Pico has been bought yet.

空的。还没有写任何代码，Pico 也还没买。

---

Licensed under MIT. See [`../LICENSE.md`](../LICENSE.md).
