# Hardware / 硬件

One directory per board. A board revision is never overwritten — revision B goes
next to revision A, because the whole point of keeping A is being able to see
what changed and why.

每块板一个目录。**改版不覆盖旧版**：B 版和 A 版并排放着，因为留下 A 版的全部意义
就是能看出改了什么、为什么改。

## Boards / 板子索引

| Board | Stage | State | 说明 |
|---|:---:|:---:|---|
| [`stage1-signal-adapter`](stage1-signal-adapter/) | 1 | `[ ]` Rev A — schematic done, footprints not frozen | Passive adapter, 10 connections / 8 nets, Pi ↔ D50A / 被动信号转接板 |

Nothing has been fabricated yet. Stage 0 deliberately produces no board — see
the [roadmap](../docs/roadmap.md).

目前还没有打样过任何板子。第 0 阶段有意不做板，见[路线图](../docs/roadmap.md)。

## No board here is a HAT / 这里没有一块板是 HAT

The Raspberry Pi 5 carries an active cooler, so **nothing can stack on its 40-pin
header.** Every board in this directory is a separate board in its own small
enclosure, connected by ribbon cable. This is a physical fact about the vehicle,
not a design preference — see
[the mechanical constraint](../docs/roadmap.md#mechanical).

树莓派 5 上装了主动散热器，**40 针排针上不能再叠任何东西**。这个目录里的每一块板都是
装在自己小外壳里的独立板，用排线连接。这是车的物理事实，不是设计偏好——见
[机械约束](../docs/roadmap.md#mechanical)。

## Directory convention / 目录约定

```text
hardware/
└── <stage>-<board-name>/
    ├── README.md              # What this board does, its revision history, its status
    ├── kicad/                 # The KiCad project — schematic, layout, project files
    ├── bom.md                 # Bill of materials, with the actual parts ordered
    ├── fab/
    │   ├── revA.zip           # The exact Gerbers that were sent to the fab
    │   └── revB.zip
    └── bringup.md             # First-power results, measurements, what was wrong
```

Example: `hardware/stage1-signal-adapter/`

## Rules / 规矩

1. **Commit the exact Gerber zip that was uploaded to the fab**, per revision.
   The ordering process and the pre-upload checklist are in
   [`../docs/fabrication.md`](../docs/fabrication.md).
   Regenerating Gerbers later from a modified project gives you files that were
   never manufactured, which makes debugging a physical board impossible.
   **提交真正上传给打样厂的那个 Gerber 压缩包**，按版本存。以后从改过的工程重新
   导出，得到的是从来没被制造过的文件，那样就没法排查手里这块实体板了。

2. **`bringup.md` is written during first power-up, not afterwards.** Record the
   current draw, the measured voltages, and every surprise, while you still
   remember what you actually did.
   **`bringup.md` 在第一次上电的过程中写，不是事后补。** 记下电流、实测电压和
   每一个意外——趁你还记得自己到底做了什么。

3. **A board's `README.md` states its status in the three-state notation:**
   `[x]` met its exit criteria on the rover · `[~]` exists and powers up ·
   `[ ]` pending. Never `[x]` because the schematic looks right.

4. **Photograph every board bare and assembled** before it goes on the rover.
   Photos go in [`../photos/`](../photos/).

5. **The KiCad project lives under the board's own directory**, not at the
   repository root. `*.kicad_prl` (per-user UI state) and editor local-history
   folders are gitignored; the schematic, layout and project files are committed.
   **KiCad 工程放在对应板子的目录下**，不放在仓库根目录。`*.kicad_prl`（每个用户的
   界面状态）和编辑器的本地历史目录已被 gitignore；原理图、布局和工程文件要提交。

6. **Empty board area is not a reason to add a circuit.** Each board's README
   lists what it deliberately does *not* do, so that an absence is a recorded
   decision rather than an oversight.
   **板上有空地不是加电路的理由。** 每块板的 README 都列出它"有意不做"的事，让"没有"
   成为一个被记录的决定，而不是一次遗漏。
