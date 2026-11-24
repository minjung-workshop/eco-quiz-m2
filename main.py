def read_number(prompt, minimum, maximum):
    """허용 범위 안의 정수를 입력받습니다."""
    while True:
        text = input(prompt).strip()

        if not text:
            print("빈 입력입니다. 숫자를 입력해주세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("숫자로 입력해주세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}~{maximum} 사이의 숫자를 입력해주세요.")


def show_menu():
    print("\n===== 우리 동네 생태 퀴즈 =====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def main():
    try:
        while True:
            show_menu()
            choice = read_number("선택: ", 1, 5)

            if choice == 5:
                print("생태 퀴즈를 종료합니다.")
                break

            print("이 기능은 다음 단계에서 구현합니다.")

    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
