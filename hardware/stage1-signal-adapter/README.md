# Stage 1 — Passive Signal Adapter / 被动信号转接板

Replaces the seven loose dupont control wires between the Raspberry Pi 5 and the
WHEELTEC D50A motor driver with one small passive board and two ribbon cables.

用一块小型被动转接板加两条排线，替换 Raspberry Pi 5 与 WHEELTEC D50A 电机驱动板之间
七根松散的杜邦控制线。

## Status / 当前状态

- `[ ]` **Rev A — pending.** Schematic in progress. Not fabricated. Cables not yet delivered.

`[ ]` **Rev A — 待办。** 原理图进行中，未打样，排线未到货。

Three-state notation, same as the rest of the project: `[x]` met its exit
criteria **on the rover** · `[~]` exists and powers up · `[ ]` pending.
**Never `[x]` because the schematic looks right.**

## Revision history / 版本历史

| Rev | Date | State | What changed / 改了什么 |
|---|---|---|---|
| A | 2026-09-12 | `[ ]` in progress | First revision. Two connectors placed in KiCad (`Conn_02x20_Odd_Even`, `Conn_02x05_Odd_Even`); nets not yet drawn |

A revision is **never overwritten** — Rev B will sit next to Rev A, because the
whole point of keeping A is being able to see what changed and why.

**改版不覆盖旧版**——B 版会和 A 版并排放着，因为留下 A 版的全部意义就是能看出改了
什么、为什么改。

## What it does / 它做什么

- 7 direct copper connections: 6 motor-control signals + GND
- Keyed, latching connectors and made-up ribbon harnesses instead of friction-fit jumpers
- Readable silkscreen on every signal
- Reserved pads for 6 pull-downs and 6 series resistors (may ship unpopulated on Rev A)

## What it deliberately does NOT do / 它有意不做的事

Rev A is minimal on purpose. Future power, sensing, safety, and motor-driver
boards are separate projects, and **they will not be added to Rev A merely
because empty PCB area exists.**

- no microcontroller, no firmware;
- no battery input, no voltage regulator;
- no motor current, no motor power;
- the D50A's two VCC positions are **intentionally not connected**.

Rev A 有意保持最小范围。以后可能制作的电源、传感、安全控制和电机驱动板仍是独立项目，
**不会因为 Rev A 有空余面积就直接塞进同一版 PCB**：不用单片机、不需要固件、不接入电池、
不做电源转换、不碰电机电流和功率；D50A 的两个 VCC 位置有意不连接。

## Files / 文件

```text
stage1-signal-adapter/
├── README.md     # this file
├── kicad/        # the KiCad project
├── bom.md        # bill of materials
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

1. Draw and label the seven logical connections in the schematic.
2. Run ERC, then **manually compare every net against the signal map**, one by one.
3. When the cables arrive, run the gating checks above.
4. Only then assign final footprints and begin PCB layout.

---

Hardware licensed under CERN-OHL-S-2.0. See [`../../LICENSE.md`](../../LICENSE.md).
