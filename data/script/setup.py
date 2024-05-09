import subprocess


# 检查Git是否安装
def git_check():
    try:
        subprocess.check_call(['git', '--version'])
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    # 如果Git未安装，则打印消息
    if not git_check():
        print("警告: Git未安装。请从 https://git-scm.com/ 下载并安装Git。")
