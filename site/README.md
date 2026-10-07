# filisi 研究文库网页

轻量纯静态中文全文文库。支持正文搜索、多关键词匹配、命中高亮、主题筛选、在线阅读、章节目录、Word/PDF 下载、明暗主题及手机布局。搜索条件、主题和文章由 URL 保存，可分享与前进/后退。无外部字体、统计、账号或服务端。

## 构建与内容边界

环境要求：Python 3.10+、Pandoc 3.1+。前端无 npm 依赖。

从仓库根目录运行：

```sh
python3 site/build.py
```

产物在 `site/dist/`。`publication.json` 是明确允许公开的文章 ID 清单，**新增 manifest 条目不会自动公开**。本次清单只包含已经确认的 34 项；以后每批确认范围再逐项加入。空清单产生空文库，不带正文、图片或原件；删除条目后重新构建会清除旧输出。构建会拒绝未知 ID 和非自身管理的既有输出目录。

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

本次自动检查：5 组 Python 构建测试、9 项 Node 搜索断言通过，34 篇的渲染和全部内部文件链接检查通过。实际 Chromium 本地启动被环境 socket 权限阻断，尚未完成浏览器视觉/交互验收；部署后必须补测，不能将静态测试视为浏览器验收。

## 文件

- `index.html` / `style.css` / `app.js`：界面、响应式样式与阅读状态
- `search.mjs`：可独立测试的中文子串搜索、排序与纯文本高亮分段
- `build.py`：显式清单驱动的 Pandoc 安全转换、附件复制及索引生成
- `publication.json`：逐项公开白名单
- `test_build.py` / `test_search.mjs` / `test_browser.py`：测试
- `dist/`：可再生发布产物，不作为源文件提交
