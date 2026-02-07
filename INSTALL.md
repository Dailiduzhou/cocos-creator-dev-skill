# Installation Guide

This guide explains how to install and use the Cocos Creator 3.x Development Skill.

## Prerequisites

- Claude AI access with skill support
- Python 3.6+ (for manual packaging only)

## Installation Methods

### Method 1: Using Pre-packaged Skill File (Recommended)

1. Download the latest `cocos-creator-dev.skill` file from the [Releases](releases) page
2. Open Claude's skill management interface
3. Import the `.skill` file
4. The skill will be automatically activated

### Method 2: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/cocos-creator-dev.git
   cd cocos-creator-dev
   ```

2. Package the skill:
   ```bash
   python package_skill.py
   ```

3. Import the generated `cocos-creator-dev.skill` file into Claude

## Verification

After installation, test the skill by asking:

```
Help me create a basic Cocos Creator component with a property
```

The skill should respond with a proper TypeScript component template.

## Troubleshooting

### Skill not loading
- Ensure you have the latest version of Claude with skill support
- Check that the `.skill` file is not corrupted

### Python packaging fails
- Verify Python 3.6+ is installed: `python --version`
- Ensure all required files are present in the `cocos-creator-dev` directory

### Skill not responding correctly
- Verify you're asking about Cocos Creator 3.x, not 2.x
- Include "Cocos Creator 3.x" in your query for best results

## Next Steps

- Read the [README.md](README.md) for usage examples
- Explore the [reference documentation](cocos-creator-dev/references/) for detailed guides
- Check the [Troubleshooting section](README.md#troubleshooting) in README for common issues

## Support

If you encounter any issues not covered here:
1. Check existing [GitHub Issues](../../issues)
2. Create a new issue with:
   - Your operating system
   - Claude version
   - Steps to reproduce the issue
   - Expected vs actual behavior