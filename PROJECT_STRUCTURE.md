# Project Structure

This document describes the organization of the Cocos Creator 3.x Development Skill repository.

## Directory Layout

```
cocos-creator-dev-github/
├── README.md                      # Main project documentation
├── INSTALL.md                     # Installation guide
├── LICENSE                        # MIT License
├── PROJECT_STRUCTURE.md           # This file
├── .gitignore                     # Git ignore rules
├── package_skill.py               # Script to package the skill
├── cocos-creator-dev.skill        # Pre-packaged skill file (ready to use)
└── cocos-creator-dev/             # Skill source files
    ├── SKILL.md                   # Main skill configuration and overview
    └── references/                # Detailed reference documentation
        ├── script-basics.md       # TypeScript scripting fundamentals
        ├── component-system.md    # Component lifecycle and management
        ├── node-hierarchy.md      # Node operations and transformations
        ├── scene-management.md    # Scene loading and data persistence
        ├── resource-management.md # Asset loading and memory management
        └── event-system.md        # Input handling and custom events
```

## File Descriptions

### Root Files

- **README.md**: Main project documentation with overview, features, and usage examples
- **INSTALL.md**: Detailed installation instructions and troubleshooting
- **LICENSE**: MIT License text
- **.gitignore**: Files and directories to ignore in version control
- **package_skill.py**: Python script to package the skill into a `.skill` file
- **cocos-creator-dev.skill**: Pre-packaged skill file ready for import into Claude

### Skill Directory (`cocos-creator-dev/`)

- **SKILL.md**: Core skill configuration file containing:
  - Skill name and description
  - Quick start templates
  - Common operations
  - API references
  - Development guidelines
  - Troubleshooting tips

### Reference Documentation (`cocos-creator-dev/references/`)

These files provide in-depth documentation on specific topics:

1. **script-basics.md**: TypeScript setup, decorators, component templates
2. **component-system.md**: Lifecycle methods, component communication patterns
3. **node-hierarchy.md**: Node creation, transformations, coordinate systems
4. **scene-management.md**: Scene loading, preloading, persist nodes
5. **resource-management.md**: Asset loading, memory management, Asset Bundles
6. **event-system.md**: Input handling, custom events, node communication

## Usage Flow

1. **End Users**: Download `cocos-creator-dev.skill` and import directly
2. **Developers**: Clone repository, modify source files, run `python package_skill.py`
3. **Contributors**: Edit reference documentation, test changes, submit pull request

## Skill File Format

The `.skill` file is a ZIP archive containing:
- `SKILL.md` (required): Main skill configuration
- `references/` (optional): Supporting documentation
- Other markdown files as needed

## Best Practices

- Keep `SKILL.md` concise and focused on quick reference
- Use `references/` for detailed explanations
- Maintain consistent formatting across all markdown files
- Update `README.md` when adding new features
- Test packaged skill before releasing

## Development Workflow

```bash
# 1. Make changes to source files
nano cocos-creator-dev/SKILL.md

# 2. Package the skill
python package_skill.py

# 3. Test the packaged skill
# Import cocos-creator-dev.skill into Claude and verify functionality

# 4. Commit and push
git add .
git commit -m "Update skill documentation"
git push
```

## Documentation Standards

- Use clear, descriptive headings
- Include code examples with syntax highlighting
- Add troubleshooting sections for complex topics
- Link related documentation
- Keep examples up-to-date with latest Cocos Creator 3.x API