# 2026-09-14 — A 160-Pin QFP on a Resistor / 一个电阻上装着 160 脚的 QFP

## Result / 本次结果

Six of the twelve resistors — `R7`–`R12`, the 10 kΩ pull-downs — carried the
footprint **`Package_QFP:PQFP-160_28x28mm_P0.65mm`**: a 28 × 28 mm, 160-pin
quad flat pack. It was committed on 2026-09-13 in
[`949f91a`](2026-09-13-twelve-resistors-drawn.md), pushed, and sat in the
repository for a day while **every document in it said "footprints not
assigned".**

十二个电阻里有六个——`R7`–`R12`，那六个 10 kΩ 下拉——封装是
**`Package_QFP:PQFP-160_28x28mm_P0.65mm`**：一个 28 × 28 mm、160 脚的四方扁平封装。
它在 2026-09-13 随 `949f91a` 提交并推送，在仓库里躺了一天，而**这个仓库里的每一份文档
当时都写着"封装未分配"。**

The six fields are now cleared, and a check that compares footprints against a
written-down map has been added to
[`check_nets.py`](../../hardware/stage1-signal-adapter/tools/check_nets.py).

---

## It was the loud member of a quiet family / 它是一个安静家族里吵闹的那一个

**Honesty first: this particular one would not have reached the factory.** Six
28 × 28 mm parts on a board whose long side is about 65 mm do not fit, and
nobody lays that out without noticing. As defects go it is deafening.

**先说实话：这一个是到不了工厂的。** 六个 28 × 28 mm 的件放在一块长边约 65 mm 的板上根本
放不下，布局时不可能看不见。作为一个缺陷，它吵得震耳。

The reason it matters is the family it belongs to. Consider
`Resistor_SMD:R_0805_2012Metric` on `R1` instead — an 0805 pad where a
through-hole series resistor belongs:

它之所以要紧，是因为它所属的那一类。把它换成 `R1` 上装 `R_0805_2012Metric`——本该是通孔串阻
的位置上出现一个 0805 焊盘：

- **It passes ERC.** `R1`–`R12` all declare the footprint filter `R_*`, and
  `R_0805_2012Metric` matches it exactly as well as `R_Axial_DIN0207_...` does.
- **It passes the netlist check.** Nets are unchanged; the resistor is still
  between the same two nets.
- **It fits.** An 0805 pad is small and unremarkable on the layout.
- **It is caught at the soldering bench**, by someone holding six 1/4 W
  through-hole resistors and a board with no holes to put them in — in a
  workshop that is [no longer the author's](2026-09-13-soldering-is-outsourced.md),
  and whose owner has no reason to know which was intended.

**ERC 过、网表核对过、板上放得下、布局上看着毫不起眼**，最后在焊台上被发现——发现的人手里
捏着六个 1/4 W 通孔电阻，面前是一块没有孔可插的板，而**那个工具间已经不是作者自己的了**，
那边的人也没有任何理由知道原本该是哪一个。

> **The PQFP was a gift.** It is the one member of this class that announces
> itself, and it arrived early enough to pay for the check that covers the rest
> of the family.
>
> **那个 PQFP 是一份礼物。** 它是这一类里唯一会自报家门的那个，而且它来得足够早，
> 早到能用它换来一个覆盖其余成员的检查。

---

## Where it came from / 它是怎么进来的

`949f91a` is the commit that drew R1–R12. Before it, `PQFP-160` appears nowhere
in the schematic's history; after it, six times. All six on `R7`–`R12`, all
identical.

That is the same mechanism [that commit's own
devlog](2026-09-13-twelve-resistors-drawn.md) had already written up, about a
different defect in the same commit:

`949f91a` 之前，`PQFP-160` 在原理图历史里一次都没出现过；之后是六次，全在 `R7`–`R12` 上，
六个一模一样。这正是**那次提交自己的日志**已经写过的机制，只不过写的是同一次提交里的另一个缺陷：

> 六条对六个块——所以不是六次手滑，而是**第一个块里的一小段多余线头被复制了五份**。……
> 这是复制粘贴的好处那一半：**错误也被精确复制。**

**One copy-paste, two defects, the same six symbols.** One was six dangling wire
ends; the other was six wrong footprints. The entry noticed the first and
concluded that copy-paste makes mistakes *easy to recognise as systematic*. It
was right, and it still missed the second one sitting in the same six blocks —
because the two defects had different visibility, not different structure:

**一次复制粘贴，两个缺陷，同样的六个符号。** 那篇日志发现了第一个，并总结说复制粘贴让错误
"一眼就能看出是系统性的"。这话没错，但它依然漏掉了藏在同样那六个块里的第二个——因为两个缺陷
**可见性不同，结构相同**：

| Defect | ERC rule | Severity that day | Seen? |
|---|---|---|---|
| Six dangling wire ends | `wire_dangling` | `warning` | **Yes** — 6 warnings appeared |
| Six `PQFP-160` footprints | `footprint_filter` | **`ignore`** | **No** — reported nothing |

The rule that would have spoken was switched off. It was switched on later the
same day, [for reasons that turned out to be
wrong](2026-09-13-erc-severities-tightened.md) — and it immediately reported all
six. Nobody read them as six.

**能说话的那条规则当时是关着的。** 它在同一天稍后被打开了（当时给的[理由后来被证明是错
的](2026-09-13-erc-severities-tightened.md)），而它**立刻把这六个都报了出来**。没有人把它们
读成六个。

---

## 44 in, 44 out / 44 进，44 出

Clearing the six wrong footprints **did not change the ERC count.**

| | Total | Made of |
|---|---|---|
| With the `PQFP-160`s | **44** | 30 `pin_not_connected` + 8 empty + **6 `pqfp-160`** |
| After clearing them | **44** | 30 `pin_not_connected` + 14 empty |

A 160-pin QFP on six resistors, and no 160-pin QFP on six resistors, produce
**the identical number.** Anyone watching the total would have seen a fix that
looked like nothing happening — and, running the other direction, would have
seen the defect arrive as nothing happening too.

一个 160 脚 QFP 装在六个电阻上，和没有装，**产生完全一样的数字**。只盯着总数的人，会看到
一次"什么也没发生"的修复；而反过来走，也会看到这个缺陷"什么也没发生"地到来。

This is the third time in four days that this repository has recorded the same
shape: [the swapped label](2026-09-13-twelve-resistors-drawn.md) that left ERC at
30 / 0 with the fault present, [the stale
panel](2026-09-13-erc-44-not-30.md) showing a number from a world the file was no
longer in, and now a count that is blind in both directions.

**So the check is not the count. It is the composition:**

```bash
grep "footprint_filter" erc.rpt | sed 's/.*已分配封装 //;s/ 与封装筛选规则.*//' | sort | uniq -c
```

```
      8 ()
      6 (pqfp-160_28x28mm_p0.65mm)
```

That one line is the difference between "fourteen to do" and "eight to do and six
that are wrong." [`tools/README.md`](../../hardware/stage1-signal-adapter/tools/README.md)
previously grouped by rule name, which produces `14 [footprint_filter]` and hides
exactly the distinction that matters.

**所以检查的不是计数，是组成。** 上面那一行，就是"还有十四个要做"和"八个要做、六个是错的"
之间的差别。`tools/README.md` 原来是按规则名统计的，那样只会得到 `14 [footprint_filter]`，
**恰好把唯一要紧的区分藏起来。**

---

## The mistake in yesterday's correction / 昨天那篇更正里的错

[Yesterday's entry](2026-09-13-erc-44-not-30.md) says:

> "No footprint assigned" is not zero violations — it is fourteen, **one for
> every symbol that declares a filter.**

It was **eight empty and six wrong.** That sentence was written after reading
three lines of a forty-four-line report and generalising from them.

昨天那篇写的是"十四条，**每一个声明了筛选规则的符号一条**"。**实际是八个空、六个错。**
那句话是在读了一份四十四行报告里的三行之后推广出来的。

Three entries, four days, one shape:

| Day | The cheap stand-in | What it stood in for |
|---|---|---|
| 09-13 | A panel showing `30 / 0` | An actual ERC run |
| 09-13 | "The enclosure sets the outline" | Measuring J1's courtyard |
| 09-14 | Three lines of the report | All forty-four |

Each time a **representative was substituted for the population**, and each time
the representative was honest — the panel really had shown 30, those three lines
really were empty. **A sample is not wrong; it is just silent about everything it
did not cover, and that silence reads exactly like agreement.**

每一次都是**用一个便宜的代表去代替全体**，而每一次那个代表本身都是诚实的：面板确实显示过
30，那三行确实是空的。**抽样不是错的，它只是对它没覆盖到的部分保持沉默——而那种沉默，
读起来和"一致"一模一样。**

---

## What was built / 做了什么

`check_nets.py` now compares footprints against the map in
`revA_expected_nets.json`, using the netlist it already parses — KiCad's netlist
carries the footprint field, so this needed no new input and no new tool.

**The map was written before the footprints are assigned**, which is the same
ordering [the net map used](../../hardware/stage1-signal-adapter/tools/README.md)
on 09-12: it fails today, and the failure prints the to-do list.

`check_nets.py` 现在用它本来就在解析的那份网表比对封装——KiCad 的网表里带封装字段，所以
不需要新输入、也不需要新工具。**这张表是在封装分配之前写的**，和 09-12 网络表用的是同一个
顺序：**它今天会失败，而失败打印出来的就是待办清单。**

```
  [FAIL]    R1  expected: Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal
                          actual:   (not assigned)
  ...
  14 footprint(s) do not match the map. ERC cannot catch this:
  R1-R12 all declare the filter `R_*`, which matches both the
  0805 and the axial through-hole footprint.
```

### And the exit criterion was wrong / 完成判据原来是错的

The plan was that **ERC returning to exactly 30 / 0 is the completion test** for
footprint assignment. It is not sufficient, and this is the sharp version of the
whole entry:

原计划是把"**ERC 回到正好 30 / 0**"当作封装分配的完成判据。**它不够**，而这是整篇日志最锋利
的一句：

> `R_*` matches `R_0805_2012Metric` and `R_Axial_DIN0207_...` equally. **Swap the
> series resistors with the pull-downs and ERC reports a clean 30 / 0.** The
> footprint filter checks that a resistor got *a resistor's* footprint. It has no
> opinion about *which* one, and "which one" is the entire difference between a
> board you can build and a board you cannot.
>
> `R_*` 对两个封装一视同仁。**把串阻和下拉的封装对调，ERC 报的是干干净净的 30 / 0。**
> 封装筛选规则检查的是"电阻拿到了**一个电阻的**封装"，它对"**哪一个**"没有意见——
> 而"哪一个"正是"一块能装的板"和"一块装不了的板"之间的全部差别。

30 / 0 stays as a criterion. It is now the *first* of two, and the second is
`check_nets.py` reporting `ALL PASS` including the footprint block.

---

## Also in this session / 本次顺带

- **The design rules Andy set on 09-13 are committed.** They match what
  [`fabrication.md`](../fabrication.md) had already specified — 0.3 mm track,
  0.3 mm clearance, 0.3 mm via hole with a 0.15 mm annular ring. The document
  went into the project file; nothing was invented here.
- **`dimension_units` reverted from `0` to `3`.** All nineteen project templates
  shipped with KiCad 10.0.6 use `3`, so `3` is both the prior value and KiCad's
  own default, and reverting needs no theory about what the enum means. This is a
  metric board going to a metric fab; a units setting that had been changed
  without a reason recorded is a setting that was changed by accident.
- **All parts are bought**, recorded in
  [`tools-and-parts.md`](../tools-and-parts.md) on 09-13. Only the PCB order, the
  courier and the enclosure remain — and the enclosure is
  [deliberately deferred](../tools-and-parts.md) until the layout fixes the
  outline.

`fabrication.md` 早就写下的设计规则被落进了工程文件，**这里没有发明任何东西**。
`dimension_units` 从 `0` 还原成 `3`——KiCad 10.0.6 自带的十九个模板全是 `3`，所以 `3` 既是
原值也是官方默认，**还原它不需要我对这个枚举有任何理论**。

---

## Status / 当前状态

| Item | State |
|---|---|
| Rev A schematic | Complete — 14 nets, unchanged |
| **Footprints** | **Zero assigned** — and now that statement is true of all fourteen |
| ERC | 44 / 0 — 30 by design + 14 unassigned |
| Netlist check | 14 nets `PASS` |
| **Footprint check** | **`FAIL` — 14 to assign, on purpose** |
| Parts | **Bought 2026-09-13**, except PCB order, courier, enclosure |
| PCB layout | Not started |
| D50A pin 1 | **Assumed** |
| Board status | `[ ]` |

## Next / 下一步

1. **Assign the fourteen footprints.** Two completion tests now, not one: ERC at
   exactly **30 / 0**, and `check_nets.py` at **`ALL PASS`** including footprints.
2. **Measure the resistors on arrival** — body length and lead diameter — before
   the axial footprint is frozen. `P10.16mm` is a choice made from a listing
   drawing, not from calipers.
3. **Board outline, board-first** — J1's courtyard is 59.46 × 9.90 mm.
4. **Still gated on the meter:** D50A pin 1, before any order.

## Files touched / 改了哪些文件

[`RoverSpine_Signal_Adapter_RevA.kicad_sch`](../../hardware/stage1-signal-adapter/kicad/RoverSpine_Signal_Adapter_RevA.kicad_sch) ·
[`RoverSpine_Signal_Adapter_RevA.kicad_pro`](../../hardware/stage1-signal-adapter/kicad/RoverSpine_Signal_Adapter_RevA.kicad_pro) ·
[`check_nets.py`](../../hardware/stage1-signal-adapter/tools/check_nets.py) ·
[`revA_expected_nets.json`](../../hardware/stage1-signal-adapter/tools/revA_expected_nets.json) ·
[`tools/README.md`](../../hardware/stage1-signal-adapter/tools/README.md) ·
[`stage1-signal-adapter/README.md`](../../hardware/stage1-signal-adapter/README.md) ·
[`roadmap.md`](../roadmap.md)
