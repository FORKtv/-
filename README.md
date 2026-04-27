# 音乐批量重命名工具

这是一个基于 `Python + Tkinter + mutagen` 的 Windows 本地音乐批量重命名工具。

当前版本已经完成：

- 第一阶段：现代化界面重构
- 第二阶段：真实元数据读取、预览生成、安全批量重命名
- 第三阶段：交互增强、历史记录、设置保存、主题切换、日志窗口

## 支持格式

- `.mp3`
- `.flac`
- `.m4a`
- `.wav`
- `.dsf`

说明：

- 扫描时忽略扩展名大小写
- 重命名时保留原始扩展名
- 不支持的文件不会加入列表
- 单个文件读取失败不会中断整个任务

## 已实现功能

- 现代化桌面界面
- 左侧导航栏页面反馈
- 拖拽文件 / 文件夹导入
- 添加文件、添加文件夹、移除
- 可选是否包含子文件夹
- 读取 `标题 / 艺术家 / 专辑 / 曲号 / 年份`
- 规则标签支持：
  - `[标题]`
  - `[艺术家]`
  - `[专辑]`
  - `[曲号]`
  - `[年份]`
- 默认规则：`[标题] - [艺术家]`
- 搜索和状态筛选
- 表格右键菜单
- 双击手动编辑“新文件名”
- 自动清理非法字符、空格、重复连接符、末尾点号、过长路径
- 重名自动编号
- 扫描、预览、重命名、撤销均为异步执行
- 支持取消扫描
- 支持取消剩余重命名任务
- 批量安全重命名
- 执行日志
- 撤销脚本
- 历史记录本地保存
- 设置本地保存
- 浅色 / 深色主题切换
- 日志窗口查看最近日志和历史日志

## 元数据读取说明

### MP3

- 读取 ID3 / EasyID3
- 支持 `Title / Artist / Album / Track / Year`

### FLAC

- 读取 Vorbis Comment
- 支持 `title / artist / album / tracknumber / date`

### M4A

- 读取 MP4 标签
- 支持标题、艺术家、专辑、曲号、日期

### WAV

- 使用 `mutagen.wave.WAVE`
- 没有标准标签时不会中断任务
- 没有标题时会显示“缺失标签”或“标题为空”

### DSF

- 使用 `mutagen.dsf.DSF`
- 尝试读取内嵌 ID3 信息
- 读取失败时只标记该文件，不影响其他文件

## 历史和设置文件

程序会在当前 Windows 用户目录下保存配置和历史：

- 配置：`%APPDATA%\\MusicTitleRenamer\\config.json`
- 历史：`%APPDATA%\\MusicTitleRenamer\\history.json`

## 项目结构

```text
.
|-- main.py
|-- requirements.txt
|-- README.md
`-- music_renamer
    |-- __init__.py
    |-- core.py
    |-- models.py
    |-- storage.py
    `-- ui.py
```

## 文件说明

- `main.py`
  程序入口。
- `music_renamer/models.py`
  定义扫描选项、元数据结构、预览表格项和撤销记录。
- `music_renamer/core.py`
  负责格式识别、元数据读取、命名规则解析、文件名清理、冲突检测、日志和撤销脚本生成。
- `music_renamer/storage.py`
  负责配置文件、历史记录和日志目录的本地持久化。
- `music_renamer/ui.py`
  负责桌面界面、导航、导入、搜索筛选、表格交互、历史页、设置页、日志窗口和异步任务联动。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python main.py
```

## PyInstaller 打包命令

```bash
pyinstaller --noconsole --onefile --name MusicTitleRenamer --collect-all mutagen --collect-all tkinterdnd2 main.py
```

打包输出：

```text
dist/MusicTitleRenamer.exe
```

## 当前 TODO

- `TODO`: 左侧“重命名规则”和“预览结果”当前采用主界面聚焦反馈，不是完全独立的复杂子页面。
- `TODO`: 预览任务已异步化，但目前没有逐项进度文本，后续可以继续细化。
- `TODO`: 日志窗口当前以文本查看为主，后续可以扩展为多标签日志浏览器。
