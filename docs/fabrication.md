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
- [ ] **Every net manually compared against the signal map**, one by one. ERC checks electrical rules; it does not know that GPIO12 was supposed to go to `PWM1`.
- [ ] **DRC passes** with zero errors.
- [ ] **Open the exported Gerbers in a separate viewer** — KiCad ships GerbView — and step through the layers one at a time. This is what catches "the outline layer never got exported" and "the silkscreen is missing", which are invisible inside the PCB editor.
- [ ] **The board outline (`Edge.Cuts`) is a closed shape.** If it is not closed, the factory does not know what shape to cut.
- [ ] **The drill file's holes line up with the pads** you placed.
- [ ] **Silkscreen is legible** at real size — zoom in on that layer specifically.

- [ ] ERC 零错误。
- [ ] **逐条网络和信号表人工核对。** ERC 查的是电气规则，它不知道 GPIO12 本该接到 `PWM1`。
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
| **1** | Passive signal adapter | Nothing. The defaults above are exactly this board |
| **2** | Signal & status board | Nothing, but first 0805 SMD pads — deliberately large, still hand-solderable |
| **3** | RP2040 co-processor | Denser SMD. **ENIG (沉金) is worth considering** for flatter pads under hot air. A **steel stencil (钢网)** becomes useful if using solder paste |
| **4** | Power board | **2 oz copper**, wide pours, thermal vias. Layout matters more than options: keep the switching loop physically tiny |
| **5** | Motor driver | **2 oz copper or heavier**, with trace widths sized from the **measured** stall current — not from the datasheet's optimism |
| **6** | Integration | **4 layers.** Costs more and takes longer. Impedance control still not needed |

第 1、2 阶段完全用上面的默认值；第 3 阶段 SMD 变密，可以考虑沉金和钢网；第 4、5 阶段要把
**铜厚加到 2 oz**，线宽按**实测的堵转电流**算，而不是按数据手册的乐观值；第 6 阶段是四层板。

---

## 6 · After it arrives / 板子到货之后

1. **Photograph the bare board** before soldering anything. A photo of the bare board is what lets you check a footprint or a trace later without desoldering. Photos go in [`../photos/`](../photos/).
2. **Continuity-check the bare board** against the signal map, pin to pin, with the multimeter — before it touches the Pi.
3. Solder. Photograph again, assembled.
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

## 7 · Expect a revision / 预期要改版

Every stage in [the roadmap](roadmap.md) budgets for at least one revision, and
Stage 3 and Stage 5 budget for two or three. This is normal. A revision is never
overwritten — Rev B sits next to Rev A, because the whole point of keeping A is
being able to see what changed and why.

[路线图](roadmap.md)里每个阶段都预留了至少改一版，第 3 和第 5 阶段预留两三版。**这是正常的。**
改版不覆盖旧版：B 版和 A 版并排放着，因为留下 A 版的全部意义就是能看出改了什么、为什么改。
