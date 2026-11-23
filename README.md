# FIRS 产业替换包 5.2.0 —— 简体中文版 (Simplified Chinese)

[FIRS Industry Replacement Set](https://github.com/andythenorth/firs) **5.2.0 标签版**的简体中文本地化构建，把 GRF 内全部 **533 条**可见字符串翻译成简体中文。

A Simplified Chinese localisation build of FIRS **5.2.0 (git tag)**, translating all **533** game-visible strings embedded in the GRF.

## 下载 / Download

见 [Releases](https://github.com/ljnljn2005/firs-zh/releases)。

### 两个变体 / Two variants

| 文件 | GRF ID | 用途 |
| --- | --- | --- |
| `FIRS-Industries-5-5.2.0-zh2.tar` | `f1250009`（同上游） | 直接替换英文版 FIRS 5，已有存档可继续加载 |
| `FIRS-Industries-5-5.2.0-zh2-bananas.tar` | `f1250091`（独立） | 独立包，用于上传 BaNaNaS / 与官方 FIRS 同时安装 |

BaNaNaS 的唯一标识就是 GRF ID，沿用 `f1250009` 会被当作官方 FIRS 的新版本；作为独立内容发布必须换成自己的 ID，所以提供第二个变体。代价是它无法替换老存档里的英文 FIRS（会提示缺少 NewGRF）。

### ⚠️ 必须用 5.2.0 标签源码构建

`main` 分支是 5.2.0 之后的开发版（内容已接近 FIRS 6），用它编译出的 GRF 约 32.6 MB，与官方结构不符，**游戏会把它判为无效并在新GRF列表中静默隐藏**（`FillGRFDetails` 失败即不入列表）。用 `refs/tags/5.2.0` 编译得到 9,074,349 B，与官方 9,060,291 B 同量级，可正常加载。

## 安装 / Install

1. 把 tar 放到 OpenTTD 的 `content_download/newgrf/` 目录（**不用再套文件夹**）：
   - Windows: `%USERPROFILE%\Documents\OpenTTD\content_download\newgrf\`
   - Linux: `~/.local/share/openttd/content_download/newgrf/`
   - macOS: `~/Documents/OpenTTD/content_download/newgrf/`
2. 如果已经装了英文版 FIRS 5.2.0，先把它移除（两者 GRFID 相同，不能共存）。
3. 启动游戏，在「游戏选项 → 新GRF设置 → 添加」里应能看到 `FIRS 产业替换包`；界面语言为简体中文时产业名/货物名显示中文。

## 兼容性 / Compatibility

- **GRFID 与上游一致**（`f1250009`，可替换变体），可以直接替换英文版 FIRS 5；由于文件 md5 不同，游戏可能提示 "GRF 已变更"，确认后即可进入，存档内容不受影响。
- 与上游 FIRS 5.2.0 的产业、货物、参数、经济数值完全一致，**只改文本**。
- 支持 OpenTTD 官方版与 JGRPP（在 JGRPP 0.73.5 上验证构建流程与加载）；GRF 语言 ID 为 `0x56`（简体中文），繁体中文（`0x0c`）玩家会回退到英文。

## 翻译范围 / Coverage

| 类别 | 条数 | 说明 |
| --- | --- | --- |
| `STR_CARGO_NAME_*` | 97 | 货物名 |
| `STR_CARGO_UNIT_*` | 97 | 货物单位（`{WEIGHT}X` / `{SIGNED_WORD}X箱` 等） |
| `STR_IND_*` | 97 | 产业名 |
| `STR_STATION_*` | 81 | 车站/码头名 |
| 参数、错误码、资助说明、产量说明等 | 62 | 含 20 条参数名/说明、E00–E04 错误码、`STR_FUND_*`、`STR_PRIMARY_*`、`STR_PORT_*` |
| `STR_CID_*` | 100 | 保持英文缩写（`{TINYFONT}XX`，游戏内 cargo 缩写，翻译会超宽） |

校验脚本保证：① 英文字符串与译文一一对应（533/533）；② 每条译文的 `{...}` 控制码多重集与英文完全一致（0 冲突）；③ 不存在漏译或多余条目。当前构建输出：`wrote 533 missing 0 badcodes 0`。

## 自行构建 / Build from source

```bash
pip install nml chameleon                       # 需要 nml 0.9.x（0.8 无法解析 5.2.0 的 nml）
git clone --depth 1 --branch 5.2.0 https://github.com/andythenorth/firs.git
cd firs && git tag 5.2.0                        # nmlc 用 git describe 取版本号，缺 tag 会报 Unrecognized identifier 'undefined'

python ../tools/build_zh520.py                  # 生成 src/grf/lang/schinese.toml
python src/render_lang.py "" "" "grf"
python src/render_nml.py "" ""
python src/render_graphics.py "" ""
nmlc -c -l generated/lang --no-optimisation-warning --list-unused-strings \
     --grf=generated/firs.grf generated/firs.nml
python src/render_docs.py "" ""
```

打包目录结构（与官方 tar 一致）：`FIRS_Industries_5-5.2.0-zh2/{firs.grf,readme.txt,changelog.txt,license.txt}`。

## 已知问题 / Known issues

- 只翻译了 GRF 文本；FIRS 随附的 GameScript 版文本（`src/gs/lang/english.toml`）不在本包内。
- 5.2.0 的语言文件是平铺的 `base` 键（无 `name`/`cargo_unit` 字段），与 `main` 分支结构不同，两套脚本不通用。
- 台湾/繁体用户会回退到英文；如需繁体可提 Issue（改 `grflangid = "0x0c"` 并重译用词即可）。

## 许可 / License

- 本翻译基于 FIRS，遵循 **GNU GPL v2**（见 `LICENSE`），与上游一致。
- 上游作者：Andy Thurlow (andythenorth) 及 FIRS 贡献者；本仓库仅新增 `src/grf/lang/schinese.toml` 与 `tools/` 下的生成脚本。
- 若发现误译，欢迎提 Issue 或 PR —— 翻译源在 `tools/zh520_*.json`，改完跑 `tools/build_zh520.py` 重新生成 TOML 即可。
