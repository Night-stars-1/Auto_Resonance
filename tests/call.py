def click(pos):
    print(pos)


action = {"type": "click", "pos": [0, 0], "test": 0}
method_name = action.pop("type")
print(method_name, action)
# 使用 getattr 来动态获取方法
method = globals().get(method_name)

try:
    if method:
        # 如果方法存在，调用它并传递位置信息
        method(**action)
    else:
        print(f"未知的方法: {method_name}")
except TypeError as error:
    error_str = str(error)
    if (
        "required positional argument" in error_str
        or "required keyword-only argument" in error_str
    ):
        missing_arg = error_str.split("argument: ")[-1].replace("'", "")
        action_data = {"type": method_name, **action}
        print(f"{action_data} - 错误：缺少必需的参数 - {missing_arg}")
    elif "got an unexpected keyword argument" in error_str:
        missing_arg = error_str.split("argument")[-1].replace("'", "")
        action_data = {"type": method_name, **action}
        print(f"{action_data} - 错误：多余的参数 - {missing_arg}")
    else:
        print(error)
