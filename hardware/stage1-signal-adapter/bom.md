# BOM — Stage 1 Passive Signal Adapter / 物料清单

**Rev A — not finalized.** Quantities and part numbers are filled in as they are
actually chosen, not guessed in advance. Cables that have been selected are
recorded with their dates in
[`docs/tools-and-parts.md`](../../docs/tools-and-parts.md).

**Rev A — 未定稿。** 数量和型号在真正选定之后才填，不提前猜。已经选定的排线连同日期
记在 [`docs/tools-and-parts.md`](../../docs/tools-and-parts.md)。

## On-board / 板上

| # | Part | 元件 | Qty | Package | Status |
|---:|---|---|---:|---|---|
| 1 | 2×20 pin header, 2.54 mm, to the Pi | 2×20 排针，接树莓派 | 1 | TH, 2.54 mm | Footprint not frozen — awaiting cable check |
| 2 | 2×5 pin header, 2.54 mm, to the D50A | 2×5 排针，接 D50A | 1 | TH, 2.54 mm | Footprint not frozen — awaiting cable check |
| 3 | Series resistors on Pi-facing signals | 信号串联电阻 | 6 | 0805 | Reserved pads; value TBD (≈33 Ω) |
| 4 | Pull-down resistors on driver inputs | 驱动输入下拉电阻 | 6 | 0805 | Reserved pads; value TBD (≈10 kΩ) — **may ship unpopulated on Rev A** |
| 5 | PCB, 2-layer, HASL | 板子，双层喷锡 | 1 | — | Size TBD after layout |

## Cables / 排线

| # | Part | Qty | Status |
|---:|---|---:|---|
| 6 | FC-10P 2×5 IDC ribbon, female-to-female, 2.54 mm, ≈35 cm | 1 | Selected 2026-09-11; awaiting delivery |
| 7 | Raspberry Pi 40-pin GPIO ribbon, 2×20 female-to-female, 2.54 mm, 10–15 cm | 1 | Selected 2026-09-11; awaiting delivery |

## Not on this board / 这块板上没有的东西

Listed explicitly so the absence is a decision rather than an oversight:
microcontroller, voltage regulator, battery input, motor power path, current
sense, LEDs, buzzer, button. See [the board README](README.md).

明确列出来，是为了让"没有"成为一个决定而不是一次遗漏：单片机、稳压器、电池输入、
电机功率回路、电流采样、LED、蜂鸣器、按钮。见[板子 README](README.md)。

## Estimated cost / 成本估算

≈ ¥40–60 including both cables and fabrication.
