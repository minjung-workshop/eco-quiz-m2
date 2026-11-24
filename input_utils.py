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


def read_text(prompt):
    """공백을 제외한 내용이 있는 문자열을 입력받습니다."""
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("빈 입력입니다. 내용을 입력해주세요.")
