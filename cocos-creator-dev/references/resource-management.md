# Resource management (Creator 3.8 baseline)

## Choose the loading boundary

| Need | Mechanism |
| --- | --- |
| Known asset configured in the editor | Serialized `@property` reference |
| Runtime path under `assets/resources/` | `resources.load(path, Type, callback)` |
| Feature/level package | `assetManager.loadBundle`, then `bundle.load` |
| Remote native image/audio/text | `assetManager.loadRemote` |
| Advance download without usable instances yet | `preload`/`preloadDir`, followed by `load` |

Do not put everything under `resources`: its contents and dependencies are included in builds, reducing automatic pruning. Dynamic assets can also live in custom Bundles.

Use paths relative to the resources/Bundle root without file extensions. For `assets/resources/textures/avatar.png`, the imported image's SpriteFrame is `textures/avatar/spriteFrame`; its Texture2D is `textures/avatar/texture`. Specifying the type alone does not replace the sub-asset path. An imported SpriteAtlas is loaded as an atlas, then accessed with `getSpriteFrame(name)`.

Preloading downloads required files but does not complete asset deserialization/initialization. It can reduce later latency, not promise instant loading.

## Ownership before release

The engine tracks serialized/static dependencies. It does **not** automatically count arbitrary JavaScript references or an assignment such as `sprite.spriteFrame = frame`.

- Call `addRef()` when a dynamic owner retains an asset, and pair it with exactly one `decRef()` when that owner stops using it.
- Clear the consuming component's reference before dropping the owner's last reference. Do not decrement an asset just because you can access it: track which references your code acquired.
- A newly loaded top-level asset is not guaranteed to have count 1. Cached assets and dependencies may already have references.
- `assetManager.releaseAsset`, `bundle.release`, and `releaseAll` force-release their target assets; they are not safe substitutes for balanced ownership even when another consumer called `addRef()`.
- Let the engine handle dependency release checks. Do not traverse dependencies and forcibly release them, or clear the asset cache as a memory-management strategy.
- Destroying a node does not automatically balance your manual dynamic asset references. Conversely, do not force-release editor-assigned shared assets in every `onDestroy`.

## Race-safe dynamic SpriteFrame component

This example owns the target Sprite's dynamic frame while enabled. Attach it to a UI node with `Sprite`; set `framePath` to an existing SpriteFrame sub-asset path. The target Sprite should not be independently updated by another component.

```typescript
import {
    _decorator, Component, isValid, resources, Sprite, SpriteFrame,
} from 'cc';
const { ccclass, property, requireComponent } = _decorator;

@ccclass('OwnedSpriteFrame')
@requireComponent(Sprite)
export class OwnedSpriteFrame extends Component {
    @property
    framePath = 'textures/avatar/spriteFrame';

    private requestId = 0;
    private owned: SpriteFrame | null = null;

    onEnable(): void {
        this.show(this.framePath);
    }

    show(path: string): void {
        const requestId = ++this.requestId;
        if (!this.enabledInHierarchy) return;

        resources.load(path, SpriteFrame, (err, frame) => {
            if (err) {
                console.error(`Failed to load ${path}`, err);
                return;
            }
            // Acquire a temporary reference even for a late result, so each
            // successful result has a balanced ownership path.
            frame.addRef();
            if (!isValid(this, true) || !this.enabledInHierarchy ||
                requestId !== this.requestId) {
                frame.decRef();
                return;
            }
            const sprite = this.getComponent(Sprite);
            if (!sprite || !isValid(sprite, true)) {
                frame.decRef();
                return;
            }
            const previous = this.owned;
            this.owned = frame;
            sprite.spriteFrame = frame;
            // Acquire before releasing: previous may be the same cached asset.
            previous?.decRef();
        });
    }

    onDisable(): void {
        this.clearOwned();
    }

    onDestroy(): void {
        this.clearOwned(); // Idempotent if onDisable already cleared it.
    }

    private clearOwned(): void {
        ++this.requestId;
        const previous = this.owned;
        this.owned = null;
        if (!previous) return;
        const sprite = this.getComponent(Sprite);
        if (sprite && isValid(sprite, true) && sprite.spriteFrame === previous) {
            sprite.spriteFrame = null;
        }
        previous.decRef();
    }
}
```

The request token rejects out-of-order results and results from a previous enable cycle; `isValid(this, true)` catches pending destruction. Neither check cancels the underlying download. All dynamic consumers sharing these assets must follow an ownership policy; this component cannot protect consumers elsewhere that never retained their assets.

For larger projects, centralize concurrent request/cache ownership in an asset service rather than copying ad-hoc force-release code into views.

## Remote image conversion

A remote image loads as `ImageAsset`, not `Texture2D` or `SpriteFrame`:

```typescript
import { assetManager, ImageAsset, SpriteFrame, Texture2D } from 'cc';

// Conversion fragment: the caller must provide owner-validity checks and cleanup.
assetManager.loadRemote<ImageAsset>(
    'https://example.com/avatar.png',
    (err, image) => {
        if (err) {
            console.error('Avatar download failed', err);
            return;
        }
        const texture = new Texture2D();
        texture.image = image;
        const frame = new SpriteFrame();
        frame.texture = texture;
        // Hand image/texture/frame to an explicit owner before assigning to UI.
    },
);
```

For URLs without an extension, pass `{ ext: '.png' }` when PNG is actually the response type. Check CORS for Web and download-domain/cache restrictions for mini games. Remote native-file loading is not a way to directly load serialized prefabs or atlases; use a built Asset Bundle for those.

The conversion fragment intentionally omits display/cleanup: retain the cached `ImageAsset` with balanced refs if needed, and track/destroy runtime-created `SpriteFrame`/`Texture2D` when no consumer uses them. Do not assume assigning runtime-created assets establishes serialized dependency ownership. A shared cache needs one consistent ownership policy, not independent forced destruction by each view.

## Asset Bundles

Configure a folder as **Is Bundle** in the Inspector. Load by configured name or a built Bundle URL; use the returned bundle's `load`/`loadScene`. `loadBundle` loads its manifest and scripts, not every contained asset. Higher-priority shared dependency Bundles may need loading first. Do not nest Bundles.

For scenes see [scene-management.md](scene-management.md). For unloading:

1. Stop new work and invalidate outstanding requests associated with the feature.
2. Destroy/detach its consumers and dispose of its pools; balance references owned by the feature.
3. If — and only if — the Bundle is confirmed exclusive (no cross-Bundle dependency, no pool or persistent consumer), release its assets first: `bundle.release(path, Type)` or `bundle.releaseAll()`.
4. Then `assetManager.removeBundle(bundle)` removes the Bundle registration/cache. Removing it alone leaves already loaded assets cached.
5. 3.8 has no `releaseUnusedAssets` sweep to fall back on, so state explicitly how an exclusive Bundle's assets are eventually released.

There is no `assetManager.releaseBundle(name)` shortcut. Do not call `releaseAll()` merely because one scene was closed; shared UI and persistent nodes may still consume its assets.

## Verification

Test load failures, immediate close, A-then-B loads completed in reverse order, two views sharing a frame, re-enable before the previous request completes, and repeated scene cycles. Measure memory after stabilization; asset-cache counts are not a direct GPU-memory metric.

## Sources

- [Asset loading and sub-assets](https://docs.cocos.com/creator/3.8/manual/en/asset/dynamic-load-resources.html)
- [Release checks and dynamic references](https://docs.cocos.com/creator/3.8/manual/en/asset/release-manager.html)
- [Asset Bundle overview](https://docs.cocos.com/creator/3.8/manual/en/asset/bundle.html)
