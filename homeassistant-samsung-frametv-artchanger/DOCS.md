# Samsung Frame TV Art Changer

This Home Assistant OS/Green app downloads artwork, sends it to a Samsung Frame
TV, and stops after one successful run. It supports:

- an atomic dashboard preview at `/media/frame/latest.jpg`;
- persistent duplicate prevention in `/media/frame/uploaded_files.json`;
- Google Arts & Culture filters for color, museum, and style/period;
- a landscape-only Google Art filter enabled by default;
- exact Google-side combinations for museum plus style;
- progressive, compact catalog caching in the app's private `/data` directory.

The app downloads and sends only one artwork per run. Its one-shot startup mode
is intentional: a Home Assistant script starts it whenever a new work is wanted.

By default, **Preserve complete artwork** is enabled. Images that are not 16:9
are centered on a black 16:9 canvas, so no part of the artwork is cropped. Turn
the option off only if you prefer the older edge-to-edge center crop.

By default, **Landscape artworks only** is also enabled for Google Art. The app
checks a small preview before the high-resolution download and skips portrait
and square works. Detected orientations are cached in `/data` without storing
the preview image. Disable the option if you want every orientation to remain
eligible.

Enable **Borderless TV format only** to accept only landscape Google Art close
enough to 16:9 that filling the screen removes no more than about 5% from each
affected edge. The accepted work is then fitted to exactly 3840x2160 without
black borders. If no such work is found within 30 new dimension checks or 60
seconds, the app falls back to a landscape work on a black 16:9 canvas when
both **Preserve complete artwork** and **Landscape artworks only** are enabled.
If even that fallback is unavailable, the app stops cleanly and leaves the
current TV image unchanged. The stricter option is disabled by default because
truly exact 16:9 museum works are rare.

## Installation

1. Add `https://github.com/oliverwehrens/homeassistant-samsung-the-frame-art-changer` to the Home
   Assistant app store repositories.
2. Install **Samsung The Frame - Art Changer**.
3. Enter the TV IP address in the app configuration.
4. Start the app manually or from a Home Assistant script/automation whenever a
   new work is wanted.

The app itself needs no `configuration.yaml` change. The dashboard resolves the preview
through Home Assistant's built-in media source.

## Home Assistant package

[`samsung-the-frame.yaml`](samsung-the-frame.yaml) contains everything this
page describes except the dashboard card: the three filter helpers, the
`script.samsung_frame_neues_google_art` start script, and an automation that
loads a new work daily at 23:00.

1. Copy `samsung-the-frame.yaml` into your Home Assistant config folder (next to
   `configuration.yaml`).
2. Add it as a package in `configuration.yaml`. If a `homeassistant:` section
   already exists, add only the `packages:` part to it:

   ```yaml
   homeassistant:
     packages:
       samsung_the_frame: !include samsung-the-frame.yaml
   ```

3. Check the app slug in the script. It assumes the app was installed from
   this repository (`9c41c859_hass-frametv-artchanger`). Otherwise copy the
   slug from the URL of the app page (`/hassio/addon/<slug>`).
4. Adjust or remove the automation time if you want.
5. Go to **Developer tools → YAML**, run **Check configuration**, then restart
   Home Assistant.

Entities defined in a package are read-only in the UI; edit the file instead.
Remove any helpers or scripts with the same entity IDs that you created in the
UI before, otherwise Home Assistant reports duplicates.

## Filter helpers

The filters can be set in two ways:

- **Fixed values**: set `google_color`, `google_museum` and `google_style` in
  the app configuration (`ANY` means no restriction) and leave the three
  `*_entity` options empty.
- **Helpers**: create three dropdown helpers that you change from a dashboard.
  The app reads them on every start. A helper value wins over the fixed value;
  if a helper is missing or unreadable, the app logs a warning and uses the
  fixed value.

Create the helpers in **Settings → Devices & services → Helpers → Create
helper → Dropdown**, or in `configuration.yaml`:

```yaml
input_select:
  samsung_frame_farbe:
    name: Frame Farbe
    options: [Alle Farben, Blau, Grün, Rot, Orange, Gelb, Violett, Rosa, Türkis, Grau]
  samsung_frame_museum:
    name: Frame Museum
    options: [Alle Museen, MoMA, Musée d'Orsay, Van Gogh Museum, Metropolitan Museum, Rijksmuseum, National Gallery London, Tate Britain]
  samsung_frame_stil:
    name: Frame Stil
    options: [Alle Stile / Epochen, Moderne Kunst, Zeitgenössische Kunst, Impressionismus, Post-Impressionismus, Expressionismus, Abstrakter Expressionismus, Surrealismus, Pop Art, Renaissance, Barock, Romantik, Realismus]
```

English values work as well (e.g. `ANY`, `Blue`, `Modern Art`,
`Impressionism`). Unknown values log a warning and mean no restriction. If you
use other entity IDs, set them in `google_color_entity`,
`google_museum_entity` and `google_style_entity`.

The default entity IDs and options are:

### `input_select.samsung_frame_farbe`

- Alle Farben
- Blau
- Grün
- Rot
- Orange
- Gelb
- Violett
- Rosa
- Türkis
- Grau

### `input_select.samsung_frame_museum`

- Alle Museen
- MoMA
- Musée d’Orsay
- Van Gogh Museum
- Metropolitan Museum
- Rijksmuseum
- National Gallery London
- Tate Britain

### `input_select.samsung_frame_stil`

- Alle Stile / Epochen
- Moderne Kunst
- Zeitgenössische Kunst
- Impressionismus
- Post-Impressionismus
- Expressionismus
- Abstrakter Expressionismus
- Surrealismus
- Pop Art
- Renaissance
- Barock
- Romantik
- Realismus

The corresponding app options are:

```yaml
google_color: ANY
google_color_entity: input_select.samsung_frame_farbe
google_museum: ANY
google_museum_entity: input_select.samsung_frame_museum
google_style: ANY
google_style_entity: input_select.samsung_frame_stil
google_landscape_only: true
google_tv_format_only: false
```

If a helper is unavailable, its `ANY` fallback means no restriction for that
dimension.

## How filtering works

With only a color selected, the app uses the Google Arts & Culture Color
Explorer. Museum and style are sent together to Google's artwork search, so a
combination such as MoMA plus Modern Art is exact. If color is added to a
museum/style query, the app groups Google's own dominant-color metadata into
the dashboard's color choices.

The first request caches up to 264 artwork records. If all matching unused
works have been sent, the app fetches the next batch, up to 2,400 records for
that filter combination. The cache contains URLs and color values, not image
files. Successfully sent artwork URLs remain excluded after app updates.

If a very narrow combination has no unused match, the app stops without
silently weakening the selected filters and without repeating an old work.

## Script to start the app

The dashboard card below calls `script.samsung_frame_neues_google_art`. Create
it in **Settings → Automations & scenes → Scripts**, or in `configuration.yaml`:

```yaml
script:
  samsung_frame_neues_google_art:
    alias: Samsung Frame neues Google Art
    sequence:
      - action: hassio.addon_start
        data:
          addon: <prefix>_hass-frametv-artchanger
```

Replace `<prefix>` with the prefix Home Assistant shows for the installed app.
You find it in the URL of the app page
(`/hassio/addon/<prefix>_hass-frametv-artchanger`) or in the log file name.

## Complete dashboard card

The card requires [button-card](https://github.com/custom-cards/button-card),
installed via HACS.

This card intentionally has no visual loading state. `button-card`'s supported
update timer plus three delayed media-source resolutions update the preview
without leaving the card stuck on “loading”.

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Kunstfilter
    show_header_toggle: false
    entities:
      - entity: input_select.samsung_frame_farbe
        name: Farbe
      - entity: input_select.samsung_frame_museum
        name: Museum
      - entity: input_select.samsung_frame_stil
        name: Stil / Epoche

  - type: custom:button-card
    name: Neues Kunstwerk laden
    icon: mdi:palette
    show_name: true
    show_state: false
    show_icon: true
    size: 50px
    aspect_ratio: 16/9
    update_timer: 5s

    styles:
      card:
        - background-image: |
            [[[
              const mediaId =
                "media-source://media_source/local/frame/latest.jpg";

              if (!this._frameArtUrl && !this._frameArtResolving) {
                this._frameArtResolving = true;

                hass.callWS({
                  type: "media_source/resolve_media",
                  media_content_id: mediaId
                }).then((result) => {
                  this._frameArtUrl = result.url;
                }).catch(() => {
                  // Beim nächsten Update-Timer wird es erneut versucht.
                }).finally(() => {
                  this._frameArtResolving = false;
                });
              }

              if (this._frameArtUrl)
                return `url("${hass.hassUrl(this._frameArtUrl)}")`;

              return "linear-gradient(to bottom, #2c3e50, #000000)";
            ]]]
        - background-size: cover
        - background-position: center
        - border-radius: 16px
        - color: white
        - font-weight: bold
        - text-shadow: 0px 2px 5px rgba(0,0,0,0.9)
        - box-shadow: 0px 4px 15px rgba(0,0,0,0.3)

      grid:
        - grid-template-areas: '"i" "n"'
        - grid-template-rows: 1fr auto

      name:
        - justify-self: center
        - padding: 10px
        - width: 100%
        - font-size: 15px
        - background: rgba(0, 0, 0, 0.5)
        - backdrop-filter: blur(8px)
        - border-bottom-left-radius: 16px
        - border-bottom-right-radius: 16px

      icon:
        - color: rgba(255, 255, 255, 0.9)
        - filter: drop-shadow(0px 2px 5px rgba(0,0,0,0.5))

    tap_action:
      action: javascript
      javascript: |
        [[[
          void helpers.runAction({
            action: "perform-action",
            perform_action: "script.samsung_frame_neues_google_art"
          });

          const mediaId =
            "media-source://media_source/local/frame/latest.jpg";

          const refreshPreview = () => {
            hass.callWS({
              type: "media_source/resolve_media",
              media_content_id: mediaId
            }).then((result) => {
              this._frameArtUrl = result.url;
            }).catch(() => {
              // Eine spätere Aktualisierung darf weiterlaufen.
            });
          };

          window.setTimeout(refreshPreview, 12000);
          window.setTimeout(refreshPreview, 24000);
          window.setTimeout(refreshPreview, 42000);

          return;
        ]]]

    hold_action:
      action: none
```

## Upstream and licensing

License clarification and the contribution proposal are tracked in
[`vivalatech/homeassistant-addons#11`](https://github.com/vivalatech/homeassistant-addons/issues/11).
