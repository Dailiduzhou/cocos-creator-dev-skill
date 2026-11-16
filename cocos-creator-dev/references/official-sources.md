# Official sources and verification policy

Documentation baseline: **Cocos Creator 3.8**. Sources below were consulted for this revision on **2026-11-15**. This is a documentation audit date, not a claim that 3.8 is the latest release or that examples have run in every 3.8 patch.

## Evidence order

1. Establish the actual editor/engine version and platform from the project.
2. Read the matching official manual for concepts and setup.
3. Check the matching API reference and installed generated declarations for exact signatures.
4. If documentation disagrees or omits behavior, inspect the matching engine tag/source rather than `develop` or an unrelated version.
5. Reproduce in Creator and on the target platform before claiming runtime validation.

Use English or Chinese official documentation as appropriate. Do not silently convert a remembered URL into a citation: search if it fails and verify the replacement. Documentation examples can omit error/lifetime handling and are not production-ready ownership policies.

## Topic index

| Official source | What it establishes |
| --- | --- |
| [Decorators](https://docs.cocos.com/creator/3.8/manual/en/scripting/decorator.html) | Class/property registration, enum types, `@executionOrder`, edit-mode behavior |
| [tsconfig.json](https://docs.cocos.com/creator/3.8/manual/en/scripting/tsconfig.html) | Preserve generated config inheritance; do not override target/module to control Creator compilation |
| [Modules](https://docs.cocos.com/creator/3.8/manual/en/scripting/modules/index.html) | TypeScript/JavaScript modules, ESM and external module boundaries |
| [Lifecycle callbacks](https://docs.cocos.com/creator/3.8/manual/en/scripting/life-cycle-callbacks.html) | Activation and callback ordering |
| [Scene management](https://docs.cocos.com/creator/3.8/manual/en/scripting/scene-managing.html) | `director` persistent roots, root-node constraint, preload vs launch |
| [Asset loading](https://docs.cocos.com/creator/3.8/manual/en/asset/dynamic-load-resources.html) | Sub-asset paths, preload, remote ImageAsset conversion |
| [Asset release](https://docs.cocos.com/creator/3.8/manual/en/asset/release-manager.html) | Static/dynamic references, ref counts, forced-release caveats |
| [Asset Bundles](https://docs.cocos.com/creator/3.8/manual/en/asset/bundle.html) | Load scene callbacks, dependency priorities, remove vs release |
| [Node events](https://docs.cocos.com/creator/3.8/manual/en/engine/event/event-node.html) | UITransform hit testing, dispatch/bubbling, Event subclassing |
| [Input events](https://docs.cocos.com/creator/3.8/manual/en/engine/event/event-input.html) | Global input, 3.4 version boundary, 3D picking |
| [3.0 upgrade guide](https://docs.cocos.com/creator/3.8/manual/en/release-notes/upgrade-guide-v3.0.html) | Historical 2.x import and migration concerns |

## API and engine entry points

- [3.8 API](https://docs.cocos.com/creator/3.8/api/en/) / [Chinese manual](https://docs.cocos.com/creator/3.8/manual/zh/)
- [Node](https://docs.cocos.com/creator/3.8/api/en/class/Node)
- [Component](https://docs.cocos.com/creator/3.8/api/en/class/Component)
- [Game compatibility aliases](https://docs.cocos.com/creator/3.8/api/en/class/Game?id=addPersistRootNode) — persistent-root helpers deprecated since 3.6, not removed in this reference.
- [Director source at v3.8.7](https://github.com/cocos/cocos-engine/blob/v3.8.7/cocos/game/director.ts) — `runScene` defers launch to frame end; verify the matching tag for other patches.
- [UITransform](https://docs.cocos.com/creator/3.8/api/en/class/UITransform)
- [EventTouch](https://docs.cocos.com/creator/3.8/api/en/class/EventTouch)
- [KeyCode](https://docs.cocos.com/creator/3.8/api/en/enumeration/KeyCode)
- [Official engine repository](https://github.com/cocos/cocos-engine) — select the project-compatible tag.

## Beyond the bundled scope

For shaders/render pipelines, advanced physics, animation graphs, native integrations, editor extensions, platform publishing, or detailed batching advice, locate the relevant chapter from the versioned manual rather than extrapolating these runtime-script examples. Distinguish editor-only APIs from APIs that can be shipped in the game.

When no editor is available, report which documents/signatures were checked and what remains to test. Do not present text review or a mock compiler stub as an engine compile/runtime test.
