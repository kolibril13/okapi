# /img

Save the **macOS clipboard** image as **WebP + JPEG** in `~/Downloads` (same timestamp stem), then **read the JPEG** for context, pick a **short descriptive filename**, and **copy the WebP** to the root of the current workspace (repository root).

**Speed / ordering:** Do not read workspace files, plan, or use the clipboard for anything else until clipboard capture is done. The clipboard can change at any moment—the capture command must be the **first** action.

## Part 1 — save from clipboard

1. **Immediately** from the workspace repository root (the folder that contains `.cursor/commands/`), run—before anything else:
   ```bash
   uv run ./clipboard_to_webp.py
   ```
2. If this fails, stop and report the error.

3. Parse paths from the output:
   - **WebP (for repo / embed):** `SAVED_PATH_WEBP=...` (or `SAVED_PATH=...`, same value).
   - **JPEG (for reading / analysis):** `SAVED_PATH_JPEG=...`.

## Part 2 — understand, name, copy project WebP

4. **Open/read the JPEG** at `SAVED_PATH_JPEG` (image-capable read) and briefly note what is visible (UI, text, subject).
5. Choose a **new base name** (stem only, no extension):
   - Lowercase **kebab-case**, ASCII `a-z`, `0-9`, hyphens only.
   - **3–6 words** worth of meaning, e.g. `blender-geometry-nodes-graph`.
   - Avoid generic names like `screenshot` or `image` unless nothing else fits.
6. From the **same** workspace root, copy the **WebP** only:
   ```bash
   uv run ./image_to_workspace.py "<absolute-path-from-SAVED_PATH_WEBP>" "<descriptive-stem>"
   ```
   Use the exact WebP path; quote paths with spaces.
7. Report:
   - One-line summary of what the image shows.
   - Final file path under the project root (from the script output `Copied to:`).

## Notes

- **macOS only** for clipboard capture (`clipboard_to_webp.py`: Pillow + PyObjC).
- **WebP:** quality **84**, method **6** (embed). **JPEG:** quality **90**, `optimize=True` (preview/read).
- `image_to_workspace.py` **copies the WebP** into the current directory and avoids overwriting (`name-2.webp`, …).
- Timestamped **`.webp` and `.jpg`** remain in `~/Downloads` unless you delete them.
