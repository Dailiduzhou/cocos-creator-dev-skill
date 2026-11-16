# Cocos Creator 3.x 开发技能 (Skill)

一个为 [Claude](https://claude.ai) 提供的综合技能，专注于使用 TypeScript 进行 Cocos Creator 3.x 游戏开发的专家指导。

## 概述

本技能覆盖 Cocos Creator 常见运行时开发流程，以 **3.8 官方文档为参考基线**，选择 API 前先核对实际项目版本：
- 使用装饰器的 TypeScript 脚本编写
- 组件系统和生命周期管理
- 节点层级和场景组织
- 资源加载和内存管理
- 事件系统和输入处理
- 性能优化技术
- 从 2.x 迁移到 3.x

## 安装

### 使用技能文件（推荐）

1. 从 [Releases](releases) 页面下载最新的 `cocos-creator-dev.skill` 文件
2. 将技能导入 Claude 的技能系统
3. 立即开始使用

### 手动安装

1. 克隆此仓库
2. 使用打包脚本：
   ```bash
   python package_skill.py
   ```
3. 导入生成的 `.skill` 文件

## 使用方法

安装后，当您需要 Cocos Creator 3.x 开发帮助时，此技能会自动激活。使用以下短语：

- "帮我创建一个组件..."
- "如何在 Cocos Creator 中加载资源？"
- "调试这个 TypeScript 脚本..."
- "解释组件生命周期..."
- "如何优化性能..."

## 功能特性

### 📝 脚本开发
- TypeScript 组件模板
- 正确的装饰器使用（`@ccclass`、`@property`）
- 代码风格指南和最佳实践

### 🎮 组件系统
- 生命周期方法（`onLoad`、`start`、`update`）
- 组件创建和管理
- 组件通信模式

### 🌳 场景和节点管理
- 节点层级操作
- 场景加载和转换
- 持久节点用于数据保存

### 📦 资源管理
- 资源加载策略
- 内存优化
- Asset Bundle 使用

### 🎯 事件系统
- 输入处理（触摸、鼠标、键盘）
- 自定义事件创建
- 节点间通信

### ⚡ 性能优化
- 内存泄漏预防
- 对象池技术
- 性能分析和调试

## 示例

当您请求组件帮助时，您将获得详细指导：

```typescript
import { _decorator, Component, Node } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('PlayerController')
export class PlayerController extends Component {
    @property
    moveSpeed: number = 5;

    start() {
        // 初始化代码
    }

    update(deltaTime: number) {
        // 更新逻辑
    }
}
```

## 文档结构

该技能包含详细的参考文档：

- **[脚本基础](cocos-creator-dev/references/script-basics.md)** - TypeScript 设置和组件创建
- **[组件系统](cocos-creator-dev/references/component-system.md)** - 生命周期和组件管理
- **[节点与层级](cocos-creator-dev/references/node-hierarchy.md)** - 节点操作和变换
- **[场景管理](cocos-creator-dev/references/scene-management.md)** - 场景加载和数据持久化
- **[资源管理](cocos-creator-dev/references/resource-management.md)** - 资源加载和内存管理
- **[事件系统](cocos-creator-dev/references/event-system.md)** - 输入处理和自定义事件
- **[版本迁移](cocos-creator-dev/references/migration.md)** - 2.x 迁移与早期 3.x 的版本边界
- **[官方来源](cocos-creator-dev/references/official-sources.md)** - 版本化文档与核验策略

## 兼容性

- 示例以 Creator **3.8 官方文档**为基线，需结合已安装的具体小版本核对。
- 新组件使用 TypeScript；Creator 也支持 JavaScript 模块和插件脚本。
- Web、原生和小游戏需要在目标平台验证，编辑器预览不能替代实机测试。
- 高级渲染、物理、编辑器扩展和平台集成需额外查阅对应版本的官方章节。

## 评估与验证

[`cocos-creator-dev/evals/evals.json`](cocos-creator-dev/evals/evals.json) 包含三个回归案例及评分条件：共享动态资源、Bundle 场景导航、UI 事件与生命周期。更新前版本应先快照保存，避免基线测试误读新版参考资料。

本地对比结果和 skill-creator HTML 评审页面保存在 `cocos-creator-dev-workspace/`（不提交 Git）。这些是代码生成与静态审查测试，不代表 Creator 运行验证。未发布更新以源码目录为准，预打包的 `.skill` 文件在发布时另行更新。

## 贡献

欢迎贡献！请：

1. Fork 此仓库
2. 创建功能分支
3. 进行更改
4. 充分测试
5. 提交拉取请求

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 外部资源

- [Cocos Creator 3.x 官方手册](https://docs.cocos.com/creator/3.8/manual/zh/)
- [Cocos Creator 3.x API 参考](https://docs.cocos.com/creator/3.8/api/zh/)
- [示例项目](https://github.com/cocos/cocos-example-projects)

## 支持

如有问题或疑问：
- 查看技能文档中的[故障排除](cocos-creator-dev/SKILL.md#troubleshooting)部分
- 查阅参考文件了解特定主题
- 在此仓库中提交 issue

---

*此技能使用 [skill-creator](https://github.com/anthropics/skill-creator) 框架创建。*