# BOM — Stage 1 Passive Signal Adapter / 物料清单

**Rev A — not finalized.** Quantities and part numbers are filled in as they are
actually chosen, not guessed in advance. The resistor values and packages below
were settled on 2026-09-12 together with
[the net structure](../../docs/roadmap.md#nets) — see
[that devlog](../../docs/devlog/2026-09-12-reserved-resistor-pads.md). Cables that have been selected are
recorded with their dates in
[`docs/tools-and-parts.md`](../../docs/tools-and-parts.md).

**Rev A — 未定稿。** 数量和型号在真正选定之后才填，不提前猜。已经选定的排线连同日期
记在 [`docs/tools-and-parts.md`](../../docs/tools-and-parts.md)。

## On-board / 板上

| # | Part | 元件 | Qty | Package | Status |
|---:|---|---|---:|---|---|
| 1 | 2×20 boxed header (`DC3-40P`), 2.54 mm, to the Pi | 2×20 牛角座，接树莓派 | 1 | TH, 2.54 mm | Footprint not frozen — awaiting cable check |
| 2 | 2×5 boxed header (`DC3-10P`), 2.54 mm, to the D50A | 2×5 牛角座，接 D50A | 1 | TH, 2.54 mm | **Boxed required** — the D50A's header is shrouded. Footprint not frozen; **D50A pin 1 must be resolved with a meter first** |
| 3 | Series resistors on Pi-facing signals, `R1`–`R6` | 信号串联电阻 | 6 | **TH, axial** | **33 Ω. Must be populated** — in the signal path, so an empty pad is an open signal. Through-hole for leads through plated holes (mechanically stronger on a vehicle that vibrates than two solder fillets) and for something to clip a probe to. *Reason amended 2026-09-13; the package did not change.* Part bought 2026-09-13: 1/4 W metal film, 1%, body 6.0 × 2.3 mm, lead **ød 0.35 mm** per the listing — **confirm with calipers before the footprint is frozen** |
| 4 | Pull-down resistors on driver inputs, `R7`–`R12` | 驱动输入下拉电阻 | 6 | 0805 | 10 kΩ. **The only genuinely optional parts on this board** — may ship unpopulated on Rev A, in which case mark them **DNP** in KiCad rather than noting it here. Part bought 2026-09-13: 0805, 1%, 100 pcs of a single value |
| 5 | PCB, 2-layer, HASL | 板子，双层喷锡 | 1 | — | Size TBD after layout |

## Cables / 排线

| # | Part | Qty | Status |
|---:|---|---:|---|
| 6 | FC-10P 2×5 IDC ribbon, female-to-female, 2.54 mm — **30 cm and 40 cm** | 2 | Bought 2026-09-13. 35 cm is not a stocked length; both were bought and the fit is decided at test-fit |
| 7 | Raspberry Pi 40-pin GPIO ribbon, 2×20 female-to-female, 2.54 mm, **15 cm** | 1 | Ordered 2026-09-13, plain F–F (no flying lead). "Selected 2026-09-11" had been recorded but no order was ever placed — corrected 2026-09-13 |

## Not on this board / 这块板上没有的东西

Listed explicitly so the absence is a decision rather than an oversight:
microcontroller, voltage regulator, battery input, motor power path, current
sense, LEDs, buzzer, button. See [the board README](README.md).

**Note what *is* on it, and was previously listed as absent:** the `+3V3` net
that feeds the D50A's `V` pins. It is a copper net with no components, sourced
only from Pi pins 1 and 17. Corrected 2026-09-12 — see
[the devlog](../../docs/devlog/2026-09-12-d50a-control-header-correction.md).

**And note what stopped being true:** this board is no longer "pure copper, not
one component can burn". Six series resistors are now mandatory parts on the
signal path. Nothing on it can still burn — a 33 Ω resistor passing a GPIO's
milliamps is not a thermal event — but *passive* and *component-free* are two
different claims, and only the first one survives.

**另外注意一件不再成立的事：** 这块板不再是"纯铜箔，一个元件都烧不了"——6 个串阻现在是
信号路径上的必装件。板上依然没有任何东西会烧（33 Ω 上过 GPIO 那几毫安算不上热事件），
但**"被动"和"没有元件"是两个不同的说法**，现在只有前一个还成立。

明确列出来，是为了让"没有"成为一个决定而不是一次遗漏：单片机、稳压器、电池输入、
电机功率回路、电流采样、LED、蜂鸣器、按钮。见[板子 README](README.md)。

**注意一样"原来被列为没有、现在有"的东西**：喂给 D50A 两个 `V` 脚的 `+3V3` 网络。
它是一条不带任何元件的铜箔，只从 Pi 的 1 号和 17 号针取电。2026-09-12 更正。

## Estimated cost / 成本估算

≈ ¥40–60 including both cables and fabrication.
