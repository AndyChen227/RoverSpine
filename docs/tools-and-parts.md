# Tools and Parts Log / 工具与零件记录

This file does two jobs:

1. **[The inventory](#inventory)** — everything the project needs, with its state,
   so "what do I still have to buy" has one answer in one place.
2. **[The dated log](#log)** — why each item was chosen, on the day it was chosen.

Items are added only after a real need is identified. **This is still not a wish
list** — everything below is traceable to a specific board or a specific
measurement.

这个文件做两件事：**[总账](#inventory)**——项目需要的全部东西及其状态，让"还要买什么"有
一个唯一的答案；**[按日期的记录](#log)**——每一件东西是在哪一天、为什么选的。

只有确认用途之后才加入。**这里依然不是愿望清单**——下面每一件都能追溯到某块具体的板子，
或者某个具体的测量。

<a id="inventory"></a>

## Inventory / 总账

State: ✅ have it · 🛒 ordered, in transit · ⬜ to buy · ❓ unknown — **needs Andy to fill in**

状态：✅ 已有 · 🛒 已下单在途 · ⬜ 待买 · ❓ 不确定——**需要你自己填**

### Software / 软件

| Item | Version | State | Needed from |
|---|---|:---:|:---:|
| KiCad | 10.0.6 | ✅ *(2026-09-08)* | Stage 0 |
| Git and GitHub | — | ✅ *(2026-09-11)* | Stage 0 |
| Pico SDK / arduino-pico / MicroPython toolchain | — | ⬜ | Stage 0 — all three, for [the language evaluation](roadmap.md#lang-eval) |

### Tools — Stage 0 / 工具，第 0 阶段

| Item | 工具 | Approx. ¥ | State |
|---|---|---:|:---:|
| Temperature-controlled soldering iron (T12 / 936) | 恒温烙铁 | 150–300 | ❓ |
| Multimeter, with continuity and **diode mode** | 万用表，要有蜂鸣档和**二极管档** | 100–200 | ❓ |
| Solder wire — **Sn63Pb37, 0.8 mm, rosin core** | 焊锡丝，含铅 0.8 mm 松香芯 | 25 | ❓ |
| No-clean rosin flux | 免洗松香助焊剂 | 15 | ❓ |
| Desoldering wick | 吸锡带 | 10 | ❓ |
| Tweezers, flush cutters | 镊子、斜口钳 | 25 | ❓ |
| Tip cleaner — brass wool or sponge | 清洁钢丝球或海绵 | 10 | ❓ |
| Soldering practice kit | 焊接练习板 | 20 | ⬜ |

> Leaded solder (Sn63Pb37) melts about 40 °C lower than lead-free and wets far
> more willingly. For learning, that difference is worth more than the
> lead-free purity. Wash your hands, and do not eat at the bench.
>
> 含铅焊锡（Sn63Pb37）比无铅的熔点低约 40 °C，上锡也听话得多。学焊接的阶段，这个差别
> 比"无铅"更重要。**焊完洗手，别在工作台上吃东西。**

### Stage 1 — the signal adapter / 第 1 阶段：信号转接板

Everything needed to get Rev A in hand and onto the rover. Details on the
connector choice are in [the next section](#connectors).

| # | Item | 零件 | Qty | Approx. ¥ | State |
|---:|---|---|---:|---:|:---:|
| 1 | PCB fabrication, 2-layer, 5 pcs | 打样，双层，5 片 | 1 order | 20–50 | ⬜ |
| 2 | Courier | 运费 | — | 10–20 | ⬜ |
| 3 | **2×20 male header for the Pi ribbon** — boxed (DC3-40P) preferred | **2×20 公座**，建议牛角座 | 1–2 | 3–8 | ⬜ |
| 4 | **2×5 male header for the D50A ribbon** — boxed (DC3-10P) preferred | **2×5 公座**，建议牛角座 | 1–2 | 1–3 | ⬜ |
| 5 | 0805 resistor assortment kit | 0805 电阻样品盒 | 1 | 15–30 | ⬜ — covers Stage 2 and beyond too |
| 6 | FC-10P 2×5 IDC ribbon, F–F, ≈35 cm | 10P IDC 排线，母对母 | 1 | ~10 | 🛒 *(selected 2026-09-11)* |
| 7 | Pi 40-pin GPIO ribbon, 2×20 F–F, 10–15 cm | 树莓派 40 针排线，母对母 | 1 | ~10 | 🛒 *(selected 2026-09-11)* |
| 8 | Small enclosure for the board | 小外壳 | 1 | 5–15 | ⬜ |
| 9 | Double-sided tape | 双面胶 | 1 | 5 | ⬜ |
| 10 | Cable ties / clips — **strain relief** | 扎带或线夹，**拉力缓解** | few | 5 | ⬜ |

> [!NOTE]
> Item 10 is not an afterthought. The README lists "keyed connectors, strain
> relief" as what this board adds — the connector is on the PCB, but the strain
> relief is a cable tie. Without it the ribbon's weight hangs on the connector,
> which is the failure mode this board exists to remove.
>
> 第 10 项不是可有可无。README 里写这块板增加的是"带锁扣连接器**与拉力缓解**"——连接器在
> 板上，拉力缓解是一根扎带。没有它，排线的重量全挂在连接器上，而那正是这块板本来要消除的
> 失效模式。

**Buy 5 pcs of the PCB** (the minimum order costs the same as one) and **two of
each header** — a spare costs a few ¥ and a botched desoldering costs an evening.

**板子买 5 片**（起订量和买 1 片一样钱），**排针每种买两个**——备件几块钱，拆坏一个要搭上
一个晚上。

### Firmware track / 固件线

| Item | Qty | Approx. ¥ | State | Needed from |
|---|---:|---:|:---:|:---:|
| Raspberry Pi Pico | **2** | 50 | ⬜ | Stage 0 — [language evaluation](roadmap.md#lang-eval) |
| Breadboard and jumper wires | 1 | 30 | ⬜ | Stage 0 |

### Deferred — buy at the stage that needs it / 推迟，到需要的阶段再买

| Item | 工具 | Approx. ¥ | Needed from |
|---|---|---:|:---:|
| **Bench supply with current limit** | **带限流的可调直流电源** | 200–400 | **Stage 2** — the first board that draws current |
| USB logic analyzer (8 ch) | USB 逻辑分析仪 | 30–80 | Stage 3 |
| Hot air station | 热风枪 | 200 | Stage 3 |
| Solder paste, steel stencil | 锡膏、钢网 | 50–100 | Stage 3, optional |
| Entry digital oscilloscope | 入门数字示波器 | 800+ | Stage 4 |

Stage 1 is passive copper with no power input of its own, so the bench supply is
not needed yet — **but buy it before the first board that draws current.**

第 1 阶段是纯被动铜板，自己不取电，所以台面电源还不需要——**但一定要在第一块真正吃电的板子
之前买到。**

### Running total / 累计

| Bucket | Approx. ¥ |
|---|---:|
| Software | 0 |
| Stage 0 tools | 350–600 |
| Stage 1 board, parts, cables | 75–165 |
| Firmware track (2 Picos + breadboard) | 80 |
| **To the end of Stage 1** | **≈ 500–850** |
| Stage 2 onward (bench supply first) | 200–400, then per the roadmap |

Against the roadmap's **¥2000–3000 for the year**, which still looks right.

对照路线图里"全年大约两三千"，目前看仍然成立。

<a id="connectors"></a>

## The connector decision / 连接器怎么选

Both ribbons are **female-to-female**, so the board needs **male** headers at
both positions. Two kinds are available at the same 2.54 mm pitch:

两条排线都是**母对母**，所以板上两个位置都要**公头**。同样 2.54 mm 间距，有两种可选：

| | Plain header / 光排针 | **Boxed header / 牛角座** |
|---|---|---|
| Part | 排针 2×20 / 2×5 | **DC3-40P / DC3-10P**（也叫简易牛角、IDC 公座） |
| Keyed? | ❌ No — the socket can be pushed on reversed | ✅ **Yes** — a notch in the shroud means one orientation only |
| Height | Low | Taller, bigger footprint — affects enclosure height |
| Cost | ¥1–2 | ¥2–5 |

**Recommendation: boxed headers.** Keying is not a nicety on this board — it is
the point. The README's own argument is that a detached or mis-inserted direction
pin is undefined motor behavior, and a reversed 2×5 ribbon swaps `PWM`/`INA`/`INB`
wholesale.

**建议用牛角座。** 防呆在这块板上不是锦上添花，而是这块板的意义本身。README 自己的论证就是
"方向线一旦脱落或插错，电机行为未定义"，而 2×5 排线插反会把 `PWM`/`INA`/`INB` 整组换位。

> [!WARNING]
> **Keying only protects your own end.** The Pi's 40-pin header and the D50A's
> 2×5 header are both plain unshrouded pins, so those ends can still be plugged
> in reversed or offset by a row. **Check the red stripe every single time.**
>
> **防呆只保得住自己这一端。** 树莓派的 40 针排针和 D50A 的 2×5 排针都是光针，那两端仍然
>可以插反或错开一排。**每次插之前都看红边。**

> [!IMPORTANT]
> **Verify before freezing footprints.** Standard IDC sockets mate with boxed
> headers, but confirm it with the cables in hand rather than assuming: check that
> the socket has the matching key bump, and that it seats fully. This is exactly
> what [the arrival checks](#arrival) are for. If the delivered cables turn out to
> be plain sockets with no key, fall back to plain headers and rely on the red
> stripe.
>
> **锁封装前先验证。** 标准 IDC 母座是能配牛角座的，但要拿到线实测确认，不要假设：看母座
> 上有没有对应的防呆凸起，以及能不能完全插到底。这正是[到货检查](#arrival)的用途。如果到货的
> 排线是没有防呆的光母座，就退回用光排针，靠红边。

<a id="log"></a>

## Dated log / 按日期的记录

### 2026-09-11 — Rev A cable selection / Rev A 排线选择

#### 1. 10P IDC ribbon cable / 10P IDC 排线

- Connector: 2×5 female to female / 2×5 母头对母头
- Pitch: 2.54 mm
- Length: about 35 cm / 约 35 cm
- Quantity: 1
- Search phrase: FC-10P 2x5 IDC 母对母 排线 35cm
- Purpose: flexible connection from the upper-deck adapter PCB to the lower-deck D50A motor driver / 从第二层转接板绕到第一层 D50A 驱动板
- Status: selected; waiting for delivery / 已选定，等待到货

#### 2. Raspberry Pi 40-pin GPIO ribbon cable / 树莓派 40 针 GPIO 排线

- Connector: 2×20 female to female / 2×20 母头对母头
- Pitch: 2.54 mm
- Length: 10–15 cm
- Quantity: 1
- Search phrase: 树莓派 40Pin GPIO 母对母 排线 15cm
- Purpose: connect the Raspberry Pi 5 to the adapter without stacking a PCB above the active cooler / 在不遮挡主动散热器的情况下连接树莓派与转接板
- Status: selected; waiting for delivery / 已选定，等待到货

### 2026-09-12 — Picos for the language evaluation / 用于语言评估的 Pico

The firmware language is [an explicit end-of-month-1 decision](roadmap.md#lang-eval)
made from a measurement, not from reading. These parts are what the measurement
needs.

固件语言改成[第 1 个月末根据实测做的决定](roadmap.md#lang-eval)，而不是读出来的判断。
这几件就是做这个实测所需要的东西。

#### 3. Raspberry Pi Pico × 2 / 树莓派 Pico ×2

- Quantity: **2** — the second one matters, see below / 数量 2，第二块很关键
- Approx. cost: ¥25 each, ¥50 total
- Purpose: write the same `blink` in each candidate language (C on the Pico SDK, C++ on arduino-pico, MicroPython) and decide from experience. The Pico carries the same RP2040 that goes on the Stage 3 board but needs **no PCB at all** / 用每个候选语言各写一遍同一个 blink，根据实际体验定语言。Pico 上的芯片和第 3 阶段板上要用的是同一颗，但它完全不需要 PCB
- **Why two:** the second one, flashed with `debugprobe` firmware, becomes an SWD debugger for the first. Embedded code has no REPL (except MicroPython) and a crash is usually a silent hang / 第二块刷 `debugprobe` 固件就是第一块的 SWD 调试器；嵌入式崩溃通常表现为静默死机，有调试器和没调试器是两个世界
- Status: not yet purchased / 尚未购买

#### 4. Breadboard and jumper wires / 面包板与跳线

- Approx. cost: ¥30
- Purpose: the firmware track runs on a breadboard from month 1, so Stage 3 becomes "move firmware that already works onto a board of my own" / 固件线从第 1 个月起就在面包板上跑，这样第 3 阶段变成"把已经跑通的固件搬到自己的板上"
- Status: not yet purchased / 尚未购买

### 2026-09-12 — Stage 1 shopping list and the connector decision / 第 1 阶段采购清单与连接器选择

The full Stage 1 list is in [the inventory](#inventory) above; the reasoning for
the boxed-header recommendation is in
[the connector decision](#connectors). Two items worth calling out because they
are easy to forget:

完整清单见上面的[总账](#inventory)，牛角座的理由见[连接器怎么选](#connectors)。
两项特别容易忘：

#### 5. Male headers, boxed / 公头，牛角座

- 2×20 (DC3-40P) × 2 and 2×5 (DC3-10P) × 2 — two of each, one as a spare
- Both ribbons are female-to-female, so the **board side must be male**
- Boxed rather than plain, for the key notch. **Confirm socket compatibility when the cables arrive** before freezing footprints
- Status: not yet purchased / 尚未购买

#### 6. Strain relief / 拉力缓解

- Cable ties or clips, a few, ≈¥5
- The README credits this board with "keyed connectors **and strain relief**". The connector is on the PCB; the strain relief is a cable tie. Without it, the ribbon's weight hangs on the connector — the exact failure this board exists to remove
- Status: not yet purchased / 尚未购买

<a id="arrival"></a>

## Arrival checks / 到货后检查

### The two cables / 两条排线

- Verify that both cables are truly female-to-female.
- Verify 2.54 mm pitch and keyed-plug orientation.
- **Check whether the sockets have the key bump that mates with a boxed header** — this decides item 5 above.
- Identify the red-stripe/pin-1 direction at both ends of both cables.
- Check continuity pin by pin **before either cable touches the rover**.
- Check the connector body size and clearance against the intended enclosure.

- 确认两条排线确实都是母对母。
- 确认 2.54 mm 间距以及防呆口方向。
- **确认母座上有没有和牛角座配对的防呆凸起**——这决定上面第 5 项怎么买。
- 确认两条线两端红边对应的 1 号针方向。
- **在任何一条排线接触小车之前**，先用万用表逐针检查导通关系。
- 对照打算用的外壳，确认连接器本体尺寸和空间。

### The bare PCB / 空板

- Photograph it before soldering anything — [`../photos/`](../photos/).
- Read the silkscreen at real size. If the labels are not legible, the board has failed at its one job.
- Continuity-check pin to pin against the signal map, before it touches the Pi.

- 焊之前先拍照。
- 按实际尺寸读一遍丝印。标注看不清，这块板就在它唯一的任务上失败了。
- 对照信号表逐针检查导通，在它接触树莓派之前。

---

See also: [`fabrication.md`](fabrication.md) — how the board gets made and
ordered · [`roadmap.md`](roadmap.md) — which stage needs what.
