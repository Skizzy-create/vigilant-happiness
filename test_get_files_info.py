from functions.get_files_info import get_files_info


def main():

    test1 = get_files_info("calculator", ".")
    test2 = get_files_info("calculator", "pkg")
    test3 = get_files_info("calculator", "/bin")
    test4 = get_files_info("calculator", "../")

    print(test1)
    print(test2)
    print(test3)
    print(test4)

    return {
        "test1_results": test1,
        "test2_results": test2,
        "test3_results": test3,
        "test4_results": test4,
    }


if __name__ == "__main__":
    main()
