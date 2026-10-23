# Changelog

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
