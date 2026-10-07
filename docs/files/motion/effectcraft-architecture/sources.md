# 来源与验证边界

2026-10-07归档。研究原文按字节保留；本次未重新运行上游源码或复核其所有结论。

[原报告](readable.md) · [源码锚点与哈希](source-map.json) · [原创标准库算例](synthetic_checks.py) · [算例结果](synthetic-results.json) · [依赖许可抽样](dependency-license-sample.json)

EffectCraft源码基线：f5ebe5f6c5e887dddda4a2be1fcb47154e959b81

## 固定版本来源

- [crates/time/src/lib.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/time/src/lib.rs)
- [crates/keyframe/src/lib.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/keyframe/src/lib.rs)
- [crates/render/src/lib.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/render/src/lib.rs)
- [crates/render/src/cache.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/render/src/cache.rs)
- [crates/render/src/disk_cache.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/render/src/disk_cache.rs)
- [crates/render/src/audio.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/render/src/audio.rs)
- [crates/render/src/tests_audio_fx.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/render/src/tests_audio_fx.rs)
- [crates/render/src/tests_time.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/render/src/tests_time.rs)
- [crates/engine/src/lib.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/engine/src/lib.rs)
- [crates/engine/src/history.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/engine/src/history.rs)
- [crates/engine/src/remote.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/engine/src/remote.rs)
- [crates/project/src/lib.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/project/src/lib.rs)
- [crates/export/src/pipeline.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/export/src/pipeline.rs)
- [crates/export/src/lib.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/export/src/lib.rs)
- [crates/ui-egui/src/frames.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/ui-egui/src/frames.rs)
- [crates/ui-egui/src/panels/graph.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/ui-egui/src/panels/graph.rs)
- [crates/ui-egui/tests/ui_timeline_zoom.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/ui-egui/tests/ui_timeline_zoom.rs)
- [crates/ui-egui/tests/ui_panel_focus.rs](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/ui-egui/tests/ui_panel_focus.rs)
- [crates/ui-egui/Cargo.toml](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/crates/ui-egui/Cargo.toml)
- [docs/web.md](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/docs/web.md)
- [docs/architecture.md](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/docs/architecture.md)
- [Cargo.toml](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/Cargo.toml)
- [LICENSE-MIT](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/LICENSE-MIT)
- [LICENSE-APACHE](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/LICENSE-APACHE)
- [NOTICE](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/NOTICE)
- [ATTRIBUTION.md](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/ATTRIBUTION.md)
- [docs/brand/LICENSE-brand.txt](https://github.com/storytold/effectcraft/blob/f5ebe5f6c5e887dddda4a2be1fcb47154e959b81/docs/brand/LICENSE-brand.txt)

仅收录原创研究、路径/哈希/链接元数据与自造数据算例；没有复制EffectCraft仓库、品牌图标、字体、模型或用户媒体。上游测试未实际执行，许可核对为抽样，不能视为完整分发审计。
