# 2026-09-13 — The Twelve Resistors Are on the Drawing / 十二个电阻画上去了

## Result / 本次结果

Rev A's schematic is **complete**: 14 nets, ERC 30 errors / 0 warnings, and the
netlist checker reports `ALL PASS` against
[the net structure](../roadmap.md#nets).

Status remains `[ ]`. Nothing is fabricated, no footprints are assigned, and
D50A pin 1 is still an assumption waiting on a cable that has not arrived.

Rev A 的原理图**完工**：14 个网络，ERC 30 错误 / 0 警告，网表核对脚本对着
[网络结构表](../roadmap.md#nets)报 `ALL PASS`。

状态仍为 `[ ]`：没有打样，没有分配封装，D50A 的 1 号脚仍是一个等着排线到货去证实的假设。

```
[PASS]    PWM1 = J1-32 R1          [PASS]    P1   = J2-7 R1 R7
[PASS]    INA1 = J1-16 R2          [PASS]    A1   = J2-5 R2 R8
[PASS]    INB1 = J1-18 R3          [PASS]    B1   = J2-3 R3 R9
[PASS]    PWM2 = J1-33 R4          [PASS]    P2   = J2-8 R4 R10
[PASS]    INA2 = J1-29 R5          [PASS]    A2   = J2-6 R5 R11
[PASS]    INB2 = J1-31 R6          [PASS]    B2   = J2-4 R6 R12
[PASS]    +3V3 = J1-1 J1-17 J2-9 J2-10
[PASS]    GND  = J1-34 J1-39 J2-1 J2-2 R7 R8 R9 R10 R11 R12

single-pin unconnected nets: 30   (expected 30)
unexpected extra nets:        0
auto-named (unlabelled) nets: 0

RESULT: ALL PASS
```

---

## How it was drawn: six islands / 画法：六座孤岛

The twelve resistors are **not** drawn between J1 and J2. They sit in six
identical blocks in empty sheet space, each one shaped like this:

```
   PWM1 ──[ R1 · 33 ]──┬── P1
                       │
                   [ R7 · 10k ]
                       │
                      GND
```

`PWM1` and `P1` here are labels, not wires to anywhere. The same names already
exist on J1 pin 32 and J2 pin 7, and same-named labels are one net — so the
resistor lands in the middle of that net without a single line crossing the
sheet.

12 个电阻**不是**画在 J1 和 J2 中间的，而是在空白处摆了六个一样的小块。块里的 `PWM1` 和
`P1` 是标签，不通向任何地方；这两个名字在 J1 的 32 脚和 J2 的 7 脚上已经存在，**同名标签
即同一网络**，于是电阻就落进了那个网络的中间，图上一根横穿纸面的长线都不用画。

This is the same method [yesterday's entry](2026-09-12-revA-schematic-complete.md)
chose for the connectors, used a second time. What is new is what it buys here:
**the resistor is the joint between the two naming schemes**, and because the
joint is a physical part, the thing that was an argument in a document is now
something you can point at on a board.

这和[昨天那篇](2026-09-12-revA-schematic-complete.md)给连接器选的是同一个办法，只是再用了
一次。新的地方在于它在这里买到了什么：**电阻就是两套命名之间的那个接头** —— 而因为接头是
一个实体元件，昨天还是文档里一段论证的东西，现在是板子上能用手指头指到的东西。

---

## The error the checker exists for / 脚本存在的理由，出现了一次

While reviewing the six blocks, one was wrong: the block fed by `INB2` had its
driver-side label set to **`P1`** instead of `B2` — a copy that was placed and
then not renamed.

The consequence was not "one missing name". It was two faults at once:

- `P1` appeared **three times** on the sheet — J2 pin 7, the `PWM1` block, and
  this one. Three places merge into one net, so **`INB2`'s signal and `PWM1`'s
  signal would have been shorted together on the board.**
- `B2` never paired with anything. J2 pin 4 became a one-pin net, and so did
  `INB2`.

**ERC said nothing.** Every pin had a wire, every wire had a label, nothing
dangled and nothing conflicted — the report was 30 / 0 with the fault present,
exactly as it would have been without it.

复查六个块的时候发现一处错：`INB2` 那一块，驱动侧的标签是 **`P1`** 而不是 `B2`——复制之后
忘了改名。后果不是"少一个名字"，而是两件事同时发生：`P1` 在图上出现**三次**，三处并成一个
网络，等于 **`INB2` 的信号和 `PWM1` 的信号在板上短接**；而 `B2` 一次都没有配对，J2 的 4 脚
成了单引脚网络。

**ERC 一声不响。** 引脚都有线、线都有标签、没有悬空也没有冲突——**带着这个故障，报告依然是
30 / 0**，和没有故障时一模一样。

This is the failure mode
[yesterday's entry](2026-09-12-revA-schematic-complete.md) described in the
abstract, one day later, in the concrete. The prediction was that it would look
like two signals swapped onto each other's pins; what actually happened was one
signal duplicated onto another's net. Same class, same silence from ERC.

> It was caught by eye during review, not by the checker — the checker had not
> been run yet. Worth recording plainly, because the honest reading is not "the
> tool saved us." The tool would have caught it independently and that is why it
> exists; on this occasion a human got there first. **The point of the checker is
> not that it is smarter, it is that it does not get tired on the sixth block.**
>
> 这个错是复查时用眼睛看出来的，不是脚本抓到的——那时脚本还没跑。照实记下来，因为诚实的说法
> 不是"工具救了我们"。**脚本的意义不在于它更聪明，而在于它到第六个块的时候不会累。**

---

## Six warnings that were one mistake / 六条警告，其实是一个错误

ERC came back **30 errors / 0 warnings → 30 errors / 6 warnings**: six
occurrences of `未连接的连线端点`, each a vertical wire **50 mils** long with a
free end.

Six warnings, six blocks — so not six slips, but **one leftover stub in the first
block, copied five times.** That is the useful half of building by copy-paste:
mistakes are reproduced exactly, which makes them easy to recognise as
systematic and cheap to fix in one pass.

ERC 报了 **30 错误 / 6 警告**，六条都是"未连接的连线端点"，每条是一段 **50 mils** 长、有一端
悬空的竖线。六条对六个块——所以不是六次手滑，而是**第一个块里的一小段多余线头被复制了五份**。
这是复制粘贴的好处那一半：**错误也被精确复制**，因此一眼就能看出它是系统性的，改也是一次改完。

### The root cause was a setting, not a slip / 根因是一个设置，不是手滑

`50 mils` is **half** of the 100 mil grid that KiCad's symbol pins sit on. Half-
grid endpoints are exactly where "almost connected" and "half a wire left over"
come from, and on screen they look identical to the correct thing.

The reason wires were landing on half-grid was not the active grid setting. It
was **Preferences → Schematic Editor → Grid Options → Grid Overrides**, which
had:

| Override | Was | Now |
|---|---|---|
| Connected items / 已连接项 | 50 mils | **100 mils** |
| Wires / 连线 | 50 mils | **100 mils** |
| Text / 文本 | 10 mils | unchanged |

A Grid Override means *"whatever the current grid is, snap this class of thing to
this instead."* So changing the active grid to 100 mils would **not** have helped
— the wire override would have pulled it back to 50. This is worth knowing
because the symptom (a half-grid wire) points at the grid, and the grid is not
where the setting lives.

`50 mils` 正好是 KiCad 符号引脚所在的 100 mil 栅格的**一半**。半格端点正是"差一点点没接上"和
"多出半截线"的来源，而它们在屏幕上和正确的东西长得一模一样。

线会落在半格上，原因**不是**当前栅格设置，而是**偏好设置 → 原理图编辑器 → 栅格选项 →
栅格重写**里"连线"和"已连接项"两项被写死成 50 mils。栅格重写的含义是"**不管当前栅格是多少**，
这类东西一律按这个吸附"——所以**光把当前栅格改成 100 是没用的**，连线会被重写回 50。值得记下来
是因为：症状指向栅格，而那个设置并不住在栅格里。

Both overrides are now 100 mils, so wire endpoints can only land where a pin
could be. The six stubs were deleted individually — changing a setting does not
repair geometry that is already drawn.

---

## The prediction, and what it actually covered / 那个预测，以及它实际覆盖了什么

[Yesterday's entry](2026-09-12-reserved-resistor-pads.md) wrote the ERC result
down before the drawing existed: **30 errors / 0 warnings.**

The errors came back at exactly 30. The warnings did not — six appeared. The
prediction was not wrong about anything it actually reasoned over; it reasoned
over **pin connectivity** (how many pins each net has, and that no single-pin net
is created), and pin connectivity was exactly right. Dangling wire *geometry* is
a different property, and nothing in the prediction covered it.

So the refinement worth keeping is about what a prediction is for. It was still
worth writing: **because 30 was committed to in advance, the 30 coming back
carried real information**, and the 6 stood out immediately as something
unaccounted for rather than as background noise. A prediction that covers half
the report still makes that half meaningful — and it makes the uncovered half
visible as uncovered.

昨天那篇在图还不存在的时候就写下了 ERC 的预期：**30 错误 / 0 警告**。错误回来正好是 30，
警告不是——冒出来 6 条。

预测在它真正推理过的部分上没有错：它推理的是**引脚的连接关系**（每个网络几个引脚、不产生
单引脚网络），而这一部分完全正确。**悬空线头是另一种性质的东西**，预测里没有任何一句覆盖到它。

所以值得留下的修正是关于"预测是干什么用的"：它依然值得写——**正因为 30 是事先押下的，回来的
30 才携带真实信息**，而那 6 条才会立刻显得"没法解释"，而不是混在背景噪声里。**一个只覆盖了
报告一半的预测，仍然让那一半变得有意义，并且让没覆盖的另一半显形为"没覆盖"。**

---

## Reference numbering, done by hand on purpose / 编号是手工改的，有意为之

KiCad's auto-annotation produced series resistors on odd numbers and pull-downs
on even ones — `R1`/`R2` for `PWM1`, `R3`/`R4` for `INA1`, and so on. Consistent,
and not what the design says.

All twelve were re-lettered by hand to match
[the net structure](../roadmap.md#nets): **`R1`–`R6` are the series resistors,
`R7`–`R12` the pull-downs.** Grouping by function rather than by position is
worth twelve double-clicks because of one sentence in the assembly instructions:

> **`R1`–`R6` through-hole 33 Ω, must be populated. `R7`–`R12` are 0805 10 kΩ and
> may ship empty.**

Under the interleaved numbering that becomes "do not populate R2, R4, R6, R8,
R10, R12" — a list to check against, read while holding a soldering iron over a
board that will not lie flat. The same information, in a form that can be
misread. **Letting the tool's default decide the numbering would have been
letting a convenience decide a document that gets read under bad conditions.**

KiCad 自动编号编出来的是"串阻单数、下拉双数"。一致，但不是设计里写的那个。12 个全部手工改成
和[网络结构表](../roadmap.md#nets)一致：**`R1`–`R6` 是串阻，`R7`–`R12` 是下拉。**

按功能分组值这 12 次双击，理由是装配说明里的一句话：**"R1–R6 通孔 33 Ω 必焊，R7–R12 是 0805
10 kΩ 可以先不焊。"** 交叉编号的话，这句话会变成"R2、R4、R6、R8、R10、R12 不焊"——同样的信息，
但换成了一个需要对照着数的号码表，而**读它的时候你一手扶着放不平的板子、一手拿着烙铁。**
**让工具的默认值去决定编号，等于让一个方便决定了一份要在糟糕条件下被阅读的文档。**

---

## Status / 当前状态

| Item | State |
|---|---|
| Rev A schematic | **Complete — 14 nets** |
| ERC | 30 errors / 0 warnings, every one accounted for |
| Netlist check | **`ALL PASS`**, reproducible from the committed script |
| Footprints | Not assigned, not frozen |
| PCB layout | Not started (`.kicad_pcb` is still an empty file) |
| Cables | Selected 2026-09-11, **not yet delivered** |
| Headers, enclosure, resistors | **Not yet bought** |
| D50A pin 1 | **Assumed** |
| Boards fabricated | 0 |
| Board status | `[ ]` |

## Next / 下一步

Everything from here is gated on parts, not on drawing.

从这里开始，卡住的全部是实物，不是画图。

1. **Buy what is still outstanding** — the two boxed headers, the enclosure, the
   through-hole and 0805 resistor assortments. The enclosure sets the board
   outline and the headers set the connector clearance, so **no layout step can
   start until they are in hand.** About ¥40.
2. **When the cables arrive:** resolve D50A pin 1 end-to-end with a meter. Still
   the one error that shorts 3.3 V to ground.
3. **Before assigning footprints:** re-enable the ERC check
   `分配的封装不匹配封装筛选规则`, still `ignore` in the project file. Verified
   2026-09-12 that enabling it will not false-alarm on the intended footprints.
4. Then footprints, layout, DRC, Gerber — see
   [`fabrication.md`](../fabrication.md).
