# Cocos Creator 3.x Development Skill

A comprehensive skill for [Claude](https://claude.ai) that provides expert guidance for Cocos Creator 3.x game development using TypeScript.

## Overview

This skill offers complete coverage of Cocos Creator 3.x development including:
- TypeScript scripting with proper decorators
- Component system and lifecycle management
- Node hierarchy and scene organization
- Resource loading and memory management
- Event systems and input handling
- Performance optimization techniques
- Migration from 2.x to 3.x

## Installation

### Using the Skill File (Recommended)

1. Download the latest `cocos-creator-dev.skill` file from the [Releases](releases) page
2. Import the skill into Claude's skill system
3. Start using the skill immediately

### Manual Installation

1. Clone this repository
2. Use the packaging script:
   ```bash
   python package_skill.py
   ```
3. Import the generated `.skill` file

## Usage

Once installed, this skill automatically activates when you need help with Cocos Creator 3.x development. Use phrases like:

- "Help me create a component that..."
- "How do I load resources in Cocos Creator?"
- "Debug this TypeScript script..."
- "Explain the component lifecycle..."
- "How to optimize performance for..."

## Features

### 📝 Script Development
- TypeScript component templates
- Proper decorator usage (`@ccclass`, `@property`)
- Code style guidelines and best practices

### 🎮 Component System
- Lifecycle methods (`onLoad`, `start`, `update`)
- Component creation and management
- Component communication patterns

### 🌳 Scene & Node Management
- Node hierarchy operations
- Scene loading and transitions
- Persist nodes for data preservation

### 📦 Resource Management
- Asset loading strategies
- Memory optimization
- Asset Bundle usage

### 🎯 Event System
- Input handling (touch, mouse, keyboard)
- Custom event creation
- Node-to-node communication

### ⚡ Performance Optimization
- Memory leak prevention
- Object pooling techniques
- Profiling and debugging

## Example

When you ask for help with a component, you'll get detailed guidance:

```typescript
import { _decorator, Component, Node } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('PlayerController')
export class PlayerController extends Component {
    @property
    moveSpeed: number = 5;

    start() {
        // Initialization code
    }

    update(deltaTime: number) {
        // Update logic
    }
}
```

## Documentation Structure

The skill includes detailed reference documentation:

- **[Script Basics](cocos-creator-dev/references/script-basics.md)** - TypeScript setup and component creation
- **[Component System](cocos-creator-dev/references/component-system.md)** - Lifecycle and component management
- **[Node & Hierarchy](cocos-creator-dev/references/node-hierarchy.md)** - Node operations and transformations
- **[Scene Management](cocos-creator-dev/references/scene-management.md)** - Scene loading and data persistence
- **[Resource Management](cocos-creator-dev/references/resource-management.md)** - Asset loading and memory management
- **[Event System](cocos-creator-dev/references/event-system.md)** - Input handling and custom events

## Compatibility

- ✅ Cocos Creator 3.0 and above
- ✅ TypeScript exclusively (JavaScript not supported in 3.x)
- ✅ All platforms supported by Cocos Creator 3.x

## Contributing

Contributions are welcome! Please:

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## External Resources

- [Cocos Creator 3.x Official Manual](https://docs.cocos.com/creator/3.8/manual/zh/)
- [Cocos Creator 3.x API Reference](https://docs.cocos.com/creator/3.8/api/zh/)
- [Example Projects](https://github.com/cocos/cocos-example-projects)

## Support

For issues or questions:
- Check the [Troubleshooting](cocos-creator-dev/SKILL.md#troubleshooting) section in the skill documentation
- Review the reference files for specific topics
- Open an issue in this repository

---

*This skill was created using the [skill-creator](https://github.com/anthropics/skill-creator) framework.*