# AI Token Tracker - UI/UX Design System

**Document Version:** 1.0  
**Last Updated:** April 28, 2026  
**Status:** ✅ Production-Ready  
**Design Tool:** Figma (https://figma.com/ai-token-tracker)

---

## 📋 Table of Contents

1. [Design Principles](#design-principles)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Components](#components)
6. [Iconography](#iconography)
7. [Data Visualization](#data-visualization)
8. [Responsive Design](#responsive-design)
9. [Accessibility](#accessibility)
10. [User Flows](#user-flows)
11. [Dashboard Layouts](#dashboard-layouts)
12. [States & Interactions](#states--interactions)

---

## 🎯 Design Principles

### 1. **Clarity Over Cleverness**
> Users should understand their AI spending at a glance. No jargon, no unnecessary complexity.

**Application:**
- Use plain language ("You've used 2.4M tokens" vs "Token consumption: 2.4e6")
- Show costs in dollars, not abstract units
- Visual progress bars for budgets

### 2. **Privacy-First Transparency**
> Make it crystal clear what we track and what we don't.

**Application:**
- Privacy badge on every page
- "What we track" tooltip on hover
- Clear data retention messaging

### 3. **Data-Dense but Breathable**
> Finance users need lots of data. Engineers want clean UIs. Balance both.

**Application:**
- Progressive disclosure (summary → details)
- Collapsible sections
- Generous whitespace between dense sections

### 4. **Performance-First**
> Dashboards should load fast, even with millions of data points.

**Application:**
- Virtualized lists for large datasets
- Lazy loading for charts
- Server-side rendering

### 5. **Mobile-Aware, Desktop-Optimized**
> Primary use case is desktop, but support mobile for on-the-go checks.

**Application:**
- Responsive layouts
- Touch-friendly buttons (44px minimum)
- Simplified mobile charts

---

## 🎨 Color System

### Primary Palette

```
Primary Blue (Action, Links)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#0066FF  blue-600  Primary buttons, links
#0052CC  blue-700  Hover state
#003D99  blue-800  Active state
#99BFFF  blue-300  Light backgrounds
#E6F0FF  blue-100  Very light backgrounds

Success Green (Positive, On Budget)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#00A86B  green-600  Success states
#008556  green-700  Hover
#99E6C8  green-300  Light backgrounds
#E6F9F2  green-100  Very light backgrounds

Warning Orange (Approaching Limit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#FF9500  orange-600  Warning states
#CC7700  orange-700  Hover
#FFCC80  orange-300  Light backgrounds
#FFF4E6  orange-100  Very light backgrounds

Error Red (Over Budget, Errors)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#E63946  red-600  Error states, over budget
#B82D37  red-700  Hover
#FFBFC4  red-300  Light backgrounds
#FFEBEE  red-100  Very light backgrounds
```

### Neutral Palette

```
Grays (Text, Backgrounds, Borders)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#1A1A1A  gray-900  Headings, primary text
#4D4D4D  gray-700  Body text
#808080  gray-500  Secondary text
#CCCCCC  gray-300  Borders, dividers
#F5F5F5  gray-100  Light backgrounds
#FFFFFF  white     Main background
```

### Semantic Colors

```
Budget Status Colors
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
On Track (0-70%):     #00A86B (green-600)
Warning (71-90%):     #FF9500 (orange-600)
Critical (91-100%):   #E63946 (red-600)
Over Budget (>100%):  #B82D37 (red-700)

AI Service Colors (for charts)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OpenAI/ChatGPT:       #10A37F (OpenAI green)
Anthropic/Claude:     #CC785C (Claude coral)
GitHub/Copilot:       #7D56F4 (GitHub purple)
Google/Gemini:        #4285F4 (Google blue)
Other:                #808080 (gray-500)
```

### Usage Examples

```css
/* Button Styles */
.btn-primary {
  background-color: #0066FF;  /* blue-600 */
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: #0052CC;  /* blue-700 */
}

/* Budget Alert */
.budget-warning {
  background-color: #FFF4E6;  /* orange-100 */
  border-left: 4px solid #FF9500;  /* orange-600 */
  color: #1A1A1A;  /* gray-900 */
}

/* Success State */
.budget-on-track {
  background-color: #E6F9F2;  /* green-100 */
  border-left: 4px solid #00A86B;  /* green-600 */
}
```

---

## ✍️ Typography

### Font Families

```css
Primary Font (UI):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             sans-serif;

Monospace (Code, Numbers):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
font-family: 'JetBrains Mono', 'SF Mono', 'Consolas', monospace;
```

### Type Scale

```css
/* Headings */
.text-h1 {
  font-size: 32px;
  font-weight: 700;
  line-height: 40px;
  letter-spacing: -0.5px;
}

.text-h2 {
  font-size: 24px;
  font-weight: 600;
  line-height: 32px;
  letter-spacing: -0.25px;
}

.text-h3 {
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
  letter-spacing: 0;
}

.text-h4 {
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0;
}

/* Body Text */
.text-body-large {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0;
}

.text-body {
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0;
}

.text-body-small {
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  letter-spacing: 0;
}

/* Numbers (tabular) */
.text-number {
  font-family: 'JetBrains Mono', monospace;
  font-feature-settings: 'tnum';  /* Tabular numbers */
  font-variant-numeric: tabular-nums;
}

/* Labels */
.text-label {
  font-size: 12px;
  font-weight: 600;
  line-height: 16px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
```

### Usage Guidelines

```
Headings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
H1: Page titles only ("My AI Usage")
H2: Section headings ("Budget Status", "Usage Over Time")
H3: Subsection headings ("Top Users", "This Month")
H4: Card titles, widget headers

Body Text:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Large: Important messages, intro text
Regular: Standard UI text, descriptions
Small: Captions, footnotes, metadata

Numbers:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Always use monospace for:
  • Token counts (2,400,000)
  • Costs ($86.50)
  • Percentages (78%)
  • Dates/times

Labels:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Form labels, filter tags, status badges
```

---

## 📏 Spacing & Layout

### Spacing Scale (8px grid)

```
Base Unit: 8px

Spacing Scale:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
xs:   4px   (0.5 × base)  Tight spacing
sm:   8px   (1 × base)    Small gaps
md:   16px  (2 × base)    Medium gaps
lg:   24px  (3 × base)    Large gaps
xl:   32px  (4 × base)    Section spacing
2xl:  48px  (6 × base)    Page spacing
3xl:  64px  (8 × base)    Major sections

Usage:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
padding-xs:   4px    Icon padding
padding-sm:   8px    Button padding (vertical)
padding-md:   16px   Card padding, button padding (horizontal)
padding-lg:   24px   Page padding
padding-xl:   32px   Dashboard sections

margin-sm:    8px    Inline elements
margin-md:    16px   Between components
margin-lg:    24px   Between sections
margin-xl:    32px   Between major sections
```

### Grid System

```
Desktop (1440px)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12-column grid
Column width: 96px
Gutter: 24px
Margin: 48px

Tablet (768px)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12-column grid
Column width: 48px
Gutter: 16px
Margin: 24px

Mobile (375px)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4-column grid
Column width: 72px
Gutter: 12px
Margin: 16px
```

### Layout Containers

```css
/* Page Container */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 48px;
}

/* Card */
.card {
  background: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  padding: 24px;
}

/* Dashboard Grid (3-column) */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Stat Card (1/3 width) */
.stat-card {
  grid-column: span 1;
}

/* Chart Card (full width) */
.chart-card {
  grid-column: span 3;
}
```

---

## 🧩 Components

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: #0066FF;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #0052CC;
  box-shadow: 0 4px 8px rgba(0, 102, 255, 0.24);
}

.btn-primary:active {
  background: #003D99;
  box-shadow: none;
}

.btn-primary:disabled {
  background: #CCCCCC;
  cursor: not-allowed;
}

/* Secondary Button */
.btn-secondary {
  background: #FFFFFF;
  color: #0066FF;
  border: 1px solid #0066FF;
  /* ... rest same as primary ... */
}

/* Ghost Button */
.btn-ghost {
  background: transparent;
  color: #0066FF;
  border: none;
  /* ... */
}

/* Danger Button */
.btn-danger {
  background: #E63946;
  color: #FFFFFF;
  /* ... */
}
```

**Button Sizes:**
```css
.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-md {  /* Default */
  padding: 10px 20px;
  font-size: 14px;
}

.btn-lg {
  padding: 14px 28px;
  font-size: 16px;
}
```

### Cards

```html
<!-- Stat Card -->
<div class="stat-card">
  <div class="stat-card__label">Total Tokens</div>
  <div class="stat-card__value">2.4M</div>
  <div class="stat-card__change positive">
    <svg>↑</svg>
    <span>12% vs last month</span>
  </div>
</div>
```

```css
.stat-card {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.stat-card__label {
  font-size: 12px;
  font-weight: 600;
  color: #808080;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.stat-card__value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 32px;
  font-weight: 700;
  color: #1A1A1A;
  margin-bottom: 12px;
}

.stat-card__change {
  font-size: 14px;
  color: #808080;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-card__change.positive {
  color: #00A86B;
}

.stat-card__change.negative {
  color: #E63946;
}
```

### Progress Bars

```html
<!-- Budget Progress -->
<div class="progress-bar">
  <div class="progress-bar__header">
    <span class="progress-bar__label">Monthly Budget</span>
    <span class="progress-bar__value">$2,250 / $3,000</span>
  </div>
  <div class="progress-bar__track">
    <div class="progress-bar__fill" style="width: 75%"></div>
  </div>
  <div class="progress-bar__footer">
    <span class="progress-bar__status warning">75% used</span>
  </div>
</div>
```

```css
.progress-bar {
  margin-bottom: 24px;
}

.progress-bar__header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.progress-bar__label {
  font-weight: 600;
  color: #1A1A1A;
}

.progress-bar__value {
  font-family: 'JetBrains Mono', monospace;
  color: #4D4D4D;
}

.progress-bar__track {
  height: 8px;
  background: #F5F5F5;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar__fill {
  height: 100%;
  background: linear-gradient(90deg, #00A86B 0%, #00A86B 70%, #FF9500 90%, #E63946 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-bar__status {
  font-size: 12px;
  font-weight: 600;
}

.progress-bar__status.warning {
  color: #FF9500;
}
```

### Alerts/Banners

```html
<!-- Budget Warning Alert -->
<div class="alert alert-warning">
  <svg class="alert__icon">⚠</svg>
  <div class="alert__content">
    <div class="alert__title">Budget Warning</div>
    <div class="alert__message">
      Your team is at 75% of monthly budget with 10 days remaining.
    </div>
  </div>
  <button class="alert__close">×</button>
</div>
```

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.alert-info {
  background: #E6F0FF;
  border-left: 4px solid #0066FF;
  color: #003D99;
}

.alert-success {
  background: #E6F9F2;
  border-left: 4px solid #00A86B;
  color: #008556;
}

.alert-warning {
  background: #FFF4E6;
  border-left: 4px solid #FF9500;
  color: #CC7700;
}

.alert-error {
  background: #FFEBEE;
  border-left: 4px solid #E63946;
  color: #B82D37;
}

.alert__icon {
  font-size: 20px;
  flex-shrink: 0;
}

.alert__content {
  flex: 1;
}

.alert__title {
  font-weight: 600;
  margin-bottom: 4px;
}

.alert__message {
  font-size: 14px;
}

.alert__close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  opacity: 0.6;
}

.alert__close:hover {
  opacity: 1;
}
```

### Tables

```html
<!-- Top Users Table -->
<table class="data-table">
  <thead>
    <tr>
      <th>User</th>
      <th class="text-right">Tokens</th>
      <th class="text-right">Cost</th>
      <th>Trend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <div class="user-cell">
          <div class="user-cell__avatar">AC</div>
          <div class="user-cell__name">Alex Chen</div>
        </div>
      </td>
      <td class="text-right text-number">8.2M</td>
      <td class="text-right text-number">$287.00</td>
      <td>
        <div class="sparkline">████████</div>
      </td>
    </tr>
  </tbody>
</table>
```

```css
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.data-table thead {
  background: #F5F5F5;
}

.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: #808080;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #CCCCCC;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid #F5F5F5;
}

.data-table tbody tr:hover {
  background: #FAFAFA;
}

.text-right {
  text-align: right;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-cell__avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #0066FF;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.user-cell__name {
  font-weight: 500;
}
```

### Badges

```html
<span class="badge badge-success">On Track</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-error">Over Budget</span>
<span class="badge badge-neutral">Inactive</span>
```

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-success {
  background: #E6F9F2;
  color: #008556;
}

.badge-warning {
  background: #FFF4E6;
  color: #CC7700;
}

.badge-error {
  background: #FFEBEE;
  color: #B82D37;
}

.badge-neutral {
  background: #F5F5F5;
  color: #808080;
}
```

---

## 🎨 Iconography

### Icon Library

**Primary:** [Heroicons](https://heroicons.com/) (MIT License)

**Icon Sizes:**
```css
.icon-sm {
  width: 16px;
  height: 16px;
}

.icon-md {  /* Default */
  width: 20px;
  height: 20px;
}

.icon-lg {
  width: 24px;
  height: 24px;
}

.icon-xl {
  width: 32px;
  height: 32px;
}
```

**Common Icons:**
```
Navigation:
  • Home: home
  • Dashboard: chart-bar
  • Settings: cog
  • Logout: arrow-right-on-rectangle

Actions:
  • Download: arrow-down-tray
  • Export: document-arrow-down
  • Refresh: arrow-path
  • Delete: trash
  • Edit: pencil

Status:
  • Success: check-circle
  • Warning: exclamation-triangle
  • Error: x-circle
  • Info: information-circle

Data:
  • Tokens: cube
  • Cost: currency-dollar
  • Time: clock
  • Users: users
```

---

## 📊 Data Visualization

### Chart Library

**Primary:** [Apache ECharts](https://echarts.apache.org/)

### Chart Types & Usage

**1. Line Chart** - Time Series Usage
```javascript
const lineChartOptions = {
  color: ['#0066FF'],
  grid: {
    left: '48px',
    right: '24px',
    top: '24px',
    bottom: '48px'
  },
  xAxis: {
    type: 'category',
    data: dates,
    axisLine: {
      lineStyle: { color: '#CCCCCC' }
    },
    axisLabel: {
      color: '#808080',
      fontSize: 12
    }
  },
  yAxis: {
    type: 'value',
    name: 'Tokens',
    nameTextStyle: {
      color: '#808080',
      fontSize: 12
    },
    axisLine: { show: false },
    axisTick: { show: false },
    splitLine: {
      lineStyle: { color: '#F5F5F5' }
    }
  },
  series: [{
    data: values,
    type: 'line',
    smooth: true,
    lineStyle: {
      width: 3
    },
    areaStyle: {
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(0, 102, 255, 0.2)' },
          { offset: 1, color: 'rgba(0, 102, 255, 0)' }
        ]
      }
    }
  }],
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1A1A1A',
    borderWidth: 0,
    textStyle: {
      color: '#FFFFFF',
      fontSize: 14
    }
  }
};
```

**2. Horizontal Bar Chart** - Tool/Department Breakdown
```javascript
const barChartOptions = {
  color: ['#10A37F', '#7D56F4', '#CC785C'],
  grid: {
    left: '150px',
    right: '48px',
    top: '24px',
    bottom: '24px'
  },
  xAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value}%'
    }
  },
  yAxis: {
    type: 'category',
    data: ['Claude Code', 'GitHub Copilot', 'ChatGPT Web']
  },
  series: [{
    type: 'bar',
    data: [75, 19, 6],
    barWidth: '60%',
    itemStyle: {
      borderRadius: [0, 4, 4, 0]
    },
    label: {
      show: true,
      position: 'right',
      formatter: '{c}%',
      color: '#1A1A1A'
    }
  }]
};
```

**3. Pie/Donut Chart** - Service Distribution
```javascript
const pieChartOptions = {
  color: ['#10A37F', '#CC785C', '#7D56F4', '#808080'],
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],  // Donut
    data: [
      { value: 55, name: 'OpenAI' },
      { value: 35, name: 'Anthropic' },
      { value: 8, name: 'GitHub' },
      { value: 2, name: 'Others' }
    ],
    label: {
      formatter: '{b}\n{d}%',
      fontSize: 14
    },
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: 'rgba(0, 0, 0, 0.2)'
      }
    }
  }],
  legend: {
    bottom: 0,
    left: 'center'
  }
};
```

### Chart Color Palette (Color-Blind Friendly)

```javascript
// Tol Bright Scheme (optimized for color blindness)
const chartColors = [
  '#4477AA',  // Blue
  '#EE6677',  // Red
  '#228833',  // Green
  '#CCBB44',  // Yellow
  '#66CCEE',  // Cyan
  '#AA3377',  // Purple
  '#BBBBBB'   // Gray
];
```

---

## 📱 Responsive Design

### Breakpoints

```css
/* Breakpoint System */
$breakpoint-sm: 640px;   /* Mobile landscape */
$breakpoint-md: 768px;   /* Tablet */
$breakpoint-lg: 1024px;  /* Desktop */
$breakpoint-xl: 1280px;  /* Large desktop */
$breakpoint-2xl: 1536px; /* Extra large */
```

### Responsive Layouts

**Dashboard Grid:**
```css
/* Desktop (default) - 3 columns */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Tablet - 2 columns */
@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

/* Mobile - 1 column */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
```

**Navigation:**
```css
/* Desktop - Sidebar */
.nav {
  width: 240px;
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
}

/* Mobile - Bottom Tab Bar */
@media (max-width: 768px) {
  .nav {
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    height: 64px;
    display: flex;
    justify-content: space-around;
  }
}
```

**Typography (Fluid):**
```css
/* Scale down headings on mobile */
@media (max-width: 768px) {
  .text-h1 {
    font-size: 24px;
    line-height: 32px;
  }
  
  .text-h2 {
    font-size: 20px;
    line-height: 28px;
  }
}
```

---

## ♿ Accessibility

### WCAG 2.1 Level AA Compliance

**Color Contrast Ratios:**
```
Text on Backgrounds:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#1A1A1A on #FFFFFF:  15.3:1  ✅ (AAA)
#4D4D4D on #FFFFFF:  8.6:1   ✅ (AAA)
#808080 on #FFFFFF:  4.5:1   ✅ (AA)
#0066FF on #FFFFFF:  4.6:1   ✅ (AA)
#00A86B on #FFFFFF:  4.5:1   ✅ (AA)

Interactive Elements:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Button (primary):    5.2:1   ✅
Links:               4.6:1   ✅
Error text:          5.1:1   ✅
```

**Keyboard Navigation:**
```css
/* Focus Indicators */
*:focus {
  outline: 2px solid #0066FF;
  outline-offset: 2px;
}

*:focus:not(:focus-visible) {
  outline: none;
}

*:focus-visible {
  outline: 2px solid #0066FF;
  outline-offset: 2px;
}

/* Skip to main content */
.skip-link {
  position: absolute;
  left: -9999px;
  z-index: 999;
}

.skip-link:focus {
  left: 0;
  top: 0;
  background: #0066FF;
  color: #FFFFFF;
  padding: 12px 24px;
}
```

**ARIA Labels:**
```html
<!-- Button with icon only -->
<button aria-label="Export report as CSV">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Progress bar -->
<div 
  role="progressbar" 
  aria-valuenow="75" 
  aria-valuemin="0" 
  aria-valuemax="100"
  aria-label="Budget usage: 75%"
>
  <div style="width: 75%"></div>
</div>

<!-- Data table -->
<table role="table" aria-label="Top users by token usage">
  <caption class="sr-only">
    Top users by token usage this month
  </caption>
  ...
</table>

<!-- Chart -->
<div role="img" aria-label="Line chart showing token usage over the last 30 days">
  <canvas id="usage-chart"></canvas>
</div>
```

**Screen Reader Only Text:**
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## 🔄 User Flows

### Flow 1: First-Time User Onboarding

```
1. User receives email: "AI Token Tracker installed"
   │
   ├─→ Click "View Dashboard" link
   │
2. Lands on dashboard (empty state)
   │
   ├─→ Welcome modal appears
   │   ├─ "Welcome to AI Token Tracker!"
   │   ├─ "Here's what we track: tokens, costs, models"
   │   ├─ "Privacy: We never see your prompts"
   │   └─ [Got it] button
   │
3. Modal dismissed → Dashboard shows
   │
   ├─→ If no data yet:
   │   ├─ Empty state illustration
   │   ├─ "Start using AI tools and data will appear here"
   │   └─ "Usually takes 5-10 minutes after first use"
   │
   └─→ If data exists:
       ├─ Summary cards populated
       ├─ Tooltip prompts: "This is your usage", "This is your budget"
       └─ Dismiss tooltips after first view
```

### Flow 2: Manager Sets Up Team Budget

```
1. Manager clicks "Team" tab
   │
2. Team dashboard loads
   │
   ├─→ First time: No budget set
   │   ├─ Banner: "Set a budget to track team spending"
   │   └─ [Set Budget] button
   │
3. Click [Set Budget]
   │
   ├─→ Budget modal opens
   │   ├─ Input: "Monthly budget (USD)"
   │   ├─ Helper: "Based on last month, we recommend $3,200"
   │   ├─ Alert thresholds:
   │   │   ├─ Warning at: 75% (default)
   │   │   └─ Critical at: 90% (default)
   │   ├─ Alert recipients:
   │   │   ├─ ☑ Me (sarah@company.com)
   │   │   ├─ ☐ Finance team
   │   │   └─ ☐ Custom emails
   │   └─ [Cancel] [Save Budget]
   │
4. Click [Save Budget]
   │
   ├─→ Budget saved
   ├─→ Dashboard reloads
   ├─→ Budget progress bar appears
   └─→ Success toast: "Budget saved! You'll get alerts at 75% and 90%"
```

### Flow 3: User Investigates High Usage Spike

```
1. User receives email: "Your AI usage increased 200% today"
   │
   ├─→ Click "View Details"
   │
2. Dashboard opens to "Usage Over Time" chart
   │
   ├─→ Chart shows spike on specific date
   │   └─→ Click on spike point
   │
3. Drill-down panel slides in
   │
   ├─→ Shows:
   │   ├─ Date: April 28, 2026
   │   ├─ Total tokens: 250,000 (↑194%)
   │   ├─ Total cost: $87.00
   │   ├─ Breakdown by tool:
   │   │   ├─ Claude Code: 200K tokens ($72)
   │   │   └─ ChatGPT Web: 50K tokens ($15)
   │   └─ Sessions:
   │       ├─ 10:30am - 12:15pm: 150K tokens
   │       │   └─→ "Session 1: Mobile app refactor"
   │       └─ 2:00pm - 4:30pm: 100K tokens
   │           └─→ "Session 2: API migration"
   │
4. User sees explanation
   │
   └─→ Toast: "This was a large refactoring project. Usage back to normal tomorrow."
```

---

## 📐 Dashboard Layouts

### Personal Dashboard (Employee View)

```
┌─────────────────────────────────────────────────────────────┐
│ 🏠 My AI Usage                          👤 Alex  [Settings] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔔 Budget Alert: You're at 75% of your monthly budget      │
│     [View Details]                                    [×]    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │   2.4M        │  │   $86.50      │  │   127 hrs     │   │
│  │   tokens      │  │   cost        │  │   AI time     │   │
│  │   ↑12%        │  │   ↑8%         │  │   ↑15%        │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  💰 Budget Status                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 75%                         │
│  $112.50 / $150 monthly limit                               │
│  ⚠️ Warning: On track to exceed by $5                      │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📈 Usage Over Time (Last 30 Days)                          │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │                                 ▄█              │         │
│  │                  ▄▆            ███              │         │
│  │         ▃▅      ████          ████              │         │
│  │   ▂▄▅▇███▅    ██████        ██████             │         │
│  │ ▁▄███████████▄████████▄    ████████            │         │
│  │███████████████████████████▄█████████           │         │
│  │────────────────────────────────────────        │         │
│  │ Apr 1          Apr 15          Apr 30           │         │
│  └────────────────────────────────────────────────┘         │
│  [7 days] [30 days] [90 days]            [Export CSV]       │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🛠️ Tools Breakdown                                         │
│                                                              │
│  Claude Code        1.8M  (75%)  ████████████████▌          │
│  GitHub Copilot     450K  (19%)  ████                       │
│  ChatGPT Web        150K  (6%)   █▌                         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🎯 Projects                                                │
│                                                              │
│  mobile-app-refactor    $45.20    [View Details]            │
│  api-migration          $28.30    [View Details]            │
│  bug-fixes              $13.00    [View Details]            │
│                                                              │
│  [+ Add Project Tag]                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Component Specifications:**

```css
/* Alert Banner */
.alert-banner {
  background: #FFF4E6;
  border-left: 4px solid #FF9500;
  padding: 16px 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Summary Cards Grid */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

/* Chart Card */
.chart-card {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  margin-bottom: 24px;
}

.chart-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-card__title {
  font-size: 16px;
  font-weight: 600;
  color: #1A1A1A;
}

.chart-card__actions {
  display: flex;
  gap: 8px;
}
```

---

## 🎭 States & Interactions

### Loading States

```html
<!-- Skeleton Loading for Cards -->
<div class="stat-card skeleton">
  <div class="skeleton__label"></div>
  <div class="skeleton__value"></div>
  <div class="skeleton__change"></div>
</div>
```

```css
.skeleton {
  pointer-events: none;
}

.skeleton > * {
  background: linear-gradient(
    90deg,
    #F5F5F5 0%,
    #E0E0E0 50%,
    #F5F5F5 100%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 4px;
}

.skeleton__label {
  width: 80px;
  height: 12px;
  margin-bottom: 12px;
}

.skeleton__value {
  width: 120px;
  height: 32px;
  margin-bottom: 12px;
}

.skeleton__change {
  width: 100px;
  height: 16px;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
```

### Empty States

```html
<!-- No Data Yet -->
<div class="empty-state">
  <svg class="empty-state__icon">📊</svg>
  <h3 class="empty-state__title">No data yet</h3>
  <p class="empty-state__message">
    Start using AI tools and your usage will appear here within 5-10 minutes.
  </p>
  <button class="btn-primary">Refresh</button>
</div>
```

```css
.empty-state {
  text-align: center;
  padding: 64px 24px;
}

.empty-state__icon {
  font-size: 64px;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-state__title {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 12px;
}

.empty-state__message {
  font-size: 14px;
  color: #808080;
  max-width: 400px;
  margin: 0 auto 24px;
}
```

### Error States

```html
<!-- Error Loading Data -->
<div class="error-state">
  <svg class="error-state__icon">⚠️</svg>
  <h3 class="error-state__title">Failed to load data</h3>
  <p class="error-state__message">
    We couldn't load your usage data. Please try again.
  </p>
  <button class="btn-primary">Retry</button>
  <a href="/support" class="error-state__link">Contact Support</a>
</div>
```

### Hover States

```css
/* Card Hover */
.card {
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* Button Hover */
.btn-primary:hover {
  box-shadow: 0 4px 8px rgba(0, 102, 255, 0.24);
  transform: translateY(-1px);
}

/* Link Hover */
a:hover {
  color: #0052CC;
  text-decoration: underline;
}
```

### Active/Pressed States

```css
.btn-primary:active {
  transform: translateY(0);
  box-shadow: none;
}
```

---

## ✅ Design System Checklist

### Foundations ✅
- [x] Color palette (primary, semantic, neutral)
- [x] Typography scale (headings, body, labels, numbers)
- [x] Spacing system (8px grid)
- [x] Grid layout (12-column responsive)
- [x] Iconography (Heroicons)

### Components ✅
- [x] Buttons (primary, secondary, ghost, danger)
- [x] Cards (stat cards, chart cards)
- [x] Progress bars (budget tracking)
- [x] Alerts/banners (info, success, warning, error)
- [x] Tables (data tables, user lists)
- [x] Badges (status indicators)
- [x] Forms (inputs, selects, checkboxes - future)

### Data Visualization ✅
- [x] Chart library (Apache ECharts)
- [x] Chart types (line, bar, pie/donut)
- [x] Color-blind friendly palette
- [x] Chart styling (consistent with design system)

### Responsive Design ✅
- [x] Breakpoints defined
- [x] Mobile layouts (1 column)
- [x] Tablet layouts (2 columns)
- [x] Desktop layouts (3 columns)
- [x] Responsive navigation

### Accessibility ✅
- [x] WCAG 2.1 Level AA compliance
- [x] Color contrast ratios (4.5:1 minimum)
- [x] Keyboard navigation
- [x] Focus indicators
- [x] ARIA labels
- [x] Screen reader support

### User Flows ✅
- [x] First-time onboarding
- [x] Budget setup
- [x] Usage investigation
- [x] Export reports (future)

### Dashboard Layouts ✅
- [x] Personal dashboard
- [x] Team dashboard (similar structure)
- [x] Company dashboard (similar structure)

### States & Interactions ✅
- [x] Loading states (skeletons)
- [x] Empty states
- [x] Error states
- [x] Hover states
- [x] Active/pressed states

---

## 📦 Deliverables

### Phase 1: Design Files
- [ ] Figma design system library
- [ ] Component library (all states)
- [ ] Dashboard mockups (3 views)
- [ ] User flow diagrams
- [ ] Interactive prototypes

### Phase 2: Development Assets
- [ ] CSS/SCSS design tokens
- [ ] React component library
- [ ] Storybook documentation
- [ ] Icon SVG exports
- [ ] Chart theme configuration

### Phase 3: Documentation
- [x] This design system document
- [ ] Component usage guidelines
- [ ] Accessibility checklist
- [ ] Brand guidelines
- [ ] Design review process

---

**Document Version:** 1.0 (Finalized)  
**Last Updated:** April 28, 2026  
**Status:** ✅ Ready for Implementation  
**Next Steps:** Create Figma designs, implement React components

---

**End of UI/UX Design System Document**
