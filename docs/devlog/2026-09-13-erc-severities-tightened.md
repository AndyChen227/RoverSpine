# 2026-09-13 — Two ERC Severities Raised, and What the Re-run Actually Proved / 两项 ERC 严重性调高了，以及重跑真正证明了什么

## Result / 本次结果

Two rule severities changed in the project file. ERC re-run: **30 errors / 0
warnings**, unchanged. The netlist checker, run again from the committed script,
still reports `ALL PASS` against [the net structure](../roadmap.md#nets).

工程文件里改了两项规则的严重性。ERC 重跑：**30 错误 / 0 警告**，没变。网表脚本再跑一次，
对着[网络结构表](../roadmap.md#nets)仍是 `ALL PASS`。

| Rule / 规则 | Was | Now | Planned? / 在计划里吗 |
|---|---|---|---|
| `footprint_filter` — 分配的封装不匹配封装筛选规则 | `ignore` | **`error`** | **Yes** — [Stage 1 README](../../hardware/stage1-signal-adapter/README.md) step 5, carried since 2026-09-12 |
| `pin_to_pin` — 引脚到引脚冲突 | `warning` | **`error`** | **No** — tightened in the same sitting |

Nothing else moved. The board, the schematic, the values and the footprint plan
are exactly where [this morning's entry](2026-09-13-twelve-resistors-drawn.md)
left them. Board status stays `[ ]`.

板子、原理图、阻值、封装计划和[今天早些时候那篇](2026-09-13-twelve-resistors-drawn.md)
留下的完全一样，板子状态仍是 `[ ]`。

---

## The planned one: armed before it can fire / 计划中的那一项：在它能开火之前就架好

`footprint_filter` compares an **assigned** footprint against the filter
patterns declared on the symbol. Rev A has **no footprints assigned**, so today
the test has nothing to compare and cannot pass or fail. Turning it on now
proves nothing about the design.

That is the reason to do it now rather than later. The check guards exactly one
step — fitting the 2×20 symbol with a wrong-pitch or wrong-pin-count footprint,
which is the fatal mistake available at that step — and **it is switched on
before that step, not after.** Enabling it afterwards would mean doing the work
with the check off and then asking the tool to bless what was already drawn,
which is a different and much weaker question.

`footprint_filter` 比对的是**已分配的封装**与符号上声明的筛选规则。Rev A **一个封装都没分配**，
所以今天这项检查没有比对对象，既通不过也不会失败——现在打开它，对设计本身什么都没证明。

**这恰恰是现在做而不是以后做的理由。** 它守的就是一步：给 2×20 的符号配了错间距或错引脚数的
封装——那一步上唯一致命的错误。**它在那一步之前就被打开，而不是之后。** 之后再打开，等于先在
检查关着的情况下把活干完，再让工具追认已经画好的东西，那是另一个问题，而且弱得多。

There was no surprise today because there was nothing left to find out:
[2026-09-12](2026-09-12-reserved-resistor-pads.md) had already checked by hand
that enabling this rule would not false-alarm on the two connector symbols'
intended footprints. **That verification is what made today a settings change
instead of an investigation.**

今天没有意外，因为该查的[昨天](2026-09-12-reserved-resistor-pads.md)已经查过了：手工确认过
打开它不会对两个连接器符号的目标封装误报。**正是那次确认，让今天这件事是"改一个设置"而不是
"查一件事"。**

---

## The unplanned one, and why it was free / 计划外的那一项，以及它为什么是白捡的

`pin_to_pin` fires when one net carries pin electrical types that conflict — two
outputs driving each other, an output onto a power input, and so on.

**Rev A has no output pins at all.** Every pin on the sheet belongs to a
connector or a resistor: passive, or power. This is not an accident of the
current drawing, it is
[what the board is specified to be](../../hardware/stage1-signal-adapter/README.md) —
no microcontroller, no active component of any kind. So the rule has nothing on
this sheet it could fire on, in this revision or any revision that keeps Rev A's
scope.

`pin_to_pin` 抓的是同一个网络上电气类型冲突的引脚——两个输出互相驱动、输出接到电源输入，等等。

**Rev A 根本没有输出引脚。** 图上每一个引脚不是连接器的就是电阻的：被动，或者电源。这不是当前
这张图碰巧如此，而是[这块板的规格本身](../../hardware/stage1-signal-adapter/README.md)——不用
单片机，不用任何有源器件。所以只要 Rev A 的范围不变，这条规则在这张图上就没有可以开火的对象。

### What the re-run proves, and what it does not / 重跑证明了什么，没证明什么

The two changes are **not the same kind of change**, and the same `30 / 0`
carries different weight for each:

- **`ignore → error` changes whether a test runs at all.** Violations that were
  never reported could have appeared. None did.
- **`warning → error` only changes how an already-reported violation is
  classified.** The previous report had **0 warnings** — so there was nothing to
  reclassify, and `30 / 0` was **guaranteed before the setting was touched.**

So: today's report is real evidence that `footprint_filter` found nothing (for
the trivial reason that there is nothing yet to look at), and it is **not
evidence of anything at all about `pin_to_pin`.** Re-running was still right —
confirming a prediction costs one keystroke — but it is worth being precise
about which half of the report carried information, because this is the second
time in one day that a report has needed splitting that way.

两个改动**不是同一类改动**，同一个 `30 / 0` 对它们的分量不一样：`ignore → error` 改的是
**一项检查跑不跑**，本来不会被报出来的违规可能冒出来——没有冒出来；`warning → error` 改的只是
**已经报出来的违规怎么分类**，而上一次报告是 **0 警告**，没有东西可以被重新分类，
**`30 / 0` 在动这个设置之前就已经定死了。**

所以：今天的报告是 `footprint_filter` 没查到东西的真实证据（理由很平凡——现在还没有东西可查），
而它**对 `pin_to_pin` 什么都没证明**。重跑仍然是对的（验证一个预测只花一次按键），但值得把话说
精确：**报告的哪一半携带了信息**。这是同一天里第二次需要这样切开一份报告。

### A rule adopted when it cannot fire / 一条在它开不了火的时候被采纳的规则

Keeping it is not the same as pretending it did work. **The project file is a
document too.** `pin_to_pin: warning` recorded a default that nobody chose;
`pin_to_pin: error` records a position — *on this project, a pin-type conflict
is not a line you scroll past.*

And the cheapest moment to adopt a rule is precisely when it cannot fire. A rule
raised while it is already flagging things is a rule adopted under pressure to
make the report go green, and that pressure argues for lowering it again.

留着它，不等于假装它干了活。**工程文件也是一份文档。** `pin_to_pin: warning` 记录的是一个没人
选过的默认值；`pin_to_pin: error` 记录的是一个立场——**在这个工程上，引脚类型冲突不是你可以
一眼滑过去的一行。**

而**采纳一条规则最便宜的时刻，恰恰是它开不了火的时候。** 等到它已经在报东西时才去调高，那是在
"让报告变绿"的压力下做决定，而那股压力指向的是把它再调回去。

---

## A checklist item that could never be ticked / 一条永远勾不上的清单项

While checking what else in the repository talks about ERC, the pre-upload
checklist in [`fabrication.md`](../fabrication.md) §2 said:

> - [ ] **ERC passes** with zero errors.

**This board's ERC reports 30 errors by design** — the 30 unused pins on the
2×20 Pi header, each one a `pin_not_connected` error because that rule is
deliberately at `error` rather than `ignore`. The roadmap's own exit criterion
says so, and so does every devlog since 09-12. The checklist item, as written,
**can never be ticked for Rev A.**

翻仓库里还有哪些地方谈 ERC 时，发现 [`fabrication.md`](../fabrication.md) 第 2 节的上传前清单
写着"**ERC 零错误**"。**这块板的 ERC 按设计就是 30 个错误**——2×20 排针上 30 个没用到的引脚，
每一个都是 `pin_not_connected`，因为那条规则是有意设成 `error` 而不是 `ignore` 的。路线图的完成
判据这么写，09-12 以来每一篇日志也都这么写。**那一条清单项，对 Rev A 永远勾不上。**

Two documents in the same repository disagreeing about the pass condition for the
same board is not a typo. It is a checklist that will be read once, in the half
hour before an order is placed, by someone who will resolve the conflict by
believing whichever file is already open.

It now reads: **every violation accounted for, and the count matching the number
written down in advance.** That is stricter than "zero", not looser —

> **Zero is always reachable by setting rules to `ignore`.** A count committed to
> in advance is not.

同一个仓库里两份文档对同一块板的通过条件说法不一致，这不是笔误。那是一份**只会在下单前半小时被
读一次**的清单，读它的人会用"哪个文件已经开着"来解决这个冲突。

现在改成：**每一条违规都有账，而且数量和事先写下的那个数对得上。** 这比"零错误"**更严**，不是更松——

> **"零"永远可以靠把规则设成 `ignore` 达到，一个事先押下的数字不行。**

---

## Why a settings change gets its own commit / 为什么一个设置改动值得单独一个提交

A change with no visible effect is the easiest kind to lose. In six months the
diff

```
-      "pin_to_pin": "warning",
+      "pin_to_pin": "error",
```

buried in a 700-line `.kicad_pro`, with no message attached, reads as a stray
click from an unrelated session — and the natural repair for a stray click is to
put it back.

This is [this morning's problem](2026-09-13-soldering-is-outsourced.md) from the
other side. There, **a reason outlived its decision** and invited the right
decision to be undone for the wrong reason. Here, **a decision would have
outlived its reason** — and an unexplained decision invites exactly the same
undoing.

一个没有可见效果的改动最容易丢。半年后，埋在 700 行 `.kicad_pro` 里、没有任何说明的那两行 diff，
读起来就是某次无关的会话里手滑点到的——**而手滑的自然修法就是把它点回去。**

这是[今天早上那件事](2026-09-13-soldering-is-outsourced.md)的反面：那边是**理由活得比决定久**，
让一个正确的决定因为一个错误的原因被推翻；这边是**决定会活得比理由久**——
**而一个没有理由的决定，招来的是同一种推翻。**

---

## Status / 当前状态

| Item | State |
|---|---|
| Rev A schematic | Complete — 14 nets (unchanged) |
| ERC | **30 errors / 0 warnings**, re-run under the tightened rule set |
| ERC rule set | `footprint_filter` **armed**, `pin_to_pin` **raised**; three rules remain `ignore` |
| Netlist check | `ALL PASS`, reproduced from the committed script |
| Footprints | Not assigned, not frozen |
| PCB layout | Not started |
| Cables | Selected 2026-09-11, **not yet delivered** |
| Headers, enclosure, resistors | **Not yet bought** |
| D50A pin 1 | **Assumed** |
| Board status | `[ ]` |

## Next / 下一步

Unchanged and still gated on parts, with one item now struck off.

没有变化，卡的仍然是实物，只是划掉了一条。

1. **Buy what is outstanding** — two boxed headers, enclosure, through-hole and
   0805 resistor assortments, ≈¥40. **The enclosure sets the board outline and
   the headers set connector clearance, so no layout step can start until they
   are in hand.**
2. **When the cables arrive:** resolve D50A pin 1 end-to-end with a meter. Still
   the one error that shorts 3.3 V to ground.
3. ~~Re-enable `footprint_filter` before assigning footprints.~~ **Done today.**
4. Then footprints, layout, DRC, Gerber — see [`fabrication.md`](../fabrication.md).

## Files touched / 改了哪些文件

[`RoverSpine_Signal_Adapter_RevA.kicad_pro`](../../hardware/stage1-signal-adapter/kicad/RoverSpine_Signal_Adapter_RevA.kicad_pro) ·
[`fabrication.md`](../fabrication.md) ·
[`stage1-signal-adapter/README.md`](../../hardware/stage1-signal-adapter/README.md)
