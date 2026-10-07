# filisi 研究文库网页

轻量纯静态中文全文文库。支持正文搜索、多关键词匹配、命中高亮、主题筛选、在线阅读、章节目录、Word/PDF 下载、明暗主题及手机布局。搜索条件、主题和文章由 URL 保存，可分享与前进/后退。无外部字体、统计、账号或服务端。

## 构建与内容边界

环境要求：Python 3.10+、Pandoc 3.1+。前端无 npm 依赖。

从仓库根目录运行：

```sh
python3 site/build.py
```

产物在 `site/dist/`。`publication.json` 是明确允许公开的文章 ID 清单，**新增 manifest 条目不会自动公开**。本次清单只包含已经确认的 124 项；以后每批确认范围再逐项加入。空清单产生空文库，不带正文、图片或原件；删除条目后重新构建会清除旧输出。构建会拒绝未知 ID 和非自身管理的既有输出目录。

每个允许条目仅复制 manifest 声明的主 Markdown、来源索引、图片和原件，不复制整个仓库。文章渲染只允许本条目已声明的本地文件链接与 HTTP(S) 来源链接，外部图片不会加载，原始 HTML 不执行。源文稿、原件内容本身应在加入公开清单前完成隐私及版权复核。

## 本地阅读

```sh
python3 -m http.server 8766 --directory site/dist
```

浏览器访问 http://localhost:8766/ 。不要直接用 file:// 打开，它无法可靠加载 JSON。

## GitHub Pages 集成

由仓库维护者将 `site/dist/` 的**内容**同步到根 `docs/`（包括 `.nojekyll`），并配置 Pages 来源为 `main` 分支的 `/docs`。站点路径无硬编码，支持 `https://用户名.github.io/仓库名/`。不要把源仓库根目录当作 Pages 发布目录，也不要将临时预览、测试目录上传。

每次更新：先复核 manifest 和公开清单 → 运行构建与测试 → 替换 docs 中的旧生成内容 → 提交 → 等待 Pages 部署 → 在实际地址复查搜索、目录、返回和下载。

公开网页不是访问控制。未获准内容不能只在 UI 隐藏：必须不在构建清单和导出文件中。若源仓库本身公开，源仓库文件及历史也会公开，应另行核对。

## 验证

```sh
cd site
python3 -m unittest test_build -v
node test_search.mjs
node --check app.js
node --check search.mjs
```

可选真实浏览器测试（需要 Playwright Python 包与可启动的 Chromium）：启动上述本地服务器后运行 `python3 site/test_browser.py`。脚本覆盖搜索、高亮、目录、直接 URL/刷新、前进后退、恶意查询、主题、键盘、手机溢出、图像及下载。

本次本地检查覆盖124篇正文重组、全部内部文件链接、全文搜索、并发上限、失败重试和路由门禁。每次发布后还需在实际Pages检查阅读、搜索、图像与下载；不能将静态测试视为浏览器验收。

## 文件

- `index.html` / `style.css` / `app.js`：界面、响应式样式与阅读状态
- `search.mjs`：可独立测试的中文子串搜索、排序与纯文本高亮分段
- `build.py`：显式清单驱动的 Pandoc 安全转换、附件复制及索引生成
- `publication.json`：逐项公开白名单
- `test_build.py` / `test_search.mjs` / `test_browser.py`：测试
- `dist/`：可再生发布产物，不作为源文件提交

## 分片数据与发布边界

构建输出使用 schema 2。`catalog.json` 仅列出内容寻址的元数据、搜索分片；每个生成 JSON 不超过 180,000 字节，测试以 200,000 字节为硬上限。首页只加载元数据；文章分享链接按需加载对应的阅读清单及 HTML 分块；第一次非空搜索才读取全文索引，分块按原次序合并。正文、目录锚点、来源和原格式下载保持完整。

`data/` 文件名来自内容 SHA-256，入口脚本带本次索引版本。修改一篇文章时，复用其他文章的数据文件。发布必须把数据文件、索引和脚本纳入同一提交，不先改线上索引再补内容。回滚使用上一提交的完整站点产物。

验证：`python3 -m unittest test_build -v`、`node test_search.mjs`、`node test_data.mjs`、`node test_sharded_library.mjs ../docs`。全文检索测试逐篇使用正文片段探测，并校验阅读分块复原与下载路径。数据加载失败时保留明确错误和重试入口；异步旧请求不能替换新路由。


## 分片数据（schema 2）

首页的 catalog.json 仅列出元数据和搜索分片。每篇正文通过独立清单加载HTML分块；首次输入查询时加载全文搜索分片，并显示进度与失败重试。加载并发上限为4，旧查询或旧阅读路由不能覆盖最新页面。列表每次显示60条，可继续展开。分享URL和原文件下载路径保持一致。

所有生成JSON限制在180000字节以内，文件名含内容哈希；修改单篇不必重传整库正文。构建拒绝超限资源。此限制针对网站数据，归档原件及主manifest仍需按各自大小管理。运行 python3 -m unittest test_build 和 node test_search.mjs、node test_data.mjs 检查完整重组、搜索覆盖、重试和路由门禁。发布应保留前一提交，必要时以普通revert提交回滚。
