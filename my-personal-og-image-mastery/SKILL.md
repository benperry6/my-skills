---
name: my-personal-og-image-mastery
description: "[My Personal Skill] Complete guide for creating high-CTR Open Graph images combining technical specs AND marketing strategy. Covers both HOW to build og:images (dimensions, meta tags, safe zones, platforms) AND WHAT to put in them (copywriting, visual psychology, headline formulas, A/B testing). Use when: creating og:image, designing social sharing image, optimizing link preview, improving social CTR, writing og:image copy, reviewing og:image design, planning social card strategy. Triggers: og image, og:image, open graph, social sharing image, twitter card, link preview, social card, social preview, share image, meta image"
metadata:
  ownership: confirmed-personal
  provenance: "Built in-house from ChatGPT Deep Research dated 2026-03-04."
---

# OG Image Mastery

Confirmed personal skill. Source pack: ChatGPT Deep Research — 2026-03-04.

Create og:images that are technically correct AND psychologically optimized for clicks.

## Quick Reference

**Universal specs:** 1200 x 630 px, JPG (preferred) or PNG, under 5 MB, served over HTTPS as absolute URL.

**Format choice:** Prefer JPG at quality 80-85% over PNG — 3-5x lighter for images with gradients/photos, near-identical visual quality at this size. Use PNG only for flat-color/text-only designs. **Never use WebP** for og:image — not supported by Facebook, LinkedIn, and other major platforms.

**The formula:** One visual focal point + One clear promise + One brand cue = high-CTR preview.

**The mindset:** An og:image is a micro-landing page — it reduces uncertainty and creates enough motivation to interrupt scrolling. Design for high-fluency, high-trust thumbnails, not crowded ad creatives.

## Detailed References

- **Platform specs & rendering behavior:** See [references/platform-specs.md](references/platform-specs.md)
- **Visual psychology principles:** See [references/visual-psychology.md](references/visual-psychology.md)
- **Copy frameworks & hooks:** See [references/copy-frameworks.md](references/copy-frameworks.md)
- **Full Deep Research source:** See [references/deep-research-report.md](references/deep-research-report.md)

## Essential Meta Tags

```html
<!-- OG (Facebook, LinkedIn, Discord, Slack) -->
<meta property="og:title" content="Title (60 chars max)" />
<meta property="og:description" content="Description (155 chars max)" />
<meta property="og:image" content="https://yoursite.com/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:url" content="https://yoursite.com/page" />
<meta property="og:type" content="article" />

<!-- Twitter/X (always use large image) -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Title" />
<meta name="twitter:description" content="Description" />
<meta name="twitter:image" content="https://yoursite.com/og-image.png" />
```

## The Golden Layout

```
┌──────────────────────────────────────────────────┐
│  120px margin (safe zone)                        │
│  ┌──────────────────────────────────┐  ┌──────┐  │
│  │                                  │  │      │  │
│  │  Primary message (5-8 words)     │  │Brand │  │
│  │  48-64px, bold, high contrast    │  │ cue  │  │
│  │  ─────────────────────           │  │      │  │
│  │  Optional qualifier (20-28px)    │  └──────┘  │
│  │                                  │            │
│  └──────────────────────────────────┘            │
│  Safe content box: 960 x 504 px                  │
└──────────────────────────────────────────────────┘
  1200 x 630 px
```

## Design Principles (Marketing + Technical)

### What to put in the image

**Essential (always include):**
1. **One clear promise** — the "why click" in 1-2 seconds. Benefit, not feature. Simple words.
2. **One credibility cue** — brand mark, product UI screenshot, or page-specific image.

**Optional (only if it adds clarity):**
3. **A qualifier** — content format ("Guide", "Template"), audience, or timeframe.
4. **A micro-CTA** — label-style only ("Get the checklist"), never fake buttons.

**Never include:**
- Multiple competing claims or feature lists
- Dense text or full sentences
- Fake CTA buttons (triggers banner blindness)
- Generic stock photography
- Exclamation points

### Visual rules

| Rule | Why |
|------|-----|
| Dark backgrounds pop in light feeds | Contrast Effect — most feeds are white/light |
| One focal point only | Hick's Law — more options = slower decision = scroll past |
| High figure-ground contrast (WCAG AA 4.5:1) | Processing Fluency — easy to process = positive feeling |
| No text-heavy images | Apple/Google explicitly discourage; breaks at small sizes |
| Consistent template system across pages | Mere Exposure — familiarity breeds trust and recognition |
| Image must work WITHOUT text | iMessage/Google Discover constraint; also the baseline test |

### Copy rules

| Rule | Why |
|------|-----|
| Match og:image text to og:title keywords | Verbatim repetition > paraphrasing (field experiment evidence) |
| Simple, common words | Simpler writing = higher CTR (large-scale experiments) |
| Max 5-8 words on image | 1.5-second scan window; more = unreadable |
| Benefits > features | Outcome language ("Get X back") > mechanism ("AI-powered matching") |
| Forward reference for curiosity | Zeigarnik Effect creates open loop — click to resolve |

### The text-on-image decision

**Critical tension:** Apple/Google say no text. Social feeds benefit from text overlays.

**Resolution:** Design every image to pass TWO tests:
1. **Textless test:** Cover the text — does the image alone communicate value?
2. **Text reinforcement:** Does the text add clarity without being required?

If an image fails the textless test, redesign the visual first.

## Headline Formulas (Quick Ref)

| Formula | Example | Psychology |
|---------|---------|------------|
| Outcome + context | "Recover lost items faster" | Processing fluency |
| Pain → relief | "Lost your keys? Get them back." | Loss aversion |
| Forward reference | "This is why people return things" | Zeigarnik/curiosity |
| Numbers | "3 steps to get it back" | Numeric fluency |
| Question | "Tired of losing things?" | Self-referential processing |
| Negative frame | "Stop losing revenue to churn" | Loss aversion |

**More formulas and hooks:** See [references/copy-frameworks.md](references/copy-frameworks.md)

## By Use Case

| Use Case | Focal Point | Text Approach |
|----------|-------------|---------------|
| SaaS/product page | Product UI screenshot | Outcome promise + brand |
| Blog post | Topic-specific hero image | Curiosity hook + format label |
| Landing page | Match page visual | Verbatim repeat of page headline |
| E-commerce | Product photo | Minimal — product speaks |
| B2B | Editorial/clean design | Informational, not salesy |
| B2C | Authentic human emotion | Stronger emotional hook |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Same generic logo for every page | Page-specific image (Apple & Google require this) |
| Text too small to read | Min 48px title at 1200px width |
| Message mismatch (image vs title vs page) | Verbatim keyword alignment |
| Banner-ad aesthetic | Editorial design, no fake buttons |
| Ignoring platform caching | Use debug tools to refresh after changes |
| Light background disappears in feed | Dark or high-contrast background |
| Testing in isolation | Preview in mock feed (light + dark bg) |

## A/B Testing

**Method:** Create two share URLs (A/B) routing to the same content with different og:images. Don't just swap the image on one URL — platforms cache.

**What to test (one variable per test):**
- Face vs no face
- Text vs no text
- Benefit-led vs curiosity-led
- Dark vs light background

**Metrics:**
- Preview CTR (impressions → clicks)
- Qualified CTR (clicks → key on-site action)
- Share rate (re-shares after viewing)
- Bounce rate (mismatch proxy — high bounce = broken promise)

**Debug tools:** Facebook Debugger, Twitter Card Validator, LinkedIn Post Inspector, OpenGraph.xyz, Iframely

## Implementation: Next.js Dynamic OG Images

For Next.js projects, use `@vercel/og` (built into `next/og`) to generate OG images dynamically via an API route. This is the modern standard used by GitHub, PostHog, and Vercel.

**Why dynamic over static:**
- Solves the "same generic image for every page" anti-pattern
- One template, unique image per page (title, type, locale as params)
- No external design tool needed — code the design in JSX
- Rendered as optimized PNG/JPG on Vercel's edge

**Route pattern:** `/api/og?title=...&type=...&locale=...`

```tsx
// app/api/og/route.tsx
import { ImageResponse } from 'next/og';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') ?? 'Default Title';

  return new ImageResponse(
    (
      <div style={{
        width: 1200, height: 630,
        display: 'flex', alignItems: 'center',
        background: 'linear-gradient(135deg, #1a1a2e, #16213e)',
        padding: 60, fontFamily: 'system-ui', color: 'white',
      }}>
        <div style={{ flex: 1 }}>
          <h1 style={{ fontSize: 56, margin: 0, lineHeight: 1.2 }}>
            {title}
          </h1>
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

**Metadata integration:**
```tsx
// In layout.tsx or page.tsx
export const metadata = {
  openGraph: {
    images: [{
      url: '/api/og?title=Your+Page+Title&type=homepage',
      width: 1200, height: 630,
    }],
  },
};
```

**Compression notes:**
- `@vercel/og` outputs PNG by default — acceptable for text-heavy/flat designs
- For gradient/photo-heavy images: consider post-processing to JPG 80-85% quality
- Never use WebP — not universally supported for og:image across platforms
- Target < 100KB for instant loading; < 200KB is acceptable

## Production Checklist

### Strategy
- [ ] One primary promise matching page and og:title
- [ ] Promise uses simple, common words (no jargon)
- [ ] Promise is benefit/outcome, not feature
- [ ] One credibility cue (brand, UI, page-specific image)
- [ ] If curiosity hook: page resolves it within 5 seconds

### Design
- [ ] 1200 x 630 px, PNG or JPG, under 5 MB
- [ ] High figure-ground contrast (WCAG AA)
- [ ] Critical content inside safe area (120px sides, 63px top/bottom)
- [ ] Passes textless test (image works without text)
- [ ] No banner-ad tropes (fake buttons, stickers, stock photos)
- [ ] Dark or high-contrast background for feed visibility
- [ ] Consistent with brand template system

### Copy
- [ ] Max 5-8 words on image
- [ ] og:image text aligned with og:title keywords
- [ ] og:title < 60 chars, og:description < 155 chars
- [ ] No message mismatch between image, title, and page

### Technical
- [ ] Absolute HTTPS URL for og:image
- [ ] og:image:width and og:image:height set
- [ ] twitter:card set to summary_large_image
- [ ] All required meta tags present (og:title, og:description, og:image, og:url)

### Platform Validation
- [ ] Facebook Debugger — preview correct
- [ ] Twitter Card Validator — large image renders
- [ ] LinkedIn Post Inspector — not cached with old image
- [ ] Tested in mock feed (light bg + dark bg)
- [ ] Thumb test: image communicates without readable text (iMessage/WhatsApp)
