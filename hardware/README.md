# Hardware / 硬件

One directory per board. A board revision is never overwritten — revision B goes
next to revision A, because the whole point of keeping A is being able to see
what changed and why.

每块板一个目录。**改版不覆盖旧版**：B 版和 A 版并排放着，因为留下 A 版的全部意义
就是能看出改了什么、为什么改。

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

Example: `hardware/stage1-status-hat/`

## Rules / 规矩

1. **Commit the exact Gerber zip that was uploaded to the fab**, per revision.
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

## Status / 当前状态

No boards have been fabricated yet. Stage 0 deliberately produces no board — see
the [roadmap](../docs/roadmap.md).

目前还没有打样过任何板子。第 0 阶段有意不做板，见[路线图](../docs/roadmap.md)。
