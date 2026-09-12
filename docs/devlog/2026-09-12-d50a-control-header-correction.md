# 2026-09-12 — D50A Control Header: Two Corrections / D50A 控制口：两处更正

## Result / 本次结果

Two factual errors in this repository's own records were found and corrected. One
of them would have produced a **dead board**: Rev A was specified to leave the
D50A's `V` pins unconnected, and `V` is the 3.3 V supply the driver's isolated
control side needs to function at all.

本次发现并更正了本仓库记录里的两个事实错误。其中一个会直接导致**板子做出来是废的**：
Rev A 的规格写着 D50A 的 `V` 脚不连接，而 `V` 正是驱动板隔离控制侧工作所必需的 3.3 V 供电。

No hardware was built. The J1 side of the Rev A schematic is complete; the J2
side is not yet drawn.

## Source / 依据

The RoverPi wiring table for the D50A control header, which carries this warning
in bold:

> **`V` 是驱动板隔离控制侧的 3.3 V 供电，接 1 号和 17 号针，绝不能接 2、4 号的 5 V 针。**
> (`V` is the 3.3 V supply for the driver's isolated control side. Connect it to
> physical pins 1 and 17. **Never** connect it to the 5 V pins, 2 or 4.)

Plus photographs of the physical board taken 2026-09-12, and the WHEELTEC STM32
example project (`12A双通道驱动.zip`, v5.7, 2021-04-29).

依据是 RoverPi 那份 D50A 控制口接线表（其中那句加粗警告），加上 2026-09-12 拍的实物
照片，以及 WHEELTEC 的 STM32 例程工程。

---

## Correction 1 — `V` must be connected, at 3.3 V / 更正一：`V` 必须接，而且是 3.3 V

### What the records said / 原来的记录

`docs/devlog/2026-09-11-signal-adapter-planning.md`, `docs/roadmap.md`,
`hardware/stage1-signal-adapter/README.md` all said:

> ~~the two D50A VCC positions are **intentionally not connected**~~
> ~~D50A 的两个 VCC 位置**有意不连接**~~

### Why it is wrong / 为什么错

`V` is not the driver board *offering* power outward. It is the 3.3 V rail that
powers the **input side of the driver's optical/galvanic isolation** — the
product page advertises 控制信号全隔离 (fully isolated control signals), and the
block diagram shows an isolation barrier between the control headers and the
logic.

With `V` unconnected, the isolators' input side has no supply and **not one of
the six control signals works.** The board would solder up, plug in, and the
rover would not move at all.

`V` 不是驱动板对外送电，它是驱动板**隔离侧输入端**的 3.3 V 供电。产品页写的"控制信号
全隔离"和框图里的隔离屏障都指向这一点。`V` 不接，隔离器输入侧没有电源，**六个控制信号
一个都不会工作**——板子焊完插上，车一动不动。

### Where the wrong belief came from / 这个错误是怎么来的

The 2026-09-11 planning session recorded a 7-wire signal map — six motor-control
signals plus one ground. That map was **incomplete**: it omitted both `V` pins
and the second `G`. The "intentionally not connected" decision was then made
consistently *with an incomplete map*, which is why it looked reasonable at the
time and was wrong anyway.

The lesson is not "check harder". It is that **a design input needs a source, and
the source needs to be named.** The 7-wire map had no citation. The corrected map
below cites the RoverPi wiring table.

2026-09-11 那次记下的是一张 7 根线的信号表——六个控制信号加一根地。**那张表本身是不完整的**：
漏掉了两个 `V` 和第二个 `G`。"有意不连接"这个决定是在一张不完整的表上做出来的，所以它
当时看起来合理，但依然是错的。

教训不是"下次看仔细点"，而是：**设计输入必须有出处，而且出处要写出来。** 那张 7 根线的表
没有引用来源；下面这张更正后的表引用了 RoverPi 的接线表。

### The safety consequence, and what the board buys / 安全后果，以及板子买到了什么

The warning in the source table is not decoration. On the Raspberry Pi header,
**3.3 V is physical pin 1 and pin 17, while 5 V is pin 2 and pin 4** — one row
over, immediately adjacent. A dupont wire can be moved there by mistake in a
second, and 5 V into a 3.3 V isolated input is not a stall or a twitch, it is a
damaged part.

This is a **new and stronger argument for Rev A than the one the README currently
makes.** Vibration loosening a jumper causes undefined motor behavior;
mis-plugging `V` destroys hardware. A copper trace from pin 1 to `V` cannot be
mis-plugged at all — the failure mode disappears permanently.

源表里那句警告不是摆设。树莓派排针上，**3.3 V 是 1 号和 17 号针，5 V 是 2 号和 4 号针**，
就在隔壁一排、紧挨着。杜邦线一秒钟就能插错过去，而 5 V 灌进 3.3 V 的隔离输入不是"停车"或
"抽动"，是**烧器件**。

这是**比 README 现在写的理由更强的一个理由**：振动松脱导致电机行为未定义；`V` 插错直接
毁硬件。而从 1 号针到 `V` 的一段铜箔**根本无法插错**——这个失效模式永久消失。

---

## Correction 2 — it is 10 connections, not 7 / 更正二：是 10 个连接，不是 7 个

The D50A control header has 10 positions and **all 10 are used**:

```
上排 (Channel 2, 右侧电机)：V   P2   A2   B2   G
下排 (Channel 1, 左侧电机)：V   P1   A1   B1   G
```

So Rev A carries **10 copper connections forming 8 nets** — not 7 connections
and 7 nets. `V` and `G` each appear twice on the D50A but are one net each.

Every occurrence of "7 dupont wires", "7 根杜邦线", and "7 direct copper
connections" in this repository has been corrected.

D50A 控制口有 10 个位置，**10 个全部都用**。所以 Rev A 是 **10 个铜连接、8 个网络**，
不是 7 个。仓库里所有"7 根杜邦线""7 direct copper connections"都已更正。

### The corrected signal map / 更正后的信号表

| D50A silkscreen | Signal | Pi physical pin | BCM / rail | Channel |
|:---:|---|---:|---|---|
| `P1` | `PWM1` | 32 | GPIO12 | 1 — left motors |
| `A1` | `INA1` | 16 | GPIO23 | 1 |
| `B1` | `INB1` | 18 | GPIO24 | 1 |
| `P2` | `PWM2` | 33 | GPIO13 | 2 — right motors |
| `A2` | `INA2` | 29 | GPIO5 | 2 |
| `B2` | `INB2` | 31 | GPIO6 | 2 |
| `G` (×2) | `GND` | 34, 39 | GND | both |
| `V` (×2) | `+3V3` | **1, 17** | **3.3 V — never 5 V** | both |

Note the board's actual silkscreen is the short form `V P1 A1 B1 G`, **not** the
datasheet's `VCC PWM1 INA1 INB1 GND`. Confirmed from the 2026-09-12 photographs.

注意板上**实际丝印是简写 `V P1 A1 B1 G`**，不是数据手册里那套 `VCC PWM1 INA1 INB1 GND`。
由 2026-09-12 的照片确认。

---

## Also confirmed from the photographs / 照片还确认了什么

### The control header is a boxed header, and that is good news / 控制口是牛角座

The D50A's 2×5 control header sits inside a **black plastic shroud** — it is a
`DC3-10P` boxed header, not a bare pin field.

This **corrects a claim made earlier the same day**: it was stated that keying
would only protect the adapter's own end because "the D50A's header is
unshrouded". That is wrong. The D50A end is already keyed, so fitting the adapter
with a matching `DC3-10P` makes **both ends keyed** and the ribbon orientation a
single solution rather than a habit to be maintained.

D50A 的 2×5 控制口装在一圈**黑色塑料外壳**里，是 `DC3-10P` 牛角座，不是光排针。

这**更正了同一天早先的一个说法**：当时说防呆只保得住转接板自己那一端，因为"D50A 那端是
光针"。这是错的。**D50A 这一端本来就防呆**，所以转接板配上同规格的 `DC3-10P` 之后，
**两端都防呆**，排线方向从"要靠习惯维持"变成"唯一解"。

### Still unresolved: which pin is pin 1 / 仍未解决：哪个针是第 1 脚

The photographs are not sharp enough to read the shroud's key notch or to see
whether any of the header's pads is square. **This is not guessed.** Getting it
wrong swaps `PWM1` onto the driver's `P2` input and drives the wrong motors.

It does not block drawing the schematic. J2 will be drawn against a stated
assumption, and the assumption becomes a **hard gate before footprints are
frozen**, resolved with a meter once the cables arrive:

1. Plug the ribbon onto the D50A — with both ends keyed, only one orientation is possible.
2. At the other end of the ribbon, find which conductor reaches each D50A signal, by continuity.
3. The two conductors reaching `G` also verify the map, because `G` is continuous with the motor-power negative (`P-`).

照片不够清楚，看不出外壳缺口朝哪一侧，也看不出有没有方形焊盘。**这个不猜**——猜错会把
`PWM1` 接到驱动板的 `P2` 输入上，开错电机。

它不阻塞画原理图：J2 按一个写明的假设画，然后这个假设成为**锁封装前的硬闸门**，排线到货后
用万用表解决（两端都防呆，只有一个插法；逐根量导通即可，`G` 与电机电源负极 `P-` 导通，
可以交叉验证）。

### The direction truth table / 方向真值表

From WHEELTEC's own STM32 example (`moto.c`):

| Action | INA | INB | PWM duty |
|---|:---:|:---:|---|
| Forward `moto(1)` | high | low | 3000/7200 ≈ 42% |
| Reverse `moto(0)` | low | high | 4000/7200 ≈ 56% |

`pwm.c` runs the PWM at **72 MHz / 7200 = 10 kHz**, which is the frequency the
vendor's own example uses.

**The vendor never drives both direction pins to the same level.** This matters,
because the reserved pull-down resistors do exactly that: with the Pi's GPIO
high-impedance, both `A` and `B` are pulled low. For this class of H-bridge, both
low is expected to mean *stopped* — but the vendor has neither documented nor
demonstrated it.

**So "pull-downs give a safe power-on state" is an assumption, not a fact.** It
is now a bring-up test item (see below).

WHEELTEC 自己的例程里，方向是**互补**的（一高一低），**从来没有把两个方向脚驱动到同一电平**。
这件事重要，因为预留的下拉电阻做的正是"两个都低"。按这类 H 桥的通行逻辑，两个都低应该是
"停"，但**厂家既没有写进文档，也没有演示过**。

所以"下拉电阻提供上电安全状态"目前是**假设，不是事实**，已列为上电测试项。

---

## Consequences for Rev A / 对 Rev A 的影响

| | Before | After |
|---|---|---|
| Copper connections | 7 | **10** |
| Nets | 7 | **8** — `+3V3` added |
| `V` pins | intentionally unconnected | **connected to Pi 3.3 V (pins 1 and 17)** |
| Board-side connectors | plain headers acceptable | **`DC3-10P` boxed header required** at J2 |
| Does the board carry power? | no | **yes — a 3.3 V rail from the Pi.** Still no active components, no regulator, no motor power |

Because the board now routes a 3.3 V rail, two items are added to bring-up:

- **Measure the current the D50A's isolated side draws from the Pi's 3.3 V.** Expected to be small, but it is now the Pi's rail paying for it, so it gets a number instead of an assumption.
- **With wheels lifted, hold both direction pins low and apply PWM. Confirm the motor does not turn.** This is the pull-down safe-state assumption above. If both-low is not "stopped", the pull-down plan has to be redesigned.

因为板子现在要走一条 3.3 V，上电测试增加两项：**测 D50A 隔离侧从 Pi 的 3.3 V 上取多少电流**
（预计很小，但既然是 Pi 的电源在付账，就要有个数而不是一个假设）；**架空轮子，把两个方向脚
都拉低再加 PWM，确认电机不转**（验证上面那个下拉假设，不成立就要重新设计）。

---

## Files corrected / 改了哪些文件

- `README.md` — connection count, the `V` correction, and the 3.3 V / 5 V argument added to what the board buys
- `docs/roadmap.md` — Stage 1 specification, signal map, connector requirement, new bring-up items
- `docs/tools-and-parts.md` — the connector decision, and the withdrawn "keying only protects your own end" claim
- `hardware/stage1-signal-adapter/README.md`, `bom.md` — scope and BOM
- `docs/devlog/2026-09-11-signal-adapter-planning.md` — **not rewritten.** A correction banner was added at the top pointing here, per this repository's rule that withdrawn conclusions stay in the history

2026-09-11 那篇开发日志**没有被改写**，只在顶部加了一条指向本篇的更正提示——按本仓库
"被撤回的结论留在历史里"的规矩。

## Next / 下一步

1. Add `+3V3` to J1 pins 1 and 17 in the schematic, with a `PWR_FLAG` on that net. Target ERC: 40 errors / 6 warnings.
2. Draw J2's 10 connections against the stated pin-1 assumption. Warnings should fall to 0.
3. When the cables arrive: resolve pin 1 with the meter, **before footprints are frozen**.
