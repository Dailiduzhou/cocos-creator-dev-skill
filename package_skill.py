#!/usr/bin/env python3
"""Package a skill directory into a .skill archive.

The archive is reproducible: entries are sorted, timestamps are pinned and
permissions are normalised, so the same source always produces the same bytes
(and therefore the same sha256) regardless of when or where it is built.
"""
import os
import zipfile

# Development-only paths that must not ship inside the .skill archive.
EXCLUDE_DIRS = {'evals', '__pycache__', '.git'}
EXCLUDE_FILES = {'.DS_Store'}

# 1980-01-01 00:00:00, the earliest timestamp a zip entry can carry.
FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o644


def package_skill(skill_path, output_path=None):
    """Package a skill directory into a deterministic .skill file (zip archive)."""

    if output_path is None:
        output_path = skill_path.rstrip('/') + '.skill'

    entries = []
    for root, dirs, files in os.walk(skill_path):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
        for name in sorted(files):
            if name in EXCLUDE_FILES:
                continue
            full = os.path.join(root, name)
            arcname = os.path.relpath(full, skill_path).replace(os.sep, '/')
            entries.append((arcname, full))
    entries.sort()

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arcname, full in entries:
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix, so external_attr carries a mode
            info.external_attr = FILE_MODE << 16
            with open(full, 'rb') as fh:
                zipf.writestr(info, fh.read())

    print(f"Skill packaged: {output_path} ({len(entries)} files)")
    return output_path


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        package_skill(sys.argv[1])
    else:
        package_skill('cocos-creator-dev')
