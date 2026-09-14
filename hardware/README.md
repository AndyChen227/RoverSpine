# Hardware

One directory per board. A board revision is never overwritten — revision B goes
next to revision A.

## Boards

| Board | Stage | State | Description |
|---|:---:|:---:|---|
| [`stage1-signal-adapter`](stage1-signal-adapter/) | 1 | `[ ]` Rev A — schematic complete, footprints not assigned | Passive adapter, 10 connections / 14 nets, Pi ↔ D50A |

Nothing has been fabricated yet. Stage 0 deliberately produces no board.

## No board here is a HAT

The Raspberry Pi 5 carries an active cooler, so **nothing can stack on its 40-pin
header.** Every board in this directory is a separate board in its own small
enclosure, connected by ribbon cable. This is a physical fact about the vehicle —
see [the mechanical constraint](../docs/roadmap.md#mechanical).

## Directory convention

```text
hardware/
└── <stage>-<board-name>/
    ├── README.md              # What this board does, its revisions, its status
    ├── kicad/                 # The KiCad project
    ├── bom.md                 # Bill of materials
    ├── tools/                 # Checkers run after every change
    ├── fab/
    │   ├── revA.zip           # The exact Gerbers sent to the fab
    │   └── revB.zip
    └── bringup.md             # First-power results and measurements
```

## Rules

1. **Commit the exact Gerber zip that was uploaded to the fab**, per revision.
   Regenerating Gerbers later from a modified project gives files that were never
   manufactured, which makes debugging a physical board impossible. The ordering
   process and pre-upload checklist are in
   [`../docs/fabrication.md`](../docs/fabrication.md).
2. **`bringup.md` is written during first power-up, not afterwards.** Record the
   current draw, the measured voltages, and every surprise.
3. **A board's `README.md` states its status in the three-state notation:**
   `[x]` met its exit criteria on the rover · `[~]` exists and powers up ·
   `[ ]` pending. **Never `[x]` because the schematic looks right.**
4. **Photograph every board bare and assembled** before it goes on the rover.
   Photos go in [`../photos/`](../photos/).
5. **The KiCad project lives under the board's own directory**, not at the
   repository root. `*.kicad_prl` and editor local-history folders are
   gitignored; the schematic, layout and project files are committed.
6. **Empty board area is not a reason to add a circuit.** Each board's README
   lists what it deliberately does *not* do, so an absence is a recorded decision
   rather than an oversight.

---

# 硬件 / 中文

每块板一个目录。**改版不覆盖旧版**：B 版和 A 版并排放着。

## 板子索引

| 板子 | 阶段 | 状态 | 说明 |
|---|:---:|:---:|---|
| [`stage1-signal-adapter`](stage1-signal-adapter/) | 1 | `[ ]` Rev A——原理图完工，封装未分配 | 被动信号转接板，10 个连接 / 14 个网络，Pi ↔ D50A |

目前还没有打样过任何板子。第 0 阶段有意不做板。

## 这里没有一块板是 HAT

树莓派 5 上装了主动散热器，**40 针排针上不能再叠任何东西**。这个目录里的每一块板都是装在
自己小外壳里的独立板，用排线连接。这是车的物理事实——见[机械约束](../docs/roadmap.md#mechanical)。

## 目录约定

```text
hardware/
└── <阶段>-<板名>/
    ├── README.md              # 这块板做什么、版本历史、状态
    ├── kicad/                 # KiCad 工程
    ├── bom.md                 # 物料清单
    ├── tools/                 # 每次改动后要跑的核对脚本
    ├── fab/
    │   ├── revA.zip           # 真正发给工厂的那份 Gerber
    │   └── revB.zip
    └── bringup.md             # 首次上电的结果与测量
```

## 规矩

1. **提交真正上传给打样厂的那个 Gerber 压缩包**，按版本存。以后从改过的工程重新导出，
   得到的是从来没被制造过的文件，那样就没法排查手里这块实体板了。下单流程和上传前清单
   在 [`../docs/fabrication.md`](../docs/fabrication.md)。
2. **`bringup.md` 在第一次上电的过程中写，不是事后补。** 记下电流、实测电压和每一个意外。
3. **每块板的 `README.md` 用三态标注状态：** `[x]` 已在车上通过完成判据 ·
   `[~]` 存在并且能上电 · `[ ]` 待办。**原理图看起来没问题，永远不能标成 `[x]`。**
4. **每块板在装车前都要拍空板和焊好之后的照片**，放在 [`../photos/`](../photos/)。
5. **KiCad 工程放在对应板子的目录下**，不放在仓库根目录。`*.kicad_prl` 和编辑器的本地
   历史目录已被 gitignore；原理图、布局和工程文件要提交。
6. **板上有空地不是加电路的理由。** 每块板的 README 都列出它有意不做的事，让"没有"成为
   一个被记录的决定，而不是一次遗漏。
