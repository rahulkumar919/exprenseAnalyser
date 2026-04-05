# 🎨 Expense Analyser Pro - Design System

## Design Philosophy
A modern, clean, and professional expense tracking interface inspired by contemporary fintech applications. The design emphasizes clarity, hierarchy, and smooth interactions.

---

## Color Palette

### Dark Theme (Default)
```css
Background Primary:   #0f1419  /* Main background */
Background Secondary: #1a1f2e  /* Elevated surfaces */
Background Card:      #1e2433  /* Card backgrounds */

Text Primary:         #ffffff  /* Headings, important text */
Text Secondary:       #8b92a8  /* Body text, labels */
Text Muted:           #5a6175  /* Subtle text, placeholders */

Accent Primary:       #7c3aed  /* Primary actions, links */
Accent Secondary:     #a78bfa  /* Hover states, highlights */

Success:              #10b981  /* Positive actions */
Warning:              #f59e0b  /* Alerts, cautions */
Danger:               #ef4444  /* Errors, deletions */
Info:                 #3b82f6  /* Information */
```

### Light Theme
```css
Background Primary:   #f8fafc
Background Secondary: #f1f5f9
Background Card:      #ffffff

Text Primary:         #1e293b
Text Secondary:       #64748b
Text Muted:           #94a3b8

Accent Primary:       #7c3aed
Accent Secondary:     #a78bfa
```

---

## Typography

### Font Families
- **Primary**: Poppins (300, 400, 500, 600, 700)
- **Monospace**: JetBrains Mono (for numbers, amounts, code)

### Type Scale
```
Hero Title:     clamp(2.5rem, 6vw, 4rem)     | 700 weight
Section Title:  2rem                          | 600 weight
Card Title:     1.25rem                       | 600 weight
Body Large:     1rem                          | 400 weight
Body:           0.9375rem                     | 400 weight
Body Small:     0.875rem                      | 400 weight
Caption:        0.8125rem                     | 400 weight
Label:          0.75rem                       | 500 weight
Tiny:           0.6875rem                     | 500 weight
```

### Letter Spacing
- Headings: -0.02em (tighter)
- Labels: 0.05em (wider, uppercase)
- Body: normal

---

## Spacing System

```css
--spacing-xs:  0.5rem   (8px)
--spacing-sm:  1rem     (16px)
--spacing-md:  1.5rem   (24px)
--spacing-lg:  2rem     (32px)
--spacing-xl:  3rem     (48px)
```

---

## Border Radius

```css
--border-radius-sm:  12px  /* Inputs, small cards */
--border-radius-md:  16px  /* Standard cards */
--border-radius-lg:  24px  /* Large cards, modals */
--border-radius-full: 50px  /* Pills, buttons */
```

---

## Shadows

```css
Card Shadow:        0 4px 20px rgba(0, 0, 0, 0.4)
Card Hover:         0 12px 40px rgba(0, 0, 0, 0.3)
Button Shadow:      0 8px 20px rgba(124, 58, 237, 0.4)
Button Hover:       0 15px 35px rgba(124, 58, 237, 0.6)
```

---

## Components

### Stat Cards
- **Size**: 260px minimum width, auto-fit grid
- **Padding**: 1.5rem (24px)
- **Border**: 1px solid glass-border
- **Top Accent**: 2px gradient line on hover
- **Hover**: Lift 4px, enhanced shadow

### Buttons

#### Primary Button
- **Background**: Linear gradient (#7c3aed → #a78bfa)
- **Padding**: 1rem 2.5rem
- **Border Radius**: 50px (pill shape)
- **Font Weight**: 600
- **Hover**: Lift 3px, ripple effect
- **Shadow**: Glowing purple shadow

#### Secondary Button (OCR, Actions)
- **Background**: Transparent with accent border
- **Border**: 2px solid accent-primary
- **Padding**: 0.625rem 1.25rem
- **Border Radius**: 12px
- **Hover**: Fill with gradient, lift 3px

#### Icon Button (Logout, Theme)
- **Size**: 40px × 40px
- **Border Radius**: 10px
- **Background**: Transparent with subtle color
- **Hover**: Scale 1.1, fill with color

### Form Inputs
- **Height**: Auto (padding-based)
- **Padding**: 0.875rem 1rem
- **Border**: 2px solid glass-border
- **Border Radius**: 12px
- **Font Size**: 0.9375rem
- **Focus**: 
  - Border color: accent-primary
  - Shadow: 0 0 0 3px rgba(124, 58, 237, 0.1)
  - Lift: 2px

### Progress Bars
- **Height**: 4px
- **Background**: rgba(255, 255, 255, 0.04)
- **Fill**: Gradient with glow
- **Animation**: 1s cubic-bezier ease

### Tables
- **Row Padding**: 1rem
- **Border**: 1px solid glass-border (bottom only)
- **Hover**: Background rgba(124, 58, 237, 0.05)
- **Font**: 0.9rem for data

---

## Layout Structure

### Container Widths
- **Max Width**: 1400px
- **Padding**: 1.5rem (responsive)

### Grid Systems

#### Stats Grid
```css
grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
gap: 1.5rem;
```

#### Charts Grid
```css
grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
gap: 1.5rem;
```

#### Management Section
```css
grid-template-columns: 380px 1fr;
gap: 2rem;
/* Stacks on mobile */
```

---

## Animations

### Timing Functions
- **Standard**: cubic-bezier(0.4, 0, 0.2, 1)
- **Decelerate**: cubic-bezier(0, 0, 0.2, 1)
- **Accelerate**: cubic-bezier(0.4, 0, 1, 1)
- **Sharp**: cubic-bezier(0.4, 0, 0.6, 1)

### Durations
- **Fast**: 150ms (micro-interactions)
- **Normal**: 300ms (standard transitions)
- **Slow**: 500ms (complex animations)

### Key Animations
- **Fade In**: opacity 0 → 1
- **Slide Up**: translateY(40px) → 0
- **Slide Down**: translateY(-20px) → 0
- **Scale**: scale(0.95) → 1
- **Lift**: translateY(0) → translateY(-4px)

---

## Glassmorphism

```css
background: rgba(30, 36, 51, 0.8);
backdrop-filter: blur(20px) saturate(180%);
border: 1px solid rgba(255, 255, 255, 0.06);
```

---

## Accessibility

### Focus States
- **Outline**: 2px solid accent-primary
- **Offset**: 2px
- **Visible**: Only on keyboard navigation

### Color Contrast
- Text on dark: WCAG AAA compliant
- Interactive elements: Minimum 3:1 contrast

### Motion
- Respects `prefers-reduced-motion`
- Smooth scroll behavior

---

## Responsive Breakpoints

```css
Mobile:     < 768px
Tablet:     768px - 1024px
Desktop:    1024px - 1440px
Large:      > 1440px
```

### Mobile Adaptations
- Single column layouts
- Stacked navigation
- Larger touch targets (min 44px)
- Simplified animations

---

## Icons
- **Library**: Font Awesome 6.4.0
- **Style**: Solid (primary), Regular (secondary)
- **Size**: 1rem - 2.5rem (context-dependent)

---

## Best Practices

1. **Consistency**: Use design tokens (CSS variables)
2. **Hierarchy**: Clear visual weight differences
3. **Whitespace**: Generous padding and margins
4. **Feedback**: Immediate visual response to interactions
5. **Performance**: Hardware-accelerated animations
6. **Accessibility**: Keyboard navigation, screen readers
7. **Responsiveness**: Mobile-first approach

---

## Implementation Notes

### CSS Architecture
- CSS Variables for theming
- BEM-like naming convention
- Component-based organization
- Utility classes for common patterns

### Performance
- `will-change` for animated elements
- `transform` and `opacity` for animations
- Debounced scroll events
- Lazy loading for images

---

## Future Enhancements
- [ ] Dark/Light theme toggle animation
- [ ] Skeleton loading states
- [ ] Micro-interactions on data updates
- [ ] Confetti on savings milestones
- [ ] Chart animations on load
- [ ] Toast notification system
- [ ] Modal/Dialog components
- [ ] Dropdown menus
- [ ] Date picker styling
- [ ] Empty states illustrations

---

**Version**: 2.0  
**Last Updated**: 2024  
**Designer**: AI UI/UX Specialist
