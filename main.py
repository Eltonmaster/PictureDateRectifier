import argparse
from tqdm import tqdm
import os
import pywintypes, win32file, win32con
from datetime import datetime
from PIL import Image
import shutil
from sys import exit
import json
import re

def init_parser():
    parser = argparse.ArgumentParser(
        prog = "PictureDateRectifier",
        description = "\nThis program solves the problem of wrong timestamps on image files usually caused by importing images from a phone to a new phone or computer.",
    )
    parser.add_argument("folder", type=str, help="path to the folder containing the images")
    parser.add_argument("-e", "--exif-test", action="store_true", help="test if the images contain the EXIF data needed for the program to work", default=False)
    parser.add_argument("-ow", "--overwrite", action="store_true", help="overwrite the original files", default=False)
    parser.add_argument("-o", "--output", type=str, help="path to the folder where the images will be saved - skipped when overwrite is set")    
    parser.add_argument("-p", "--progress", action="store_true", help="show progress bar")
    parser.add_argument("-s", "--source", type=str, choices=["exif", "filename", "json"], help="where to draw the date information from", default="filename")
    parser.add_argument("-d", "--date", type=str, choices=["modification", "creation", "access"], help="which date to set the image to", default="modification")

    args = parser.parse_args()

    if not os.path.exists(args.folder):
        raise FileNotFoundError(f"The folder '{args.folder}' does not exist.")
    if not os.access(args.folder, os.W_OK):
        raise PermissionError(f"The folder '{args.folder}' is not writable.")
    if not args.overwrite and not args.output:
         args.output = os.path.join("output")
    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)
    elif args.output and not os.access(args.output, os.W_OK):
        raise PermissionError(f"The output folder '{args.output}' is not writable.")
    if os.name != 'nt':
        raise NotImplementedError("This program is designed to run on Windows only.")
    
    return args

def exif_test(folder):
    file_list = [entry for entry in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, entry))]
    for entry in file_list:
        try:
            exif = Image.open(os.path.join(folder, entry))._getexif()
            if not exif:
                print(f"{entry} does not contain EXIF data.")
                return 1
            exif_date = exif.get(36867)
            print(f"EXIF date for {entry}: {exif_date}")
        except Exception as e:
            print(f"Error processing {entry}: {e}")
    print("\nAll files contain EXIF data.")
    return 0

def changeFileCreationTime(fname, newtime):
    changeFileTime(fname, newtime, "creation")

def changeFileModificationTime(fname, newtime):
    changeFileTime(fname, newtime, "modification")

def changeFileAccessTime(fname, newtime):
    changeFileTime(fname, newtime, "access")

def changeFileCreationTimeCopy(fname, oldname, newtime):
    changeFileTimeCopy(fname, oldname, newtime, "creation")

def changeFileModificationTimeCopy(fname, oldname, newtime):
    changeFileTimeCopy(fname, oldname, newtime, "modification")

def changeFileAccessTimeCopy(fname, oldname, newtime):
    changeFileTimeCopy(fname, oldname, newtime, "access")

def getFileTime(fname):
    temp = win32file.CreateFile(
    fname,
    win32con.GENERIC_WRITE,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
    None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
    creation, access, modification = win32file.GetFileTime(temp)
    return creation, access, modification

def changeFileTimeCopy(fname, oldname, newtime, date_type):
    creation, access, modification = getFileTime(oldname)
    creation, access, modification = pywintypes.Time(creation), pywintypes.Time(access), pywintypes.Time(modification)
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname,
        win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
    if date_type == "creation":
        win32file.SetFileTime(winfile, wintime, access, modification)
    elif date_type == "modification":
        win32file.SetFileTime(winfile, creation, access, wintime)
    elif date_type == "access":
        win32file.SetFileTime(winfile, creation, wintime, modification)
    winfile.close()

def changeFileTime(fname, newtime, date_type):
    wintime = pywintypes.Time(newtime)   
    winfile = win32file.CreateFile(
        fname,
        win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
    if date_type == "creation":
        win32file.SetFileTime(winfile, wintime, None, None)
    elif date_type == "modification":
        win32file.SetFileTime(winfile, None, None, wintime)
    elif date_type == "access":
        win32file.SetFileTime(winfile, None, wintime, None)
    winfile.close()


def convertDatetime(date_string):
    try:
        if ":" in date_string:
            return datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
        elif len(date_string) == 8:
            return datetime.strptime(date_string, '%Y%m%d')
        elif len(date_string) == 10:
            return datetime.fromtimestamp(int(date_string))
        elif len(date_string) == 14:
            return datetime.strptime(date_string, "%Y%m%d%H%M%S")
        else:
            raise ValueError()
    except ValueError:
        raise ValueError(f"Date string '{date_string}' is not in the correct format.")

if __name__ == "__main__":
    args = init_parser()
    if args.exif_test:
        exit(exif_test(args.folder))
    file_list = [entry for entry in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, entry))]
    with tqdm(total=len(file_list), desc="Processing files", disable=not args.progress) as pbar:
        for entry in file_list:

            if not (entry.lower().endswith("jpg") or entry.lower().endswith("jpeg") or entry.lower().endswith("mp4") or entry.lower().endswith("png") or entry.lower().endswith("vid")):
                pbar.update(1)
                continue

            if args.source == "exif":
                exif = Image.open(os.path.join(args.folder, entry))._getexif()
                if not exif:
                    raise Exception(f"No EXIF data found in {entry}.")
                exif_date = exif.get(36867)
                temp_date = convertDatetime(exif_date)

            elif args.source == "filename":   #Test for different patterns via regex
                #20171231_163326.jpg
                res1 = re.search(r"\d{8}_\d{6}", entry)
                #IMG-20190426-WA0019.jpg
                res2 = re.search(r"\d{8}-W", entry)
                #Screenshot_20180110-131957.png
                res3 = re.search(r"\d{8}-\d{6}", entry)


                if res1:
                    temp_date = convertDatetime(res1.group().replace("_", ""))
                elif res2:
                    temp_date = convertDatetime(res2.group()[:-2])
                elif res3:
                    temp_date = convertDatetime(res3.group().replace("-", ""))
                else:
                    raise ValueError("The string '" + entry + "' does not match with any regular expressions")

            elif args.source == "json":
                json_path = os.path.join(args.folder, entry + ".supplemental-metadata.json")
                if not os.path.exists(json_path):
                    pbar.update(1)
                    continue
                if json_path:
                    with open(json_path, "r") as json_file:
                        data = json.load(json_file)
                    creation_date = data["creationTime"]["timestamp"]
                    temp_date = convertDatetime(creation_date)


            file_to_work_on = os.path.join(args.folder, entry)

            if not args.overwrite:
                shutil.copyfile(os.path.join(args.folder, entry), os.path.join(args.output, entry))
                file_to_work_on = os.path.join(args.output, entry)
                old_file = os.path.join(args.folder, entry)
                creation, access, modification = getFileTime(old_file)
                if args.date == "creation":
                        changeFileCreationTimeCopy(file_to_work_on, old_file, temp_date)
                elif args.date == "modification":
                        changeFileModificationTimeCopy(file_to_work_on, old_file, temp_date)
                elif args.date == "access":
                        changeFileAccessTimeCopy(file_to_work_on, old_file, temp_date)


            else:
                if args.date == "creation":
                        changeFileCreationTime(file_to_work_on, temp_date)
                elif args.date == "modification":
                        changeFileModificationTime(file_to_work_on, temp_date)
                elif args.date == "access":
                        changeFileAccessTime(file_to_work_on, temp_date)

            pbar.update(1)




