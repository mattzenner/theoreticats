import os
import dhash
import pickle
from PIL import Image
# from scipy.misc import imread, imshow, imresize
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec




# cats folder started with total of 20,009 items in total, including subfolders
# 00:3414, 01:3238, 02:3516, 03:1624, 04:2794, 05:2644, 06:2778, sum=20,008
# delted a total of 9997 .cat files, along with one doc file from each folder by hand
# should have 10,004 cat jpgs => ended up with 9,994 images after merging folders removed duplicates


# string target_path specifies full path starting with "~/"
# bool delete specifies whether to simply print and count the files in target_path folder or delete them, defaults to False for safety
# returns a string like "XXXX files (found/deleted)"
def iter_folder(target_path, delete=False):
    directory = os.path.expanduser(target_path)
    file_list = os.listdir(directory)
    count = 0  # keep track of how many files in the folder were iterated through

    if delete == True:  # function branch to remove() instead of just print()
        for filename in file_list:
            if filename.endswith(".cat"):
                os.remove(os.path.join(directory, filename))
                print("{} deleted!".format(os.path.join(directory, filename)))
                count += 1
                continue
            else:
                continue

        return "{} files deleted".format(count)
    else:
        pass

    for filename in file_list:
        if filename.endswith(".cat"):
            print(os.path.join(directory, filename))
            count += 1
            continue
        else:
            continue

    return "{} files found".format(count)


# string target_path specifies full path starting with "~/"
# rename all files in target_path directory numerically, adding 'cat_' prefix
def rename_files(target_path, prefix):
    path = os.path.expanduser(target_path)
    files = os.listdir(path)

    for index, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, ''.join([prefix, str(index), '.jpg'])))

    print("Done renaming!")


# difference hash all files in folder
def dhash_folder(target_path):
    directory = os.path.expanduser(target_path)
    file_list = os.listdir(directory)
    count = 0  # keep track of how many files in the folder were iterated through

    # if directory + ".DS_Store" in file_list:
    #     file_list.remove(directory + ".DS_Store")
    #     print("DS Store removed!")

    hash_dict = {}

    for filename in file_list:
        if not filename.endswith(".jpg"):
            continue
        with Image.open(os.path.join(directory, filename)) as image:
            hash = dhash.dhash_int(image)
            # hex = dhash.format_int(row, col)
            hash_dict[filename] = hash
            # print(dhash.format_hex(row, col))
            # print(os.path.join(directory, filename), dhash.format_hex(row, col))
        count += 1
        if count % 100 == 0:
            print("{} / 10000".format(count))

    return [hash_dict, count]


def save_obj(obj, name):
    with open('{}.pkl'.format(name), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('{}.pkl'.format(name), 'rb') as f:
        return pickle.load(f)

# # delete .cat files from all CAT_XX folders in "~/Downloads/cats/"
# # all six CAT_XX folders were then manually copied into CAT_00
# path_list = ["~/Downloads/cats/{}/".format(subfolder) for subfolder in ["CAT_00", "CAT_01", "CAT_02", "CAT_03", "CAT_04", "CAT_05", "CAT_06"]]
# path_dict = {}
# for path in path_list:
#     path_dict[path] = iter_folder(path, delete=True)
#
# for key in path_dict.keys():
#     print(key, path_dict[key])
#
# rename all files in CAT_00 numerically from 0-9993
# rename_files("~/Downloads/cats/CAT_00/")

# print(dhash_folder("~/Downloads/cats/CAT_00/"))

def dict_to_list(dict):
    list = []
    for key in dict.keys():
        list.append((key, dict[key]))
    return list


def has_duplicates(hash_dict, threshold=2):
    duplicates_found = False
    hd = hash_dict

    sorted_hashes = sorted(hd[0].values())
    for i in range(len(sorted_list)):
        if dhash.get_num_bits_different(sorted_hashes[i], sorted_hashes[i+1]) <= threshold:
            duplicates_found = True
            break

    return duplicates_found


def find_duplicates(hash_dict, threshold=2):
    hl = dict_to_list(hash_dict)

    duplicates_list = []
    sorted_list = sorted(hl, key = lambda x: x[1])
    for i in range(len(sorted_list)-1):
        diff = dhash.get_num_bits_different(sorted_list[i][1], sorted_list[i+1][1])
        if diff <= threshold:
            duplicates_list.append((sorted_list[i], sorted_list[i+1], diff))

    # print("Number of duplicate pairs found: {}".format(len(duplicates_list)))
    return duplicates_list



path = "~/Downloads/theoreticats/cats/CAT_00/"
rename_files(path, '_')

# directory = os.path.expanduser("~/Downloads/theoreticats/cats/CAT_00/")
# hash_dict = dhash_folder("~/Downloads/theoreticats/cats/CAT_00/")[0]
# save_obj(hash_dict, "cat_hash_dict")
#
# hash_dict = load_obj("cat_hash_dict")
#
# duplicates_list = find_duplicates(hash_dict, threshold = 2)
#
# print(len(duplicates_list))
# for d in duplicates_list:
#     print(d[2], d[0][0], d[1][0])
# print(len(duplicates_list))

# for d in duplicates_list:
#     os.remove(os.path.join(directory, d[0][0]))
#
# print(len(duplicates_list))
