# Stage 1 — Passive Signal Adapter / 被动信号转接板

Replaces the ten loose dupont control wires between the Raspberry Pi 5 and the
WHEELTEC D50A motor driver with one small passive board and two ribbon cables.

用一块小型被动转接板加两条排线，替换 Raspberry Pi 5 与 WHEELTEC D50A 电机驱动板之间
十根松散的杜邦控制线。

> [!NOTE]
> **Corrected 2026-09-12.** This board was previously specified as 7 connections
> with the D50A's `V` pins left unconnected. Both were wrong — `V` is the 3.3 V
> supply for the driver's isolated control side, and without it none of the
> control signals work at all. See
> [the correction devlog](../../docs/devlog/2026-09-12-d50a-control-header-correction.md).
>
> **2026-09-12 更正。** 这块板原来的规格是 7 个连接、`V` 不接。两条都错——`V` 是驱动板
> 隔离控制侧的 3.3 V 供电，不接它，控制信号一个都不工作。

## Status / 当前状态

- `[ ]` **Rev A — pending, and the schematic needs one more revision.** The 8-net version was drawn and netlist-verified on 2026-09-12 (ERC 30/0, every net compared against the signal map). Later that day the **twelve reserved resistors were found to be specified but never drawn**, which makes the real design 14 nets — see [the net structure](../../docs/roadmap.md#nets) and [that devlog](../../docs/devlog/2026-09-12-reserved-resistor-pads.md). Footprints **not assigned**, layout not started, not fabricated. Cables not yet delivered, so D50A pin 1 is still an assumption.

`[ ]` **Rev A — 待办，原理图还要再改一版。** 8 网络的版本已于 2026-09-12 画完并通过网表核对（ERC 30/0，每个网络与信号表逐条比对）。当天稍后发现**那 12 个预留电阻只写在规格里、从没画进图**，算上它们真正的设计是 14 个网络——见[网络结构](../../docs/roadmap.md#nets)和[那篇记录](../../docs/devlog/2026-09-12-reserved-resistor-pads.md)。封装**未分配**，布局未开始，未打样。排线未到货，所以 D50A 的 1 号脚仍是假设。

Three-state notation, same as the rest of the project: `[x]` met its exit
criteria **on the rover** · `[~]` exists and powers up · `[ ]` pending.
**Never `[x]` because the schematic looks right.**

## Revision history / 版本历史

| Rev | Date | State | What changed / 改了什么 |
|---|---|---|---|
| A | 2026-09-12 | `[ ]` in progress | First revision. Schematic drawn: 10 connections, 8 nets, verified against the signal map from the exported netlist. Carries a text annotation recording the unverified pin-1 assumption. Footprints not assigned. See [the devlog](../../docs/devlog/2026-09-12-revA-schematic-complete.md) |
| A | 2026-09-12 | `[ ]` in progress | Same revision, later the same day. The 12 reserved resistors were specified in the roadmap and the BOM but **not present on the schematic**; adding them splits each signal into a Pi-side and a driver-side net, so Rev A is **14 nets, not 8**. Series resistors changed from 0805 to **through-hole and mandatory** — they are in the signal path, so an empty pad is an open signal. See [the devlog](../../docs/devlog/2026-09-12-reserved-resistor-pads.md) |

A revision is **never overwritten** — Rev B will sit next to Rev A, because the
whole point of keeping A is being able to see what changed and why.

**改版不覆盖旧版**——B 版会和 A 版并排放着，因为留下 A 版的全部意义就是能看出改了
什么、为什么改。

## What it does / 它做什么

- **10 connections to the D50A forming 14 nets:** 6 motor-control signals, `GND` (two pins), `+3V3` (two pins). Each signal passes through a series resistor, which splits it into a Pi-side net (`PWM1`, `INA1`, …) and a driver-side net named after the D50A's own silkscreen (`P1`, `A1`, …). See [the net structure](../../docs/roadmap.md#nets)
- **`+3V3` sourced only from Pi physical pins 1 and 17.** 5 V (pins 2 and 4) would destroy the driver's isolated input — a copper trace makes that mis-plug impossible
- **Boxed headers (`DC3-40P` / `DC3-10P`)**, so both ends of the D50A ribbon are keyed — the D50A's own control header is shrouded
- Made-up ribbon harnesses instead of friction-fit jumpers
- Readable silkscreen on every signal — the D50A's own short-form names at J2: `V` `P1` `A1` `B1` `G`
- **6 series resistors, through-hole, 33 Ω — populated, not optional.** They sit in the signal path, so an empty series pad is an open signal and a dead board. Through-hole rather than 0805 so that Rev A stays a board a beginner can actually assemble
- **6 pull-down pads, 0805, 10 kΩ — these are the genuinely optional ones** and Rev A may ship with them empty. Populated, they make the driver inputs low while Pi GPIO is still high-impedance, so the window between Pi power-on and the Python starting means *stopped* rather than undefined

## What it deliberately does NOT do / 它有意不做的事

Rev A is minimal on purpose. Future power, sensing, safety, and motor-driver
boards are separate projects, and **they will not be added to Rev A merely
because empty PCB area exists.**

- no microcontroller, no firmware;
- no battery input, no voltage regulator, no active component of any kind;
- no motor current, no motor power.

It does route the Pi's 3.3 V to the driver's isolated side, because that rail is
**required** — see the correction above. That is a copper net, not a power stage.

Rev A 有意保持最小范围。以后可能制作的电源、传感、安全控制和电机驱动板仍是独立项目，
**不会因为 Rev A 有空余面积就直接塞进同一版 PCB**：不用单片机、不需要固件、不接入电池、
不做电源转换、不碰电机电流和功率。它确实要把 Pi 的 3.3 V 送到驱动板隔离侧，因为那条电源是
**必需的**（见上面的更正）——但那是一条铜箔网络，不是一级电源。

## Files / 文件

```text
stage1-signal-adapter/
├── README.md     # this file
├── kicad/        # the KiCad project
├── bom.md        # bill of materials
├── tools/        # the netlist checker, run after every schematic change
├── fab/          # the exact Gerber zip sent to the fab, per revision (not yet)
└── bringup.md    # first-power results (not yet)
```

## Design inputs / 设计输入

The signal map, the D50A header arrangement, the mechanical arrangement, and the
gating checks that must pass before footprints are frozen all live in:

- [`docs/roadmap.md` → Stage 1](../../docs/roadmap.md#stage-1)
- [`docs/devlog/2026-09-11-signal-adapter-planning.md`](../../docs/devlog/2026-09-11-signal-adapter-planning.md)
- [`docs/tools-and-parts.md`](../../docs/tools-and-parts.md) — the two cables that were selected

> [!IMPORTANT]
> **Footprints are not frozen until the cables are in hand and checked.** Pitch,
> key direction, pin 1 at both ends, connector body size, and continuity — all
> verified with a multimeter before either cable touches the rover.
>
> **排线到货并检查之前不锁封装。** 间距、防呆方向、两端的 1 号针、连接器本体尺寸、
> 逐针导通——全部用万用表确认，而且在任何一条排线接触小车之前完成。

## Next steps / 下一步

1. ~~Draw and label the connections in the schematic.~~ **Done 2026-09-12.**
2. ~~Run ERC, then manually compare every net against the signal map.~~ **Done — 30 errors / 0 warnings, all 8 nets PASS.**
3. **Draw the 12 resistors** per [the net structure](../../docs/roadmap.md#nets): R1–R6 in series, R7–R12 pulling the driver side down to `GND`. Then re-run ERC — **it should still be 30 / 0** — and re-run [the netlist check](tools/README.md), which now expects 14 nets and currently fails by design, listing exactly what is missing.
4. **When the cables arrive, run the gating checks above** — including resolving which physical D50A pin is pin 1, which is still an assumption.
5. **Before assigning footprints:** re-enable the ERC check `分配的封装不匹配封装筛选规则`. It catches a wrong-pitch or wrong-pin-count footprint, which is the fatal mistake available at this step.
6. Only then assign final footprints (`DC3-40P` at J1, `DC3-10P` at J2, axial through-hole for R1–R6, 0805 for R7–R12) and begin PCB layout.

---

Hardware licensed under CERN-OHL-S-2.0. See [`../../LICENSE.md`](../../LICENSE.md).
