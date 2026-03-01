"""
简单计算器程序 / Simple Calculator Program
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零 / Division by zero is not allowed")
    return a / b


def calculator():
    """
    运行交互式命令行计算器。
    用户依次输入 '数字 运算符 数字' 形式的表达式，程序输出计算结果。
    输入 'q' 退出程序。

    Runs an interactive command-line calculator.
    The user enters expressions in the form 'number operator number' and the
    program prints the result. Enter 'q' to quit.
    """
    print("欢迎使用简单计算器 / Welcome to Simple Calculator")
    print("支持操作: +  -  *  /  (输入 'q' 退出 / Enter 'q' to quit)")
    print("-" * 50)

    while True:
        user_input = input("\n请输入表达式 (例如: 3 + 4) / Enter expression (e.g. 3 + 4): ").strip()

        if user_input.lower() == 'q':
            print("再见! / Goodbye!")
            break

        parts = user_input.split()
        if len(parts) != 3:
            print("格式错误，请输入: 数字 运算符 数字 / Invalid format. Use: number operator number")
            continue

        try:
            a = float(parts[0])
            operator = parts[1]
            b = float(parts[2])
        except ValueError:
            print("无效的数字 / Invalid number")
            continue

        try:
            if operator == '+':
                result = add(a, b)
            elif operator == '-':
                result = subtract(a, b)
            elif operator == '*':
                result = multiply(a, b)
            elif operator == '/':
                result = divide(a, b)
            else:
                print(f"不支持的运算符: {operator} / Unsupported operator: {operator}")
                continue

            print(f"结果 / Result: {a} {operator} {b} = {result}")
        except ValueError as e:
            print(f"错误 / Error: {e}")


if __name__ == "__main__":
    calculator()
