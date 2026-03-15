from functions.write_files import write_file


def main():

    test1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    test2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    test3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

    print(test1)
    print(test2)
    print(test3)

    return {
        "test1_results": test1,
        "test2_results": test2,
        "test3_results": test3,
    }


if __name__ == "__main__":
    main()
