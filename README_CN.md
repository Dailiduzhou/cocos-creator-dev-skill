# Cocos Creator 3.x 开发技能 (Skill)

一个为 [Claude](https://claude.ai) 提供的综合技能，专注于使用 TypeScript 进行 Cocos Creator 3.x 游戏开发的专家指导。

## 概述

本技能涵盖了 Cocos Creator 3.x 开发的完整内容，包括：
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

## 兼容性

- ✅ Cocos Creator 3.0 及以上版本
- ✅ 仅支持 TypeScript（3.x 中不支持 JavaScript）
- ✅ Cocos Creator 3.x 支持的所有平台

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