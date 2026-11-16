# Component system (Creator 3.8 baseline)

## Lifecycle is activation-dependent

Typical first activation:

```text
onLoad → onEnable → start → update → lateUpdate
```

`onDisable` and `onEnable` may repeat. `onLoad` and `start` do not repeat for each enable cycle. Destruction is deferred; `onDestroy` is cleanup, not an ordinary disable transition.

| Callback | Use it for | Do not assume |
| --- | --- | --- |
| `onLoad` | Initialize own state; obtain serialized references/components | Every peer's `onLoad` has already run |
| `onEnable` | Subscribe to enabled-lifetime events; start schedules | It runs only once |
| `start` | Initialization before this component's first update | Inactive/dynamically created components or asynchronous dependencies are all ready |
| `update(dt)` | Frame-based behavior, scaled by seconds | A fixed frame duration |
| `lateUpdate(dt)` | Work after updates, such as camera following | A replacement for an explicit data dependency |
| `onDisable` | Remove enabled-lifetime listeners; clear transient state | The node is being destroyed |
| `onDestroy` | Release owned resources and final references | It is the right place for every enable/disable cleanup |

`onLoad` is triggered on first node activation, not merely because a script exists in a file. Other scene nodes/references can be found in `onLoad`, but finding a component does not establish that its initialization finished. Inactive nodes still contain components. Do not diagnose `getComponent()` returning null solely by testing `node.active`.

## Execution order

```typescript
import { _decorator, Component } from 'cc';
const { ccclass, executionOrder } = _decorator;

@ccclass('EarlyState')
@executionOrder(-100)
export class EarlyState extends Component {
    value = 0;

    onLoad(): void {
        this.value = 42;
    }
}
```

Lower execution-order values run earlier within the engine's supported ordering. The decorator applies to `onLoad`, `onEnable`, `start`, `update`, and `lateUpdate`, not `onDisable`/`onDestroy`. Consult the matching version for node-tree ordering; do not promise a global total order for unrelated/dynamically activated nodes.

Prefer explicit `initialize(data)` calls or readiness promises when dependencies are asynchronous. Moving code from `onLoad` to `start` does not fix every ordering bug.

## Enabled-lifetime scheduling

```typescript
import { _decorator, Component } from 'cc';
const { ccclass } = _decorator;

@ccclass('Heartbeat')
export class Heartbeat extends Component {
    onEnable(): void {
        this.schedule(this.tick, 1);
    }

    onDisable(): void {
        this.unschedule(this.tick);
    }

    private tick(): void {
        console.log('tick');
    }
}
```

Inside a component, `scheduleOnce(callback, delay)` and `schedule(callback, interval, repeat, delay)` express game-time work. For example `this.schedule(this.tick, 0.5, 5, 2)` runs after a delay and repeats five times after the first invocation (six calls total). These are positional arguments, not `repeat=5` assignment expressions.

Use stable function references to cancel. Engine-owned scheduling does not cancel network requests or arbitrary promises; invalidate their results separately. Use platform timers only when wall-clock behavior is actually required and clean them up explicitly.

## Component access and lifetime

- `node.addComponent(MyComponent)` adds a component; an active node can trigger lifecycle work during addition. If configuration must precede activation, instantiate/configure under an inactive node and activate deliberately.
- `node.getComponent(MyComponent)` returns the component or null; `getComponents` returns an array.
- Remove a component by calling its `destroy()`, not an invented `node.removeComponent(...)` API.
- Cache repeated lookups when useful, but refresh references if nodes/components are replaced.
- Use `isValid(value, true)` when a reference queued for destruction must already be considered unusable.

For owned resources, see [resource-management.md](resource-management.md); for stable event listener cleanup, see [event-system.md](event-system.md).

## Validation cases

Exercise first activation, disable/re-enable, inactive initial nodes, dynamic component addition, and destruction while asynchronous work is pending. Log callback order rather than assuming it. Test schedule/listener counts after repeated UI opening.

## Sources

- [Lifecycle callbacks](https://docs.cocos.com/creator/3.8/manual/en/scripting/life-cycle-callbacks.html)
- [Execution-order decorator](https://docs.cocos.com/creator/3.8/manual/en/scripting/decorator.html)
- [Component API](https://docs.cocos.com/creator/3.8/api/en/class/Component)
