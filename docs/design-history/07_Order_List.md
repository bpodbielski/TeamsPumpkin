# 07 — Order List (live prices, checked 2026-09-23)

Every price below was read off the vendor's page today. Amazon prices move daily — treat them as "what it cost when I looked," not a quote. ASINs are given so you land on the exact listing.

**Totals:** Adafruit **$33.31 (ordered)** · Amazon **$74.43 + tax** · Lowe's **$19.98 + tax** · FedEx **≈$5** → **≈$139** all-in with tax.

## Cart review — 2026-09-23 (validated against the screenshot before ordering)

All six items match the picks. One blocker, one caveat:

| Item in cart | Verdict |
|---|---|
| GOCHANGE 4-in-1 hot wire foam cutter, $32.99 | ✅ Correct ASIN. Confirmed contents: 12 cm & 7 cm wand hot knives, 5 cm bending knife, 18 cm bow, spare wire, holder. Wands hit 280 °C in 20 s (max 350 °C) — plenty for craft-pumpkin foam. |
| Anker USB-A→C 2-pack 6 ft, $9.99 | ✅ Correct. |
| **TRISTEAFF 5 V 3 A charger, $5.99** | ⛔ **Delivery Oct 8–10 — after the Oct 3–4 build weekend.** Swap it (below). |
| ELEGOO 120 pc jumpers, 8 in, $6.98 | ✅ Correct — 8 in = 20 cm, and the kit has the F-F and M-F types the wiring needs. |
| HiLetgo 3× HC-SR501 PIR, $8.49 | ✅ Correct. |
| BTF-LIGHTING WS2812B 5 V 1 m 60 LED IP30 black PCB, $8.99 | ✅ Correct — 5 V (not 12 V), 60 px/m, addressable. |

**Cart total: $73.43** before tax.

### Blocker: swap the wall charger
Replacements that were in stock on 2026-09-23 (verify the date in *your* cart — Amazon quotes per account):
- **Besgoods 5 V/3 A 18 W single** — `B07XPW9JVQ` — $9.99, 4.6★, in stock, next-day with Prime.
- **QC3.0 18 W 3 A USB-A** — `B094J4L3QR` — $6.99, 4.5★, in stock, next-day with Prime.
- **OKRAY 2-pack 18 W 5 V/3 A** — `B07QKC56M6` — $9.99, 4.6★ (spare included).

"Quick Charge 3.0" branding is fine here: QC chargers sit at 5 V unless a device negotiates higher over D+/D−, and this board never does.

**Or skip the purchase for now:** the board runs from any USB-A charger. Anything rated **5 V / 2.4 A or better** (a typical iPad brick) covers the ~2.0 A peak, so if one is already in a drawer, use it for the bench and the porch, and delete the charger from the cart.

### Caveat: hot-knife fumes and foam type
The GOCHANGE listing says it suits low-density foams (EPS, EPP, sponge) and **not** high-density boards (XPS, extruded). Craft pumpkins are moulded polyurethane — SKS Props cut this exact Lowe's pumpkin with a hot knife and it went easily, so this is proven in practice. Two notes:
- **Burning polyurethane is nastier than polystyrene.** Respirator on, garage door open, fan running — not optional, and not indoors.
- If the foam drags or gums the tip, let it preheat 20–25 s and slow down; keep a sharp craft knife as the fallback.

## Second-pass review — 2026-09-23 (revised cart, system-level check)

Charger swapped to `B094J4L3QR` (QC3.0 18 W 5 V/3 A, $6.99, arriving **Sun Sep 27** — ahead of the build weekend). **Cart total $74.43** pre-tax. Revised all-in ≈ **$139**.

### Every item re-checked against what the build actually needs
| Item | Electrically / mechanically correct? |
|---|---|
| QC3.0 18 W 5 V/3 A USB-A charger | ✅ 18 W QC bricks are rated 5 V/3 A and sit at 5 V unless a device negotiates higher over D+/D−; this board never does. Peak draw ≈ 2.0 A → ~1 A of headroom. |
| GOCHANGE 4-in-1 foam cutter | ✅ Ships 12 cm & 7 cm wand knives + a 5 cm bending knife; wands reach 280 °C in 20 s (max 350 °C) — well past polyurethane's melting point. |
| Anker USB-A→C 6 ft ×2 | ✅ Correct type (USB-A source, not PD). Watch for voltage drop: see bench check below. |
| ELEGOO jumpers, 8 in (20 cm) | ✅ Has F-F and M-F. 20 cm reaches from the board on the floor to the PIR at the front face of a 13" pumpkin; chain two if it's tight (you'll have 120). |
| HiLetgo HC-SR501 ×3 | ✅ 4.5–20 V in / 3.3 V out — safe on the 5 V servo header and on a 3.3 V GPIO. If a clone lacks the H/L jumper, the firmware still re-pings (it re-checks the level after each cooldown); the timing just gets less regular. |
| BTF-LIGHTING WS2812B 60 LED 5 V IP30 | ✅ 5 V, addressable, black PCB. **Must be cut to 30 px — see 04_Wiring "Before you wire".** IP30 is unsealed: fine on a covered porch, but if you see condensation inside the pumpkin in late October, that's the part to check. |

### Two build details this cart surfaced (now written into 04_Wiring.md)
1. **Cut the strip to 30 pixels and keep the half with the input connector.** Wiring all 60 at 70 % brightness draws ≈ 2.5 A for the LEDs alone and blows the power budget. The strip's included 3-pin pigtail means the connection needs no soldering.
2. **The Adafruit speaker's leads are only ~9 cm.** Mount the board within a few inches of the speaker port at the base, or plan to splice an extension.

### Not in any cart — confirm you have these
✅ **Ben confirmed 2026-09-23 that he has all of these** — respirator, ~2 mm flat-blade screwdriver, hot glue gun, paper for the diffuser, extension cord, a box for the board. Nothing further to buy.

### Add to the bench test
**Check the white is actually white.** 6 ft of USB cable at ~2 A drops some voltage; if the flash looks pink or dim, use the shorter Anker cable from the 2-pack or drop `NOTIFY_BRIGHTNESS`. That's why the 2-pack is the right buy.

## Order status
| Cart | Status | Reference |
|---|---|---|
| Adafruit | ✅ **Placed 2026-09-23 — Processing** | Order placed · $24.90 + $6.23 shipping + $2.18 tax = **$33.31** · USPS Ground Advantage, 2–5 business days after it ships (1–2 business days to ship) → expect **~Sep 26–Oct 2** |
| Amazon | ✅ **Placed 2026-09-23** | $74.43 pre-tax · strip/jumpers/cable/cutter overnight (Sep 24), PIR Sep 24, charger Sun Sep 27 |
| Lowe's | ⬜ To buy in person | Item 10 |
| FedEx | ⬜ After measuring the pumpkin face | Item 11 |

---

## Cart 1 — Adafruit (order first; 1–2 business days to ship)

✅ **PLACED 2026-09-23 — Processing.**

| # | Item | PID | Price | Ordered |
|---|---|---|---|---|
| 1 | RP2040 Prop-Maker Feather with I2S Audio Amplifier | 5768 | $19.95 | ✅ qty 1 |
| 2 | Speaker — 40 mm Diameter — 4 Ω 5 W | 3968 | $4.95 | ✅ qty 1 |

Subtotal $24.90 · USPS Ground Advantage **$6.23** · tax $2.18 · **total $33.31**.

> Shipping came in at $6.23, not the ~$1.44 I estimated from the "low cost service" wording on Adafruit's shipping page — their Ground Advantage rate for a small package is higher than that. Budget ~$6 for shipping on any future Adafruit order.

> **Do not buy the rest at Adafruit.** I checked: their PIR (PID 189, $9.95), NeoPixel strips (2508 $14.95 / 1461 $54.95) and F/F jumpers (266, $3.95) are **all out of stock today**, and the ones in stock cost more than the Amazon equivalents anyway.

---

## Cart 2 — Amazon

| # | Item | Pick (ASIN) | Price | Rating | Why this one |
|---|---|---|---|---|---|
| 3 | **WS2812B LED strip, 5 V, 60 LED/m, 1 m, IP30** | BTF-LIGHTING, UL listed — `B01CDTED80` | **$8.99** | 4.6★ | BTF-Lighting is the reliable name in WS2812B; UL-listed; exactly 60 px/m so ~30 px is a half-metre cut. Cheaper alt: `B088BRY2SH` $7.99 (4.4★, same maker). |
| 4 | **HC-SR501 PIR motion sensor** | HiLetgo 3-pack — `B07KZW86YR` | **$8.49** | 4.4★ | Amazon "Overall Pick"; HiLetgo is a known brand; 3 spares for a $2 part. Cheapest: `B0GL8BZDDN` 2-pack $6.79 (4.8★ but few reviews). |
| 5 | **Dupont jumper wires** (M-F, F-F, M-M) | ELEGOO 120 pc — `B01EV70C78` | **$6.98** | 4.8★ | You need 2× F-F and 1× M-F; this kit has all three types at 20 cm. |
| 6 | **5 V / 3 A USB-A wall charger** | `B0FJF1YXZH` 18 W | **$5.99** | 4.8★ | Single USB-A port, 5 V/3 A. **Buy USB-A, not USB-C PD** — a PD brick may not settle on 5 V for this board. UL-listed alt: `B07QK7RSX1` $9.99 (4.6★). |
| 7 | **USB-A → USB-C cable, 6 ft** | Anker 2-pack — `B07DC5PPFV` | **$9.99** | 4.7★ | Anker quality matters here: thin cable = voltage drop = pink-tinted "white" on the strip. Two cables, one spare. |
| 8 | **Hot knife / foam cutter** | GOCHANGE 4-in-1 hot wire foam cutter, 18 W — `B092S6WZ35` | **$32.99** | 4.4★ | Purpose-built for foam; includes a hot **knife blade** plus a bow cutter and engraving tips. In stock. |
| 8-alt | Cheaper: Weller 15-pc woodburning kit, 25 W — `B0962VD8DH` | | $22.98 | 4.4★ | Real brand, stay-cool handle, quick tip change; the knife tip does the same job. Pick this to save $10. |
| 9 | *(optional)* **Laser transparency film, 20 sheets** | Koala — `B07KP1G6DV` | $8.99 | 4.6★ | **Only if you print the insert yourself — and only "laser" film.** Inkjet film can melt onto a laser fuser. See the print note below. |

Amazon subtotal: **$73.43** with the GOCHANGE cutter, no film · **$82.42** adding the film · **$63.42** with the Weller instead of the GOCHANGE. Prime = free shipping.

> **Correction (2026-09-23):** an earlier version of this file mislabeled these subtotals and I quoted "≈$63" in chat — that figure is the *Weller* build. The cart as picked (GOCHANGE cutter) is **$73.43** before tax. Revised all-in: **≈$135–140** with tax.

> **Walnut Hollow note:** the specific Walnut Hollow Hot Knife from the SKS Props video is no longer listed on Amazon (the brand's tools have largely disappeared from the catalog). The two picks above are the current equivalents — any ~20–30 W tool with a knife-shaped tip cuts this foam the same way.

---

## Cart 3 — Lowe's (in store or pickup)

| # | Item | Price | Details |
|---|---|---|---|
| 10 | **Holiday Living 13-in Carvable Pumpkin, glossy orange** | **$19.98** | Item #5257093 / Model #227116 · 4.9★ (31) · "500+ bought last week" · free store pickup · https://www.lowes.com/pd/Holiday-Living-12-8-in-Pumpkin-Craft-Pumpkin/5014043077 |

Buy it in person if you can — pick one with **no dents or tears** and the **widest flat face** between the seams (the logo needs ~125 mm of it). Also sold in 7.5-in and in white/black; you want the 13-in orange. Michaels/Hobby Lobby carry equivalents if Lowe's is out.

---

## Cart 4 — FedEx Office (print the color insert)

| # | Item | Est. price |
|---|---|---|
| 11 | **Page 1** of `assets/print_template.html` — **color prints: 2 copies on white cardstock/heavy paper, 1 on plain paper** | ≈$3–5 |

Save page 1 as PDF from the browser's print dialog and email it or bring it on a USB stick. **Tell them "print at 100 %, do not fit to page"** and check the 100 mm scale bar with a ruler before you leave.

### The printing decision (why not transparency at FedEx)
Your home printer is **B&W laser**, so the color insert has to be printed somewhere else. Two routes:
- **Recommended — plain/cardstock color prints at FedEx, two stacked.** No special media, works at any location, costs a few dollars. Two stacked prints double the ink density and give you saturated purple when backlit.
- **Transparency.** Better contrast, but FedEx self-serve machines are laser and generally will not take customer-supplied film, and *inkjet* film in a laser printer is a fuser-damaging mistake. Only worth it if you want to run **laser** film (item 9) through your own machine — which is B&W, so it'd only work for a black mask, not the color logo.

Decide after the backlight test in Phase 2: print all three versions, hold a flashlight behind each in the dark, pick the winner.

---

## Your home laser (free)
**Pages 2 and 3** of `assets/print_template.html` — the black cut silhouette and the full-size face layout. B&W is all they need.

---

## Order sequence
1. **Today:** Adafruit (slowest), then Amazon.
2. **This week:** Lowe's pumpkin in person.
3. ✅ **Face measured 2026-10-13: 178 × 203 mm → logo width 125 mm, template updated.** FedEx prints can go in now.
4. **Verify:** the porch outlet.
