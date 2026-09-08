# Licensing / 许可证

This repository contains two different kinds of work, and they are licensed
differently because one licence does not fit both.

本仓库包含两类不同性质的成果，采用两种不同的许可证——因为一种许可证套不住两者。

| What | 内容 | Licence | Full text |
|---|---|---|---|
| Hardware designs: schematics, PCB layouts, KiCad projects, Gerbers, board BOMs | 硬件设计：原理图、PCB 布局、KiCad 工程、Gerber、板子物料清单 | **CERN-OHL-S-2.0** | [`LICENSES/CERN-OHL-S-v2.txt`](LICENSES/CERN-OHL-S-v2.txt) |
| Firmware, scripts, and tooling | 固件、脚本与工具代码 | **MIT** | [`LICENSES/MIT.txt`](LICENSES/MIT.txt) |
| Documentation, devlogs, and photographs | 文档、开发日志与照片 | **MIT** | [`LICENSES/MIT.txt`](LICENSES/MIT.txt) |

Copyright (c) 2026 Andy Chen.

## Why two licences / 为什么用两种

MIT was written for software. It never defines what "source" means for a
circuit board — is it the schematic, the layout, the Gerbers? — and it says
nothing about the patent questions that hardware raises. CERN-OHL-S was written
by CERN specifically for open hardware, and it answers both.

**CERN-OHL-S is the strongly reciprocal variant:** anyone who makes or
distributes a product based on these designs, or a modified version of them,
has to release their design source under the same terms. That is a deliberate
choice. These boards exist to be learned from.

MIT 是为软件写的。它从未定义电路板的"源码"指什么——原理图？布局？Gerber？——也
没有处理硬件涉及的专利问题。CERN-OHL-S 是 CERN 专门为开源硬件写的，这两点都有
明确答复。

**CERN-OHL-S 是强互惠版本**：任何人基于这些设计制造或分发产品，或者分发修改后的
版本，都必须以相同条款公开自己的设计源文件。这是有意选择的——这些板子存在的意义
就是被人学习。

## Safety disclaimer / 安全免责

> [!CAUTION]
> Neither licence provides any warranty, and neither provides any warranty of
> **physical safety** in particular.
>
> This project designs circuits that carry lithium-polymer battery current and,
> in later stages, switching power supplies and motor H-bridges. A design
> published here may be untested, may be a revision that was later found to be
> wrong, or may be correct only for the specific rover it was built for.
>
> Anyone reproducing this work is responsible for their own wiring, battery
> handling, fusing, thermal design, and test procedure.

> [!CAUTION]
> 两份许可证都不提供任何担保，**尤其不对实体安全提供任何担保**。
>
> 本项目设计的电路会承载锂聚合物电池电流，后期阶段还包括开关电源与电机 H 桥。
> 这里发布的某个设计可能尚未测试、可能是后来被证明有错的版本、也可能只对它当初
> 服务的那台特定小车成立。
>
> 复现本项目的人，需要自行对接线、电池处理、保险丝、热设计和测试流程的安全负责。
