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

## It failed on purpose, and then it passed / 它曾经"应该失败"，后来通过了

When this directory was committed on 2026-09-12, `revA_expected_nets.json`
already described the **14-net** design while the schematic on disk was still the
earlier **8-net** version. Running the script printed exactly what had not been
drawn yet — six series resistors, six pull-downs, six driver-side nets — and
**that list was used as the drawing checklist.**

On 2026-09-13 the twelve resistors were drawn and the same command printed
`ALL PASS`. **The expected map was written before the drawing it checks**, which
is the only ordering in which a checklist is also a test.

2026-09-12 提交这个目录时，`revA_expected_nets.json` 描述的已经是 **14 网络**的设计，而磁盘上
的原理图还是 **8 网络**的旧版。跑脚本打印出来的正是"还没画的东西"：6 个串阻、6 个下拉、
6 个驱动侧网络——**那张清单当时就被当作画图的待办表用。**

2026-09-13 十二个电阻画完，同一条命令打印 `ALL PASS`。**期望表是在它要检查的那张图之前写下
的**——只有这个顺序，才能让一张待办清单同时是一次测试。

## ERC and DRC run from here too / ERC 和 DRC 也从这里跑

**Never read these numbers off a GUI panel.** KiCad's ERC panel does not re-run
when a rule severity changes; it keeps showing the previous result, which is
correct behaviour and, on screen, indistinguishable from a fresh run. On
2026-09-13 that cost a wrong number in a pushed commit —
[the correction](../../../docs/devlog/2026-09-13-erc-44-not-30.md).

**永远不要从 GUI 面板上读这些数字。** KiCad 的 ERC 面板不会因为规则严重性变了就自己重跑，
它继续显示上一次的结果——这是正确行为，而且在屏幕上和一次新的运行长得一模一样。
2026-09-13 这件事的代价是一个错误的数字被提交并推了上去。

`kicad-cli` ships with KiCad. On this machine (KiCad 10.0.6) it lives at
`%LOCALAPPDATA%\Programs\KiCad\10.0\bin\kicad-cli.exe` — **not** in
`Program Files`, and not on `PATH`.

```bash
cd hardware/stage1-signal-adapter/kicad
KICAD_CLI="$LOCALAPPDATA/Programs/KiCad/10.0/bin/kicad-cli.exe"

# ERC — exits non-zero if there are violations
"$KICAD_CLI" sch erc --severity-error --exit-code-violations \
    -o erc.rpt RoverSpine_Signal_Adapter_RevA.kicad_sch

# Netlist, for check_nets.py — no GUI export step needed
"$KICAD_CLI" sch export netlist \
    -o RoverSpine_Signal_Adapter_RevA.net RoverSpine_Signal_Adapter_RevA.kicad_sch

# DRC — once the layout exists
"$KICAD_CLI" pcb drc --severity-error --exit-code-violations \
    -o drc.rpt RoverSpine_Signal_Adapter_RevA.kicad_pcb
```

Both reports are generated artifacts and are gitignored, like the netlist.

**Group by the offending value, not by the rule name.** Counting by rule gives
`14 [footprint_filter]`, which hides the only distinction that matters — how many
symbols have *no* footprint versus how many have the *wrong* one. On 2026-09-13
that difference was eight and six, and the six were a 160-pin QFP sitting on the
pull-down resistors:

**按出问题的值分组，不要按规则名分组。** 按规则统计只会得到 `14 [footprint_filter]`，
它把唯一要紧的区分藏了起来：**多少个是"没有封装"，多少个是"封装错了"。**

```bash
grep -o "^\[[a-z_]*\]" erc.rpt | sort | uniq -c          # how many of each rule
grep "footprint_filter" erc.rpt \
  | sed 's/.*已分配封装 //;s/ 与封装筛选规则.*//' | sort | uniq -c   # WHICH footprints
```

```
      8 ()
      6 (pqfp-160_28x28mm_p0.65mm)
```

See [that devlog](../../../docs/devlog/2026-09-14-a-160-pin-qfp-on-a-resistor.md).

### Expected counts / 期望数字

| When | ERC | Made of |
|---|---|---|
| Schematic complete, **footprints not assigned** | **44 / 0** | 30 `pin_not_connected` + 14 `footprint_filter` |
| After all fourteen footprints are assigned and match | **30 / 0** | 30 `pin_not_connected` |

The 30 are the unused pins on the 2×20 Pi header — **by design, and deliberately
not hidden behind no-connect flags.** The 14 are the symbols still without a
footprint: an **empty** footprint field is compared like any other value and
matches no filter, so the count is a live to-do list that empties itself.

那 30 条是 2×20 排针上没用到的引脚——**设计如此，而且有意不用 no-connect 标记藏起来**。
那 14 条是还没有封装的符号：**空的封装字段和任何别的值一样参与比对，而空不匹配任何规则**，
所以这个计数是一张会自己清空的待办表。

> [!WARNING]
> **`30 / 0` is not sufficient on its own.** `R1`–`R12` all declare the footprint
> filter `R_*`, and both `R_0805_2012Metric` and `R_Axial_DIN0207_...` match it.
> **Swap the series resistors with the pull-downs and ERC reports a clean
> 30 / 0** — the rule checks that a resistor got *a resistor's* footprint, and has
> no opinion about which one. That is the entire difference between a board you
> can build and a board you cannot, so it is checked below instead.
>
> **光有 `30 / 0` 不够。** `R1`–`R12` 声明的筛选规则都是 `R_*`，而 0805 和轴向通孔两个封装
> 都匹配它。**把串阻和下拉的封装对调，ERC 报的是干干净净的 30 / 0**——这条规则检查的是
> "电阻拿到了**一个电阻的**封装"，对"**哪一个**"没有意见。而"哪一个"正是"能装的板"和
> "装不了的板"之间的全部差别，所以它由下面这项检查负责。

## Footprints are checked the same way / 封装用同一个办法检查

`check_nets.py` also compares every component's footprint against
`expected_footprints` in the same JSON map, using the same netlist — KiCad's
netlist carries the footprint field, so this needs no extra input.

**The map was written before the footprints were assigned**, so today it fails,
and the failure prints the to-do list:

`check_nets.py` 同时用同一份网表、同一张表比对每个元件的封装。**这张表是在封装分配之前写下
的**，所以它今天会失败，而失败打印出来的就是待办清单：

```
  [FAIL]    R1  expected: Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal
                          actual:   (not assigned)
```

Completion is **both** tests: ERC at exactly `30 / 0`, **and** `check_nets.py` at
`ALL PASS` with the footprint block included.

完成判据是**两项**：ERC 正好 `30 / 0`，**并且** `check_nets.py` 连封装那一段一起 `ALL PASS`。

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
