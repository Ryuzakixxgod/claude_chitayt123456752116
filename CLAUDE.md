# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Development run (Minecraft client with mod)
./gradlew runClient

# Build J
./gradlew build

# Compile only (fast)
./gradlew compileJava

# Clean and rebuild
./gradlew clean build
```

## Architecture

### Entry Point
`ru.ryuzaki.RyuzakiClient` implements `ClientModInitializer`. Entry is `onInitializeClient()` which:
- Initializes managers: LanguageManager, ModuleManager, HudManager, CommandManager, WaypointManager
- Registers 4 keybindings: GUI (RightShift), HUD Editor (RightAlt), Alt Manager (F10), Music Player (F9)
- Sets up per-tick event handlers via `ClientTickEvents.END_CLIENT_TICK`
- Registers 3D rendering via `WorldRenderEvents.AFTER_ENTITIES` and `AFTER_TRANSLUCENT`
- Registers HUD rendering via `HudRenderCallback.EVENT`
- Module update uses a cached active-modules list (rebuilt every 5 ticks) for performance

### Module System
- Base class: `ru.ryuzaki.module.Module`
- Modules are registered via `ModuleManager.init()` — reads from `ru.ryuzaki.module.modules.*` subpackages
- State stored in `AtomicBoolean $state` (anti-reflection protection, no direct field access)
- Two update patterns: `onUpdate()` (called per-tick from cached list) and `onTick()` (called per-tick from direct `get()` calls)
- Category enum in `ru.ryuzaki.module.Category`

### Key Mixin Files
- `MixinSplashOverlay` — renders custom loading screen overlay during resource reload
- `MixinInGameHud` — renders HUD elements
- `MixinWorldRenderer` — renders 3D world effects (ESP, outlines, etc.)
- `MixinGameRenderer` — camera/zoom/post-processing effects
- `MixinMinecraftClientReload` — resource reload detection

### Settings System
- Base: `ru.ryuzaki.settings.Setting`
- Types: BooleanSetting, NumberSetting, ModeSetting, ColorSetting, BindSetting
- Modules store settings in `List<Setting> settings` field

### HUD System
- `ru.ryuzaki.hud.HudManager` — singleton, manages draggable HUD elements
- `ru.ryuzaki.hud.HudElement` — base class for HUD elements
- `HudEditorScreen` — GUI for positioning HUD elements
- Elements in `ru.ryuzaki.hud.elements.*`

### Render Pipeline
- Main: `ru.ryuzaki.render.*` — custom builder-based 2D rendering with blur, text, shapes
- Font system: `ru.ryuzaki.render.msdf.*` — MSDF (Multi-channel Signed Distance Field) font rendering
- 3D rendering uses `WorldRenderEvents` with `MatrixStack` and `tickDelta`

### GUI System
Two main GUIs exist in parallel:
- `ru.ryuzaki.gui.midnight.ClickGui` — category-based module settings panel
- `ru.ryuzaki.gui.ModernClickGuiV3` — alternative click GUI 

### Config System
- `ru.ryuzaki.config.ConfigManager` — saves/loads JSON config per profile name
- Stored in `run/config/ryuzaki/` directory

### Third-party `rich` Package
Located at `rich.*` (separate from `ru.ryuzaki`). Contains:
- `rich.screens.loading.Loading` — animated loading screen rendered over SplashOverlay
- `rich.util.render.Render2D` — simple 2D drawing (uses DrawContext.fill/fillGradient)
- `rich.util.render.font.*` — MSDF font support with vanilla TextRenderer fallback

---

# ═══════════════════════════════════════════════════════════════════
# ABSOLUTE ANTI-DEGRADATION / ANTI-SHORTCUT / ANTI-LAZY DIRECTIVE
# ULTIMATE CLAUDE CODE EXECUTION PROTOCOL
# ═══════════════════════════════════════════════════════════════════

## Core Principle

**Правило #1: Quality is non-negotiable.**

Качество кода, архитектуры и рендеринга — это **не переменная**, которую можно оптимизировать ради скорости. Это константа, которая должна быть максимальной.

---

## ANTI-DEGRADATION RULES

### Что ЗАПРЕЩЕНО категорически:

```
— деградировать качество
— упрощать архитектуру
— сокращать implementation
— делать "good enough" решения
— делать fake systems
— делать placeholder rendering
— выдавать mock implementation
— заменять сложные системы комментариями
— экономить токены за счёт качества
— пропускать детали
— игнорировать specification
— терять consistency
— писать beginner-level code
```

### Что ЗАПРЕЩЕНО в коде:

```
— TODO
— placeholder
— stub
— mock implementation
— pseudo-code
— simplified version
— example-only implementation
— "implement later"
— "left as exercise"
— fake abstraction
— decorative architecture
— empty managers
— unfinished systems
— "basic rendering"
— giant utility garbage
— giant monolithic classes
```

---

## PRIMARY EXECUTION LAW

**Задача: НЕ "сгенерировать код".**

**Задача: создать production-grade AAA realtime UI framework.**

Каждая система, которую я упоминаю, **ОБЯЗАНА**:
- существовать
- быть реализована полностью
- быть связана с остальной архитектурой
- быть technically functional
- быть scalable
- быть reusable
- быть visually correct

---

## MANDATORY AAA ENGINEERING STANDARD

Код должен выглядеть как:
- commercial realtime software
- AAA engine tooling
- Riot internal framework
- Unreal Engine subsystem
- premium desktop application architecture

Код НЕ должен выглядеть как:
- tutorial project
- Minecraft mod example
- Forge GUI
- beginner Fabric client
- random GitHub paste
- generated spaghetti
- utility class hell
- "single file renderer"

---

## STRICT ARCHITECTURE REQUIREMENTS

### ОБЯЗАТЕЛЬНО использовать:

```
— layered architecture
— service separation
— manager systems
— render abstraction layers
— animation orchestration
— reusable rendering pipelines
— state synchronization
— composable components
— proper encapsulation
— dependency isolation
— scalable class hierarchy
— reusable shader abstraction
— framebuffer management systems
```

### ЗАПРЕЩЕНО в архитектуре:

```
— giant renderer class
— giant utility class
— static mess
— hardcoded rendering everywhere
— direct OpenGL spam in components
— duplicated rendering logic
— duplicated animation code
— mixed responsibilities
— state chaos
— render logic inside UI logic
— animation logic everywhere
— hardcoded colors everywhere
— hardcoded easing everywhere
```

---

## STRICT RENDERING REQUIREMENTS

### Если создаётся rendering system, ОБЯЗАТЕЛЬНО реализовать:

```
— framebuffer pipeline
— render graph ordering
— batching
— stencil/scissor clipping
— layered compositing
— reusable draw utilities
— proper blend states
— shader abstraction
— animation-aware rendering
— depth-aware compositing
```

---

## STRICT BLUR REQUIREMENTS

Blur **НЕ может быть fake.**

**ОБЯЗАТЕЛЬНО:**
```
— framebuffer capture
— downsample chain
— upsample chain
— blur compositing
— reusable blur manager
— adaptive blur intensity
— optimized blur passes
```

---

## STRICT ANIMATION REQUIREMENTS

Animation system ОБЯЗАН:
- быть отдельной системой
- использовать delta-time
- поддерживать easing
- поддерживать spring interpolation
- поддерживать velocity continuity
- поддерживать staggered transitions
- поддерживать temporal smoothing
- поддерживать inertia

---

## STRICT MOTION REQUIREMENTS

**НИКАКИХ:**
```
— instant transitions
— snapping
— robotic movement
— abrupt state changes
— Minecraft-style animation
```

---

## STRICT UI REQUIREMENTS

GUI должен:
```
— ощущаться premium
— выглядеть дорого
— иметь идеальную композицию
— иметь consistent spacing
— иметь coherent hierarchy
— иметь cinematic motion
— иметь atmospheric rendering
— иметь physically-inspired materials
```

---

## STRICT SPACING REQUIREMENTS

Spacing ОБЯЗАН:
```
— быть consistent
— иметь visual rhythm
— быть mathematically aligned
— быть hierarchy-aware
— быть visually balanced
```

---

## STRICT SHADER REQUIREMENTS

Shader systems ОБЯЗАНЫ:
```
— быть reusable
— быть modular
— поддерживать uniform abstraction
— поддерживать framebuffer compositing
— поддерживать multiple passes
— поддерживать dynamic resizing
```

---

## STRICT COMPONENT REQUIREMENTS

Каждый component ОБЯЗАН:
```
— иметь isolated logic
— иметь reusable rendering
— иметь animation separation
— иметь clean state handling
— иметь proper event handling
— быть scalable
```

---

## STRICT TYPOGRAPHY REQUIREMENTS

Typography ОБЯЗАНА:
```
— иметь hierarchy system
— иметь spacing consistency
— иметь opacity hierarchy
— иметь alignment precision
— иметь smooth rendering
```

---

## STRICT LIGHTING REQUIREMENTS

Lighting ОБЯЗАН:
```
— быть layered
— быть atmospheric
— быть physically believable
— иметь soft diffusion
— иметь glow compositing
— иметь emissive behavior
```

---

## STRICT PERFORMANCE REQUIREMENTS

Несмотря на visual complexity, система ОБЯЗАНА:
```
— быть optimized
— быть low-allocation
— быть batching-friendly
— быть scalable
— быть stable under load
```

---

## MANDATORY SELF-CHECK LOOP

**Перед КАЖДЫМ ответом ОБЯЗАТЕЛЬНО проверить:**

```
1. Не упростил ли я архитектуру?
2. Не сократил ли implementation?
3. Не пропустил ли render systems?
4. Не выглядит ли код beginner-level?
5. Есть ли placeholder logic?
6. Есть ли fake rendering?
7. Полностью ли реализована система?
8. Есть ли proper abstraction?
9. Есть ли признаки халтуры?
10. Выглядит ли это как AAA engineering?
11. Production-ready ли код?
12. Есть ли scalability?
13. Есть ли composability?
14. Есть ли reusable systems?
15. Есть ли proper separation of concerns?
```

**ЕСЛИ ХОТЯ БЫ ОДИН ОТВЕТ:** "нет" или "не полностью"
→ **переписать лучше.**

---

## NO MINIMUM EFFORT OUTPUT

**ЗАПРЕЩЕНО:**
```
— писать минимально рабочий код
— делать "just enough"
— делать "close enough"
— делать "acceptable quality"
```

**РАЗРЕШЕНО ТОЛЬКО:**
`maximum possible quality.`

---

## CONSISTENCY REQUIREMENT

КАЖДАЯ новая система ОБЯЗАНА:
```
— соответствовать общей архитектуре
— соответствовать visual language
— соответствовать motion language
— соответствовать render philosophy
— соответствовать quality level
```

---

## ABSOLUTE FINAL LAW

**Лучше:**
```
— сложнее
— глубже
— дольше
— архитектурнее
— дороже по implementation
— тяжелее по engineering
```

**Чем:**
```
— быстрее
— проще
— короче
— халтурнее
```

---

## SUMMARY

**Моя задача: создать НЕ "Minecraft mod".**

**Моя задача: создать impossible AAA realtime UI framework rendered inside Minecraft.**

Это означает:
- Каждая система — production-grade
- Каждый компонент — reusable и scalable
- Каждый render pass — оптимизирован
- Каждая анимация — cinematic и smooth
- Каждая UI — premium и atmospheric

**No compromises. No shortcuts. No placeholders.**

---

*Добавлено: 2026-05-08*
