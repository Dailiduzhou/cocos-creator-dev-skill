#!/usr/bin/env python3
import zipfile
import os

def package_skill(skill_path, output_path=None):
    """Package a skill directory into a .skill file (zip archive)."""

    if output_path is None:
        output_path = skill_path + '.skill'

    skill_name = os.path.basename(skill_path)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
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
