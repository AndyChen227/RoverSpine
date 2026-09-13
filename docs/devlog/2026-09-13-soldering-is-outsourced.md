# 2026-09-13 — Assembly Moves Off This Track / 焊接这条线交出去了

## The fact / 事实

**From today, the soldering is done in a relative's workshop, not by the author.**
That workshop already has the iron, the solder, the flux, the wick and the rest.

This is a project fact, not a design change, but it touches more of this
repository than it looks like it should — because several decisions here were
justified by *who would be holding the iron*.

**从今天起，焊接在亲戚的工具间完成，不由作者本人做**，那边烙铁、焊锡、助焊剂、吸锡带都齐全。

这是一件项目事实，不是设计变更。但它牵动的文件比看上去多——因为这个仓库里有好几个决定，
当初的理由是**谁会拿着烙铁**。

---

## What it changes / 它改变了什么

### 1. The tool list loses its largest item / 工具清单少掉最大的一项

Every soldering tool moves from `❓ unknown` to `✅ workshop`, and the practice
kit leaves the list entirely. That is ¥150–300 for the iron alone.

**One row did not move: the multimeter.** It is not a soldering tool, and it is
needed **at the rover** — for the D50A pin-1 gate, for the bare-board continuity
check before the board touches the Pi, and for every bring-up measurement after
that. None of those happen in the workshop. It is now the only tool on the
hardware track that has to be bought, and it was always the more urgent one:
the iron waits for a board, the meter is needed the day the cables arrive.

所有焊接工具从 `❓ 不确定` 变成 `✅ 工具间`，练习板直接从清单上消失，光烙铁就是 ¥150–300。

**只有一行没有跟着走：万用表。** 它不是焊接工具，而且它要用在**车那边**——D50A 的 1 号脚闸门、
板子碰树莓派之前的空板逐针导通、以及之后每一次上电测量。这些都不发生在工具间。它现在是硬件线上
唯一必须买的工具，而且它本来就更急：**烙铁可以等板子，万用表要在排线到货那天就用上。**

### 2. The soldering documentation changes reader, not content / 焊接文档换的是读者，不是内容

[`fabrication.md`](../fabrication.md)'s assembly order and the
straight-header technique were written as steps to follow. They are now
**requirements to hand over**. Almost none of the text needed rewriting; what
needed writing was the fact that somebody else reads it.

So section 6 gained an explicit four-item handover list, because every one of
them is specific to *this* board and would not be guessed by a competent person
who has not read this repository:

装配顺序和排针焊直的手法原本是"照着做的步骤"，现在是"**交接给别人的要求**"。文字几乎不用改，
要补的是"有另一个人会读它"这件事。所以第 6 节加了一张明确的四条交接清单——这四条**每一条都只
属于这块板**，一个手艺很好但没读过这个仓库的人不会猜到：

1. **Shortest parts first.** Once the 2×20 header is on, the board will not lie
   flat and the low pads get awkward.
2. **Both boxed headers square to the board.** A leaning header will not accept
   the ribbon, or accepts it under permanent stress.
3. **Whether `R7`–`R12` are populated is a decision, made before the first
   joint** — and "later" now costs a second trip to the workshop, not just an
   awkward angle.
4. **No substitutions.** 33 Ω and 10 kΩ are values that passed a netlist check
   done as a string comparison. A helpful swap to whatever is in the drawer
   quietly invalidates that check.

Item 4 is the one that would not have needed saying before. When the person
soldering is the person who drew the schematic, "why is it 33 Ω" has an obvious
answer. When it is not, **the value's provenance has to travel with the board.**

第 4 条是以前根本不必写的。焊的人就是画图的人时，"为什么是 33 Ω"不用问；不是同一个人时，
**这个值的来历必须跟着板子一起走。**

### 3. Stage 0's exit criterion moves from producing to accepting / 第 0 阶段的判据从"做得出"变成"看得出"

It used to read:

> you can **produce** a solder joint you are willing to put on a moving vehicle

It now reads:

> you can **look at** a solder joint and say whether you are willing to put it on
> a moving vehicle

**It was not deleted, and that is the point.** A board is going to come back
assembled, and somebody has to decide whether it goes on the rover. That
somebody cannot be the person who soldered it, because they do not know what
this vehicle does to a joint — they know how to make a good one, which is a
different question. Inspection is the half of the skill that does not transfer
with the work.

原来的判据是"**你能做出**一个你愿意装到运动的车上的焊点"，现在是"**你能看出**一个焊点你愿不愿意
把它装到运动的车上"。

**它没有被删掉，而这正是关键。** 板子会焊好送回来，总得有人决定它能不能装车。**这个人不能是焊它
的那个人**——焊的人知道怎么焊好，但不知道这台车会对一个焊点做什么，那是两个问题。
**验收是这项技能里不随着工作一起转移出去的那一半。**

`fabrication.md`'s post-arrival steps gained the matching step: inspect before
anything else, then re-run continuity on the assembled board — including the two
readings the bare board could not give, ≈33 Ω across each series resistor and
≈10 kΩ (or open) at each pull-down.

---

## Two justifications that expired / 两条过期的理由

Both were found by asking the same question of every affected file: *did this
sentence depend on who holds the iron?*

两条都是靠对每个受影响的文件问同一个问题找出来的：**这句话是不是依赖于"谁拿着烙铁"？**

### The series resistors stay through-hole — for different reasons / 串阻保持通孔，但理由换了

The package was chosen [yesterday](2026-09-12-reserved-resistor-pads.md) with
this reason:

> Through-hole rather than 0805 so that **Rev A stays a board a beginner can
> actually assemble.**

That reason is gone. The decision is not, because two reasons survive that never
depended on skill:

- **Leads through plated holes hold better than two solder fillets** on a vehicle
  that vibrates, and these six are mandatory parts in the signal path.
- **A lead is something you can clip a probe to**, or desolder without hot air.

Board area is not scarce here, so keeping it costs nothing.

**What was updated is the sentence, not the footprint.** Leaving the old wording
in place would have been worse than either choice: the next reader — including
this one in three months — would find "through-hole so a beginner can solder it",
know perfectly well that a beginner is not soldering it, and conclude the reason
is false. **A stale justification invites the right decision to be undone for the
wrong reason.**

昨天选通孔的理由是"**让 Rev A 保持成一块新手真能装得起来的板**"。这个理由没了；决定还在，因为
还剩两条从来不依赖手艺的理由：引脚穿过镀铜孔，在会振动的车上比两个焊点结实，而这六个是信号路径上的
必装件；引脚还给了你夹表笔和不用热风枪拆件的余地。板子不缺面积，保留它不花钱。

**改的是那句话，不是那个封装。** 留着旧措辞比改成任何一种都糟：下一个读的人（包括三个月后的作者
本人）会看到"通孔是为了新手好焊"，心里清楚焊的根本不是新手，于是判定这条理由是假的。
**一条过期的理由，会让一个正确的决定因为一个错误的原因被推翻。**

### JLCPCB assembly is still declined — on narrower grounds / 贴片服务仍然不用，但理由窄了

[`fabrication.md`](../fabrication.md) argued against 嘉立创's PCBA service for
Stage 1 on four grounds, of which the last was decisive: *it would skip the one
thing this stage exists to teach.*

That ground no longer applies and has been withdrawn. The conclusion stands on
the other three — through-hole assembly carries more restrictions, costs more,
takes longer, and needs every part to come from LCSC's library, while the
workshop costs nothing and takes no schedule.

**Worth noticing that the conclusion did not have to change for the argument to
need fixing.** An argument with a dead premise still reaching the right answer is
the easiest kind of wrong text to leave lying around, because nothing downstream
looks broken.

原来反对用嘉立创贴片服务的理由有四条，最后一条是决定性的："它会跳过这个阶段存在的唯一目的"。
那条不再成立，已撤回；结论靠其余三条站着——通孔贴片限制多、更贵、更慢、料号必须来自立创商城，
而工具间不花钱也不占进度。

**值得注意的是：结论根本没变，但论证仍然需要修。** 一个前提已死、却依然得出正确答案的论证，
是最容易被留在原地的错误文本——**因为下游看起来没有任何东西是坏的。**

---

## What did not change / 没有变的东西

- The board, the schematic, the netlist, the values, the footprint plan.
- The one rule: **the rover must be drivable at the end of every session.**
- Who accepts the board.
- Who writes `bringup.md`, and who holds the multimeter while doing it.

板子、原理图、网表、阻值、封装计划都没动。唯一的铁律没动。**验收的人没变，写 `bringup.md` 的人
没变，上电时握着万用表的人也没变。**

## Files touched / 改了哪些文件

`README.md` · [`roadmap.md`](../roadmap.md) ·
[`tools-and-parts.md`](../tools-and-parts.md) ·
[`fabrication.md`](../fabrication.md) ·
[`stage1-signal-adapter/README.md`](../../hardware/stage1-signal-adapter/README.md) ·
[`stage1-signal-adapter/bom.md`](../../hardware/stage1-signal-adapter/bom.md)
