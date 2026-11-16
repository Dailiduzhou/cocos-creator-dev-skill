# Events and input (Creator 3.8 baseline)

## Choose the correct event boundary

| Requirement | API / behavior |
| --- | --- |
| Global keyboard, pointer, device input | `input.on(Input.EventType.*, callback, target)` |
| Hit-tested UI touch/mouse events | `node.on(Node.EventType.*, callback, target)`; needs `UITransform` |
| Button click | `Button.EventType.CLICK` on the Button's node |
| Local custom notification | `node.emit(name, payload)`; does not traverse ancestors |
| Cross-system event bus | An owned `EventTarget` instance |
| Custom event through ancestors | Subclass `Event`, enable bubbling, and call `node.dispatchEvent(event)` |
| Picking 3D objects | Input screen position → camera ray → raycast/hit test |

The `input` singleton was introduced in 3.4; check older projects rather than copying it into any 3.x version. Input ordering/interception is version-sensitive (3.4.0 and 3.4.1 differ); do not assume UI propagation flags alone gate every gameplay input listener. If gameplay must ignore UI interaction, define and test an explicit interaction policy.

## Stable subscriptions

```typescript
import { _decorator, Component, EventKeyboard, input, Input, KeyCode } from 'cc';
const { ccclass } = _decorator;

@ccclass('KeyboardAction')
export class KeyboardAction extends Component {
    onEnable(): void {
        input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }

    onDisable(): void {
        input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }

    private onKeyDown(event: EventKeyboard): void {
        if (event.keyCode === KeyCode.SPACE) {
            this.node.emit('jump-requested');
        }
    }
}
```

Use the same event type, callback identity, target, and capture flag for `off` as for `on`. Avoid inline `.bind(this)` on both calls: it creates two different function objects. Use `onLoad`/`onDestroy` instead if the listener should remain active while the component is disabled, and make that choice explicit.

A custom bus created with `new EventTarget()` does not need a persistent node just to exist in a module. Consumers still own their subscriptions and must unsubscribe. For held keyboard state, clear the pressed-key set on disable/focus-loss handling so a missing key-up does not leave movement stuck.

## UI coordinates and dragging

UI hit testing uses the node's `UITransform`. For a standard Canvas UI camera, convert `getUILocation()` to the destination parent's anchor-relative local space. The following component drags a child directly to the pointer; it intentionally does not preserve the initial grab offset.

```typescript
import { _decorator, Component, EventTouch, Node, UITransform, Vec3 } from 'cc';
const { ccclass } = _decorator;

@ccclass('DragToPointer')
export class DragToPointer extends Component {
    private touchId: number | null = null;
    private point = new Vec3();

    onEnable(): void {
        this.node.on(Node.EventType.TOUCH_START, this.begin, this);
        this.node.on(Node.EventType.TOUCH_MOVE, this.move, this);
        this.node.on(Node.EventType.TOUCH_END, this.end, this);
        this.node.on(Node.EventType.TOUCH_CANCEL, this.end, this);
    }

    onDisable(): void {
        this.node.off(Node.EventType.TOUCH_START, this.begin, this);
        this.node.off(Node.EventType.TOUCH_MOVE, this.move, this);
        this.node.off(Node.EventType.TOUCH_END, this.end, this);
        this.node.off(Node.EventType.TOUCH_CANCEL, this.end, this);
        this.touchId = null;
    }

    private begin(event: EventTouch): void {
        if (this.touchId !== null) return;
        this.touchId = event.getID();
        this.move(event);
    }

    private move(event: EventTouch): void {
        if (event.getID() !== this.touchId) return;
        const parentUI = this.node.parent?.getComponent(UITransform);
        if (!parentUI) return;
        const ui = event.getUILocation();
        this.point.set(ui.x, ui.y, 0);
        parentUI.convertToNodeSpaceAR(this.point, this.point);
        this.node.setPosition(this.point.x, this.point.y, this.node.position.z);
    }

    private end(event: EventTouch): void {
        if (event.getID() === this.touchId) this.touchId = null;
    }
}
```

Attach to a UI node with `UITransform`, under a UI parent with `UITransform`. Account for Layout/Widget overriding positions. Test scaled/rotated parents, Canvas scaling, and touch cancellation. Custom cameras and world-space UI require camera-aware conversions; with several UI cameras/Canvases, pick the camera that actually renders the node (per-Canvas `cameraPriority`, not "the" main camera), and note that a camera whose target is a RenderTexture does not map one-to-one to the display. There is no general `EventTouch.getLocalLocation()` for the desired node's space.

## Emission versus propagation

Prefer an owned `EventTarget` for application-level custom events: the 3.8 manual states that Node objects are no longer recommended for custom event listen/emit (it is less efficient, and Node should carry node-related events). Use node `emit`/`dispatchEvent` when the notification is inherently about the node tree (ancestor reaction, UI layering), and reserve bubbling `Event` subclasses for that case.

```typescript
import { Event, Node } from 'cc';

export class HealthChanged extends Event {
    constructor(public readonly health: number) {
        super('health-changed', true);
    }
}

export function notifyAncestors(node: Node, health: number): void {
    node.dispatchEvent(new HealthChanged(health));
}
```

`node.emit('health-changed', value)` invokes listeners on that emitter only. `dispatchEvent` participates in the node event delivery system; bubbling must be enabled for ancestor delivery. Creator 3.x removed `Event.EventCustom`, so subclass `Event` instead.

For propagated events, `target` is the original node and `currentTarget` is the node handling this stage. `event.propagationStopped = true` stops further propagation; this is different from allowing touches to penetrate overlapping siblings. Use capture flags only where the matching version supports them, and match them during removal. Buttons, ScrollViews, and `BlockInputEvents` affect UI event delivery; test the real hierarchy.

## Troubleshooting

- No UI input: inspect `UITransform` hit area, effective activity, Canvas/camera, overlap, masks, and input-blocking components.
- Repeated callback: inspect registration sites and callback identity. Pair lifetimes instead of blindly adding more listeners.
- Event bus receives messages while disabled: `emit` is not automatically gated by component activation; unsubscribe or explicitly gate handling.
- Parent misses a custom message: verify `emit` vs `dispatchEvent`, bubbling, event spelling, and registration timing.
- Avoid internal fields such as `node.eventListeners.size` as diagnostics; log your own registration lifecycle.

## Sources

- [Input event system and version notes](https://docs.cocos.com/creator/3.8/manual/en/engine/event/event-input.html)
- [Node event system](https://docs.cocos.com/creator/3.8/manual/en/engine/event/event-node.html)
- [EventTouch API](https://docs.cocos.com/creator/3.8/api/en/class/EventTouch)
- [UITransform API](https://docs.cocos.com/creator/3.8/api/en/class/UITransform)
