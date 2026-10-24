<img src="homeassistant-samsung-frametv-artchanger/logo.png" alt="Samsung The Frame - Art Changer logo" width="160">

# Samsung The Frame - Art Changer add-on for Home Assistant

![TV with some art on it ](https://i.imgur.com/BunHdwb.jpeg)

This add-on is built on the awesome work of <https://github.com/ow/samsung-frame-art> and <https://github.com/gijsvdhoven/homeassistant-addons>. 

It is a fork of the original add-on by [vivalatech](https://github.com/vivalatech/homeassistant-addons) and includes these pull requests from that repository:
- [#9 Support staged local Frame TV artwork](https://github.com/vivalatech/homeassistant-addons/pull/9) by [@Yurii201811](https://github.com/Yurii201811)
- [#12 Add Google Arts filters, preview, aspect-ratio preservation, and duplicate prevention](https://github.com/vivalatech/homeassistant-addons/pull/12) by [@volkue-tech](https://github.com/volkue-tech)
- [#13 Fix media folder path and handle unreachable TV](https://github.com/vivalatech/homeassistant-addons/pull/13)

It pushes images from different sources to your Samsung Frame TV. Supported sources are Google Arts & Culture, Bing Wallpapers and the local media folder.

By starting the add-on it will pick an image based on your configuration and put it on your frame; after the image is placed the add-on will automatically stop again. This for instance can be triggered via an automation to run on a daily basis. Please find an example below.

If multiple sources are enabled it will randomly choose a source on each run. 

## Features

- **Google Arts & Culture filters**: restrict artworks by color, museum and style/period, set in the add-on options or from Home Assistant `input_select` helpers.
- **Landscape only**: skips portrait and square Google artworks before the high-res download (on by default).
- **Borderless TV format**: optionally accept only Google artworks close to 16:9, so they fill the screen without black borders.
- **Preserve complete artwork**: fits the whole image on a black 16:9 canvas instead of cropping it (on by default).
- **No repeats**: images already sent are not picked again, across all sources. The history is kept in `/media/frame/uploaded_files.json` and survives add-on updates.
- **Dashboard preview**: the image sent to the TV is saved as `/media/frame/latest.jpg`.
- **Staged local artwork**: put `/media/frame/selected_frame_art.jpg` in place to show exactly that image.
- **Multiple TVs**: set `tv` to a comma-separated list of IPs (spaces allowed, e.g. `192.168.1.10, 192.168.1.11`). TVs are updated one after another; each gets its own image unless **Same Image** is enabled. A TV that is off is skipped. Images already sent to any TV are not picked again for another TV.
- **Unreachable TV handling**: if the TV is off or not on the network, the run stops after 10 seconds with one log line and leaves the TV unchanged.

# Google Art
By default the addon configuration has "Google Art" mode enabled, which takes random images from the Google Arts and Culture site and pushes them to the Samsung Frame TV.

Filters for color, museum and style/period can be combined. Each filter is read from a Home Assistant `input_select` helper if it exists, otherwise from the add-on option (`ANY` means no restriction). Both English and German values are accepted (e.g. `BLUE` or `Blau`). If no unused artwork matches, the add-on stops without changing the TV.

Supported values:
- **Color**: Blue, Green, Red, Orange, Yellow, Purple, Pink, Teal, Gray
- **Museum**: MoMA, Musée d'Orsay, Van Gogh Museum, Metropolitan Museum, Rijksmuseum, National Gallery London, Tate Britain
- **Style/period**: Modern, Contemporary, Impressionism, Post-Impressionism, Expressionism, Abstract Expressionism, Surrealism, Pop Art, Renaissance, Baroque, Romanticism, Realism

See [DOCS.md](homeassistant-samsung-frametv-artchanger/DOCS.md) for the helper setup and a complete dashboard card.

# Bing Wallpaper
"Bing Wallpapers" mode displays random high-quality 4K wallpapers from Bing (from 2021-08-28 onward) on your Samsung Frame TV.

# Local Media Folder
Looks for images in the /media/frame folder (including subfolders) and randomly pushes an image to your Samsung Frame TV. When you start the addon for the first time it creates a specific directory in Media called "frame" where you can place your custom images.

Only .jpg and .png files are supported (upper- or lower-case extension). `latest.jpg` is the dashboard preview and is never used as a source.

If `/media/frame/selected_frame_art.jpg` exists, the add-on will upload that file instead of choosing a random image. This makes it possible for a Home Assistant dashboard, script, or shell command to stage one exact local artwork before starting the add-on. The file is uploaded fresh on every run, so you can replace it under the same name. If that file is not present, the normal random local-media behavior is used.


## Installation

Install this addon by adding the repository:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Foliverwehrens%2Fhomeassistant-samsung-the-frame-art-changer)


## Configuration Options

| Option | Default | Description |
| --- | --- | --- |
| `tv` | `192.168.1.199` | IP address of your Samsung Frame TV. Comma-separate multiple TVs, e.g. `192.168.1.10, 192.168.1.11`. |
| `google_art` | `true` | Use images from Google Arts & Culture. |
| `google_color` | `ANY` | Color filter, used when the color helper is unavailable. |
| `google_color_entity` | `input_select.samsung_frame_color` | Helper entity for the color filter. |
| `google_museum` | `ANY` | Museum filter, used when the museum helper is unavailable. |
| `google_museum_entity` | `input_select.samsung_frame_museum` | Helper entity for the museum filter. |
| `google_style` | `ANY` | Style/period filter, used when the style helper is unavailable. |
| `google_style_entity` | `input_select.samsung_frame_style` | Helper entity for the style filter. |
| `google_landscape_only` | `true` | Skip portrait and square Google artworks. |
| `google_tv_format_only` | `false` | Only accept Google artworks close to 16:9. Falls back to a landscape work on a black canvas if none is found. |
| `download_high_res` | `true` | (Google Art only) Download high-resolution images using dezoomify. |
| `bing_wallpapers` | `false` | Use wallpapers from Bing. |
| `media_folder` | `false` | Use images from `/media/frame`. |
| `preserve_aspect_ratio` | `true` | Fit the whole image on a black 16:9 canvas instead of cropping. |
| `same_image` | `false` | Send the same image to all TVs. |


## Example Automation

Here's an example of how to set up an automation to change the image daily at 23:00:

```yaml
description: "Change Samsung Frame TV Art Daily"
mode: single
trigger:
  - platform: time
    at: "23:00:00"
condition: []
action:
  - service: hassio.addon_start
    data:
      addon: 9c41c859_hass-frametv-artchanger
```

`9c41c859_hass-frametv-artchanger` is the slug when the add-on is installed from this repository. Otherwise use the slug from the URL of the add-on page (`/hassio/addon/<slug>`).
