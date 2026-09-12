# Netlist check / 网表核对

One script, and the table it compares against.

一个脚本，加上它用来比对的那张表。

## Why / 为什么有这个东西

**ERC checks structure, not intent.** Suppose `PWM1` and `PWM2` were placed on
each other's connector pins. Then each net still connects exactly two pins,
nothing dangles, nothing conflicts — **ERC reports no violation at all**, the
board gets fabricated, and the left and right motors' speed control is reversed.

The fix is to compare every net's membership against a written-down map. Doing
that by reading the schematic is how the error gets in; doing it as a **string
comparison** is how it gets caught. That was done by hand on 2026-09-12 and the
output was pasted into
[the devlog](../../../docs/devlog/2026-09-12-revA-schematic-complete.md) — but
the script itself was never committed, so the check was not reproducible. This
directory fixes that.

**ERC 检查的是结构，不是意图。** 假设 `PWM1` 和 `PWM2` 贴到了对方的连接器引脚上：两个网络
各自仍然连着 2 个引脚，没有悬空、没有冲突，**ERC 一声不响**，板子照样打样出来，然后左右
电机的调速是反的。

办法是把每个网络的成员与一张写下来的表逐条比对。**用眼睛读原理图正是错误进来的途径，
做成字符串比对才是抓住它的途径。** 2026-09-12 手工做过一次，输出贴进了开发日志，但脚本
本身没有提交，所以那次核对是不可复现的。这个目录解决的就是这件事。

## Usage / 用法

Export the netlist from KiCad (`File → Export → Netlist`, KiCad XML/S-expression
format), then:

从 KiCad 导出网表（`文件 → 导出 → 网表`），然后：

```bash
cd hardware/stage1-signal-adapter/tools
python check_nets.py ../kicad/RoverSpine_Signal_Adapter_RevA.net revA_expected_nets.json
```

Exit status is 0 on `ALL PASS` and 1 otherwise. Standard library only — no
KiCad installation and no packages needed, so it also runs on a machine that has
never had KiCad on it.

`ALL PASS` 时返回 0，否则返回 1。只用标准库，不需要装 KiCad 也不需要装任何包。

> [!NOTE]
> **The netlist itself is not committed** — `*.net` is gitignored. It is a
> generated artifact, reproducible from the schematic at any time. What is
> committed is the schematic it comes from, the expected map, and the script.
>
> **网表本身不提交**（`*.net` 已在 gitignore 里）：它是生成物，随时能从原理图重新导出。
> 提交的是它的来源（原理图）、期望表和脚本。

## As of now it fails, on purpose / 现在它是"应该失败"的

`revA_expected_nets.json` describes the **14-net** design from
[the net structure](../../../docs/roadmap.md#nets). The schematic currently on
disk is the earlier **8-net** version, drawn before the twelve reserved
resistors were noticed to be missing from it.

So running the script today prints a list of exactly what has not been drawn
yet — six missing series resistors, six missing pull-downs, six driver-side nets
that do not exist. **That list is the drawing checklist.** When the schematic is
finished, the same command prints `ALL PASS` and nothing had to be read by eye.

`revA_expected_nets.json` 描述的是[网络结构](../../../docs/roadmap.md#nets)里那个 **14 网络**
的设计，而磁盘上的原理图还是更早的 **8 网络**版本——那是在发现 12 个预留电阻从没画进图之前画的。

所以今天跑这个脚本，打印出来的正是"还没画的东西"的清单：6 个串阻、6 个下拉、6 个不存在的
驱动侧网络。**那张清单就是画图的待办表。** 原理图画完之后，同一条命令会打印 `ALL PASS`，
而全程没有任何一处是靠眼睛读的。

## Two conventions worth knowing / 两个值得知道的约定

**Resistors are compared by reference, not by pad number.** A resistor is
symmetric, so which of its pads is pin 1 depends on how the symbol happens to be
rotated on the sheet. Requiring `R1-1` on the Pi side would check the drawing's
orientation rather than the circuit, and would fail a schematic that is
electrically correct. Wiring a resistor between the wrong two nets is still
caught — it goes missing from one net and turns up in another. Connector pins
*are* compared as `REF-PIN`, because which physical pin a signal lands on is the
entire point of this board.

**电阻按编号比，不按引脚号比。** 电阻是对称的，哪一脚是 1 号取决于符号在图上转了多少度。
要求"`R1` 的 1 脚在 Pi 侧"是在检查画图的朝向而不是电路，会把一个电气上完全正确的原理图
判成失败。而"电阻接错了两个网络"仍然抓得到——它会从一个网络里消失、在另一个网络里冒出来。
连接器引脚**是**按 `REF-PIN` 比的，因为信号落在哪个物理针上正是这块板的全部意义。

**A leading `/` is stripped from net names.** Local labels carry the sheet path
(`/PWM1`); power symbols are global and carry none (`GND`). Irrelevant on a
single-sheet design, and normalised away here — but it will matter as soon as
there are hierarchical sheets.

**网络名前导的 `/` 会被去掉。** 局部标签带图页路径（`/PWM1`），电源符号是全局网络、不带
（`GND`）。单页设计里无所谓，这里统一掉——但一旦有多页图就会遇上。

## What it also reports / 它还会报什么

| Line | What it means |
|---|---|
| `single-pin unconnected nets` | Unused connector pins. On J1 that is expected behaviour, not a defect — 30 of them, deliberately not hidden with no-connect flags. The **count** is checked, so an unexplained change shows up |
| `unexpected extra nets` | A multi-pin net that is not in the expected map at all. Something was connected that the design does not call for |
| `auto-named (unlabelled) nets` | A net with more than one pin that KiCad had to invent a name for (`Net-(R1-Pad1)`). It means **a missing label**, which on this board is the one thing that must never happen: the label's name is what becomes the silkscreen |
