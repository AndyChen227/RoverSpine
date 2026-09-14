# BOM — Stage 1 Passive Signal Adapter

**Rev A — not finalized.** Part numbers are filled in as they are chosen, not
guessed in advance. Prices and purchase dates are in
[`docs/tools-and-parts.md`](../../docs/tools-and-parts.md).

## On-board

| # | Part | Qty | Package | Status |
|---:|---|---:|---|---|
| 1 | 2×20 boxed header (`DC3-40P`), 2.54 mm, to the Pi | 1 | TH, 2.54 mm | Bought. Footprint not frozen — awaiting cable check |
| 2 | 2×5 boxed header (`DC3-10P`), 2.54 mm, to the D50A | 1 | TH, 2.54 mm | **Boxed required** — the D50A's header is shrouded. Bought. Footprint not frozen; **D50A pin 1 must be resolved with a meter first** |
| 3 | Series resistors on Pi-facing signals, `R1`–`R6` | 6 | **TH, axial** | **33 Ω. Must be populated** — in the signal path, so an empty pad is an open signal. Through-hole for mechanical strength on a vehicle that vibrates and for probeable leads. Bought: 1/4 W metal film, 1%, body 6.0 × 2.3 mm, lead ød 0.35 mm per the listing — **confirm with calipers before the footprint is frozen** |
| 4 | Pull-down resistors on driver inputs, `R7`–`R12` | 6 | 0805 | 10 kΩ. **The only genuinely optional parts** — may ship unpopulated on Rev A, in which case mark them **DNP** in KiCad rather than noting it here. Bought: 0805, 1%, 100 pcs of a single value |
| 5 | PCB, 2-layer, HASL | 1 | — | Size TBD after layout |

## Cables

| # | Part | Qty | Status |
|---:|---|---:|---|
| 6 | FC-10P 2×5 IDC ribbon, female-to-female, **30 cm and 40 cm** | 2 | Bought. 35 cm is not a stocked length; the fit is decided at test-fit and the other becomes the spare |
| 7 | Raspberry Pi 40-pin GPIO ribbon, 2×20 female-to-female, **15 cm** | 1 | Ordered. Plain F–F, no flying lead |

## Not on this board

Listed explicitly so the absence is a decision rather than an oversight:
microcontroller, voltage regulator, battery input, motor power path, current
sense, LEDs, buzzer, button. See [the board README](README.md).

**What is on it:** the `+3V3` net that feeds the D50A's `V` pins. It is a copper
net with no components, sourced only from Pi physical pins 1 and 17.

This board is **passive**, not component-free — six series resistors are
mandatory parts on the signal path. Nothing on it can burn: a 33 Ω resistor
passing a GPIO's milliamps is not a thermal event.

## Estimated cost

≈ ¥40–60 including both cables and fabrication.

---

# 物料清单 —— 第 1 阶段被动信号转接板 / 中文

**Rev A——未定稿。** 型号在真正选定之后才填，不提前猜。价格和购买日期记在
[`docs/tools-and-parts.md`](../../docs/tools-and-parts.md)。

## 板上

| # | 元件 | 数量 | 封装 | 状态 |
|---:|---|---:|---|---|
| 1 | 2×20 牛角座（`DC3-40P`），2.54 mm，接树莓派 | 1 | 通孔，2.54 mm | 已买。封装未锁定——等排线核对 |
| 2 | 2×5 牛角座（`DC3-10P`），2.54 mm，接 D50A | 1 | 通孔，2.54 mm | **必须是牛角座**——D50A 的控制口带外壳。已买。封装未锁定；**必须先用万用表定死 D50A 的 1 号脚** |
| 3 | Pi 侧信号串联电阻，`R1`–`R6` | 6 | **通孔，轴向** | **33 Ω，必须焊上**——在信号路径上，焊盘空着就是断路。选通孔是为了在会振动的车上更结实，以及引脚能夹表笔。已买：1/4 W 金属膜，1%，商品图纸给的是体长 6.0 × 2.3 mm、引脚 ød 0.35 mm——**锁封装前用卡尺确认** |
| 4 | 驱动输入下拉电阻，`R7`–`R12` | 6 | 0805 | 10 kΩ。**板上唯一真正可选的件**——Rev A 可以不焊，那种情况下在 KiCad 里标 **DNP**，而不是在这里写备注。已买：0805，1%，单一阻值 100 个 |
| 5 | PCB，双层，喷锡 | 1 | — | 尺寸待布局之后确定 |

## 排线

| # | 元件 | 数量 | 状态 |
|---:|---|---:|---|
| 6 | FC-10P 2×5 IDC 排线，母对母，**30 cm 与 40 cm** | 2 | 已买。35 cm 没有现货；试插时选合适的，另一条做备件 |
| 7 | 树莓派 40 针 GPIO 排线，2×20 母对母，**15 cm** | 1 | 已下单。普通母对母，不带飞线 |

## 这块板上没有的东西

明确列出来，是为了让"没有"成为一个决定而不是一次遗漏：单片机、稳压器、电池输入、
电机功率回路、电流采样、LED、蜂鸣器、按钮。见[板子 README](README.md)。

**板上确实有的：** 喂给 D50A 两个 `V` 脚的 `+3V3` 网络。它是一条不带任何元件的铜箔，
只从 Pi 的 1 号和 17 号针取电。

这块板是**被动**的，但不是"没有元件"——6 个串阻是信号路径上的必装件。板上依然没有任何
东西会烧：33 Ω 上过 GPIO 那几毫安算不上热事件。

## 成本估算

约 ¥40–60，含两条排线和打样。
