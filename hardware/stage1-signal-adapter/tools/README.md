# Checks

One script, the map it compares against, and the commands that produce their own
inputs.

## Why this exists

**ERC checks structure, not intent.** If `PWM1` and `PWM2` were placed on each
other's connector pins, each net still connects exactly two pins, nothing dangles
and nothing conflicts — **ERC reports no violation at all**, the board gets
fabricated, and the left and right motors' speed control is reversed.

The same applies to footprints, for a sharper reason. `R1`–`R12` all declare the
footprint filter `R_*`, and **both `R_0805_2012Metric` and
`R_Axial_DIN0207_...` match it.** ERC cannot tell a 0805 pull-down from a
through-hole series resistor, so swapping those two groups passes at a clean
30 / 0.

The fix for both is to compare against a written-down map as a **string
comparison**. Reading the schematic is how the error gets in; comparing strings
is how it gets caught.

## Usage

```bash
cd hardware/stage1-signal-adapter
KICAD_CLI="$LOCALAPPDATA/Programs/KiCad/10.0/bin/kicad-cli.exe"

"$KICAD_CLI" sch export netlist \
    -o kicad/RoverSpine_Signal_Adapter_RevA.net \
       kicad/RoverSpine_Signal_Adapter_RevA.kicad_sch

python tools/check_nets.py \
    kicad/RoverSpine_Signal_Adapter_RevA.net \
    tools/revA_expected_nets.json
```

Exit status is 0 on `ALL PASS` and 1 otherwise. The script is standard library
only — no KiCad installation and no packages needed, so it also runs on a machine
that has never had KiCad on it.

**The netlist is not committed** (`*.net` is gitignored). It is a generated
artifact, reproducible from the schematic at any time. What is committed is the
schematic it comes from, the expected map, and the script.

## ERC and DRC run from here too

**Never read these numbers off a GUI panel.** KiCad's ERC panel does not re-run
when a rule severity changes; it keeps showing the previous result, which is
correct behaviour and, on screen, indistinguishable from a fresh run.

`kicad-cli` ships with KiCad. On this machine (10.0.6) it is at
`%LOCALAPPDATA%\Programs\KiCad\10.0\bin\kicad-cli.exe` — **not** in
`Program Files`, and not on `PATH`.

```bash
cd hardware/stage1-signal-adapter/kicad

# ERC — exits non-zero if there are violations
"$KICAD_CLI" sch erc --severity-error --exit-code-violations \
    -o erc.rpt RoverSpine_Signal_Adapter_RevA.kicad_sch

# DRC — once the layout exists
"$KICAD_CLI" pcb drc --severity-error --exit-code-violations \
    -o drc.rpt RoverSpine_Signal_Adapter_RevA.kicad_pcb
```

Both reports are generated artifacts and are gitignored.

**Group by the offending value, not by the rule name.** Counting by rule gives
`14 [footprint_filter]`, which hides the only distinction that matters — how many
symbols have *no* footprint versus how many have the *wrong* one:

```bash
grep -o "^\[[a-z_]*\]" erc.rpt | sort | uniq -c          # how many of each rule
grep "footprint_filter" erc.rpt \
  | sed 's/.*已分配封装 //;s/ 与封装筛选规则.*//' | sort | uniq -c   # WHICH footprints
```

### Expected counts

| When | ERC | Made of |
|---|---|---|
| Schematic complete, **footprints not assigned** | **44 / 0** | 30 `pin_not_connected` + 14 `footprint_filter` |
| After all fourteen footprints are assigned and match | **30 / 0** | 30 `pin_not_connected` |

The 30 are the unused pins on the 2×20 Pi header — by design, and deliberately
not hidden behind no-connect flags. The 14 are the symbols without a footprint:
an **empty** footprint field is compared like any other value and matches no
filter, so the count is a to-do list that empties itself.

**Completion is both tests:** ERC at exactly `30 / 0`, **and** `check_nets.py` at
`ALL PASS` with the footprint block included.

## Two conventions worth knowing

**Resistors are compared by reference, not by pad number.** A resistor is
symmetric, so which of its pads is pin 1 depends on how the symbol happens to be
rotated on the sheet. Requiring `R1-1` on the Pi side would check the drawing's
orientation rather than the circuit, and would fail a schematic that is
electrically correct. Wiring a resistor between the wrong two nets is still
caught — it goes missing from one net and turns up in another. Connector pins
*are* compared as `REF-PIN`, because which physical pin a signal lands on is the
entire point of this board.

**A leading `/` is stripped from net names.** Local labels carry the sheet path
(`/PWM1`); power symbols are global and carry none (`GND`). Irrelevant on a
single-sheet design, and normalised away here — but it will matter as soon as
there are hierarchical sheets.

## What else the script reports

| Line | What it means |
|---|---|
| `single-pin unconnected nets` | Unused connector pins. On J1 that is expected — 30 of them, deliberately not hidden with no-connect flags. The **count** is checked, so an unexplained change shows up |
| `unexpected extra nets` | A multi-pin net not in the expected map at all. Something was connected that the design does not call for |
| `auto-named (unlabelled) nets` | A net with more than one pin that KiCad had to invent a name for (`Net-(R1-Pad1)`). It means **a missing label**, which on this board must never happen: the label's name is what becomes the silkscreen |

---

# 核对脚本 / 中文

一个脚本、一张它用来比对的表，以及几条自己生成输入的命令。

## 为什么有这个东西

**ERC 检查的是结构，不是意图。** 假设 `PWM1` 和 `PWM2` 贴到了对方的连接器引脚上：两条网络
各自仍然连着 2 个引脚，没有悬空、没有冲突，**ERC 一声不响**，板子照样打样出来，然后左右
电机的调速是反的。

封装也一样，而且理由更尖锐。`R1`–`R12` 声明的筛选规则都是 `R_*`，而
**`R_0805_2012Metric` 和 `R_Axial_DIN0207_...` 都匹配它**。ERC 分不出 0805 下拉和通孔
串阻，所以把这两组对调能拿到干干净净的 30 / 0。

两者的解法都是把它与一张写下来的表做**字符串比对**。**用眼睛读原理图正是错误进来的途径，
做成字符串比对才是抓住它的途径。**

## 用法

```bash
cd hardware/stage1-signal-adapter
KICAD_CLI="$LOCALAPPDATA/Programs/KiCad/10.0/bin/kicad-cli.exe"

"$KICAD_CLI" sch export netlist \
    -o kicad/RoverSpine_Signal_Adapter_RevA.net \
       kicad/RoverSpine_Signal_Adapter_RevA.kicad_sch

python tools/check_nets.py \
    kicad/RoverSpine_Signal_Adapter_RevA.net \
    tools/revA_expected_nets.json
```

`ALL PASS` 时返回 0，否则返回 1。脚本只用标准库，不需要装 KiCad 也不需要装任何包。

**网表本身不提交**（`*.net` 已在 gitignore 里）：它是生成物，随时能从原理图重新导出。
提交的是它的来源（原理图）、期望表和脚本。

## ERC 和 DRC 也从这里跑

**永远不要从 GUI 面板上读这些数字。** KiCad 的 ERC 面板不会因为规则严重性变了就自己重跑，
它继续显示上一次的结果——这是正确行为，而且在屏幕上和一次新的运行长得一模一样。

`kicad-cli` 随 KiCad 一起安装。这台机器上（10.0.6）它在
`%LOCALAPPDATA%\Programs\KiCad\10.0\bin\kicad-cli.exe`——**不在** `Program Files`，
也不在 `PATH` 上。

```bash
cd hardware/stage1-signal-adapter/kicad

# ERC——有违规时返回非零
"$KICAD_CLI" sch erc --severity-error --exit-code-violations \
    -o erc.rpt RoverSpine_Signal_Adapter_RevA.kicad_sch

# DRC——等布局存在之后
"$KICAD_CLI" pcb drc --severity-error --exit-code-violations \
    -o drc.rpt RoverSpine_Signal_Adapter_RevA.kicad_pcb
```

两份报告都是生成物，不提交。

**按出问题的值分组，不要按规则名分组。** 按规则统计只会得到 `14 [footprint_filter]`，
它把唯一要紧的区分藏了起来：**多少个是"没有封装"，多少个是"封装错了"。**

```bash
grep -o "^\[[a-z_]*\]" erc.rpt | sort | uniq -c          # 每条规则各多少条
grep "footprint_filter" erc.rpt \
  | sed 's/.*已分配封装 //;s/ 与封装筛选规则.*//' | sort | uniq -c   # 到底是哪些封装
```

### 期望数字

| 什么时候 | ERC | 组成 |
|---|---|---|
| 原理图完工，**封装未分配** | **44 / 0** | 30 `pin_not_connected` + 14 `footprint_filter` |
| 十四个封装全部分配且匹配之后 | **30 / 0** | 30 `pin_not_connected` |

那 30 条是 2×20 排针上没用到的引脚——设计如此，而且有意不用 no-connect 标记藏起来。
那 14 条是还没有封装的符号：**空的封装字段和任何别的值一样参与比对，而空不匹配任何规则**，
所以这个计数是一张会自己清空的待办表。

**完成判据是两项：** ERC 正好 `30 / 0`，**并且** `check_nets.py` 连封装那一段一起
`ALL PASS`。

## 两个值得知道的约定

**电阻按编号比，不按引脚号比。** 电阻是对称的，哪一脚是 1 号取决于符号在图上转了多少度。
要求"`R1` 的 1 脚在 Pi 侧"是在检查画图的朝向而不是电路，会把一个电气上完全正确的原理图
判成失败。而"电阻接错了两个网络"仍然抓得到——它会从一个网络里消失、在另一个网络里冒出来。
连接器引脚**是**按 `REF-PIN` 比的，因为信号落在哪个物理针上正是这块板的全部意义。

**网络名前导的 `/` 会被去掉。** 局部标签带图页路径（`/PWM1`），电源符号是全局网络、
不带（`GND`）。单页设计里无所谓，这里统一掉——但一旦有多页图就会遇上。

## 脚本还会报什么

| 行 | 含义 |
|---|---|
| `single-pin unconnected nets` | 没用到的连接器引脚。J1 上这是预期行为，30 个，有意不用 no-connect 藏起来。**计数**会被检查，所以无法解释的变化会显形 |
| `unexpected extra nets` | 一条多引脚网络，完全不在期望表里。说明接了设计上没有要求的东西 |
| `auto-named (unlabelled) nets` | 一条引脚数大于 1、KiCad 不得不替它编名字的网络（`Net-(R1-Pad1)`）。它意味着**少了一个标签**，而这在这块板上绝不能发生：标签的名字就是丝印的名字 |
