# Scene management (Creator 3.8 baseline)

## Scene loading choices

Creator runs one active scene. Switching destroys the previous scene's ordinary nodes; persistent roots are the exception.

- `director.loadScene('GamePlay', callback)` loads and launches a scene available through the build's scene configuration. Check **Included Scenes** and **Start Scene** in the Build panel; do not invent runtime editor-builder APIs.
- `director.preloadScene(...)` prepares a scene without launching it. Later call `director.loadScene(...)`. Deserialization/activation still costs time; preload does not mean instant transition.
- `bundle.loadScene(name, callback)` loads a scene from that Bundle without launching it. Pass the returned scene asset to `director.runScene(sceneAsset)`.
- Use `director.getScene()` for the current scene and guard null. Do not use a supposed `director.getSceneByName` or `bundle.getScene` to retrieve the loaded result.

## Persistent root manager

Attach this component to a **direct child of the scene root**, not a nested Canvas child. It owns navigation and remains valid across scene changes. Ensure repeated loading of a bootstrap scene cannot create duplicate managers.

Do not hard-fail when the current scene is not the production bootstrap scene: opening a Bundle scene directly in the editor is a normal debugging path. Gate registration on "no live instance yet" and log a warning instead of disabling the component.

```typescript
import { _decorator, assetManager, Component, director, isValid } from 'cc';
const { ccclass } = _decorator;

@ccclass('SceneNavigator')
export class SceneNavigator extends Component {
    static instance: SceneNavigator | null = null;
    private busy = false;
    private requestId = 0;

    onLoad(): void {
        const existing = SceneNavigator.instance;
        if (existing && isValid(existing, true) && existing !== this) {
            this.node.destroy();
            return;
        }
        if (this.node.parent !== director.getScene()) {
            console.error('SceneNavigator must be a direct child of the scene');
            this.enabled = false;
            return;
        }
        SceneNavigator.instance = this;
        director.addPersistRootNode(this.node);
    }

    openBundleScene(bundleName: string, sceneName: string): void {
        if (SceneNavigator.instance !== this || this.busy) return;
        this.busy = true; // Prevent double-click transitions.
        const requestId = ++this.requestId;
        assetManager.loadBundle(bundleName, (bundleError, bundle) => {
            if (!isValid(this, true) || requestId !== this.requestId) return;
            if (bundleError) {
                this.busy = false;
                console.error(`Bundle ${bundleName} failed`, bundleError);
                return;
            }
            bundle.loadScene(sceneName, (sceneError, sceneAsset) => {
                if (!isValid(this, true) || requestId !== this.requestId) return;
                if (sceneError) {
                    this.busy = false;
                    console.error(`Scene ${sceneName} failed`, sceneError);
                    return;
                }
                try {
                    director.runScene(sceneAsset, undefined, (launchError) => {
                        if (!isValid(this, true) || requestId !== this.requestId) return;
                        if (launchError) {
                            // Old scene may already be gone: keep navigation locked
                            // until an application-level recovery flow takes over.
                            console.error('Scene launch failed; recovery required', launchError);
                            return;
                        }
                        this.busy = false;
                    });
                } catch (launchError) {
                    console.error('Scene launch threw; recovery required', launchError);
                    // Retain the lock: do not assume a failed launch rolled back.
                }
            });
        });
    }

    onDestroy(): void {
        ++this.requestId;
        if (SceneNavigator.instance === this) {
            SceneNavigator.instance = null;
            director.removePersistRootNode(this.node);
        }
    }
}
```

Keep the transition lock through the launch callback: `runScene` schedules the transition, so unlocking immediately after calling it permits another request before launch. The example keeps the lock on launch failure because the old scene may already be destroyed; add an application-level recovery/restart UI rather than claiming automatic rollback.

This manager does not claim ownership of all Bundle assets and deliberately does not call `releaseAll`. In a production navigation service, centralize request serialization, loading-screen state, cancellation, and disposal policies. If the service can be destroyed during loading, decide who owns/releases successful late-loaded scenes without force-releasing assets shared with another transition.

Removing persistent status with `director.removePersistRootNode(node)` does not immediately destroy the node. Call `destroy()` separately if that is intended. Use the `director` methods, not the nonexistent `game.addPersistRoot`/`game.removePersistRoot`. The differently named `game.addPersistRootNode`/`game.removePersistRootNode` aliases still appear in the 3.8 API, but are deprecated since 3.6; do not confuse a deprecated alias with a nonexistent method.

## Passing state

- Use a small module-level store for plain session data that does not need component behavior.
- Use a persistent root for ongoing audio/network/component behavior; release stale scene references when changing scenes.
- Let the destination scene read state during initialization. A one-shot event emitted before its listeners exist is not durable state transfer.
- Persistence across scenes is not disk persistence. Save data through an appropriate storage mechanism if it must survive process termination.

## Progress and callback lifetime

`director.preloadScene(name, onProgress, onComplete)` can drive a loading UI; guard `total > 0` before division. Progress is resource-work progress, not a guarantee of linear wall-clock progress.

A callback held by the director or loader can outlive the component that initiated it. Do not update the old scene's progress UI after switching; check validity/request identity or host the navigation flow in a persistent service. `EVENT_AFTER_SCENE_LAUNCH` does not mean every component's `start` or asynchronous initialization has finished.

## Scene resource release

The scene asset's **Auto Release Assets** setting is configured in the editor's Inspector. It governs scene-dependent assets, not all dynamic ownership in arbitrary code. Do not call internal `assetManager.dependUtil.init/destroy` methods to implement scene cleanup.

Persistent components retaining dynamically loaded assets need their own balanced references. Bundle removal and asset release are separate operations; see [resource-management.md](resource-management.md).

## Verification

Test from a built project, not only preview: missing scene/Bundle, failed download, repeated clicks, re-entering the bootstrap scene, nested-manager misconfiguration, and several back-and-forth transitions. Check duplicate managers and listener/resource growth.

## Sources

- [Loading and switching scenes](https://docs.cocos.com/creator/3.8/manual/en/scripting/scene-managing.html)
- [Game API compatibility aliases](https://docs.cocos.com/creator/3.8/api/en/class/Game?id=addPersistRootNode)
- [Bundle scenes and removal](https://docs.cocos.com/creator/3.8/manual/en/asset/bundle.html)
- [Scene auto-release](https://docs.cocos.com/creator/3.8/manual/en/asset/release-manager.html)
