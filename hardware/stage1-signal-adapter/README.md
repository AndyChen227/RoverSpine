# Stage 1 — Passive Signal Adapter

Replaces the ten loose dupont control wires between the Raspberry Pi 5 and the
WHEELTEC D50A motor driver with one small passive board and two ribbon cables.

## Status

`[ ]` **Rev A — schematic complete, footprints not assigned.**

| Item | State |
|---|---|
| Schematic | Complete — 14 nets |
| ERC | 44 / 0 — 30 unused Pi-header pins by design, plus 14 symbols with no footprint |
| Netlist check | `ALL PASS` |
| Footprint check | `FAIL` — 14 to assign |
| PCB layout | Not started |
| Parts | Bought 2026-09-13, not delivered |
| D50A pin 1 | **Assumed** |
| Boards fabricated | 0 |

Three-state notation, same as the rest of the project: `[x]` met its exit
criteria **on the rover** · `[~]` exists and powers up · `[ ]` pending.
**Never `[x]` because the schematic looks right.**

## What it does

- **10 connections to the D50A forming 14 nets:** 6 motor-control signals, `GND`
  (two pins), `+3V3` (two pins). Each signal passes through a series resistor,
  which splits it into a Pi-side net (`PWM1`, `INA1`, …) and a driver-side net
  named after the D50A's own silkscreen (`P1`, `A1`, …). See
  [the net structure](../../docs/roadmap.md#nets).
- **`+3V3` sourced only from Pi physical pins 1 and 17.** 5 V (pins 2 and 4)
  would destroy the driver's isolated input — a copper trace makes that mis-plug
  impossible.
- **Boxed headers (`DC3-40P` / `DC3-10P`)**, so both ends of the D50A ribbon are
  keyed — the D50A's own control header is shrouded.
- Made-up ribbon harnesses instead of friction-fit jumpers.
- Readable silkscreen on every signal — the D50A's own short-form names at J2:
  `V` `P1` `A1` `B1` `G`.
- **6 series resistors, through-hole, 33 Ω — populated, not optional.** They sit
  in the signal path, so an empty series pad is an open signal and a dead board.
  Through-hole for two reasons: leads through plated holes hold better than two
  solder fillets on a vehicle that vibrates, and a lead is something you can clip
  a probe to or desolder without hot air.
- **6 pull-down pads, 0805, 10 kΩ — the genuinely optional ones**, and Rev A may
  ship with them empty. Populated, they make the driver inputs low while Pi GPIO
  is still high-impedance, so the window between Pi power-on and the Python
  starting means *stopped* rather than undefined.

## What it deliberately does NOT do

Rev A is minimal on purpose. Future power, sensing, safety and motor-driver
boards are separate projects, and **they will not be added to Rev A merely
because empty PCB area exists.**

- No microcontroller, no firmware.
- No battery input, no voltage regulator, no active component of any kind.
- No motor current, no motor power.

It does route the Pi's 3.3 V to the driver's isolated side, because that rail is
**required**. That is a copper net, not a power stage.

## Revision history

| Rev | Date | State | What changed |
|---|---|---|---|
| A | 2026-09-12 | `[ ]` | First revision. Schematic drawn: 10 connections, 8 nets, verified against the signal map. Carries a text annotation recording the unverified pin-1 assumption |
| A | 2026-09-12 | `[ ]` | Same revision. The 12 reserved resistors were specified but **not present on the schematic**; adding them splits each signal into a Pi-side and a driver-side net, so Rev A is **14 nets, not 8**. Series resistors changed from 0805 to **through-hole and mandatory** |
| A | 2026-09-13 | `[ ]` | R1–R12 drawn. **14 nets, netlist check `ALL PASS`.** A mislabelled driver-side net (`INB2` wired to `P1` instead of `B2`) was found and fixed during review — ERC reported nothing about it. Six 50-mil dangling wire ends traced to KiCad's Grid Override for wires and removed |
| A | 2026-09-13 | `[ ]` | ERC severities raised: `footprint_filter` `ignore` → **error**, `pin_to_pin` warning → **error**. ERC against the files is **44 / 0**, not the 30 / 0 first recorded — an empty footprint field is compared like any other value and matches no filter |
| A | 2026-09-14 | `[ ]` | **No change to the circuit.** `R7`–`R12` had carried `Package_QFP:PQFP-160_28x28mm_P0.65mm` since R1–R12 were drawn; cleared. **The ERC count did not change: 44 before, 44 after.** Footprint comparison added to [the checker](tools/README.md). Design rules from `fabrication.md` committed to the project file |

A revision is **never overwritten** — Rev B will sit next to Rev A.

## Files

```text
stage1-signal-adapter/
├── README.md     # this file
├── kicad/        # the KiCad project
├── bom.md        # bill of materials
├── tools/        # the checker, run after every schematic change
├── fab/          # the exact Gerber zip sent to the fab (not yet)
└── bringup.md    # first-power results (not yet)
```

## Gating checks — before footprints are frozen

- [ ] Both cables confirmed female-to-female, 2.54 mm pitch, sockets seating into
      a boxed header.
- [ ] **Which physical D50A pin is pin 1 — resolved with a meter, not assumed.**
      Both ends keyed means one possible orientation: plug the ribbon on and find
      by continuity which conductor reaches each signal. `G` is continuous with
      the motor-power negative `P-`, which cross-checks the map.
- [ ] Pin 1 / red-stripe direction identified at both ends of both cables.
- [ ] Continuity checked pin by pin **before either cable touches the rover**.
- [ ] Connector body size and clearance checked against the enclosure.
- [ ] **Axial resistor body length and lead diameter measured.**

## Next steps

1. **Assign the fourteen footprints.** **Two completion tests, not one:** ERC at
   exactly **30 / 0**, *and* [the checker](tools/README.md) at **`ALL PASS`**
   including its footprint block. ERC alone is not enough — `R1`–`R12` all declare
   the filter `R_*`, so an 0805 on a series resistor passes it silently.

   | Symbol | Part | KiCad footprint | Courtyard |
   |---|---|---|---|
   | J1 | `DC3-40P` boxed | `Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical` | 59.46 × 9.90 mm |
   | J2 | `DC3-10P` boxed | `Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical` | 21.36 × 9.90 mm |
   | R1–R6 | 33 Ω, THT, 1/4 W | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | 12.26 × 3.00 mm |
   | R7–R12 | 10 kΩ, 0805 | `Resistor_SMD:R_0805_2012Metric` | 3.36 × 1.90 mm |

2. **PCB layout, board-first.** The board's long side is set by J1 at 59.46 mm —
   a floor no enclosure choice can lower — so the outline is decided here and the
   enclosure is bought to fit it.
3. **When the cables arrive, run the gating checks above.**

---

# 第 1 阶段 —— 被动信号转接板 / 中文

用一块小型被动转接板加两条排线，替换 Raspberry Pi 5 与 WHEELTEC D50A 电机驱动板之间
十根松散的杜邦控制线。

## 当前状态

`[ ]` **Rev A —— 原理图完工，封装未分配。**

| 项目 | 状态 |
|---|---|
| 原理图 | 完工——14 个网络 |
| ERC | 44 / 0——30 条是排针上没用到的引脚（设计如此），14 条是没有封装的符号 |
| 网表核对 | `ALL PASS` |
| 封装核对 | `FAIL`——14 个待分配 |
| PCB 布局 | 未开始 |
| 物料 | 2026-09-13 已买，未到货 |
| D50A 1 号脚 | **假设** |
| 已打样数量 | 0 |

三态标注和项目其余部分一致：`[x]` 已**在车上**通过完成判据 · `[~]` 存在并且能上电 ·
`[ ]` 待办。**原理图看起来没问题，永远不能标成 `[x]`。**

## 它做什么

- **到 D50A 共 10 个连接，构成 14 个网络：** 6 路电机控制信号、`GND`（两针）、
  `+3V3`（两针）。每路信号经过一个串阻，被拆成 Pi 侧网络（`PWM1`、`INA1`…）和按 D50A
  自己丝印命名的驱动侧网络（`P1`、`A1`…）。见[网络结构](../../docs/roadmap.md#nets)。
- **`+3V3` 只从 Pi 的 1 号和 17 号针取电。** 5 V（2 号和 4 号针）会烧掉驱动板的隔离
  输入——铜箔让这种插错变得不可能。
- **用牛角座（`DC3-40P` / `DC3-10P`）**，所以 D50A 那条排线两端都防呆——D50A 自己的
  控制口本来就带外壳。
- 用成组排线，不用靠摩擦固定的杜邦线。
- 每路信号都有清楚的丝印——J2 那端用 D50A 自己的简写：`V` `P1` `A1` `B1` `G`。
- **6 个串阻，通孔，33 Ω——必装，不是可选。** 它们在信号路径上，焊盘空着就是断路、
  板子是死的。选通孔有两个理由：引脚穿过镀铜孔在会振动的车上比两个焊点结实；
  引脚可以夹表笔，也能不用热风枪拆下来。
- **6 个下拉焊盘，0805，10 kΩ——这才是真正可选的**，Rev A 可以空着出厂。焊上之后，
  在 Pi 的 GPIO 还是高阻态时它们把驱动输入拉低，于是从 Pi 上电到 Python 启动这段窗口
  的含义是**停**，而不是未定义。

## 它有意不做的事

Rev A 有意保持最小范围。以后的电源、传感、安全控制和电机驱动板是独立项目，
**不会因为 Rev A 有空余面积就塞进同一版 PCB**：

- 不用单片机，不需要固件。
- 不接入电池、没有稳压器、没有任何有源元件。
- 不碰电机电流和功率。

它确实要把 Pi 的 3.3 V 送到驱动板隔离侧，因为那条电源是**必需的**——但那是一条铜箔网络，
不是一级电源。

## 版本历史

| 版本 | 日期 | 状态 | 改了什么 |
|---|---|---|---|
| A | 2026-09-12 | `[ ]` | 第一版。画出原理图：10 个连接、8 个网络，与信号表核对过。图上有一段文字注记，记录未经证实的 1 号脚假设 |
| A | 2026-09-12 | `[ ]` | 同一版。12 个预留电阻写在规格里但**没画进图**；补上之后每路信号被拆成 Pi 侧和驱动侧两条网络，所以 Rev A 是 **14 个网络不是 8 个**。串阻从 0805 改成**通孔且必装** |
| A | 2026-09-13 | `[ ]` | 画上 R1–R12。**14 个网络，网表核对 `ALL PASS`。** 复查时发现并修掉一个写错的驱动侧标签（`INB2` 接成了 `P1` 而不是 `B2`）——ERC 对此一声不响。六段 50 mil 悬空线头来自 KiCad 的连线栅格重写，已删除 |
| A | 2026-09-13 | `[ ]` | 调高 ERC 严重性：`footprint_filter` 从 `ignore` 改成 **error**，`pin_to_pin` 从警告改成 **error**。对着文件跑，ERC 是 **44 / 0**，不是最先记下的 30 / 0——空的封装字段和任何别的值一样参与比对，而空不匹配任何规则 |
| A | 2026-09-14 | `[ ]` | **电路没有变化。** `R7`–`R12` 从画上 R1–R12 那次起就带着 `Package_QFP:PQFP-160_28x28mm_P0.65mm`，现已清除。**ERC 计数没有变化：之前 44，之后还是 44。** 给[核对脚本](tools/README.md)加上封装比对。`fabrication.md` 里的设计规则落进工程文件 |

**改版不覆盖旧版**——B 版会和 A 版并排放着。

## 文件

```text
stage1-signal-adapter/
├── README.md     # 本文件
├── kicad/        # KiCad 工程
├── bom.md        # 物料清单
├── tools/        # 核对脚本，每次改原理图之后跑
├── fab/          # 真正发给工厂的那份 Gerber（还没有）
└── bringup.md    # 首次上电结果（还没有）
```

## 锁封装前必须先做

- [ ] 两条排线都确认是母对母、2.54 mm 间距，母座能插进牛角座。
- [ ] **用万用表定死 D50A 物理上哪个针是第 1 脚，不是假设。** 两端都防呆意味着只有一种
      插法：插上去逐根量导通，看哪根线通到哪个信号。`G` 与电机电源负极 `P-` 导通，
      可以交叉验证。
- [ ] 两条线两端的 1 号针 / 红边方向都认出来。
- [ ] **在任何一条排线接触小车之前**，先逐针检查导通。
- [ ] 对照外壳确认连接器本体尺寸和间隙。
- [ ] **量出轴向电阻的体长和引脚直径。**

## 下一步

1. **分配 14 个封装。** **完成判据是两项不是一项：** ERC 正好 **30 / 0**，
   **并且**[核对脚本](tools/README.md)连封装那一段一起 **`ALL PASS`**。光有 ERC 不够——
   `R1`–`R12` 声明的筛选规则都是 `R_*`，串阻上装一个 0805 也能悄悄通过。

   | 符号 | 元件 | KiCad 封装 | courtyard |
   |---|---|---|---|
   | J1 | `DC3-40P` 牛角座 | `Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical` | 59.46 × 9.90 mm |
   | J2 | `DC3-10P` 牛角座 | `Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical` | 21.36 × 9.90 mm |
   | R1–R6 | 33 Ω，通孔，1/4 W | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | 12.26 × 3.00 mm |
   | R7–R12 | 10 kΩ，0805 | `Resistor_SMD:R_0805_2012Metric` | 3.36 × 1.90 mm |

2. **PCB 布局，以板定外壳。** 板子的长边由 J1 的 59.46 mm 定死——这是任何外壳选择都降不下来
   的下限——所以板框在这里定，外壳按它去买。
3. **排线到货后，执行上面的锁封装前检查。**

---

Hardware licensed under CERN-OHL-S-2.0. See [`../../LICENSE.md`](../../LICENSE.md).
