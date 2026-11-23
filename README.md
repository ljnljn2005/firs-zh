# FIRS 产业替换包 5.2.0 —— 简体中文版 (Simplified Chinese)

[FIRS Industry Replacement Set](https://github.com/andythenorth/firs) 5.2.0 的简体中文本地化版本，把 GRF 内全部 357 条可见字符串翻译成简体中文。

A Simplified Chinese localisation build of FIRS 5.2.0 (OpenTTD NewGRF), translating all 357 game-visible strings embedded in the GRF.

## 下载 / Download

见 [Releases](https://github.com/ljnljn2005/firs-zh/releases)：`FIRS-Industries-5-5.2.0-zh1.tar`

### 两个变体 / Two variants

| 文件 | GRF ID | 用途 |
| --- | --- | --- |
| `FIRS-Industries-5-5.2.0-zh1.tar` | `f1250009`（同上游） | 直接替换英文版 FIRS 5，已有存档可继续加载 |
| `FIRS-Industries-5-5.2.0-zh1-bananas.tar` | `f1250091`（独立） | 独立包，用于上传 BaNaNaS / 与官方 FIRS 同时安装 |

BaNaNaS 的唯一标识就是 GRF ID，沿用 `f1250009` 会被当作官方 FIRS 的新版本；作为独立内容发布必须换成自己的 ID，所以提供第二个变体。代价是它无法替换老存档里的英文 FIRS（会提示缺少 NewGRF）。

## 安装 / Install

1. 把 tar 放到 OpenTTD 的 `content_download/newgrf/` 目录：
   - Windows: `%USERPROFILE%\Documents\OpenTTD\content_download\newgrf\`
   - Linux: `~/.local/share/openttd/content_download/newgrf/`
   - macOS: `~/Documents/OpenTTD/content_download/newgrf/`
2. 如果已经装了英文版 FIRS 5.2.0，先把它移除（两者 GRFID 相同，不能共存）。
3. 启动游戏，在「游戏选项 → 新GRF设置」里应能看到 `FIRS 产业替换包`，且界面语言为简体中文时产业名/货物名显示中文。

## 兼容性 / Compatibility

- **GRFID 与上游一致**（`f1250009`），因此可以直接替换英文版 FIRS 5，已使用 FIRS 5 的存档照常加载；由于文件 md5 不同，游戏可能提示 "GRF 已变更"，确认后即可进入，存档内容不受影响（已在 JGRPP 0.73.5 上实测加载）。
- 与上游 FIRS 5.2.0 的产业、货物、参数、经济数值完全一致，**只改文本**，不影响联机存档一致性判断以外的任何逻辑。
- 支持 OpenTTD 官方版与 JGRPP；GRF 语言 ID 为 `0x56`（简体中文），繁体中文（`0x0c`）玩家会回退到英文。

## 翻译范围 / Coverage

| 类别 | 条数 | 说明 |
| --- | --- | --- |
| `STR_CARGO_*` | 112 | 货物名 + 单位（保留 `{WEIGHT}` / `{VOLUME}` 等控制码） |
| `STR_IND_*` | 104 | 产业名 |
| `STR_STATION_*` | 87 | 车站/机场/码头名 |
| 其它 | 55 | GRF 名称与描述、参数名与说明、错误提示、资助项目、产量说明等 |

校验脚本保证：① 英文字符串与译文一一对应；② 每条译文的 `{...}` 控制码多重集与英文完全一致；③ 不存在漏译或多余条目。

## 自行构建 / Build from source

```bash
pip install nml chameleon
git clone https://github.com/andythenorth/firs.git
cd firs && git checkout 5.2.0      # 或对应 tag；nmlc 需要 git tag 生成版本号

python tools/build_zh.py            # 生成本仓库的 src/grf/lang/schinese.toml 到 firs/src/grf/lang/
python src/render_lang.py "" "" "grf"
python src/render_nml.py "" ""
python src/render_graphics.py "" ""
nmlc -c -l generated/lang --no-optimisation-warning --list-unused-strings \
     --grf=generated/firs.grf generated/firs.nml
python src/render_docs.py "" ""
```

打包目录结构（与官方 tar 一致）：`FIRS_Industries_5-5.2.0-zh1/{firs.grf,readme.txt,changelog.txt,license.txt}`。

注意：`src/grf/templates/header.pynml` 里的版本号来自 `git describe`，所以在没有 git 元数据的源码副本里编译会报 `Unrecognized identifier 'undefined'`。

## 已知问题 / Known issues

- 本仓库构建出的 `firs.grf` 约 32.6 MB，而官方发布的是 9.1 MB。nmlc 报告 35916 sprites / 34368 duplicates，功能与显示均正常，体积差异推测与 nmlc 版本的精灵编码策略有关，尚未定位。
- 只翻译了 GRF 文本，随附的 GameScript 版 FIRS（`src/gs/lang/english.toml`）未包含在本包内。

## 许可 / License

- 本翻译基于 FIRS，遵循 **GNU GPL v2**（见 `LICENSE`），与上游一致。
- 上游作者：Andy Thurlow (andythenorth) 及 FIRS 贡献者；本仓库仅新增 `src/grf/lang/schinese.toml` 与 `tools/` 下的生成脚本。
- 若发现误译，欢迎提 Issue 或 PR —— 翻译源在 `tools/zh_*.json`，改完跑 `tools/build_zh.py` 重新生成 TOML 即可。
