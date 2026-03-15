from os.path import abspath, commonpath, join, normcase


def is_valid_target(working_directory, target_path):

    abs_working_directory = abspath(working_directory)
    target_path = normcase(abspath(join(abs_working_directory, target_path)))

    valid = commonpath([abs_working_directory, target_path]) == abs_working_directory

    return valid, abs_working_directory, target_path
