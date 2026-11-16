# Migration and version boundaries

Use this reference for porting Creator 2.x code to a chosen 3.x version, not as permission to upgrade an existing project automatically.

## Migration workflow

1. Confirm source and target versions, platform, and whether the task is migration or maintenance.
2. Back up or branch the project before editor conversion. Preserve assets and metadata; use the version's supported import workflow instead of regex-rewriting scene JSON.
3. Inventory scripts, plugins, physics, materials/effects, UI components, build extensions, and platform SDKs. Script compilation alone does not establish migration success.
4. Port a small representative scene first. Validate serialization, visual output, interaction, and a real platform build before scaling up.
5. Check the target version's manual/API and engine declarations for each changed subsystem.

## Common porting decisions

| Older pattern | 3.8-oriented direction |
| --- | --- |
| Global `cc` namespace, `cc.Class` components | ESM imports from `cc`, TypeScript classes with `_decorator` |
| `cc.loader` / `loadRes` | `resources` or `assetManager`/Bundle loading, with correct sub-asset paths |
| `node.width`, `height`, anchor-related UI state | `UITransform` |
| `node.opacity` for UI | `UIOpacity` |
| Global `systemEvent` | `input` for 3.4+, with its event callback signature |
| `cc.Event.EventCustom` | An `Event` subclass and `dispatchEvent` when propagation is needed |
| Old persistent-root helpers | Verify target API; 3.8 uses `director.addPersistRootNode` |
| Broad release calls after every scene | Static vs dynamic ownership and balanced asset references |

These are review prompts, not a complete automated conversion table. In particular, render pipelines, effects, physics, native bindings, and editor extensions need their own target-version documentation.

## Earlier 3.x projects

Do not equate “3.x” with “3.8”: `input` was introduced in 3.4, input priority changed in 3.4.1, and newer APIs can differ by minor/patch release. Preserve working older APIs when fixing an older project unless the user requests a migration.

Use the installed editor's generated configuration rather than overwriting it with a copied `tsconfig`. JavaScript modules and plugins are distinct from authoring new decorated TypeScript components; do not describe all JavaScript as unsupported.

## Source

- [Official 3.0 upgrade guide](https://docs.cocos.com/creator/3.8/manual/en/release-notes/upgrade-guide-v3.0.html) — historical migration guidance, not a current release recommendation.
- [Input version changes](https://docs.cocos.com/creator/3.8/manual/en/engine/event/event-input.html)
- [Official source index](official-sources.md)
