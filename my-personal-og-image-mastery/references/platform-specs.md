# Platform Specifications & Behavior

Technical specs and rendering behavior for each platform. Use this reference when optimizing OG images for specific channels.

## Table of Contents
- Universal Specs
- Facebook
- Twitter/X
- LinkedIn
- Discord
- Slack
- iMessage
- WhatsApp
- Telegram
- Google Discover
- Cross-Platform Tension: Text on Images

---

## Universal Specs

**Safe bet for all platforms:** 1200 x 630 px, JPG (preferred) or PNG, under 5 MB.

**Format warning: NEVER use WebP for og:image.** Only Twitter/X explicitly supports it. Facebook, LinkedIn, Slack, iMessage document only JPG/PNG. A WebP og:image that doesn't render = worse than no image.

**Compression target:** < 100KB ideal, < 200KB acceptable. JPG at quality 80-85% is 3-5x lighter than PNG for gradient/photo images with near-identical visual quality.

| Platform | Dimensions | Aspect Ratio | File Size | Format |
|----------|-----------|--------------|-----------|--------|
| Facebook | 1200 x 630 px | 1.91:1 | < 8 MB | JPG, PNG |
| Twitter/X (large) | 1200 x 628 px | 1.91:1 | < 5 MB | JPG, PNG, WEBP, GIF |
| Twitter/X (summary) | 800 x 418 px | 1.91:1 | < 5 MB | JPG, PNG |
| LinkedIn | 1200 x 627 px | 1.91:1 | < 5 MB | JPG, PNG |
| Discord | 1200 x 630 px | 1.91:1 | < 8 MB | JPG, PNG |
| Slack | 1200 x 630 px | 1.91:1 | — | JPG, PNG |
| iMessage | 1200 x 630 px | 1.91:1 | — | JPG, PNG |

---

## Facebook

- Uses Open Graph protocol (the original OG standard)
- OG image is the dominant visual cue in feed shares
- White/light feed background — dark OG images pop
- Supports og:image:width and og:image:height for faster rendering

**Debug tool:** [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)

**Design priorities:** Clarity, authenticity, avoid stock imagery

---

## Twitter/X

- Supports both `twitter:card` and `og:` fallback
- `summary_large_image` → full-width image (much more real estate, always prefer)
- `summary` → small thumbnail on the left
- Dark mode is very common — test both light and dark backgrounds

**Meta tags:**
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Title here" />
<meta name="twitter:description" content="Description" />
<meta name="twitter:image" content="https://yoursite.com/og-image.png" />
```

**Debug tool:** [Twitter Card Validator](https://cards-dev.twitter.com/validator)

**Design priorities:** High contrast, readable at both light/dark mode, test large card crop

---

## LinkedIn

- Uses OG metadata
- Small images can display as thumbnails (not just large cards)
- Square/vertical images might be cropped when shared organically
- Caches previews aggressively — must use Post Inspector to refresh
- Professional context — trust cues and scannability matter more

**Debug tool:** [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

**Design priorities:** Professional, scannable, readable even as thumbnail, avoid tiny typography

---

## Discord

- Uses Twitter and OG metadata to generate embeds
- Custom handling for some domains (YouTube, Twitter, etc.)
- Chat context = high-speed, skeptical environment
- Embeds appear inline in conversation

**Design priorities:** Clarity wins, avoid ad-like design, trust signals matter

---

## Slack

- "Classic link unfurling" crawls OG and Twitter Card metadata
- Renders a "micro-approximation" of the content
- Professional conversation context
- Previews appear inline in channels/DMs

**Design priorities:** Trust cues, specificity, professional appearance

---

## iMessage

**Critical constraints (Apple's official guidance):**
- Rich links appear "at many sizes, across many devices"
- **"Text in an image will not scale well"** — Apple explicitly warns against text in OG images
- Must use og:image for "interesting images specific to the page"
- Generic fallback images (logos) are explicitly discouraged
- Avoid duplicating the site name in og:title (domain is shown automatically)

**Design priorities:** Image must work with NO readable text. Strong photography, clear iconography, or product UI screenshots. The image alone must communicate value.

---

## WhatsApp

- Uses Open Graph tags including og:image
- Trust-sensitive context ("friend sent this")
- Shares often happen in private/group conversations
- Clickbait framing is particularly harmful here (breaks trust in personal context)

**Design priorities:** Authenticity, no clickbait, clear indication of what the link contains

---

## Telegram

- Generates link previews after URL paste
- Uses og:image, og:title, og:description
- Messaging-first surface similar to Slack/Discord

**Cache refresh:** Use [Telegram Webpage Bot](https://t.me/webpagebot)

**Design priorities:** Legibility, non-spam signals, works at small preview size

---

## Google Discover

- Explicitly discourages text in og:image
- Discourages generic images like site logos
- Prefers large, high-quality images specific to the content
- Minimum recommended width: 1200px

**Design priorities:** High-quality, page-specific imagery, no text overlays, no logos as primary image

---

## Cross-Platform Tension: Text on Images

This is the most important design decision.

**Against text (Apple, Google):**
- Apple: "Images should not include text" (iMessage rich links)
- Google Discover: avoid text in og:image
- Text doesn't scale across device sizes

**For text (social feeds):**
- Text overlays can increase CTR on Facebook, LinkedIn, Twitter/X
- A clear promise in the image helps when platforms show images prominently

**Resolution — design for two modes:**

1. **Textless comprehension:** The image alone signals topic/value (photo, product UI, iconography). This is the baseline — every OG image must pass this test.

2. **Text-optional reinforcement:** If text is added, keep it extremely short, high-contrast, and non-essential. It should improve performance on social feeds without being required for comprehension on messaging platforms.

**Practical approach:**
- Primary focal point: always visual (not text)
- If adding text: max 1 short line (5-8 words), large enough to read at 50% scale
- Test: cover the text with your thumb — does the image still communicate?

---

## Safe Area for All Platforms

Because platforms crop differently, use a 10% margin:

```
1200 x 630 canvas:
- Left/right margin: 120 px
- Top/bottom margin: 63 px
- Safe content box: 960 x 504 px
```

The skill's technical source also recommends 40px minimum padding from all edges. For maximum safety, use the larger value (120px sides is more conservative and recommended).

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌──────────────────────────────────────────────┐│
│  │ 120px side / 63px top-bottom margin          ││
│  │                                              ││
│  │  All critical content stays here             ││
│  │                                              ││
│  │                                              ││
│  └──────────────────────────────────────────────┘│
│                                                  │
└──────────────────────────────────────────────────┘
```
