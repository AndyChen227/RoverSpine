# Fabrication / 打样与下单

How a finished KiCad project becomes a board in your hand. This file is the
process; the parts and tools each board needs are in
[`tools-and-parts.md`](tools-and-parts.md).

一份画好的 KiCad 工程怎么变成手里的实体板。这个文件写流程，每块板需要什么零件和工具写在
[`tools-and-parts.md`](tools-and-parts.md)。

## The whole path / 整个流程

```text
KiCad: schematic → ERC → footprints → layout → DRC
  ↓
Export Gerber (.gbr) + drill files (.drl) → one .zip
  ↓
Check the zip yourself, in a Gerber viewer
  ↓
Upload to 嘉立创 → pick the options → pay
  ↓
24–48 h production + 1–3 days courier
  ↓
Board in hand. Commit the exact zip that was uploaded.
```

**Typical total: 3–5 days and ¥30–60 for a small two-layer board.** The slow part
is not the factory; it is your own drawing and checking.

**小板双层，通常 3–5 天、¥30–60。** 慢的不是工厂，是你自己画和检查那一段。

---

## 1 · What the factory actually needs / 工厂到底要什么

The factory does not read your schematic and does not open your KiCad project.
It accepts exactly two kinds of file:

| File | 是什么 | Count |
|---|---|---|
| **Gerber** (`.gbr`) | One image per layer — top copper, bottom copper, soldermask, silkscreen, and the **board outline** | 6–8 files |
| **Drill** (`.drl`) | Where every hole is, and how wide | 1–2 files |

In KiCad: **File → Fabrication Outputs → Gerbers…**, then **File → Fabrication
Outputs → Drill Files…**. Export both into the same empty folder, then zip that
folder's contents.

工厂不看原理图，也不打开 KiCad 工程，它只认两种文件：**Gerber**（每一层的图形，包括
**板子外形层**）和**钻孔文件**。KiCad 里的路径是**文件 → 制造输出 → Gerber 文件**，然后
**文件 → 制造输出 → 钻孔文件**，导到同一个空文件夹，再把里面的文件打包成一个 `.zip`。

> [!TIP]
> 嘉立创 has a KiCad plugin that reads the project directly. **Learn the Gerber
> path first anyway** — Gerber is the industry's common language, so it works at
> any factory with any EDA tool. The plugin only works at one factory.
>
> 嘉立创有能直接读 KiCad 工程的插件，但**第一次还是走 Gerber 这条路**。Gerber 是行业通用
> 语言，换工厂、换软件都能用；插件只在一家工厂好用。

---

## 2 · Check it yourself, before uploading / 上传前自己检查

> [!CAUTION]
> **The factory does not check your netlist.** It manufactures exactly what you
> send, faithfully, including your mistakes — and then charges you for them. The
> entire checking burden is yours.
>
> **工厂不检查你的网表。** 它一丝不差地做出你发过去的东西，包括你的错误，然后照常收钱。
> **检查的责任 100% 在你。**

- [ ] **ERC passes** with zero errors.
- [ ] **Every net compared against the net structure**, one by one, by [the checker](../hardware/stage1-signal-adapter/tools/README.md) rather than by reading. ERC checks electrical rules; it does not know that GPIO12 was supposed to go to `PWM1`, and it stays silent if two signals are swapped onto each other's pins.
- [ ] **DRC passes** with zero errors.
- [ ] **Open the exported Gerbers in a separate viewer** — KiCad ships GerbView — and step through the layers one at a time. This is what catches "the outline layer never got exported" and "the silkscreen is missing", which are invisible inside the PCB editor.
- [ ] **The board outline (`Edge.Cuts`) is a closed shape.** If it is not closed, the factory does not know what shape to cut.
- [ ] **The drill file's holes line up with the pads** you placed.
- [ ] **Silkscreen is legible** at real size — zoom in on that layer specifically.

- [ ] ERC 零错误。
- [ ] **逐条网络与网络结构核对**，用[脚本](../hardware/stage1-signal-adapter/tools/README.md)跑，不要用眼睛读。ERC 查的是电气规则，它不知道 GPIO12 本该接到 `PWM1`，两个信号互换了它也一声不响。
- [ ] DRC 零错误。
- [ ] **用单独的 Gerber 查看器打开导出的文件**（KiCad 自带 GerbView），一层一层翻。这一步专门抓"外形层没导出""丝印层漏了"——这类错误在 PCB 编辑器里看不出来。
- [ ] **外形层必须闭合**，不闭合工厂就不知道该切成什么形状。
- [ ] 钻孔文件里的孔和你放的焊盘对得上。
- [ ] **丝印按实际尺寸看得清**——专门放大这一层检查。

---

## 3 · Ordering at 嘉立创 / 在嘉立创下单

[jlc.com](https://www.jlc.com) → PCB 打样 → upload the zip. It auto-detects the
layer count and board size, then asks for the options below.

Chinese accounts need **实名认证** (ID verification) before the first order — do
it in advance rather than at checkout.

嘉立创需要**实名认证**才能下第一单，提前弄好，别等到付款时才发现。

### Default options for a small logic board / 小信号板的默认选项

These are the settings for Stage 1 and Stage 2. Later boards differ — see
[per-stage differences](#per-stage) below.

| Option | 选项 | Pick | Why |
|---|---|---|---|
| Layers | 层数 | **2** | Enough for signals |
| Size | 尺寸 | auto-detected — **keep it under 100 × 100 mm** | Price jumps to the next tier above that |
| Quantity | 数量 | **5** | The minimum order is usually 5 and costs the same as 1. You will want spares |
| Thickness | 板厚 | **1.6 mm** | Standard, and stiff enough to take connector insertion force |
| Soldermask colour | 阻焊颜色 | **green / 绿色** | Cheapest and fastest. Other colours can cost more or add days |
| Surface finish | 表面处理 | **HASL / 喷锡** | Easiest to hand-solder. ENIG (沉金) is for fine-pitch SMD and costs more |
| Copper weight | 铜厚 | **1 oz / 35 µm** | Fine for signal currents |
| Impedance control, panelization, SMT assembly | 阻抗、拼板、SMT 贴片 | **none** | Through-hole board, soldered by hand |

### Cost and lead time / 钱和时间

| | Approx. |
|---|---|
| 2-layer, ≤100 × 100 mm, 5 pcs | **¥20–50** — new-customer coupons are common; check at order time, promotions change |
| Courier | **¥10–20** |
| Production | **24–48 h** |
| Delivery | 1–3 days |

Other fabs exist (华秋, PCBWay, JLCPCB's international site) and the Gerber zip
works at all of them. 嘉立创 is the default here on price and speed within China.

其他工厂也能做（华秋、PCBWay、JLCPCB 国际站），同一个 Gerber 压缩包都能用。国内按价格和
速度，嘉立创是默认选择。

---

## 4 · Design rules that keep the price low / 让价格留在便宜档的设计规则

Set these in KiCad **before** starting layout, so DRC enforces them for you
instead of arguing with you afterwards.

| Rule | 规则 | Value | Why |
|---|---|---|---|
| Trace width, signals | 信号线宽 | **0.3–0.5 mm** | The cheap process can do 0.127 mm, but a logic board does not need the limit. Wider is cheaper, more robust, and easier to rework |
| Clearance | 间距 | **≥ 0.3 mm** | Same reasoning |
| Via hole / annular ring | 过孔 / 环宽 | **0.3 mm / 0.6 mm** | Comfortably inside every factory's standard capability |
| Silkscreen text height | 丝印字高 | **≥ 1 mm** | Below this the factory cannot print it legibly |
| Silkscreen line width | 丝印笔画宽 | **≥ 0.15 mm** | Thinner strokes smear or drop out |

> [!IMPORTANT]
> **Silkscreen rules matter more on this project than on most.** Stage 1 exists
> specifically so that every connector is labelled — if the silkscreen comes back
> unreadable, the board has failed at its one job. Check that layer at real scale
> before ordering, and again on the bare board when it arrives.
>
> **丝印规则对这个项目比对别人重要。** 第 1 阶段存在的理由就是"每个接口都有清楚的标注"——
> 如果丝印印出来看不清，这块板就在它唯一的任务上失败了。下单前按实际尺寸检查这一层，
> 空板到货后再检查一次。

<a id="per-stage"></a>

## 5 · What changes per stage / 各阶段的差异

| Stage | Board | What changes from the defaults |
|:---:|---|---|
| **1** | Passive signal adapter | Nothing — the defaults above *are* this board. Through-hole as built: the 6 series resistors are through-hole axial parts and **must be populated**, and only the 6 reserved 0805 pull-down pads may ship empty |
| **2** | Signal & status board | Nothing in the order, but the first 0805 parts that are definitely populated — deliberately large, still hand-solderable with a plain iron |
| **3** | RP2040 co-processor | Denser SMD. **ENIG (沉金) is worth considering** for flatter pads under hot air. A **steel stencil (钢网)** becomes useful if using solder paste |
| **4** | Power board | **2 oz copper**, wide pours, thermal vias. Layout matters more than options: keep the switching loop physically tiny |
| **5** | Motor driver | **2 oz copper or heavier**, with trace widths sized from the **measured** stall current — not from the datasheet's optimism |
| **6** | Integration | **4 layers.** Costs more and takes longer. Impedance control still not needed |

第 1、2 阶段完全用上面的默认值；第 3 阶段 SMD 变密，可以考虑沉金和钢网；第 4、5 阶段要把
**铜厚加到 2 oz**，线宽按**实测的堵转电流**算，而不是按数据手册的乐观值；第 6 阶段是四层板。

---

## 6 · After it arrives / 板子到货之后

### What arrives / 到货的是什么

A **bare board** — plated holes, soldermask, silkscreen, and nothing else. **Every
component is soldered on by you.**

嘉立创 does offer SMT/PCBA assembly, but for Stage 1 it is the wrong trade:
through-hole parts carry more restrictions, cost more, take longer, and require
every part to come from LCSC's library — and decisively, it would skip the one
thing this stage exists to teach. It is worth reconsidering from Stage 3, where
the parts get dense and fine-pitch.

到货的是一块**光板**：镀铜的孔、阻焊层、丝印，别的什么都没有。**所有元件都由你自己焊上去。**

嘉立创确实有 SMT 贴片 / PCBA 服务，但第 1 阶段用它是笔亏本的交易：通孔件限制多、更贵、更慢，
元件还必须用立创商城库里的料号——而最关键的是，**它会跳过这个阶段存在的唯一目的**。
到第 3 阶段元件变密、封装变小，那时候再考虑才有意义。

### The steps / 步骤

1. **Photograph the bare board** before soldering anything. A photo of the bare board is what lets you check a footprint or a trace later without desoldering. Photos go in [`../photos/`](../photos/).
2. **Continuity-check the bare board** against the signal map, pin to pin, with the multimeter — before it touches the Pi.
3. **Solder** — see [the assembly order](#assembly) below. Photograph again, assembled.
4. **Write `bringup.md` during first power-up, not afterwards.** Current draw, measured voltages, and every surprise, while you still remember what you actually did.
5. **Commit the exact zip that was uploaded**, as `hardware/<board>/fab/revA.zip`.

> [!IMPORTANT]
> Rule 1 of [`hardware/README.md`](../hardware/README.md): commit the zip you
> actually uploaded. Regenerating Gerbers later from a modified project gives you
> files that were never manufactured, which makes debugging the physical board in
> your hand impossible.
>
> 提交**真正上传的那个压缩包**。以后从改过的工程重新导出，得到的是从来没被制造过的文件，
> 那样就没法排查手里这块实体板了。

1. 焊之前先拍**空板照片**——以后核对封装或走线时不用拆元件。照片放 [`../photos/`](../photos/)。
2. 空板先用万用表**逐针核对导通**，在它接触树莓派之前。
3. 焊接，焊完再拍一组。
4. **`bringup.md` 在第一次上电的过程中写，不是事后补。**
5. **提交真正上传的那个 Gerber 压缩包。**

<a id="assembly"></a>

### Assembly order / 焊接顺序

> **Shortest parts first, tallest last. SMD before through-hole.**
>
> **先矮后高，先贴片后通孔。**

Once a tall boxed header is on the board, the board no longer lies flat on the
bench — and every low pad still to be soldered becomes awkward to reach. For
Stage 1 the order is:

一旦高的牛角座焊上去，板子就没法平放在桌面上了，剩下的矮焊盘会变得很难焊。
第 1 阶段的顺序是：

```text
0805 pull-downs  →  axial series resistors  →  2×5 boxed header  →  2×20 boxed header
0805 下拉电阻     →  通孔串联电阻              →  2×5 牛角座          →  2×20 牛角座
```

> [!IMPORTANT]
> **Decide about the pull-downs before the first joint, not after.** Leaving
> them for later is electrically fine — the pads stay on the board and take a
> resistor any time. It is *physically* much harder: by then the 2×20 header is
> on, the board will not lie flat, and you are holding it with one hand while
> soldering an 0805 with the other. So populate them or deliberately skip them.
> "Leave it for now" is the option that costs the most.
>
> **下拉焊不焊，要在第一个焊点之前决定，不是之后。** 留到以后在电气上没问题——焊盘一直
> 在板上，随时能焊。但在**物理上**难得多：那时 2×20 牛角座已经上去，板子放不平，你得
> 一手扶着板、一手焊 0805。所以要么焊掉，要么有意识地决定不焊；**"先放着以后说"是代价
> 最大的那个选项。**

Joint count for Stage 1 Rev A / 第 1 阶段 Rev A 的焊点数：

| Part | 焊点 | |
|---|---:|---|
| 2×20 header | 40 | required |
| 2×5 header | 10 | required |
| `R1`–`R6` series, through-hole / 通孔串阻 | 12 | **required** — in the signal path |
| `R7`–`R12` pull-downs, 0805 / 下拉 | 12 | optional on Rev A |
| **Total** | **62–74** | |

Twenty to thirty minutes once you are practised; an hour the first time is
normal. **Practise 30–50 joints on a practice kit before touching a real board** —
that is Stage 0's exit criterion: a joint you are willing to put on a moving
vehicle.

熟练后 20–30 分钟，第一次花一个小时也正常。**在碰真板子之前，先在练习板上焊 30–50 个焊点**
——这是第 0 阶段的完成判据：能做出一个你愿意装到运动的车上的焊点。

### Soldering a long header straight / 长排针怎么焊得不歪

A crooked header will not accept the ribbon, or accepts it under stress. The
technique is to make the first two joints rescuable:

排针歪了插不进排线，或者插进去带着应力。手法的核心是：让最初两个焊点还救得回来。

1. Insert the header, flip the board over.
2. **Solder only two diagonally opposite pins** — pin 1 and pin 40.
3. **Flip back and check that it is square.** If it leans, reheat those two joints and push it straight.
4. **Only then** solder the remaining pins.

1. 排针插进孔里，板子翻过来。
2. **只焊对角两个引脚**——第 1 脚和第 40 脚。
3. **翻过来检查垂不垂直。** 歪了就重新加热那两个焊点，把它推正。
4. **正了之后**，再焊剩下的引脚。

> The whole point is step 3. With two pins soldered it can still be rescued; with
> ten it cannot.
>
> 全部意义都在第 3 步：**焊了两个脚还能救，焊了十个脚就救不回来了。**

> [!TIP]
> **0805 needs only an iron — no hot air.** That is exactly why the roadmap picks
> 0805 rather than something smaller: "deliberately large". The hot air station is
> not needed until Stage 3.
>
> **0805 用普通烙铁就能焊，不需要热风枪。** 这正是路线图刻意选 0805 而不是更小封装的原因
> （"deliberately large"）。热风枪要到第 3 阶段才需要。

## 7 · Expect a revision / 预期要改版

Every stage in [the roadmap](roadmap.md) budgets for at least one revision, and
Stage 3 and Stage 5 budget for two or three. This is normal. A revision is never
overwritten — Rev B sits next to Rev A, because the whole point of keeping A is
being able to see what changed and why.

[路线图](roadmap.md)里每个阶段都预留了至少改一版，第 3 和第 5 阶段预留两三版。**这是正常的。**
改版不覆盖旧版：B 版和 A 版并排放着，因为留下 A 版的全部意义就是能看出改了什么、为什么改。
