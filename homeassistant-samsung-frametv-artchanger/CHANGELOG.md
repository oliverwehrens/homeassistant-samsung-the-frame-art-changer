# Changelog

## 1.1.7

- Don't interrupt someone watching TV. When the TV is not in art mode, the
  image is uploaded and selected, and shows the next time art mode is on.
- Drop support for armhf, armv7 and i386. Home Assistant no longer supports
  these platforms.
- Build on the multi-arch Home Assistant base image (Alpine 3.23) instead of
  the per-architecture 3.18 images. Remove `build.yaml`.

## 1.1.6

- New colorful icon and logo.

## 1.1.5

- Use the name "Samsung The Frame - Art Changer" in the repository and docs.

## 1.1.4

- Log one line instead of a stack trace when the TV is unreachable while the
  connection is created.

## 1.1.3

- Default helper entity IDs are now English: `input_select.samsung_frame_color`
  and `input_select.samsung_frame_style` (`samsung_frame_museum` is unchanged).
  Existing installs keep their saved values; update them in the configuration.
- Add `samsung-the-frame.yaml` package with helpers, start script and daily automation.

## 1.1.2

- Allow spaces in Google Art filter options (e.g. `National Gallery London`).

## 1.1.1

- Rename the add-on to "Samsung The Frame - Art Changer".
- Build the add-on from this repository instead of pulling the vivalatech image.
- Allow spaces in the comma-separated TV IP list.
- Always upload a staged `selected_frame_art.jpg`, even if a file with that name was sent before.
- Read local media from `/media/frame` and skip TVs without an available image.
- Time out after 10 seconds and log one line when a TV is unreachable.

## 1.1.0

- Add Google Arts & Culture color, museum, and style/period filters.
- Support exact museum plus style combinations.
- Use Google-provided dominant-color metadata for combined filtering.
- Preserve sent-art history across app updates and avoid repeat uploads.
- Publish the processed TV image atomically as `/media/frame/latest.jpg`.
- Add progressive catalog caching with bounded storage.
- Add filter tests, translated configuration labels, and dashboard documentation.
- Preserve the complete artwork and add black borders when its aspect ratio is not 16:9.
- Bound Google dimension selection by attempts and elapsed time, fall back from strict TV format to a preserved-aspect landscape work, and exit cleanly when no work matches.
