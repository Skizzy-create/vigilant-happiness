from functions.get_file_content import get_file_content
from config import MAX_CHARS


def main():

    test0 = get_file_content("calculator", "lorem.txt")
    # print(len(test0))
    # print(test0[:200])
    # print(test0[-200:])
    # assert isinstance(test0, str)

    # trunc_start = test0.find("[...File")
    # if trunc_start == -1:
    #    trunc_start = test0.find(f"truncated at {MAX_CHARS}")

    # content_only = test0[:trunc_start] if trunc_start != -1 else test0

    # assert len(content_only) >= MAX_CHARS, (
    # f"{MAX_CHARS} is the limit, but got ->{len(content_only)}"
    # )
    # print("test_get_file_content passed")

    test1 = get_file_content("calculator", "main.py")
    test2 = get_file_content("calculator", "pkg/calculator.py")
    test3 = get_file_content("calculator", "/bin/cat")
    test4 = get_file_content("calculator", "pkg/does_not_exist.py")

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


main()
