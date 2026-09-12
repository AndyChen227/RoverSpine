# Tools and Parts Log / 工具与零件记录

This is a dated record of tools, software, cables, and parts actually selected for RoverSpine. Items are added only after a real need is identified; this is not a wish list.

这里按日期记录 RoverSpine 已经确定要用的软件、工具、排线和零件。只有确认用途之后才加入，不把它写成愿望清单。

## 2026-09-11 — Rev A cable selection / Rev A 排线选择

### 1. 10P IDC ribbon cable / 10P IDC 排线

- Connector: 2×5 female to female / 2×5 母头对母头
- Pitch: 2.54 mm
- Length: about 35 cm / 约 35 cm
- Quantity: 1
- Search phrase: FC-10P 2x5 IDC 母对母 排线 35cm
- Purpose: flexible connection from the upper-deck adapter PCB to the lower-deck D50A motor driver / 从第二层转接板绕到第一层 D50A 驱动板
- Status: selected; waiting for delivery / 已选定，等待到货

### 2. Raspberry Pi 40-pin GPIO ribbon cable / 树莓派 40 针 GPIO 排线

- Connector: 2×20 female to female / 2×20 母头对母头
- Pitch: 2.54 mm
- Length: 10–15 cm
- Quantity: 1
- Search phrase: 树莓派 40Pin GPIO 母对母 排线 15cm
- Purpose: connect the Raspberry Pi 5 to the adapter without stacking a PCB above the active cooler / 在不遮挡主动散热器的情况下连接树莓派与转接板
- Status: selected; waiting for delivery / 已选定，等待到货

## Software currently used / 当前软件

| Tool | Version | Purpose | Added |
|---|---|---|---|
| KiCad | 10.0.6 | Schematic capture and PCB layout / 原理图与 PCB 设计 | 2026-09-08 |
| Git and GitHub | — | Revision history and project documentation / 版本管理与项目记录 | 2026-09-11 |

## Arrival checks / 到货后检查

- Verify that both cables are truly female-to-female.
- Verify 2.54 mm pitch and keyed-plug orientation.
- Identify the red-stripe/pin-1 direction at both ends.
- Check continuity before connecting either cable to the rover.

- 确认两条排线确实都是母对母。
- 确认 2.54 mm 间距以及防呆口方向。
- 确认排线两端红边对应的 1 号针方向。
- 接入小车前先用万用表逐针检查导通关系。
