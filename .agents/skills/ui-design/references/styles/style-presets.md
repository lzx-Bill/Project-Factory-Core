# Style Presets — 风格预设

本文档定义 5 种风格预设，每个预设包含完整的视觉变量定义。

---

## Style 1: Modern Minimal

**关键词**: 大量留白、细线、功能感、现代简洁
**适用场景**: 工具类、效率应用、生产力软件

### 色彩系统

```yaml
colors:
  primary: "#2563EB"      # 品牌蓝
  secondary: "#64748B"     # 中性灰
  background:
    light: "#FFFFFF"
    dark: "#0F172A"
  text:
    primary: "#0F172A"     # 接近黑
    secondary: "#64748B"   # 次要灰
    muted: "#94A3B8"      # 占位灰
  semantic:
    success: "#10B981"     # 绿色
    warning: "#F59E0B"    # 橙色
    error: "#EF4444"       # 红色
    info: "#3B82F6"        # 蓝色
```

### 字体

```yaml
typography:
  fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
  sizes:
    display: "32px / 40px bold"
    h1: "24px / 32px semibold"
    h2: "18px / 24px medium"
    body: "16px / 24px regular"
    caption: "12px / 16px regular"
```

### 间距 & 圆角 & 阴影

```yaml
spacing:
  unit: 4
  scale: [4, 8, 12, 16, 24, 32, 48, 64]

borderRadius:
  button: 8px
  card: 12px
  input: 8px
  pill: 9999px

shadow:
  none: "none"
  sm: "0 1px 2px rgba(0,0,0,0.05)"
  md: "0 4px 6px rgba(0,0,0,0.07)"
  lg: "0 10px 15px rgba(0,0,0,0.1)"
```

### 组件特征

- 按钮: 细边框或纯色，轻微阴影
- 卡片: 白色背景，细边框或无边框
- 图标: 线性图标，2px 描边
- 输入框: 细边框，聚焦时边框加粗

---

## Style 2: Soft Elegant

**关键词**: 柔和渐变、圆角卡片、温暖感、优雅现代
**适用场景**: 消费类、情感化产品、健康/生活方式应用

### 色彩系统

```yaml
colors:
  primary: "#7C3AED"      # 紫罗兰
  secondary: "#A78BFA"     # 浅紫
  background:
    light: "#FAFAF9"      # 暖白
    dark: "#1C1917"       # 暖黑
  text:
    primary: "#1C1917"
    secondary: "#57534E"
    muted: "#A8A29E"
  semantic:
    success: "#22C55E"
    warning: "#FACC15"
    error: "#F87171"
    info: "#60A5FA"
  gradient:
    primary: "linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%)"
    surface: "linear-gradient(180deg, #FFFFFF 0%, #FAFAF9 100%)"
```

### 字体

```yaml
typography:
  fontFamily: "Source Han Sans CN, PingFang SC, -apple-system, sans-serif"
  sizes:
    display: "34px / 42px bold"
    h1: "26px / 34px semibold"
    h2: "20px / 28px medium"
    body: "16px / 26px regular"
    caption: "13px / 18px regular"
```

### 间距 & 圆角 & 阴影

```yaml
spacing:
  unit: 4
  scale: [4, 8, 16, 20, 24, 32, 48, 64]

borderRadius:
  button: 16px
  card: 20px
  input: 12px
  pill: 9999px

shadow:
  none: "none"
  sm: "0 2px 8px rgba(124, 58, 237, 0.08)"
  md: "0 8px 24px rgba(124, 58, 237, 0.12)"
  lg: "0 16px 48px rgba(124, 58, 237, 0.16)"
```

### 组件特征

- 按钮: 渐变背景，大圆角，轻柔阴影
- 卡片: 纯白背景，大圆角，微阴影
- 图标: 填充图标，保持柔和感
- 输入框: 淡边框，聚焦时发光效果

---

## Style 3: Neo-Brutalism

**关键词**: 粗边框、高对比、无阴影、几何感
**适用场景**: 强调个性、年轻用户、创意产品

### 色彩系统

```yaml
colors:
  primary: "#000000"       # 纯黑
  secondary: "#333333"     # 深灰
  background:
    light: "#FFFEF0"       # 米黄白
    dark: "#1A1A1A"       # 纯黑
  text:
    primary: "#000000"
    secondary: "#333333"
    muted: "#666666"
  semantic:
    success: "#00FF00"      # 亮绿
    warning: "#FFFF00"     # 亮黄
    error: "#FF0000"       # 纯红
    info: "#0000FF"        # 纯蓝
  accent: "#FF6B6B"        # 珊瑚红
```

### 字体

```yaml
typography:
  fontFamily: "Space Grotesk, -apple-system, sans-serif"
  sizes:
    display: "36px / 40px bold"
    h1: "28px / 32px bold"
    h2: "22px / 28px semibold"
    body: "16px / 24px medium"
    caption: "14px / 20px regular"
```

### 间距 & 圆角 & 阴影

```yaml
spacing:
  unit: 8
  scale: [8, 16, 24, 32, 48, 64]

borderRadius:
  button: 0px              # 方形
  card: 0px
  input: 0px
  pill: 4px

shadow:
  none: "none"
  sm: "4px 4px 0px #000000"   # 硬阴影
  md: "6px 6px 0px #000000"
  lg: "8px 8px 0px #000000"
```

### 组件特征

- 按钮: 黑色粗边框(3-4px)，无圆角，硬阴影
- 卡片: 白色背景，黑色边框，硬阴影
- 图标: 粗描边，几何形状
- 输入框: 黑色边框，背景透明

---

## Style 4: Premium Dark

**关键词**: 深色背景、金属光泽、精致动效、高端感
**适用场景**: 高端工具、专业软件、游戏化产品

### 色彩系统

```yaml
colors:
  primary: "#818CF8"       # 淡紫
  secondary: "#A5B4FC"     # 更淡紫
  background:
    light: "#1E1E2E"      # 深紫灰
    dark: "#0D0D0D"       # 近黑
  surface:
    light: "#2A2A3C"      # 卡片背景
    dark: "#1A1A2E"
  text:
    primary: "#F1F5F9"     # 近白
    secondary: "#94A3B8"
    muted: "#64748B"
  semantic:
    success: "#34D399"
    warning: "#FBBF24"
    error: "#F87171"
    info: "#60A5FA"
  glow: "rgba(129, 140, 248, 0.4)"  # 发光效果
```

### 字体

```yaml
typography:
  fontFamily: "SF Pro Display, -apple-system, sans-serif"
  sizes:
    display: "34px / 40px bold"
    h1: "26px / 32px semibold"
    h2: "20px / 28px medium"
    body: "16px / 24px regular"
    caption: "12px / 16px regular"
```

### 间距 & 圆角 & 阴影

```yaml
spacing:
  unit: 4
  scale: [4, 8, 12, 16, 24, 32, 48]

borderRadius:
  button: 12px
  card: 16px
  input: 8px
  pill: 9999px

shadow:
  none: "none"
  sm: "0 0 10px rgba(129, 140, 248, 0.2)"
  md: "0 0 20px rgba(129, 140, 248, 0.3)"
  lg: "0 0 40px rgba(129, 140, 248, 0.4)"
  glow: "0 0 60px rgba(129, 140, 248, 0.5)"
```

### 组件特征

- 按钮: 渐变边框，发光效果
- 卡片: 深色背景，细边框发光
- 图标: 线性图标，微发光
- 输入框: 细边框，聚焦时边框发光

---

## Style 5: Playful Colorful

**关键词**: 渐变、活泼、圆润、激励感
**适用场景**: 激励类、习惯追踪、儿童应用、游戏化

### 色彩系统

```yaml
colors:
  primary: "#F97316"       # 橙色
  secondary: "#FBBF24"      # 黄色
  background:
    light: "#FFFBEB"       # 暖白
    dark: "#1C1917"
  text:
    primary: "#1C1917"
    secondary: "#57534E"
    muted: "#A8A29E"
  gradient:
    primary: "linear-gradient(135deg, #F97316 0%, #FBBF24 100%)"
    success: "linear-gradient(135deg, #22C55E 0%, #4ADE80 100%)"
    playful: "linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%)"
  semantic:
    success: "#22C55E"
    warning: "#FBBF24"
    error: "#EF4444"
    info: "#3B82F6"
```

### 字体

```yaml
typography:
  fontFamily: "Nunito, -apple-system, sans-serif"
  sizes:
    display: "32px / 40px bold"
    h1: "24px / 32px bold"
    h2: "18px / 26px semibold"
    body: "16px / 26px regular"
    caption: "13px / 18px medium"
```

### 间距 & 圆角 & 阴影

```yaml
spacing:
  unit: 4
  scale: [4, 8, 12, 16, 24, 32, 48, 64]

borderRadius:
  button: 24px
  card: 24px
  input: 16px
  pill: 9999px

shadow:
  none: "none"
  sm: "0 4px 12px rgba(249, 115, 22, 0.15)"
  md: "0 8px 24px rgba(249, 115, 22, 0.2)"
  lg: "0 16px 40px rgba(249, 115, 22, 0.25)"
```

### 组件特征

- 按钮: 渐变背景，超大圆角，活泼阴影
- 卡片: 白色或渐变背景，大圆角
- 图标: 填充图标，色彩丰富
- 输入框: 大圆角，柔和边框

---

## 选择指南

| 风格 | 用户画像 | 情感基调 | 技术产品示例 |
|------|---------|---------|------------|
| Modern Minimal | 效率优先、专业 | 冷静、功能感 | Linear, Notion |
| Soft Elegant | 注重体验、品质 | 温暖、关怀 | Calm, Headspace |
| Neo-Brutalism | 追求个性、创意 | 大胆、有态度 | Heron Preston, Kidult |
| Premium Dark | 追求品质、专业 | 高端、沉浸 | Arc, Raycast |
| Playful Colorful | 激励成长、年轻 | 活力、正向 | Duolingo, Habitica |
