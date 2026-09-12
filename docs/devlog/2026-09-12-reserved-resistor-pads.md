# 2026-09-12 — The Twelve Resistors That Were Specified But Never Drawn / 写在规格里、从没画进图的十二个电阻

## Result / 本次结果

Three things were found and fixed, all of them **before** any board was ordered:

1. The **12 reserved resistors were in the specification and in the BOM, but not
   on the schematic.** They cannot be added after fabrication.
2. The line saying **all twelve pads could ship empty was wrong.** Six of them
   are in the signal path, and an empty series pad is an open signal — a board
   that does nothing at all.
3. Adding them changes the design from **8 nets to 14**, which means the netlist
   verification that passed this morning is no longer verifying the right thing.

No schematic has been redrawn yet. What changed today is **the written design**,
plus a committed checker so the re-verification is reproducible.

今天发现并修掉了三件事，全都在下单打样**之前**：

1. **那 12 个预留电阻写在规格里、写在 BOM 里，但从没画进原理图。** 打样之后就加不了。
2. **"12 个焊盘都可以先不焊"这句话是错的**——其中 6 个在信号路径上，串阻焊盘空着就是
   信号断路，板子一点反应都没有。
3. 把它们加进去，设计从 **8 个网络变成 14 个**，也就是说今天上午通过的那次网表核对，
   核对的已经不是正确的对象了。

原理图还没重画。今天改的是**写下来的设计**，另外提交了一个脚本，让重新核对是可复现的。

---

## 1. How the omission happened / 遗漏是怎么发生的

The morning's devlog recorded the schematic as "electrically complete", and it
was consistent with itself: the ERC count reconciled exactly, and all eight nets
matched the signal map. **Both checks passed because both were built from the
same table** — the signal map, which lists 10 connections and 8 nets.

The 12 resistors live somewhere else: in
[the two nearly-free additions](../roadmap.md#stage-1), a separate section, one
table lower. Nothing in the netlist check knew that section existed.

So the failure mode is worth naming: **a check built from one part of the
specification cannot see what the other part of the specification asked for.**
The netlist check verified that the drawing matched the signal map. It did. The
signal map was never the whole requirement.

上午那篇日志把原理图记为"电气内容完工"，而它是**自相一致**的：ERC 的数字精确对得上，
8 个网络也和信号表逐条吻合。**两项检查都通过，是因为两项都是从同一张表建起来的**——那张
列着 10 个连接、8 个网络的信号表。

那 12 个电阻住在别的地方：在[两个几乎不花钱的增补](../roadmap.md#stage-1)里，另一个小节，
低一张表。网表核对根本不知道那一节存在。

所以这个失效模式值得起个名字：**用规格的一部分建起来的检查，看不见规格的另一部分要求了什么。**
网表核对验证的是"图和信号表一致"。它确实一致。**只是信号表从来就不是全部要求。**

---

## 2. The contradiction: an empty series pad is an open signal / 矛盾：串阻焊盘空着就是断路

The roadmap said:

> **Through-hole only as built.** The reserved 0805 pads below are pads, not
> populated parts: Rev A can ship with **all of them** empty and still be a pure
> through-hole assembly

That is true for six of the twelve and false for the other six:

| | If the pad ships empty | Result |
|---|---|---|
| **Pull-down** (driver side to `GND`) | nothing is pulling the input down | No power-on safe state. The board still works |
| **Series** (in the signal path) | the signal has **no path at all** | Six open signals. **The board does nothing** |

A pull-down is a feature that can be absent. A series resistor is a **wire** that
happens to be 33 Ω, and a wire cannot be absent.

[`bom.md`](../../hardware/stage1-signal-adapter/bom.md) had this right already —
its pull-down row said "may ship unpopulated on Rev A" and its series row did
not. The roadmap's "all of them" was the sentence that overreached, and the two
documents had been disagreeing since the day they were written.

下拉是一个**可以缺席的功能**；串阻是一根**恰好有 33 Ω 的导线**，而导线不能缺席。

BOM 那边其实本来就是对的——下拉那一行写着"Rev A 可以先不焊"，串阻那一行没写。是路线图里
"all of them"这句话说过头了，而这两份文档从写下来那天起就在互相矛盾。

### The consequence: through-hole, not 0805 / 后果：改成通孔，不是 0805

If the six series resistors must be populated, then Rev A is no longer a
pure through-hole assembly — unless the resistors themselves are through-hole.

"Rev A is a board a beginner can actually assemble" was a deliberate constraint,
not an accident, so the constraint wins and the package changes:

| | Package | Value | Populated? |
|---|---|---|---|
| `R1`–`R6`, series | **through-hole axial** | 33 Ω | **Mandatory** |
| `R7`–`R12`, pull-down | 0805 | 10 kΩ | Optional on Rev A |

Board area is not scarce on a board this size, and a 1/4 W axial resistor is far
easier to solder well than an 0805 — on the first board anyone has ever
assembled, that is worth more than the area. The cost is one more line on the
shopping list: a through-hole resistor assortment, about ¥10.

如果 6 个串阻必须焊，那 Rev A 就不再是纯通孔板——**除非电阻本身是通孔的**。

"Rev A 是一块新手真能装得起来的板"是一个有意定下的约束，不是巧合，所以约束赢，改封装：
串阻用**通孔轴向**电阻（33 Ω，必焊），下拉用 0805（10 kΩ，Rev A 可选）。这么小的板子不缺
面积，而 1/4 W 轴向电阻比 0805 好焊得多——对一个人这辈子装的第一块板来说，这比省下的面积
值钱。代价是采购清单上多一行：一盒通孔电阻，约 ¥10。

### And one claim that stopped being true / 一句不再成立的话

The planning devlog's first argument for this board was:

> **Pure copper. Not one component can burn.**

Half of that no longer holds. Six resistors are now mandatory parts on the
signal path, so the board is not component-free. Nothing on it can still burn — a
33 Ω resistor passing a GPIO's few milliamps is not a thermal event — but
**"passive" and "component-free" are two different claims, and only the first
one survives.** Recorded rather than quietly dropped, because the whole reason
that sentence was written was to justify choosing this board as the first one.

这块板最初的第一条理由是"纯铜箔，一个元件都烧不了"。**这句话现在只有一半成立**：板上有 6 个
必装元件，不再是"没有元件"；但依然没有任何东西会烧（33 Ω 上过 GPIO 那几毫安算不上热事件）。
**"被动"和"没有元件"是两个不同的说法，现在只有前一个还成立。** 记下来而不是悄悄改掉，
因为当初写那句话的全部用途就是论证"把这块板选作第一块"。

---

## 3. The net structure, and the three decisions in it / 网络结构，和里面的三个决定

A series resistor cuts each signal in two, so 8 nets become 14. The table now
lives in [the roadmap](../roadmap.md#nets) as the authority, and this is what is
in it:

| Pi-side net | J1 pin | Series R | Driver-side net | Pull-down | J2 pin | D50A silkscreen |
|---|---:|---|---|---|---:|:---:|
| `PWM1` | 32 | R1 33 Ω | `P1` | R7 10 kΩ → `GND` | 7 | `P1` |
| `INA1` | 16 | R2 33 Ω | `A1` | R8 10 kΩ → `GND` | 5 | `A1` |
| `INB1` | 18 | R3 33 Ω | `B1` | R9 10 kΩ → `GND` | 3 | `B1` |
| `PWM2` | 33 | R4 33 Ω | `P2` | R10 10 kΩ → `GND` | 8 | `P2` |
| `INA2` | 29 | R5 33 Ω | `A2` | R11 10 kΩ → `GND` | 6 | `A2` |
| `INB2` | 31 | R6 33 Ω | `B2` | R12 10 kΩ → `GND` | 4 | `B2` |
| `GND` | 34, 39 | — | — | — | 1, 2 | `G` |
| `+3V3` | 1, 17 | — | — | — | 9, 10 | `V` |

### Decision 1 — the driver-side nets are named `P1`, not `PWM1_D` / 驱动侧网络叫 `P1`，不叫 `PWM1_D`

This morning's entry argued that a net label's name should travel end to end:

```
label  →  net name  →  PCB net  →  silkscreen  →  what you read when checking
```

The series resistor creates a second net per signal, and therefore a free
choice of what to call it. Naming it after the D50A's own silkscreen finishes
the argument instead of weakening it: the Pi-side net carries the name RoverPi's
`wiring.md` uses, the driver-side net carries the name printed on the driver, and
J2's silkscreen is the driver's own name with **no translation step anywhere.**

The board's job was always to join two naming schemes. **Now the joint is a
physical part you can point at.**

串阻给每个信号造出了第二个网络，也就给了"叫它什么"一个自由选择。用 D50A 板上印的名字去命名，
是把上午那条论证**走完**而不是削弱它：Pi 侧用 RoverPi `wiring.md` 的名字，驱动侧用驱动板上
印的名字，J2 的丝印于是**全程不需要翻译**。这块板的工作本来就是把两套命名接起来——**而现在
那个接头是一个你能用手指头指得到的元件。**

### Decision 2 — the pull-down goes on the driver side / 下拉接在驱动侧

After the series resistor, not before it. Electrically the two placements are
nearly indistinguishable: the driver input is high-impedance, so no current
flows in the 33 Ω and there is no drop across it.

The reason to choose is **a failure mode.** Suppose a series resistor is
missing, badly soldered, or its joint cracks on a vehicle that vibrates:

| Pull-down location | With a broken series resistor |
|---|---|
| **Driver side** (chosen) | The driver input is **still held low.** Safe state survives |
| Pi side | The driver input **floats.** Undefined behaviour |

So the safe state does not depend on the series resistor being there — and this
matters more than it sounds, because the pull-down exists *specifically* to
cover the window where nothing else is defining that pin's level. A safety
feature that depends on another part being intact is worth less than one that
does not.

选驱动侧的理由是**失效模式**：万一某个串阻没装、虚焊，或者在会振动的车上焊点裂了，
驱动侧的下拉**仍然**把驱动输入按在低电平，安全状态活下来；下拉放 Pi 侧的话，同一个故障
会让驱动输入悬空，那是未定义行为。**安全状态因此不依赖串阻在不在**——而这比听起来要紧，
因为下拉存在的意义**恰恰**是覆盖"没有别的东西在定义这个脚的电平"的那个窗口。一个依赖
另一个零件完好的安全功能，不如一个不依赖的。

### Decision 3 — ERC should still report 30 / 0 / ERC 应该仍然是 30 / 0

The twelve resistors add 24 pins and **every one of them is connected**: each
Pi-side net has 2 pins, each driver-side net 3, `GND` grows from 4 pins to 10,
`+3V3` stays at 4, and no single-pin net is created.

So the number is written down **before** the drawing exists, which makes it a
**prediction rather than an observation.** If the report is not 30 / 0 after
drawing, something is wired wrong — it is not "the numbers moved because there
are more parts now." A number you predicted and then measured is worth
considerably more than the same number read off a screen and accepted.

12 个电阻多出 24 个引脚，而且**每一个都有连接**。所以这个数字是在图存在**之前**写下来的，
它因此是**预测而不是观察**：画完如果不是 30 / 0，那就是接错了，**不是"元件变多所以数字
就变了"**。一个先预测、再实测的数字，比一个从屏幕上读下来就接受的同样的数字值钱得多。

---

## 4. The checker is now committed / 核对脚本进仓库了

This morning's netlist comparison was done with a script that was **never
committed** — only its output was, pasted into the devlog. That makes the check
unreproducible, which for a check whose entire purpose is "do not read this by
eye" is a poor arrangement.

It now lives in
[`hardware/stage1-signal-adapter/tools/`](../../hardware/stage1-signal-adapter/tools/README.md)
with the expected net map as a JSON file beside it, and it takes an exit code so
it can gate a commit later. Standard library only; it runs on a machine that
has never had KiCad installed.

上午那次网表比对用的脚本**没有提交**，只提交了它的输出。这让检查变得不可复现——而对一项
"全部目的就是不要用眼睛读"的检查来说，这个安排很糟。现在脚本和期望网络表（JSON）一起
进了仓库，带退出码，以后可以拿来卡提交。只用标准库，没装过 KiCad 的机器上也能跑。

**Run against the schematic as it stands today, it fails** — and that is the
useful part. The output is a list of exactly what has not been drawn yet:

对着今天这版原理图跑，**它是失败的**——而这恰好是有用的地方。输出就是"还没画的东西"的清单：

```
[PASS]    +3V3 = J1-1 J1-17 J2-10 J2-9
[MISSING] A1    net does not exist in the netlist
[MISSING] A2    net does not exist in the netlist
[MISSING] B1    net does not exist in the netlist
[MISSING] B2    net does not exist in the netlist
[FAIL]    GND
            missing:  R10 R11 R12 R7 R8 R9
[FAIL]    INA1
            expected: J1-16 R2
            actual:   J1-16 J2-5
[MISSING] P1    net does not exist in the netlist
[MISSING] P2    net does not exist in the netlist
...
single-pin unconnected nets: 30   (expected 30)
RESULT: FAIL
```

**A failing check that names what is missing is a to-do list.** It stops being
one the moment the drawing is finished, and the same command prints `ALL PASS`.

**一个会失败、并且说清缺什么的检查，就是一张待办清单。** 图画完的那一刻它就不再是清单了，
同一条命令会打印 `ALL PASS`。

### One design note inside the script / 脚本里的一个设计决定

Resistors are compared **by reference, not by pad number.** A resistor is
symmetric, so which pad is pin 1 depends on how the symbol happens to be rotated
on the sheet. Requiring `R1-1` on the Pi side would check the *drawing's
orientation* rather than the circuit, and would fail a schematic that is
electrically correct — a check that cries wolf gets ignored, and then it is worse
than no check. Wiring a resistor between the wrong two nets is still caught: it
goes missing from one net and turns up in another. Connector pins *are* compared
as `REF-PIN`, because which physical pin a signal lands on is the entire point of
this board.

电阻**按编号比，不按引脚号比**：电阻对称，哪一脚是 1 号取决于符号转了多少度。要求"`R1` 的
1 脚在 Pi 侧"是在检查**画图的朝向**而不是电路，会把一个电气上完全正确的图判成失败——
**一个爱谎报的检查会被忽略，那时它比没有检查更糟。** 而"电阻接错了两个网络"仍然抓得到。
连接器引脚**是**按 `REF-PIN` 比的，因为信号落在哪个物理针上正是这块板的全部意义。

---

## 5. Two more bring-up checks fall out of this / 顺带多出两条上电检查

Adding a resistor to a signal path changes what a correct meter reading looks
like, so the exit criteria gained two items:

- **Pi-side to driver-side should now read ≈33 Ω, not 0 Ω.** Read the *value*;
  do not just listen for the continuity buzzer, which beeps at anything under
  about 50 Ω and would therefore beep identically for a correct 33 Ω resistor
  and for a solder bridge across it. 0 Ω means bridged or shorted; open means
  missing.
- **Each pull-down measured to `GND`:** ≈10 kΩ if populated, open if
  deliberately left empty. Either is acceptable. **A value that is neither is a
  fault.**

The first one is the more interesting: before today, "beeps" was a correct
answer on this board. Now it is the wrong answer, and the meter has to be read
rather than listened to.

给信号路径加一个电阻，**改变了"正确的表读数长什么样"**：

- **Pi 侧到驱动侧现在应该读到约 33 Ω，不是 0 Ω。** 要读**数值**，不要只听蜂鸣——蜂鸣档
  在 50 Ω 以下都会响，所以"正确的 33 Ω 电阻"和"电阻两端被焊锡短接"在它听来一模一样。
  读到 0 Ω 是短了，读到断路是缺件。
- **每个下拉对 `GND` 量一下：** 焊了约 10 kΩ，故意不焊则断路。两者都可以，**既不是这个
  也不是那个的读数就是故障。**

第一条更有意思：在今天之前，"响"在这块板上是正确答案；现在"响"是错的答案，**表要读，
不能只听。**

---

## Status / 当前状态

| Item | State |
|---|---|
| Written design (roadmap, README, BOM, parts list) | **Updated — 14 nets, packages settled** |
| Rev A schematic | **8 nets as drawn. Needs the 12 resistors added** |
| Netlist checker | **Committed**, expects 14 nets, currently FAIL by design |
| ERC after redraw | Predicted 30 errors / 0 warnings |
| Footprints | Not assigned, not frozen |
| PCB layout | Not started (`.kicad_pcb` is still an empty file) |
| Cables | Selected 2026-09-11, **not yet delivered** |
| D50A pin 1 | **Assumed**, recorded in three places |
| Boards fabricated | 0 |
| Board status | `[ ]` |

## Next / 下一步

1. **Draw R1–R12** per [the net structure](../roadmap.md#nets). Re-run ERC (expect
   30 / 0) and re-run the checker (expect `ALL PASS`).
2. **Re-enable the ERC check** `分配的封装不匹配封装筛选规则`, currently `ignore`
   in the project file. Verified today that turning it on will not false-alarm:
   `Conn_02x05_Odd_Even` / `Conn_02x20_Odd_Even` filter on `Connector*:*_2x??_*`,
   and the intended footprints `Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical`
   and `IDC-Header_2x20_P2.54mm_Vertical` both match.
3. **Buy the through-hole resistor assortment** along with everything else still
   outstanding on [the Stage 1 list](../tools-and-parts.md#inventory).
4. **When the cables arrive:** resolve D50A pin 1 end-to-end with a meter. Still
   the hard gate before footprints are frozen.

1. **按[网络结构](../roadmap.md#nets)画 R1–R12**，重跑 ERC（预期 30 / 0）和核对脚本（预期 `ALL PASS`）。
2. **打开那项被关掉的 ERC 检查**。今天顺手验证了打开它不会误报：两个连接器符号的筛选规则是
   `Connector*:*_2x??_*`，而准备用的两个 IDC 封装都能匹配。
3. **把通孔电阻盒和清单上其余还没买的东西一起下单。**
4. **排线到货后**：用万用表端到端确定 D50A 的 1 号脚。这仍然是锁封装前的硬闸门。
