# Nodes, transforms, and lifetime (Creator 3.8 baseline)

## Hierarchy and validity

- Use `new Node(name)` for an empty node, `instantiate(prefab)` for a configured hierarchy, and `addChild`/`setParent` to attach it.
- Guard `parent`, `getChildByName`, `getChildByPath`, and component lookups; they may be absent.
- `find(path, root?)` searches a hierarchy path; it is not an unrestricted recursive name search.
- `removeFromParent()` detaches; it does not destroy. `destroy()` and `destroyAllChildren()` schedule destruction, not immediate deallocation.
- `node.active` is local intent; `node.activeInHierarchy` includes ancestor activity. Setting a parent's `active` does not rewrite each child's local flag.
- Inactive is not invalid. Check `isValid(node, true)` for a destroyed or pending-destruction reference rather than using activity as a proxy.

## Transform signatures

The following fragments assume a valid `node: Node` and imports from `cc`:

```typescript
node.setPosition(10, 20, 0);          // Parent-local coordinates
node.setWorldPosition(10, 20, 0);     // World coordinates
node.setRotationFromEuler(0, 0, 90);  // Degrees
node.setScale(2, 2, 2);               // Explicit uniform scale

const rotation = new Quat();
Quat.fromEuler(rotation, 0, 90, 0);
node.setRotation(rotation);          // Quaternion, not three Euler angles
node.rotate(rotation);              // Relative quaternion rotation
```

Do not pass a `Vec3` to `rotate()` or assume `setScale(2)` means uniform scale. Use setters rather than mutating individual members of a returned transform vector, so the engine's transform updates are notified.

For reparenting while preserving world transforms, check the installed version's `setParent(parent, keepWorldTransform)` signature and use the second argument deliberately.

## Coordinate conversion

For a point in local space, transform it with the node's world matrix; `getWorldPosition(out)` returns only the node origin, not an arbitrary transformed point.

```typescript
import { Node, Vec3 } from 'cc';

export function pointInOtherSpace(
    source: Node, destination: Node, point: Vec3, out: Vec3,
): Vec3 {
    Vec3.transformMat4(out, point, source.worldMatrix);
    destination.inverseTransformPoint(out, out);
    return out;
}
```

For UI dragging under a standard Canvas UI camera, obtain `event.getUILocation()`, turn it into `Vec3(x, y, 0)`, then call the **parent's** `UITransform.convertToNodeSpaceAR(...)` before assigning the child's local position. A custom camera, render texture, or world-space UI needs camera-aware screen/world conversion instead. See [event-system.md](event-system.md).

Use `UITransform` for UI content size/anchor, `UIOpacity` for UI opacity, and `Layers.Enum`/`Layers.BitMask` for engine layers. A camera's visibility mask must include the node's layer. Do not invent a `LayerManager.Mask.UI` constant.

## Safe prefab creation

```typescript
import { _decorator, Component, instantiate, Prefab } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('Spawner')
export class Spawner extends Component {
    @property(Prefab)
    prefab: Prefab | null = null;

    spawn(): void {
        if (!this.prefab) {
            console.warn('Assign Spawner.prefab in the Inspector');
            return;
        }
        const child = instantiate(this.prefab);
        child.setPosition(0, 0, 0);
        this.node.addChild(child);
    }
}
```

Wire the Prefab in the Inspector. Instantiating a dynamically loaded prefab does not remove the need to define ownership of its source/dependencies; keep the asset ownership valid for its live instances.

## Pooling and performance

Pool only when profiling shows frequent creation/destruction matters. Define the whole pool lifecycle:

1. Acquire: create or retrieve, configure/reset state, parent it, then activate.
2. Return: invalidate async work, stop owned tweens/schedules/listeners, deactivate, detach, and prevent duplicate returns.
3. Dispose: destroy retained nodes and release assets owned by the pool after consumers are gone.

Pooling without resetting component state can turn a performance optimization into a correctness bug. Removing all children is not pool disposal. Likewise, grouping nodes under a parent does not guarantee batching; measure material/texture compatibility, masks, render ordering, and target-platform draw calls. Do not use nonexistent helpers such as `addComponentStatic`.

## Sources

- [Node API](https://docs.cocos.com/creator/3.8/api/en/class/Node)
- [UITransform API](https://docs.cocos.com/creator/3.8/api/en/class/UITransform)
- [Node input requirements](https://docs.cocos.com/creator/3.8/manual/en/engine/event/event-node.html)
