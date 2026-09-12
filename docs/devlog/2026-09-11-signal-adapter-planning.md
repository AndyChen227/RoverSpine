# 2026-09-11 — Passive Signal Adapter Planning / 被动信号转接板规划

## Result / 本次结果

We defined the first PCB to be designed for RoverSpine: a small passive adapter that replaces the seven loose Dupont control wires between the Raspberry Pi 5 and the WHEELTEC D50A motor driver.

今天确定了 RoverSpine 第一块准备实际设计的 PCB：一块小型被动转接板，用来替换 Raspberry Pi 5 与 WHEELTEC D50A 电机驱动板之间七根松散的杜邦控制线。

This session produced a design decision and an implementation plan, not a finished schematic or fabricated board. Status remains [ ] pending.

本次完成的是设计决策和实施计划，不是已经完成的原理图或实体板；状态仍为 [ ] 待办。

## Why this board / 为什么先做这块板

The existing wiring works electrically, but seven individual Dupont jumpers depend on friction, are difficult to organize, and are easy to reconnect incorrectly. The new board changes the connection into two organized ribbon cables with clear labels. Its benefit is mechanical reliability, repeatable wiring, and easier debugging; it does not change the rover's control algorithm.

现有接线在电气上可以工作，但七根杜邦线只靠摩擦固定、不容易整理，也容易重新接错。新板把它们变成两条成组排线和明确标注的连接器。它改善的是机械可靠性、可重复接线和排错，不改变小车控制算法。

## Rev A scope / Rev A 范围

Rev A is deliberately minimal:

- two connectors;
- seven direct copper connections: six motor-control signals and ground;
- readable silkscreen labels;
- no microcontroller and no firmware;
- no battery input, voltage regulator, motor current, or motor power;
- the two D50A VCC positions are intentionally not connected.

Rev A 有意保持最小范围：两个连接器、六路电机控制信号和地线、清楚的丝印；不使用单片机，不需要固件；不接入电池、电源转换、电机电流或电机功率；D50A 的两个 VCC 位置有意不连接。

Future power, sensing, safety, and motor-driver boards remain separate projects. They will not be added to Rev A merely because empty PCB area exists.

以后可能制作的电源、传感、安全控制和电机驱动板仍是独立项目，不会因为 Rev A 有空余面积就直接塞进同一版 PCB。

## Physical arrangement / 机械安装方案

The Raspberry Pi is on the upper deck and already has an active cooler, so a stacked HAT is not practical. The D50A is on the lower deck. The adapter will sit in a small enclosure on the upper deck, attached with double-sided tape, with a flexible cable running down to the driver.

树莓派位于第二层，上方已经安装主动散热器，因此不适合再叠一块 HAT。D50A 位于第一层。转接板计划装入小外壳，用双面胶固定在第二层，再用柔性排线绕到第一层的驱动板。

    Raspberry Pi 5
        │  2×20, 40-pin female-to-female ribbon, 10–15 cm
        ▼
    RoverSpine passive adapter PCB (upper deck enclosure)
        │  2×5, 10-pin IDC female-to-female ribbon, about 35 cm
        ▼
    WHEELTEC D50A (lower deck)

## Confirmed signal map / 已确认信号表

| Function | Raspberry Pi BCM | Pi physical pin |
|---|---:|---:|
| PWM1 | GPIO12 | 32 |
| INA1 | GPIO23 | 16 |
| INB1 | GPIO24 | 18 |
| PWM2 | GPIO13 | 33 |
| INA2 | GPIO5 | 29 |
| INB2 | GPIO6 | 31 |
| GND | GND | 39 |

The D50A header is arranged as follows:

| Top row | VCC | PWM2 | INA2 | INB2 | GND |
|---|---|---|---|---|---|
| Bottom row | VCC | PWM1 | INA1 | INB1 | GND |

The measured distance from the first to the fifth position is slightly over 11 mm, consistent with 2.54 mm pitch. The final footprint and pin-1 orientation will not be frozen until the delivered cables are physically checked.

第一列到第五列的实测距离略大于 11 mm，与 2.54 mm 间距相符。最终封装和 1 号针方向要等排线到货、实际试插之后才锁定。

## Learning method / 学习方式

Andy will draw this board in KiCad one step at a time. The assistant explains each decision, checks the work, and helps diagnose mistakes instead of silently completing the design.

这块板由 Andy 在 KiCad 中一步一步亲自绘制。助手负责解释每个决定、检查结果和帮助排错，而不是代替 Andy 完成全部设计。

## Next steps / 下一步

1. Create a KiCad project for Rev A.
2. Place a generic 2×20 Raspberry Pi connector and a generic 2×5 D50A connector.
3. Draw and label the seven logical connections.
4. Run ERC and manually compare every net with the table above.
5. When the cables arrive, verify pitch, key direction, pin 1, connector body size, and clearance.
6. Only then assign final footprints and begin PCB layout.
