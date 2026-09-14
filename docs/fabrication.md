# Fabrication

How a board goes from KiCad to a physical part on the rover.

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

Typical total for a small two-layer board: **3–5 days, ¥30–60.**

---

## 1 · What the factory needs

The factory does not read the schematic and does not open the KiCad project. It
accepts two kinds of file:

| File | Contents | Count |
|---|---|---|
| **Gerber** (`.gbr`) | One image per layer — top copper, bottom copper, soldermask, silkscreen, and the **board outline** | 6–8 |
| **Drill** (`.drl`) | Where every hole is, and how wide | 1–2 |

**File → Fabrication Outputs → Gerbers…**, then **Drill Files…**. Export both
into the same empty folder and zip that folder's contents.

嘉立创 has a KiCad plugin that reads the project directly. Use the Gerber path
anyway: Gerber works at any factory with any EDA tool; the plugin works at one.

## 2 · Check it yourself, before uploading

The factory manufactures exactly what you send, including your mistakes, and
charges you for them. The whole checking burden is yours.

- [ ] **ERC run from the command line**, with every violation accounted for and
      the count matching the number written down in advance. For Rev A that is
      **30 errors / 0 warnings** — the 30 unused pins on the 2×20 header. "Zero
      errors" is the wrong target and a weaker one: zero is always reachable by
      setting rules to `ignore`.
- [ ] **Every net and every footprint compared** against the map by
      [the checker](../hardware/stage1-signal-adapter/tools/README.md), not by
      reading. ERC does not know that GPIO12 was meant to reach `PWM1`, and stays
      silent if two signals are swapped onto each other's pins.
- [ ] **DRC passes** with zero errors.
- [ ] **Open the exported Gerbers in a separate viewer** — KiCad ships GerbView —
      and step through the layers one at a time. This catches "the outline layer
      never got exported" and "the silkscreen is missing", which are invisible
      inside the PCB editor.
- [ ] **The board outline (`Edge.Cuts`) is a closed shape.**
- [ ] **The drill file's holes line up with the pads.**
- [ ] **Silkscreen is legible at real size** — zoom in on that layer specifically.

## 3 · Ordering at 嘉立创

[jlc.com](https://www.jlc.com) → PCB 打样 → upload the zip. It auto-detects layer
count and board size, then asks for the options below. Chinese accounts need
**实名认证** before the first order; do it in advance.

| Option | Pick | Why |
|---|---|---|
| Layers | **2** | Enough for signals |
| Size | **under 100 × 100 mm** | Price jumps to the next tier above that |
| Quantity | **5** | Minimum order, same price as 1 |
| Thickness | **1.6 mm** | Standard, stiff enough for connector insertion force |
| Soldermask | **green** | Cheapest and fastest |
| Surface finish | **HASL** | Easiest to hand-solder; ENIG is for fine-pitch SMD |
| Copper weight | **1 oz / 35 µm** | Fine for signal currents |
| Impedance control, panelization, SMT | **none** | Through-hole board, soldered by hand |

| | Approx. |
|---|---|
| 2-layer, ≤100 × 100 mm, 5 pcs | **¥20–50** |
| Courier | **¥10–20** |
| Production | **24–48 h** |
| Delivery | 1–3 days |

华秋, PCBWay and JLCPCB's international site take the same Gerber zip. 嘉立创 is
the default here on price and speed within China.

## 4 · Design rules

Set these in KiCad **before** starting layout, so DRC enforces them.

| Rule | Value |
|---|---|
| Trace width, signals | **0.3–0.5 mm** |
| Clearance | **≥ 0.3 mm** |
| Via hole / outer diameter | **0.3 mm / 0.6 mm** |
| Silkscreen text height | **≥ 1 mm** |
| Silkscreen line width | **≥ 0.15 mm** |

The cheap process can do 0.127 mm traces. A logic board does not need the limit,
and wider is more robust and easier to rework.

**Silkscreen rules matter more here than on most projects.** Stage 1 exists so
that every connector is labelled; an unreadable silkscreen means the board failed
at its one job. Check that layer at real scale before ordering, and again on the
bare board.

<a id="per-stage"></a>

## 5 · What changes per stage

| Stage | Board | Change from the defaults |
|:---:|---|---|
| **1** | Passive signal adapter | None. The 6 series resistors are through-hole and must be populated; only the 6 pull-down pads may ship empty |
| **2** | Signal & status board | None in the order. First 0805 parts that are definitely populated |
| **3** | RP2040 co-processor | Denser SMD. **ENIG** worth considering; a **steel stencil** if using solder paste |
| **4** | Power board | **2 oz copper**, wide pours, thermal vias. Keep the switching loop physically tiny |
| **5** | Motor driver | **2 oz copper or heavier**, trace widths from the **measured** stall current |
| **6** | Integration | **4 layers.** Impedance control still not needed |

## 6 · After it arrives

What arrives is a **bare board** — plated holes, soldermask, silkscreen, nothing
else. Assembly is done in the home workshop, not by the author. 嘉立创's PCBA
service is not used for Stage 1: through-hole assembly carries more restrictions,
costs more, takes longer, and needs every part to come from LCSC's library. Worth
reconsidering from Stage 3.

### The steps

1. **Photograph the bare board** before soldering anything. Photos go in
   [`../photos/`](../photos/).
2. **Continuity-check the bare board** against the signal map, pin to pin, before
   it touches the Pi.
3. **Hand it over for assembly** with [the four requirements](#assembly).
4. **Inspect what comes back, before anything else.** Joints shiny and concave,
   wetting both pad and lead; no bridges, especially across the 0805 pads and
   between adjacent header pins; both boxed headers square to the board.
5. **Re-run continuity on the assembled board**, adding what the bare board could
   not show: Pi-side to driver-side reads ≈33 Ω, and each pull-down reads ≈10 kΩ
   to `GND` or open. Photograph again, assembled.
6. **Write `bringup.md` during first power-up, not afterwards.** Current draw,
   measured voltages, and every surprise.
7. **Commit the exact zip that was uploaded**, as `hardware/<board>/fab/revA.zip`.
   Regenerating Gerbers later from a modified project gives files that were never
   manufactured.

<a id="assembly"></a>

### Assembly order

> **Shortest parts first, tallest last. SMD before through-hole.**

```text
0805 pull-downs → axial series resistors → 2×5 boxed header → 2×20 boxed header
```

Once a tall boxed header is on, the board no longer lies flat and every low pad
still to be soldered becomes awkward to reach.

**Decide about the pull-downs before the first joint.** Leaving them for later is
electrically fine but physically much harder, and assembly happens elsewhere, so
"later" means a second trip to the workshop.

| Part | Joints | |
|---|---:|---|
| 2×20 header | 40 | required |
| 2×5 header | 10 | required |
| `R1`–`R6` series, through-hole | 12 | **required** — in the signal path |
| `R7`–`R12` pull-downs, 0805 | 12 | optional on Rev A |
| **Total** | **62–74** | 20–30 minutes for someone practised |

**The four requirements to hand over with the board.** None is general soldering
advice; all four are specific to this board.

1. **Shortest parts first, tallest last**, in the order above.
2. **Both boxed headers square to the board.** A leaning header will not accept
   the ribbon, or accepts it under permanent stress.
3. **Whether `R7`–`R12` are populated is decided before the first joint.**
4. **Nothing gets substituted.** 33 Ω and 10 kΩ are values in a checked netlist.

### Soldering a long header straight

1. Insert the header, flip the board over.
2. **Solder only two diagonally opposite pins** — pin 1 and pin 40.
3. **Flip back and check that it is square.** If it leans, reheat those two
   joints and push it straight.
4. **Only then** solder the remaining pins.

Step 3 is the one that matters: two pins can still be rescued, ten cannot.

0805 needs only an iron — no hot air. That is why the roadmap picks 0805 rather
than something smaller. A hot air station is not needed until Stage 3.

## 7 · Expect a revision

Every stage in [the roadmap](roadmap.md) budgets for at least one revision;
Stages 3 and 5 budget for two or three. A revision is never overwritten — Rev B
sits next to Rev A.

---

# 打样与下单 / 中文

一块板从 KiCad 到装上车的完整路径。

```text
KiCad：原理图 → ERC → 封装 → 布局 → DRC
  ↓
导出 Gerber（.gbr）+ 钻孔文件（.drl）→ 打包成一个 .zip
  ↓
自己用 Gerber 查看器检查这个压缩包
  ↓
上传到嘉立创 → 选项目 → 付款
  ↓
24–48 小时生产 + 1–3 天快递
  ↓
板子到手。提交真正上传的那个压缩包。
```

小板双层通常 **3–5 天、¥30–60**。

---

## 1 · 工厂要什么

工厂不看原理图，也不打开 KiCad 工程，只认两种文件：

| 文件 | 内容 | 数量 |
|---|---|---|
| **Gerber**（`.gbr`） | 每一层的图形——顶层铜、底层铜、阻焊、丝印，以及**板子外形层** | 6–8 个 |
| **钻孔**（`.drl`） | 每个孔在哪、多大 | 1–2 个 |

**文件 → 制造输出 → Gerber 文件**，再**钻孔文件**。两者导到同一个空文件夹，把里面的文件
打包成一个 `.zip`。

嘉立创有能直接读 KiCad 工程的插件。仍然走 Gerber 这条路：Gerber 换工厂换软件都能用，
插件只在一家工厂能用。

## 2 · 上传前自己检查

工厂一丝不差地做出你发过去的东西，包括你的错误，然后照常收钱。**检查的责任 100% 在你。**

- [ ] **用命令行跑 ERC**，每一条违规都有账，而且数量和事先写下的那个数对得上。Rev A 是
      **30 错误 / 0 警告**——2×20 排针上 30 个没用到的引脚。目标不是"零错误"，"零"反而更松：
      把规则设成 `ignore` 随时能到零。
- [ ] **每条网络、每个封装都用[脚本](../hardware/stage1-signal-adapter/tools/README.md)比对**，
      不要用眼睛读。ERC 不知道 GPIO12 本该接到 `PWM1`，两个信号互换了它也一声不响。
- [ ] **DRC 零错误。**
- [ ] **用单独的 Gerber 查看器打开导出的文件**（KiCad 自带 GerbView），一层一层翻。这一步
      专门抓"外形层没导出""丝印层漏了"——这类错误在 PCB 编辑器里看不出来。
- [ ] **外形层（`Edge.Cuts`）必须闭合。**
- [ ] **钻孔文件里的孔和焊盘对得上。**
- [ ] **丝印按实际尺寸看得清**——专门放大这一层检查。

## 3 · 在嘉立创下单

[jlc.com](https://www.jlc.com) → PCB 打样 → 上传压缩包。它会自动识别层数和板子尺寸，
然后问下面这些选项。国内账号需要**实名认证**才能下第一单，提前弄好。

| 选项 | 选什么 | 理由 |
|---|---|---|
| 层数 | **2** | 信号够用 |
| 尺寸 | **控制在 100 × 100 mm 以内** | 超过就跳到下一个价格档 |
| 数量 | **5** | 起订量，和做 1 片一个价 |
| 板厚 | **1.6 mm** | 标准，够硬，扛得住插拔力 |
| 阻焊颜色 | **绿色** | 最便宜最快 |
| 表面处理 | **喷锡 HASL** | 手焊最容易；沉金是给细间距 SMD 的 |
| 铜厚 | **1 oz / 35 µm** | 信号电流够用 |
| 阻抗控制、拼板、SMT 贴片 | **都不要** | 通孔板，手工焊 |

| | 大约 |
|---|---|
| 双层，≤100 × 100 mm，5 片 | **¥20–50** |
| 运费 | **¥10–20** |
| 生产 | **24–48 小时** |
| 快递 | 1–3 天 |

华秋、PCBWay、JLCPCB 国际站都能用同一个 Gerber 压缩包。国内按价格和速度，嘉立创是默认选择。

## 4 · 设计规则

布局**开始之前**就在 KiCad 里设好，让 DRC 替你把关。

| 规则 | 取值 |
|---|---|
| 信号线宽 | **0.3–0.5 mm** |
| 间距 | **≥ 0.3 mm** |
| 过孔孔径 / 外径 | **0.3 mm / 0.6 mm** |
| 丝印字高 | **≥ 1 mm** |
| 丝印笔画宽 | **≥ 0.15 mm** |

便宜档的工艺能做到 0.127 mm 线宽。逻辑板不需要贴着极限走，宽一点更结实、也更好返修。

**丝印规则对这个项目比对别人重要。** 第 1 阶段存在的理由就是每个接口都有清楚的标注；
丝印印出来看不清，这块板就在它唯一的任务上失败了。下单前按实际尺寸检查这一层，
空板到货后再检查一次。

## 5 · 各阶段的差异

| 阶段 | 板子 | 与默认值的差异 |
|:---:|---|---|
| **1** | 被动信号转接板 | 无。6 个串阻是通孔件且必须焊上，只有 6 个下拉焊盘可以空着 |
| **2** | 信号与状态板 | 下单选项无变化。第一次出现必焊的 0805 件 |
| **3** | RP2040 协处理器 | SMD 变密。可以考虑**沉金**；用锡膏的话**钢网**有用 |
| **4** | 电源板 | **铜厚 2 oz**、大面积铺铜、散热过孔。开关回路要在物理上做小 |
| **5** | 电机驱动板 | **2 oz 铜或更厚**，线宽按**实测的**堵转电流算 |
| **6** | 集成板 | **四层板。** 仍然不需要阻抗控制 |

## 6 · 板子到货之后

到货的是一块**光板**：镀铜的孔、阻焊层、丝印，别的什么都没有。焊接在家里的工具间完成，
不由作者本人做。第 1 阶段不用嘉立创的 PCBA 服务：通孔贴片限制多、更贵、更慢，而且元件必须
用立创商城的料号。从第 3 阶段起值得重新考虑。

### 步骤

1. 焊之前先拍**空板照片**。照片放 [`../photos/`](../photos/)。
2. 空板先用万用表**逐针核对导通**，在它接触树莓派之前。
3. **连同[那四条要求](#assembly)一起交出去焊。**
4. **焊回来先验收，别的都往后放。** 焊点又亮又凹、焊盘和引脚都吃上锡；没有连锡，尤其是
   0805 焊盘之间和排针相邻针之间；两个牛角座和板面垂直。
5. **在焊好的板上重跑一次导通检查**，并加上空板查不出来的两项：Pi 侧到驱动侧应读到约
   33 Ω，每个下拉对 `GND` 约 10 kΩ 或断路。然后再拍一组装配后的照片。
6. **`bringup.md` 在第一次上电的过程中写，不是事后补。** 记电流、实测电压和每一个意外。
7. **提交真正上传的那个压缩包**，放在 `hardware/<board>/fab/revA.zip`。以后从改过的工程
   重新导出，得到的是从来没被制造过的文件。

### 焊接顺序

> **先矮后高，先贴片后通孔。**

```text
0805 下拉电阻 → 通孔串联电阻 → 2×5 牛角座 → 2×20 牛角座
```

高的牛角座一旦焊上，板子就没法平放，剩下的矮焊盘会变得很难焊。

**下拉焊不焊，要在第一个焊点之前决定。** 留到以后在电气上没问题，但物理上难得多；
而且焊接在别处完成，"以后"意味着再跑一趟工具间。

| 件 | 焊点 | |
|---|---:|---|
| 2×20 牛角座 | 40 | 必焊 |
| 2×5 牛角座 | 10 | 必焊 |
| `R1`–`R6` 通孔串阻 | 12 | **必焊**——在信号路径上 |
| `R7`–`R12` 0805 下拉 | 12 | Rev A 可选 |
| **合计** | **62–74** | 熟练的人 20–30 分钟 |

**随板交接的四条要求。** 没有一条是通用焊接常识，四条都只属于这块板：

1. **先矮后高**，按上面的顺序。
2. **两个牛角座必须与板面垂直。** 歪了插不进排线，或者插进去长期带着应力。
3. **`R7`–`R12` 焊不焊，在第一个焊点之前定下。**
4. **不许替换任何元件。** 33 Ω 和 10 kΩ 是过了网表核对的值。

### 长排针怎么焊得不歪

1. 排针插进孔里，板子翻过来。
2. **只焊对角两个引脚**——第 1 脚和第 40 脚。
3. **翻过来检查垂不垂直。** 歪了就重新加热那两个焊点，把它推正。
4. **正了之后**，再焊剩下的引脚。

关键在第 3 步：**焊了两个脚还能救，焊了十个脚就救不回来了。**

0805 用普通烙铁就能焊，不需要热风枪。这正是路线图选 0805 而不是更小封装的原因。
热风枪要到第 3 阶段才需要。

## 7 · 预期要改版

[路线图](roadmap.md)里每个阶段都预留了至少改一版，第 3 和第 5 阶段预留两三版。
改版不覆盖旧版：B 版和 A 版并排放着。
