# 2026-09-12 — Plan Revision: Stage Renumbering and the Withdrawn Language Decision / 计划修订：阶段重新编号，撤回语言决定

## Result / 本次结果

Two decisions, both affecting the shape of the whole plan rather than any one
board. No hardware was built, no code was written, and no board status changed.

本次产出两个决定，影响的是整份计划的形状，而不是某一块板。没有做任何硬件，没有写任何
代码，没有任何板子的状态发生变化。

1. **The stages were renumbered.** The first board is now the passive signal
   adapter; the status indicator functions moved into Stage 2.
2. **The 2026-09-08 commitment to C was withdrawn.** The firmware language is now
   an explicit end-of-month-1 decision, made from a measurement.

一、**阶段重新编号**：第一块板改成被动信号转接板，状态指示功能并入第 2 阶段。
二、**撤回 2026-09-08 定下的 C**：固件语言改成第 1 个月末根据实测做的决定。

---

## Decision 1 — The first board is the passive adapter / 决定一：第一块板是被动转接板

### What the plan said before / 原计划

| Stage | Board |
|:---:|---|
| 1 | Status indicator HAT — LEDs, buzzer, button |
| 2 | Signal board — keyed connectors **and** encoder inputs |

### What it says now / 现在的计划

| Stage | Board |
|:---:|---|
| 1 | **Passive signal adapter** — pure copper, 7 connections, two connectors |
| 2 | **Signal & status board** — encoder inputs **+ LEDs, buzzer, button** |

### Why / 理由

The [2026-09-11 session](2026-09-11-signal-adapter-planning.md) had already
committed to designing the passive adapter first, and a KiCad project for it
already exists. So the numbering in `roadmap.md` had drifted out of step with
what was actually being built — the kind of gap that is confusing to read back in
six months.

Given that the adapter was going first anyway, the question was whether that is
the *right* order. It is, for four reasons:

1. **Pure copper. Not one component on it can burn.** It is actually a safer
   first board than the status indicator, which drives LEDs and a buzzer from Pi
   GPIO.
2. It still teaches the **entire** pipeline: schematic, footprint, layout, DRC,
   Gerber, the 嘉立创 ordering flow, soldering, bring-up, installation. That was
   the whole purpose of the original Stage 1.
3. It replaces a **real failure mode** rather than being a practice piece —
   vibration works a dupont jumper loose, and a detached direction pin is
   undefined motor behavior.
4. The fallback is **five minutes**: unplug the ribbon, put the dupont wires
   back. That satisfies the one rule directly.

Merging the status functions into Stage 2 costs almost nothing, because the
original Stage 2 specification already said "everything from Stage 1 carried
forward." Building them as two boards would have meant **fabricating the status
circuit twice.**

[2026-09-11 那次](2026-09-11-signal-adapter-planning.md)已经决定先做被动转接板，KiCad
工程也已经建好了，所以 `roadmap.md` 里的编号和实际在做的事已经脱节——这种落差半年后回头
看会让人困惑。

既然转接板反正要先做，那问题就变成"这个顺序对不对"。它是对的，四个理由：**(1)** 纯铜，
板上没有一个元件会烧，比用 Pi 的 GPIO 驱动 LED 和蜂鸣器的状态板更安全；**(2)** 它教的仍然
是完整的一条流水线（原第 1 阶段的全部目的就在这里）；**(3)** 它替换的是真实失效，不是练习品；
**(4)** 退路只要五分钟——拔排线、插回杜邦线，直接满足唯一的铁律。

把状态功能并进第 2 阶段几乎不花代价，因为原第 2 阶段的规格里本来就写着"第 1 阶段的东西
全部继承过来"；分成两块板做，等于**把状态电路打样两次**。

### The cost, stated plainly / 代价，说清楚

The main roadmap's "run without an active SSH session" milestone now waits until
**months 3–4** instead of months 1–2, because the status LEDs ship with Stage 2.
This was accepted deliberately.

主路线图里"脱离 SSH 独立运行"这个里程碑，现在要等到**第 3–4 个月**而不是第 1–2 个月，
因为状态灯跟着第 2 阶段一起出。这个代价是明知道并且接受的。

---

## Decision 2 — The language decision is withdrawn / 决定二：撤回语言决定

### What was withdrawn / 撤回了什么

On 2026-09-08 this project committed to **C** on the Raspberry Pi Pico SDK, and
wrote a long justification for it: C is the language embedded work is actually
done in, every chip datasheet's reference code is C, and it teaches what Python
and Java hide. It also argued explicitly against C++.

**That reasoning is still sound. The decision was still wrong to make.**

It was made while `firmware/` was empty and no Pico had been bought. It was a
judgment formed from *reading about* a language, not from writing a line of it.
This repository's own rule covers exactly this case:

> **Measure before you draw.** A value invented before the measurement is a guess
> wearing a footprint.

A language chosen before writing any code in it is the same thing. So the
commitment is withdrawn, and the choice becomes a **month-1 deliverable decided
from a measurement.**

2026-09-08 这个项目定下用 **C** + Pico SDK，并且写了很长的理由：C 是嵌入式实际使用的语言、
每颗芯片数据手册的参考代码都是 C、它教的正是 Python 和 Java 藏起来的东西，还明确论证了
为什么不选 C++。

**那些理由现在依然成立。但那个决定本身当时就不该下。** 它是在 `firmware/` 还空着、Pico 还
没买的时候下的——是"读关于一门语言的材料"形成的判断，不是写过一行它的代码得出的结论。
这个仓库自己的规矩正好覆盖这种情况：**先测量，再画图；测量之前定下来的数值，只是一个套着
封装的猜测。** 在写一行代码之前选定的语言，是同一件事。所以决定撤回，选择变成**第 1 个月
根据实测得出的产出**。

### The trigger / 触发它的事

Andy said he would rather use C++, because "C is too hard and a lot of it looks
like too much trouble." That is a legitimate report about his own experience and
it is recorded here as-is — but the technical claim behind it needed correcting,
and the correction is now written into
[`roadmap.md`](../roadmap.md#c-track) and
[`firmware/README.md`](../../firmware/README.md) so it does not have to be argued
again:

**C++ is not the easier one.** It is a superset of C. Pointers, memory layout,
fixed-width integers, bit manipulation and manual resource handling are all still
there, and on a microcontroller most of what makes C++ feel convenient is
unavailable — `std::string` and `std::vector` need the heap, exceptions and RTTI
are disabled, `new`/`delete` fragment memory over a long run. Embedded C++ means
learning all of C **plus** carrying a list of C++ features that must not be used.

**What is usually painful is the toolchain, not the language:** CMake,
`pico_sdk_import.cmake`, environment variables, dragging a `.uf2`, no REPL, a
crash that presents as a silent hang, `printf` needing `stdio_init_all()` first.
Changing language does not fix any of that. Changing **framework** does.

Andy 说他想用 C++，因为"C 语言太难了，很多东西看起来太麻烦"。这是他关于自己体验的真实
反馈，原样记在这里——但它背后的技术判断需要纠正，而纠正已经写进
[`roadmap.md`](../roadmap.md#c-track) 和 [`firmware/README.md`](../../firmware/README.md)，
免得以后再争一遍：

**C++ 不是更简单的那个**，它是 C 的超集；C 里麻烦的东西一个都不会消失，而 C++ 里好用的
东西在单片机上基本用不了。所以嵌入式 C++ 是"既要学 C 的全部，又要额外背一张不能用的清单"。
**真正折磨人的通常是工具链，不是语言**——换语言解决不了，换**框架**才解决。

### How it will be decided / 怎么定

Buy two Picos (¥50 total), write the same `blink` in each candidate, and judge by
one criterion:

> **After finishing blink, which one makes you want to write a second program?**

That is the only measurement that predicts whether the Stage 3 firmware actually
gets finished.

| Candidate | Verdict expected to hinge on |
|---|---|
| C on the Pico SDK | Whether CMake and the toolchain are tolerable |
| C++ on arduino-pico | Whether losing the raw SDK matters — it exposes PIO, so Stage 3 stays reachable |
| MicroPython | Whether having a REPL outweighs translating every vendor example by hand |

买两块 Pico（共 ¥50），用每个候选各写一遍同一个 `blink`，判据只有一条：**写完 blink 之后，
哪一个让你想写第二个程序。** 这是唯一能预测第 3 阶段固件会不会真的做完的测量。

### Why this matters less than it feels like it does / 为什么它没那么关键

While working through the capability list, one thing became clear and is now
recorded as [the capability menu](../roadmap.md#menu):

**The microcontroller has exactly one irreplaceable job in this project:
four-channel high-speed quadrature decode** (~28 000 edges/s across four wheels
at full speed, which Python drops silently). Everything else has a no-firmware
path:

| Function | No-firmware implementation |
|---|---|
| Battery voltage | ADS1115 — I2C 16-bit ADC, read from the existing Python |
| Current sensing | INA226 / INA219 — I2C current and power monitor |
| E-stop | A switch in the driver enable path |
| **Heartbeat watchdog** | Retriggerable monostable (CD4538) or a watchdog IC (TPS3813 / MAX6369) — **arguably better than firmware, because pure hardware has no firmware that can itself hang** |
| IMU, bumpers, cliff, ultrasonic | I2C modules and plain switches |

Two consequences: **Tier A and most of Tier B are reachable without writing a
single line of firmware**, and the language decision therefore governs one board
that is still months away.

在整理功能清单的过程中有一件事变清楚了，现在记在[功能清单](../roadmap.md#menu)里：
**单片机在这个项目里只有一个真正不可替代的用途——四路高速正交解码。** 其余功能都有不写
固件的路，其中**心跳看门狗用纯硬件反而更好**，因为纯硬件没有固件可以自己死机。两个结论：
A 档和 B 档的大半可以在一行固件都不写的情况下拿到手；语言这个决定只管一块板，而那块板
还有几个月才到。

---

## Also recorded today / 今天还记下的

### The mechanical constraint is now a stated rule / 机械约束升级成明文规矩

The 2026-09-11 session established that the Pi 5's active cooler makes stacking
impossible. That fact was sitting in one devlog entry while `roadmap.md` still
described Stage 1 and Stage 2 as **HATs**. It is now a named section,
[the mechanical constraint](../roadmap.md#mechanical), and every board in the plan
has been restated as a separate board in its own enclosure, ribbon-connected.

2026-09-11 已经确认主动散热器让叠板不可行，但这个事实只待在一篇开发日志里，而
`roadmap.md` 里第 1、2 阶段还写着 **HAT**。现在它变成了一个专门的小节
[机械约束](../roadmap.md#mechanical)，计划里每一块板都改成"装在自己外壳里、用排线连接的
独立板"。

### Two nearly-free additions proposed for Rev A / 给 Rev A 提的两个几乎不花钱的增补

Neither is decided yet. Both cost nothing now and cannot be added after
fabrication.

| Addition | Reasoning |
|---|---|
| **Connect both of the D50A's GND positions** | The D50A header has two GND pins; Rev A's plan connects one. That makes a single IDC contact the only return path for all six signals. If it opens, return current finds a path through the signal pins — the same class of failure this board exists to remove. The second pin already exists, so using it costs nothing |
| **Reserve pads for 6 pull-downs + 6 series resistors, unpopulated on Rev A** | Pull-downs hold the driver inputs low while Pi GPIO is high-impedance, so the window between Pi power-on and the Python starting means *stopped* instead of undefined. **No Python can close that window, because the Python is not running yet.** Reserving pads is free; adding them later costs a fabrication run |

两个都还没定。**(1) 两个 GND 都接**——D50A 有两个 GND 脚，只接一个意味着六路信号的全部回流
走一个 IDC 触点，它一旦开路，回流会去找信号脚当返回路径，而这正是这块板存在的目的要消除的
那一类失效；第二个脚本来就在，用它不花钱。**(2) 留 6 个下拉 + 6 个串阻焊盘，Rev A 可以不焊**
——下拉电阻让 Pi 上电到 Python 启动之间那段窗口默认为"停"而不是"未定义"，**任何 Python 都
关不掉这个窗口，因为那时候 Python 还没跑**；留焊盘免费，以后想加就得重新打样。

### Repository housekeeping / 仓库整理

- The KiCad project moved from the repository root into
  `hardware/stage1-signal-adapter/kicad/`, per the convention in
  [`hardware/README.md`](../../hardware/README.md). Its `.history/` folder moved
  with it and nothing was deleted.
- `.history/` (VS Code Local History — it snapshots every save, including
  `.kicad_sch`) added to `.gitignore`.
- `hardware/stage1-signal-adapter/README.md` and `bom.md` created.
- The two Picos and the breadboard added to
  [`tools-and-parts.md`](../tools-and-parts.md).

KiCad 工程从仓库根目录移到 `hardware/stage1-signal-adapter/kicad/`，`.history/` 一起搬过去，
没有删任何东西；`.history/` 加进 `.gitignore`；建立板子的 README 和 BOM；两块 Pico 和面包板
记进工具零件表。

---

## Status after this session / 本次之后的状态

| Item | State |
|---|---|
| Stage 1 Rev A schematic | Two connectors placed; nets not yet drawn |
| Cables | Selected 2026-09-11, **not yet delivered** |
| Footprints | **Not frozen** — waiting on the cable checks |
| Boards fabricated | 0 |
| Boards on the rover | 0 |
| Firmware language | **Undecided**, by design. Decision due end of month 1 |
| Picos | Not yet purchased |

## Next steps / 下一步

1. Draw and label the seven connections in the Rev A schematic; run ERC; **manually compare every net against the signal map**, one by one.
2. Decide the two Rev A additions above (both GNDs, and the reserved resistor pads).
3. While the cables are in transit, take [Stage 2's three gating measurements](../roadmap.md) — **encoder output level (a safety gate: Pi 5 GPIO is not 5 V tolerant)**, encoder PPR, and the driver's logic thresholds. None of them needs a new board.
4. Buy two Picos and a breadboard; write `blink` in each candidate language.
5. When the cables arrive, run the arrival checks, then freeze footprints and start layout.

1. 画完并标注 Rev A 的七个连接，跑 ERC，**逐条网络和信号表人工核对**。
2. 定上面两个 Rev A 增补（两个 GND、预留电阻焊盘）。
3. 排线在路上的这段时间，把[第 2 阶段那三个前置测量](../roadmap.md)做掉——**编码器输出电平（这是安全闸门：Pi 5 GPIO 不耐 5 V）**、编码器 PPR、驱动的逻辑阈值。这三项都不需要任何新板子。
4. 买两块 Pico 和面包板，用每个候选语言写一遍 `blink`。
5. 排线到货后做到货检查，然后锁封装、开始布局。
