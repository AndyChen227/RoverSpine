# 2026-09-12 — Rev A Schematic Complete and Netlist-Verified / Rev A 原理图完工并通过网表核对

## Result / 本次结果

Rev A's schematic is **electrically complete**: 10 connections forming 8 nets,
drawn and then **verified mechanically** against the signal map rather than by
eye.

Status remains `[ ]`. Nothing has been fabricated, no footprints have been
assigned, and one design input is still an assumption rather than a measurement.

Rev A 的原理图**电气内容完工**：10 个连接、8 个网络，画完之后**用机器**而不是用眼睛与信号表
核对过。

状态仍为 `[ ]`。没有打样，没有分配封装，而且有一个设计输入目前还是假设而不是实测。

---

## Method: labels, not wires / 方法：用标签，不拉线

Every connection is made with a **net label** on a short wire stub, not by
drawing a wire across the sheet. Same-named labels are one net.

The reason is not tidiness. It is that **the label's name propagates**:

```
label  →  net name  →  PCB net  →  silkscreen  →  what you read when checking
```

For a board whose entire purpose is that every connector is labelled, making that
one string travel end to end means checking is *reading the same string*, never
translating between two naming schemes. Every translation is a chance to be
wrong.

每个连接都是**一小段线 + 一个网络标签**，不是横穿图纸拉线。同名标签即同一网络。

理由不是整洁，而是**标签的名字会一路传下去**：标签 → 网络名 → PCB 网络 → **丝印** →
你核对时读的字。对一块"存在意义就是每个接口都有标注"的板子来说，让这一个字符串贯穿到底，
意味着核对就是**读同一个字符串**，而不是在两套命名之间做翻译。**每一次翻译都是一次出错的机会。**

`GND` and `+3V3` use **power symbols**, not text labels. Electrically either
works, but the power symbol carries the "power driven" flag that ERC's power
check needs, and it is visually distinct from a signal. Habit formed now, so that
Stage 2's regulator and LEDs do not produce a false alarm that looks like a
wiring fault.

`GND` 和 `+3V3` 用的是**电源符号**，不是文字标签。电气上两者都通，但电源符号带着 ERC 电源
检查需要的"已被驱动"标记，而且在视觉上和信号明显区分。现在养成习惯，是为了第 2 阶段上了稳压
模块和 LED 之后，ERC 不会报出一个**看起来像接线错误的假故障**。

---

## What was drawn / 画了什么

### J1 — Raspberry Pi, 2×20

| Pi pin | What | Pi pin | What |
|---:|---|---:|---|
| 1 | `+3V3` power symbol + `PWR_FLAG` | 31 | `INB2` |
| 16 | `INA1` | 32 | `PWM1` |
| 17 | `+3V3` power symbol | 33 | `PWM2` |
| 18 | `INB1` | 34 | `GND` power symbol |
| 29 | `INA2` | 39 | `GND` power symbol + `PWR_FLAG` |

### J2 — D50A control header, 2×5

| J2 pin | D50A silkscreen | Net |
|:---:|:---:|---|
| 1 | `G` (Channel 1 row) | `GND` |
| 2 | `G` (Channel 2 row) | `GND` |
| 3 | `B1` | `INB1` |
| 4 | `B2` | `INB2` |
| 5 | `A1` | `INA1` |
| 6 | `A2` | `INA2` |
| 7 | `P1` | `PWM1` |
| 8 | `P2` | `PWM2` |
| 9 | `V` (Channel 1 row) | `+3V3` |
| 10 | `V` (Channel 2 row) | `+3V3` |

Two `GND` pins and two `+3V3` pins are each **one net**, connected at both pins
anyway: the pins already exist, the redundant contact costs nothing, and it
removes the case where a single IDC contact is the only path for an entire rail.

`GND` 和 `+3V3` 各只是一个网络，但两个脚都接——针本来就在，冗余触点不花钱，而且消除了
"一整条电源全靠一个 IDC 触点"这种情况。

One `PWR_FLAG` per rail, not per symbol. The check is **per net**, so one
declaration covers every access point on it.

每条电源一个 `PWR_FLAG`，不是每个符号一个。ERC 的这项检查是**按网络**做的，所以一个声明
就覆盖该网络上的所有接入点。

---

## ERC: 30 errors, 0 warnings / ERC：30 错误，0 警告

Both numbers reconcile exactly, which is the point of watching them:

```
30 errors  = J1's 40 pins minus the 10 used   →  30 unconnected
           + J2's 10 pins, all used            →   0
 0 warnings = all 6 signal nets now have two pins each
```

**Not one violation is unaccounted for.** "Unconnected pin" on a connector is
expected behaviour, not a defect, and is deliberately not suppressed with
no-connect flags — 30 expected warnings read more honestly than a clean report
achieved by hiding them.

两个数字都能精确对上，这正是盯着它们的意义。**没有一条违规是"不知道哪来的"。** 连接器上的
"引脚未连接"是预期行为不是缺陷，所以**故意没有**用未连接标记去消除它——30 条能解释清楚的
警告，比靠隐藏得到的干净报告更诚实。

### The error that was worth having / 那条值得出现的错误

Partway through, the count was **43** when 42 was expected. The extra one was:

> `输入电源引脚没有被任何输出电源引脚驱动` — `#PWR01 pin 1 [power input]`

ERC was **correct**: there is genuinely no power source on this schematic. The
3.3 V and ground arrive from the Pi through a ribbon cable, and this board has
not one active component. The fix is a `PWR_FLAG`, which declares *"this rail is
supplied from outside this sheet."*

That statement is **true here**, which is what makes placing the flag legitimate
rather than a way to silence a complaint. Recorded because the temptation will
return: at Stage 4 there **is** a real regulator on the board, and a power ERC
error there would be a genuine fault. `PWR_FLAG` is a declaration, never a mute
button.

中途计数是 **43**，而预期是 42。多出来那一条是"输入电源引脚没有被任何输出电源引脚驱动"。

**ERC 说的是对的**：这张图上真的没有电源。3.3 V 和地是通过排线从树莓派那边来的，这块板上
一个有源元件都没有。修法是放一个 `PWR_FLAG`，它声明的是"**这条电源来自本图之外**"。

**这句话在这里是事实**，所以放它是正当的，而不是在给报警消音。记下来是因为这个诱惑还会回来：
第 4 阶段那块板上**真的有**稳压器，那时候的电源 ERC 报错就是真故障。**`PWR_FLAG` 是一句声明，
永远不是静音键。**

---

## The lesson of the day: ERC cannot catch a swap / 今天的教训：ERC 抓不出对调

This is the reason the netlist was exported and compared, and it is worth stating
plainly because "ERC passes" feels like it should be enough.

Suppose `PWM1` had been placed on J2 pin 8 and `PWM2` on J2 pin 7 — the two
labels swapped. Then:

- `PWM1` still connects exactly two pins ✅
- `PWM2` still connects exactly two pins ✅
- **ERC still reports 30 / 0** ✅

The board would be fabricated, assembled, installed, and the left and right
motors' speed control would be reversed — with ERC silent from start to finish.

**ERC checks structure, not intent.** It verifies that nothing dangles, nothing
conflicts, and every power rail has a driver. It has no idea that GPIO12 was
supposed to reach `P1`.

假设 `PWM1` 贴到了 J2 的 8 号脚、`PWM2` 贴到 7 号脚——两个标签对调。那么两个网络**各自
仍然连着 2 个引脚**，**ERC 依然报 30 / 0**。板子会被打样、焊好、装车，然后左右电机的调速
是反的，而 ERC 从头到尾一声不响。

**ERC 检查的是结构，不是意图。** 它验证没有悬空、没有冲突、每条电源都有驱动源；它不知道
GPIO12 本该到 `P1`。

This is exactly what the repository's own rule already demanded, and now it is
clear *why*:

> **Every net manually compared against the signal map, one by one.**

---

## The netlist check / 网表核对

**Method:** export the netlist from KiCad (`File → Export → Netlist`), parse it,
and compare each net's membership against the signal map in
[`roadmap.md`](../roadmap.md) — a string comparison, not a reading.

**方法：** 从 KiCad 导出网表，脚本解析，把每个网络的成员与[路线图](../roadmap.md)里那张
信号表做**字符串比对**，而不是看一遍。

```
[PASS] GND   = J1-34  J1-39  J2-1  J2-2
[PASS] +3V3  = J1-1   J1-17  J2-9  J2-10
[PASS] PWM1  = J1-32  J2-7
[PASS] PWM2  = J1-33  J2-8
[PASS] INA1  = J1-16  J2-5
[PASS] INB1  = J1-18  J2-3
[PASS] INA2  = J1-29  J2-6
[PASS] INB2  = J1-31  J2-4

single-pin unconnected nets: 30   (expected 30)
unexpected extra nets:        0
RESULT: ALL PASS
```

Not one member missing, extra, or misplaced.

**One detail worth knowing:** in the netlist the six signal nets appear as
`/PWM1`, `/INA1`, … with a leading slash — **local labels carry the sheet path**,
while power symbols (`GND`, `+3V3`) are global and carry none. Irrelevant on a
single-sheet design; it will matter as soon as there are multiple sheets.

**一个值得知道的细节：** 网表里六个信号网络的名字是 `/PWM1` 这种带前导斜杠的——**局部标签
带图页路径**，而电源符号是全局网络，不带。单页设计里无所谓，一旦有多页就会遇上。

> The netlist file itself is **not committed.** It is a generated artifact,
> reproducible from the schematic at any time, and `*.net` is gitignored. What is
> committed is the schematic it came from and this record of the comparison.
>
> 网表文件**不提交**。它是生成物，随时能从原理图重新导出，`*.net` 已在 gitignore 里。
> 提交的是它的来源（原理图）和这份核对记录。

---

## The one assumption that remains / 剩下的那一个假设

**J2's pin numbering rests on "square pad = pin 1".**

What *is* measured: the square pad on the board's underside was traced with a
meter to the same hole as the front-side `G` in the Channel 1 row, and that pin
was confirmed continuous with the motor-power negative `P-`. So pin 1 is a
ground pin, and numbering runs from the `G` end toward the `V` end.

What is **not** measured: that the square pad really is pin 1. It is a very
common PCB convention, not a standard.

**已实测的部分：** 背面那个方形焊盘用万用表追到了与正面 Channel 1 排的 `G` 同一个孔，并且
该脚与电机电源负极 `P-` 导通。所以 1 号脚是地，编号从 `G` 端向 `V` 端递增。

**未实测的部分：** 方形焊盘是否真的就是 1 号脚。那是一个**很常见的 PCB 约定，不是标准**。

### Why this one matters more than it looks / 为什么它比看起来要紧

The header's two ends are `V` and `G`. Reversing the numbering maps
1↔10, 2↔9, 3↔8, 4↔7, 5↔6 — which puts **the Pi's 3.3 V onto the driver's `G`
pin**. That is not "the wrong motor turns"; it is a **short from the Pi's 3.3 V
rail to ground.**

The two possible errors are not equally severe, and it is worth keeping them
separate:

| Error | Consequence | Caught when |
|---|---|---|
| **Wrong end** (`G` ↔ `V`) | **3.3 V shorted to ground** | At power-on, destructively |
| **Wrong row** (odd ↔ even) | Channels 1 and 2 swap — left and right motors reversed | Wheels-lifted movement tests, harmlessly |

The dangerous one is the one that was measured. The remaining row question was
resolved from the silkscreen and, if wrong, shows up in the seven previously
verified movement tests — which are done with the wheels off the ground anyway.

排针两端是 `V` 和 `G`。编号反过来会把 **Pi 的 3.3 V 接到驱动板的 `G` 脚上**——那不是
"转错轮子"，那是**Pi 的 3.3 V 直接短路到地**。

两类错误的严重程度完全不同：**端搞反**会短路、上电就出事；**排搞反**只是左右电机对调，
在架空轮子的动作测试里无害地暴露。**危险的那一类已经用万用表实测锁死了。**

### Recorded in three places, deliberately / 有意记在三处

1. **On the schematic itself**, as a text annotation next to J2.
2. In [the roadmap's Stage 1 gating checks](../roadmap.md#stage-1), as a hard gate before footprints are frozen.
3. In [the arrival checks](../tools-and-parts.md#arrival), as something to do the day the cables land.

Point 1 is the one that took a deliberate decision. A future reader — including
its author in three months — opens **the drawing**, not the devlog. **An
assumption has to live next to the thing it affects.**

第 1 条是一个有意的决定。以后打开这个工程的人（包括三个月后的作者本人）看到的是**图**，
不是开发日志。**假设必须住在它影响的那个东西旁边。**

---

## Housekeeping / 顺手整理

- `hardware/README.md`'s board index still described this board as a "Passive **7**-signal adapter" — a leftover the earlier batch correction missed, because the search terms covered "7 dupont" and "7 direct copper" but not "7-signal". Now 10 connections / 8 nets.
- `.gitignore` now ignores `_restore_backup_*/`, the folder KiCad writes when recovering a file.
- Reviewed what the `kicad/` folder holds: the schematic, project and (still empty) PCB files are committed; the `.kicad_prl` UI state, the `.net` netlist, KiCad's lock files and the editor's `.history/` snapshots are all generated or per-user, all gitignored, and all reproducible.

`hardware/README.md` 的板子索引还写着 "7-signal adapter"，是之前批量更正时漏掉的写法（搜索词
覆盖了 "7 dupont" 和 "7 direct copper"，没覆盖 "7-signal"）；`.gitignore` 加入 KiCad 的恢复
备份目录；并清点了 `kicad/` 目录里哪些该提交、哪些是可再生的本地产物。

---

## Status / 当前状态

| Item | State |
|---|---|
| Rev A schematic, electrical content | **Complete and netlist-verified** |
| ERC | 30 errors / 0 warnings, every one accounted for |
| Footprints | **Not assigned, not frozen** |
| PCB layout | Not started (`.kicad_pcb` is an empty file) |
| Cables | Selected 2026-09-11, **not yet delivered** |
| D50A pin 1 | **Assumed**, recorded as such in three places |
| Boards fabricated | 0 |
| Board status | `[ ]` |

## Next / 下一步

1. **When the cables arrive:** resolve D50A pin 1 end-to-end with a meter. Both ends are keyed, so only one orientation is possible — plug it on and find which conductor reaches each signal. This is a gate, not a nicety.
2. **Before assigning footprints:** re-enable the ERC check `分配的封装不匹配封装筛选规则` (assigned footprint does not match footprint filters), currently one of the four disabled tests. It catches exactly the fatal class of mistake available here — fitting a 2×20 symbol with a wrong-pitch or wrong-pin-count footprint.
3. Assign footprints — `DC3-40P` at J1, `DC3-10P` at J2 — then layout, then DRC.
4. Gerber export and ordering, per [`fabrication.md`](../fabrication.md).

1. **排线到货后**：用万用表端到端确定 D50A 的 1 号脚。两端都防呆，只有一种插法——插上去逐根量导通。这是闸门，不是可选项。
2. **分配封装之前**：把 ERC 里那项被关掉的"**分配的封装不匹配封装筛选规则**"打开。它拦的正是这里最致命的一类错误——给 2×20 的符号配了错间距或错引脚数的封装。
3. 分配封装（J1 用 `DC3-40P`，J2 用 `DC3-10P`）→ 布局 → DRC。
4. 按 [`fabrication.md`](../fabrication.md) 导 Gerber、下单。
