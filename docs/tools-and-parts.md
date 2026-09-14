# Tools and Parts

Everything the project needs, with its state, so "what do I still have to buy"
has one answer in one place. Items are added only after a real need is
identified — everything below is traceable to a specific board or a specific
measurement. **This is not a wish list.**

Why each item was chosen, and on which day, is in [the devlog](devlog/).

State: ✅ have it · 🛒 ordered, in transit · ⬜ to buy

<a id="inventory"></a>

## Inventory

### Software

| Item | Version | State | Needed from |
|---|---|:---:|:---:|
| KiCad | 10.0.6 | ✅ | Stage 0 |
| Git and GitHub | — | ✅ | Stage 0 |
| Pico SDK / arduino-pico / MicroPython | — | ⬜ | Stage 0 — all three, for [the language evaluation](roadmap.md#lang-eval) |

### Tools

Assembly is done in the home workshop, which already has the soldering
equipment, so no soldering tool has to be bought. **The multimeter is the
exception and the one tool that must be yours** — it is needed at the rover, for
the D50A pin-1 gate, the bare-board continuity check, and every bring-up
measurement.

| Item | 工具 | State |
|---|---|:---:|
| **Multimeter, continuity and diode mode** | **万用表，蜂鸣档和二极管档** | ✅ **— must be yours** |
| Temperature-controlled iron (T12 / 936) | 恒温烙铁 | ✅ workshop |
| Solder wire — Sn63Pb37, 0.8 mm, rosin core | 焊锡丝，含铅 0.8 mm 松香芯 | ✅ workshop |
| No-clean rosin flux | 免洗松香助焊剂 | ✅ workshop |
| Desoldering wick | 吸锡带 | ✅ workshop |
| Tweezers, flush cutters | 镊子、斜口钳 | ✅ workshop |
| Tip cleaner | 清洁钢丝球或海绵 | ✅ workshop |

Leaded solder melts about 40 °C lower than lead-free and wets more willingly.
Wash your hands; do not eat at the bench.

### Stage 1 — the signal adapter

| # | Item | Qty | ¥ | State |
|---:|---|---:|---:|:---:|
| 1 | PCB fabrication, 2-layer, 5 pcs | 1 order | 20–50 | ⬜ |
| 2 | Courier | — | 10–20 | ⬜ |
| 3 | 2×20 boxed header (`DC3-40P`), 2.54 mm straight | 5/pack | 3.17 | ✅ |
| 4 | 2×5 boxed header (`DC3-10P`), 2.54 mm straight | 5/pack | 2.21 | ✅ |
| 5 | 0805 resistors, **10 kΩ**, 1%, 100 pcs | 100 | 3.38 | ✅ — for `R7`–`R12` |
| 5b | THT metal-film resistors, 1/4 W, **33 Ω**, 1%, 200 pcs | 200 | 5.56 | ✅ — for `R1`–`R6`. Listing gives body 6.0 × 2.3 mm, lead ød 0.35 mm; **measure on arrival before freezing the footprint** |
| 6 | FC-10P 2×5 IDC ribbon, F–F, **30 cm and 40 cm** | 2 | ~20 | ✅ — the one that fits is chosen at test-fit, the other is the spare |
| 7 | Pi 40-pin GPIO ribbon, 2×20 F–F, **15 cm** | 1 | 3.89 | 🛒 — plain F–F, no flying lead |
| 8 | Small enclosure | 1 | 5–15 | ⬜ — **buy once the layout fixes the board outline** |
| 9 | Double-sided tape | 1 | 0 | ✅ |
| 10 | Cable ties / clips — **strain relief** | few | 0 | ✅ |

Item 10 is not an afterthought. The connector is on the PCB, but the strain
relief is a cable tie; without it the ribbon's weight hangs on the connector,
which is the failure mode this board exists to remove.

### Firmware track

| Item | Qty | ¥ | State | Needed from |
|---|---:|---:|:---:|:---:|
| Raspberry Pi Pico | **2** | 50 | ⬜ | Stage 0 — [language evaluation](roadmap.md#lang-eval) |
| Breadboard and jumper wires | 1 | 30 | ⬜ | Stage 0 |

### Deferred — buy at the stage that needs it

| Item | 工具 | ¥ | Needed from |
|---|---|---:|:---:|
| **Bench supply with current limit** | **带限流的可调直流电源** | 200–400 | **Stage 2** |
| USB logic analyzer (8 ch) | USB 逻辑分析仪 | 30–80 | Stage 3 |
| Hot air station | 热风枪 | 200 | Stage 3 |
| Solder paste, steel stencil | 锡膏、钢网 | 50–100 | Stage 3, optional |
| Entry digital oscilloscope | 入门数字示波器 | 800+ | Stage 4 |

Stage 1 has no power source of its own — no battery input, no regulator, not one
active component — so there is nothing for a bench supply to protect. It does
route a 3.3 V rail from the Pi to the driver's isolated side, and that rail's
current is measured at bring-up, but a bare copper net cannot run away. Buy the
supply before Stage 2, the first board that draws its own current.

### Running total

| Bucket | ¥ |
|---|---:|
| Software | 0 |
| Stage 0 tools | 0 — workshop, plus the multimeter already owned |
| Stage 1 board, parts, cables | 75–165 |
| Firmware track (2 Picos + breadboard) | 80 |
| **To the end of Stage 1** | **≈ 155–245** |
| Stage 2 onward (bench supply first) | 200–400, then per the roadmap |

Against the roadmap's ¥2000–3000 for the year.

<a id="connectors"></a>

## The connector decision

Both ribbons are **female-to-female**, so the board needs **male** headers at
both positions. Two kinds exist at 2.54 mm pitch:

| | Plain header | **Boxed header** |
|---|---|---|
| Part | 排针 2×20 / 2×5 | **DC3-40P / DC3-10P** |
| Keyed? | ❌ the socket can be pushed on reversed | ✅ a notch in the shroud means one orientation only |
| Height | Low | Taller, bigger footprint — affects enclosure height |
| Cost | ¥1–2 | ¥2–5 |

**Boxed headers at both positions.** At J2 this is not a preference: a reversed
2×5 ribbon swaps `P`/`A`/`B` wholesale and drives the wrong motors, and a
mis-plugged `V` destroys the driver's isolated input.

The D50A's own 2×5 control header is a boxed, shrouded header, so that end is
keyed by the manufacturer. Fitting J2 with a matching `DC3-10P` makes **both ends
keyed**, and the ribbon orientation becomes a single solution rather than a habit.
The Pi's 40-pin header is unshrouded, so the Pi end still relies on the red stripe.

**The socket must mate with a boxed header — this is a requirement on the cable.**
The D50A end has a shroud, so a ribbon whose sockets do not seat into one does not
fit the rover. If the delivered cable turns out that way, replace the cable.

<a id="arrival"></a>

## Arrival checks

### The two cables

- Both cables are truly female-to-female.
- 2.54 mm pitch, and the keyed-plug orientation identified.
- **The 10P cable is 同向 (same-direction)** — both connector openings facing the
  same way, so neither end has to be twisted 180° to seat. A twist is permanent
  torque on a connector.
- **The sockets seat fully into a boxed header.**
- **Which physical D50A pin is pin 1 is resolved.** Both ends keyed means one
  possible orientation: plug it on and find by continuity which conductor reaches
  each signal. `G` is continuous with the motor-power negative `P-`, which
  cross-checks it. **Until this is done, J2's footprint is not frozen.**
- The red-stripe / pin-1 direction identified at both ends of both cables.
- Continuity checked pin by pin **before either cable touches the rover**.
- Connector body size and clearance checked against the enclosure.

### The resistors

- **Measure the axial resistors' body length and lead diameter before freezing
  the footprint.** `R_Axial_DIN0207_..._P10.16mm_Horizontal` was chosen from a
  listing drawing, not from calipers. `P7.62mm` and `P15.24mm` are the
  alternatives in the same library.

### The bare PCB

- Photograph it before soldering anything — [`../photos/`](../photos/).
- Read the silkscreen at real size. If the labels are not legible, the board has
  failed at its one job.
- Continuity-check pin to pin against the signal map, before it touches the Pi.

---

See also: [`fabrication.md`](fabrication.md) — how the board gets made and
ordered · [`roadmap.md`](roadmap.md) — which stage needs what.

---

# 工具与零件 / 中文

项目需要的全部东西及其状态，让"还要买什么"有一个唯一的答案。只有确认用途之后才加入——
下面每一件都能追溯到某块具体的板子或某个具体的测量。**这里不是愿望清单。**

每一件东西是在哪一天、为什么选的，记在[开发日志](devlog/)里。

状态：✅ 已有 · 🛒 已下单在途 · ⬜ 待买

## 总账

### 软件

| 项目 | 版本 | 状态 | 从哪个阶段起需要 |
|---|---|:---:|:---:|
| KiCad | 10.0.6 | ✅ | 第 0 阶段 |
| Git 与 GitHub | — | ✅ | 第 0 阶段 |
| Pico SDK / arduino-pico / MicroPython | — | ⬜ | 第 0 阶段——三个都要，用于[语言评估](roadmap.md#lang-eval) |

### 工具

焊接在家里的工具间完成，那边设备齐全，所以没有任何焊接工具需要买。
**万用表是例外，也是唯一必须属于你自己的工具**——它要用在车那边：D50A 的 1 号脚闸门、
空板逐针导通、以及之后每一次上电测量。

| 项目 | 状态 |
|---|:---:|
| **万用表，要有蜂鸣档和二极管档** | ✅ **——必须是你自己的** |
| 恒温烙铁（T12 / 936） | ✅ 工具间 |
| 焊锡丝——Sn63Pb37，0.8 mm，松香芯 | ✅ 工具间 |
| 免洗松香助焊剂 | ✅ 工具间 |
| 吸锡带 | ✅ 工具间 |
| 镊子、斜口钳 | ✅ 工具间 |
| 清洁钢丝球或海绵 | ✅ 工具间 |

含铅焊锡比无铅的熔点低约 40 °C，上锡也更听话。焊完洗手，别在工作台上吃东西。

### 第 1 阶段：信号转接板

| # | 项目 | 数量 | ¥ | 状态 |
|---:|---|---:|---:|:---:|
| 1 | 打样，双层，5 片 | 1 单 | 20–50 | ⬜ |
| 2 | 运费 | — | 10–20 | ⬜ |
| 3 | 2×20 牛角座（`DC3-40P`），2.54 mm 直针 | 5 个/包 | 3.17 | ✅ |
| 4 | 2×5 牛角座（`DC3-10P`），2.54 mm 直针 | 5 个/包 | 2.21 | ✅ |
| 5 | 0805 电阻，**10 kΩ**，1%，100 个 | 100 | 3.38 | ✅——给 `R7`–`R12` |
| 5b | 通孔金属膜电阻，1/4 W，**33 Ω**，1%，200 个 | 200 | 5.56 | ✅——给 `R1`–`R6`。商品图纸给的是体长 6.0 × 2.3 mm、引脚 ød 0.35 mm，**到货先量，再锁封装** |
| 6 | FC-10P 2×5 IDC 排线，母对母，**30 cm 与 40 cm** | 2 | ~20 | ✅——试插时选合适的那条，另一条做备件 |
| 7 | 树莓派 40 针排线，2×20 母对母，**15 cm** | 1 | 3.89 | 🛒——普通母对母，不带飞线 |
| 8 | 小外壳 | 1 | 5–15 | ⬜ ——**等布局定下板框再买** |
| 9 | 双面胶 | 1 | 0 | ✅ |
| 10 | 扎带或线夹——**拉力缓解** | 若干 | 0 | ✅ |

第 10 项不是可有可无。连接器在板上，但拉力缓解是一根扎带；没有它，排线的重量全挂在连接器
上，而那正是这块板要消除的失效模式。

### 固件线

| 项目 | 数量 | ¥ | 状态 | 从哪个阶段起需要 |
|---|---:|---:|:---:|:---:|
| 树莓派 Pico | **2** | 50 | ⬜ | 第 0 阶段——[语言评估](roadmap.md#lang-eval) |
| 面包板与跳线 | 1 | 30 | ⬜ | 第 0 阶段 |

### 推迟——到需要的阶段再买

| 项目 | ¥ | 从哪个阶段起需要 |
|---|---:|:---:|
| **带限流的可调直流电源** | 200–400 | **第 2 阶段** |
| USB 逻辑分析仪（8 通道） | 30–80 | 第 3 阶段 |
| 热风枪 | 200 | 第 3 阶段 |
| 锡膏、钢网 | 50–100 | 第 3 阶段，可选 |
| 入门数字示波器 | 800+ | 第 4 阶段 |

第 1 阶段自己没有电源——不接电池、没有稳压器、一个有源元件都没有，所以台面电源在它身上
没有可保护的东西。它确实走一条从 Pi 到驱动板隔离侧的 3.3 V，这条电源取多少电流要在上电测试
时测出来，但一条裸铜网络不会失控。台面电源在第 2 阶段之前买到——那是第一块真正自己吃电的板。

### 累计

| 分项 | ¥ |
|---|---:|
| 软件 | 0 |
| 第 0 阶段工具 | 0——工具间，加上已有的万用表 |
| 第 1 阶段板子、零件、排线 | 75–165 |
| 固件线（2 块 Pico + 面包板） | 80 |
| **到第 1 阶段结束** | **≈ 155–245** |
| 第 2 阶段起（先买台面电源） | 200–400，之后按路线图 |

对照路线图里全年大约两三千。

## 连接器怎么选

两条排线都是**母对母**，所以板上两个位置都要**公头**。同样 2.54 mm 间距，有两种可选：

| | 光排针 | **牛角座** |
|---|---|---|
| 型号 | 排针 2×20 / 2×5 | **DC3-40P / DC3-10P** |
| 防呆 | ❌ 母座可以插反 | ✅ 外壳上的缺口只允许一个方向 |
| 高度 | 低 | 更高、占位更大——影响外壳高度 |
| 价格 | ¥1–2 | ¥2–5 |

**两个位置都用牛角座。** J2 那一端不是偏好：2×5 排线插反会把 `P`/`A`/`B` 整组换位、
开错电机，而 `V` 插错会烧掉驱动板的隔离输入。

D50A 自己的 2×5 控制口是带外壳的牛角座，那一端厂家已经做了防呆。J2 配上同规格的
`DC3-10P` 之后**两端都防呆**，排线方向从"靠习惯维持"变成"唯一解"。树莓派的 40 针排针是
光针，所以 Pi 那一端仍然要靠红边。

**母座必须能配牛角座——这是对排线的要求。** D50A 那端有外壳，插不进去的排线就是装不上车。
到货发现不对就换线。

## 到货后检查

### 两条排线

- 确认两条确实都是母对母。
- 确认 2.54 mm 间距，并认出防呆口方向。
- **确认 10P 那条是同向**——两个接头开口朝同一边，哪一端都不需要拧 180° 才插得进去。
  拧过去就是一个长期作用在连接器上的扭力。
- **确认母座能完全插进牛角座。**
- **确定 D50A 那个 2×5 哪个针是第 1 脚。** 两端都防呆意味着只有一种插法：插上去逐根量导通，
  看哪一根到哪个信号。`G` 与电机电源负极 `P-` 导通，可以交叉验证。
  **这件事做完之前，J2 的封装不锁定。**
- 认出两条线两端红边对应的 1 号针方向。
- **在任何一条排线接触小车之前**，先逐针检查导通。
- 对照外壳确认连接器本体尺寸和空间。

### 电阻

- **锁封装之前，先量轴向电阻的体长和引脚直径。**
  `R_Axial_DIN0207_..._P10.16mm_Horizontal` 是按商品图纸选的，不是量出来的。
  同一个库里还有 `P7.62mm` 和 `P15.24mm` 可选。

### 空板

- 焊之前先拍照——[`../photos/`](../photos/)。
- 按实际尺寸读一遍丝印。标注看不清，这块板就在它唯一的任务上失败了。
- 对照信号表逐针检查导通，在它接触树莓派之前。
