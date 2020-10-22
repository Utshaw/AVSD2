#!/usr/bin/env python3
import os
import shutil

PARENT_DIR="./input_videos"



def main():
    fileNo = 1
    for root, dirs, files in os.walk(PARENT_DIR):
        print('--'*10)
        print(root)
        print(dirs)
        print(files)
        for file in files:
            if file.endswith('.mp4'):
                shutil.move(os.path.join(root, file), os.path.join(PARENT_DIR, 'separated', str(fileNo) + ".mp4"))
                fileNo += 1


if __name__ == "__main__":
    main()