#!/usr/bin/env python3
import zipfile
import os

# Development-only paths that must not ship inside the .skill archive.
EXCLUDE_DIRS = {'evals', '__pycache__', '.git'}
EXCLUDE_FILES = {'.DS_Store'}


def package_skill(skill_path, output_path=None):
    """Package a skill directory into a .skill file (zip archive)."""

    if output_path is None:
        output_path = skill_path + '.skill'

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
            for file in sorted(files):
                if file in EXCLUDE_FILES:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_path)
                zipf.write(file_path, arcname)

    print(f"Skill packaged: {output_path}")
    return output_path


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        package_skill(sys.argv[1])
    else:
        package_skill('cocos-creator-dev')
