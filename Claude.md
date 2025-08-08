# Claude.md - 项目核心信息

## 项目概述
- **项目名称**: simulate-to-survive
- **游戏类型**: 文字游戏
- **开发语言**: Python + Pygame
- **项目状态**: 基础框架完成，可运行

## 调试和测试方法

### 快速调试方法

#### 后台运行游戏
```bash
# 启动游戏并输出日志到logs文件夹
nohup python src/simulate_to_survive/main.py > logs/game.log 2>&1 &

# 查看日志
cat logs/game.log

# 停止游戏进程
kill <进程ID>
```

#### 日志管理
```bash
# 查看所有日志文件
python clean_logs.py list

# 清理所有日志文件
python clean_logs.py clean

# 保留最新的2个日志文件
python clean_logs.py clean --keep 2
```

#### 系统测试
```bash
# 运行系统测试
python simple_test.py

# 运行音频调试
python debug_audio.py
```

### 常见问题解决

#### macOS SDL线程问题
在macOS上，SDL事件处理必须在主线程中进行。如果遇到线程相关错误，避免在子线程中调用pygame事件处理。

#### 音频文件路径问题
音频管理器会自动从以下路径加载音频文件：
- `assets/audio/sfx/environment/` - 环境音效
- `assets/audio/sfx/ui/` - UI音效
- `assets/audio/music/background/` - 背景音乐
- `assets/audio/music/ambient/` - 环境音乐

#### 场景加载问题
确保场景ID在SceneManager中已注册，默认场景包括：
- `main_menu` - 主菜单
- `CH0_PHASE_01` - 序章第一段
- `CH1_PHASE_01` - 第一章第一段

### 开发工作流程

1. **功能开发** → 编写代码
2. **快速测试** → 后台运行游戏
3. **查看日志** → 检查logs文件夹
4. **问题修复** → 根据日志信息调试
5. **清理日志** → 使用clean_logs.py清理

## 下一步行动
1. **基于游戏设定文档添加真实剧情内容**
2. **完善UI界面和用户体验**
3. **添加更多游戏机制和交互**

游戏设计请看 "游戏设定.md"
---
*最后更新: 2024年*
