---
name: cocos-creator-dev
description: "Develop, debug, and review Cocos Creator 3.x games using version-aware TypeScript, components, nodes, UI/input events, scenes, Asset Bundles, and resource ownership. Use this skill whenever a request involves Cocos Creator scripts, lifecycle bugs, SpriteFrame loading, scene transitions, memory leaks, or migrating Creator 2.x code to 3.x, even if the user only supplies code importing from 'cc' without naming the engine. Do not apply Creator APIs to Cocos2d-x/C++ or unrelated TypeScript projects."
---

# Cocos Creator Development

Deliver small, project-compatible changes with explicit editor setup and verification. Use the user's language. The bundled references are grounded in the **Creator 3.8** documentation, not a promise that every API works in every 3.x release.

## 1. Establish the project contract

Before choosing APIs, inspect the supplied code and available project files:

- Determine the exact Creator version from project metadata (for example `package.json`'s `creator.version`), existing configuration, or the user. Do not interpret the application's own `version` as the engine version.
- Identify 2D UI vs 3D, target platform (Web/native/mini game), and whether the task concerns runtime scripts or editor extensions.
- Read the existing component, its callers, and relevant asset/scene setup. Preserve naming, serialization, and project conventions.
- Preserve the project's generated TypeScript configuration chain and asset `.meta` files. Avoid rewriting serialized scenes, prefabs, UUIDs, or generated directories unless the task needs it and the format is understood.

Ask only for information that changes the solution. For a standalone example without a project, state a 3.8 assumption and proceed. For a 2.x project, clarify whether to fix 2.x or migrate; do not silently mix APIs.

## 2. Load only the relevant references

| Task | Read |
| --- | --- |
| Component authoring, decorators, TypeScript configuration | [script-basics.md](references/script-basics.md) |
| Initialization order, enable/disable, scheduling, dependencies | [component-system.md](references/component-system.md) |
| Node lifetime, transforms, UI coordinates, pooling | [node-hierarchy.md](references/node-hierarchy.md) |
| Scene loading, persistent managers, Bundle scenes | [scene-management.md](references/scene-management.md) |
| Dynamic assets, remote images, ref counts, Bundle unloading | [resource-management.md](references/resource-management.md) |
| UI input, global input, custom events, cleanup | [event-system.md](references/event-system.md) |
| Porting 2.x or evaluating an older 3.x API | [migration.md](references/migration.md) |
| API uncertainty or a topic beyond these references | [official-sources.md](references/official-sources.md) |

For version-sensitive or unfamiliar APIs, verify the matching official manual/API and, when necessary, the installed engine declarations or matching engine source tag. State uncertainty rather than inventing methods. A search snippet alone is not enough to validate a signature.

## 3. Implement with explicit lifetimes

- Use ESM imports from `cc` and TypeScript for new components. JavaScript modules/plugins also exist; do not claim that 3.x forbids all JavaScript.
- Use unique `@ccclass` names, explicit **cc** property types (`Node`, `Sprite`, `SpriteFrame`, `Prefab`), and nullable fields for unassigned Inspector references. Let `String`/`Number`/`Boolean` infer from the default value: the manual warns against `type: String` and friends. Explain which node receives the script and which properties must be wired.
- Distinguish **existence**, **validity**, and **activation**: `getComponent()` may return null; inactive nodes still have components; `activeInHierarchy` governs effective activity. For pending destruction, consider `isValid(object, true)`.
- Treat `onLoad` as own initialization, not proof that every other component has initialized. Use `@executionOrder(...)` or explicit initialization contracts when order matters.
- Pair subscriptions and schedules with the lifetime that owns them, usually `onEnable`/`onDisable`. Keep the same callback and target when unregistering.
- Treat every asynchronous result as potentially late: handle errors, destroyed owners, disabled views where relevant, and superseded requests. Decide resource ownership before adding cleanup.
- Prefer paired `addRef()`/`decRef()` for owned dynamic assets. Assignment to a component is not an automatic ownership increment. Force-release APIs can invalidate other consumers.
- Keep coordinate spaces explicit. Euler angles use `setRotationFromEuler`; quaternion rotation uses `Quat`. UI hit testing and UI coordinates are not 3D picking.
- Optimize from measurements: reproduce on the target platform, identify CPU/GPU/loading/memory cost, then test one change. Do not prescribe invented batching APIs or universal pooling.

## 4. Validate the change

1. Check imports, nullability, decorators, API signatures, resource paths, and Inspector wiring.
2. Run existing project checks when available. Use its local TypeScript checker and generated engine declarations; do not install an arbitrary compiler or replace the project's config just to silence errors.
3. In Creator, check script import/compilation, preview, and the affected scene. Repeat enable/disable, fast navigation, and resource-load races when relevant.
4. Test the build on its actual platform for platform-dependent behavior. Editor preview alone does not establish native/mini-game compatibility.
5. If Creator or a runnable project is unavailable, report **static review only** and give exact manual checks. Never claim a compiled or runtime-tested result from documentation review.

## 5. Deliver a usable result

For implementation/debugging requests, include:

- **Version and diagnosis**: assumptions, root cause, and relevant official source links for non-obvious behavior.
- **Changes**: actual file paths and concise rationale; complete imports for standalone code.
- **Editor setup**: node/component placement, serialized property wiring, resource/Bundle/Build panel configuration.
- **Validation**: what ran, what passed, and what still needs Creator or device testing.

For a simple conceptual question, answer directly rather than forcing this full template.

## Troubleshooting checkpoints

| Symptom | Check first |
| --- | --- |
| Missing component | Attachment, script import errors, class identity, null lookup; not merely `node.active` |
| Callback runs twice or after closing UI | Matching subscription lifetime, stable callback identity, async request invalidation |
| SpriteFrame fails to load | Correct resources/Bundle root, no extension, image `/spriteFrame` sub-asset path |
| Shared UI turns blank after closing one view | Forced release of shared assets or unbalanced ownership |
| Scene fails in build only | Included Scenes/Bundle configuration, scene name, platform packaging |
| Touch position is wrong | UI vs screen vs world coordinates; transform into the intended parent space |
| Memory grows | Repeated scene-cycle measurements, listeners, pools, retained assets, Bundle ownership; not just cache count |
