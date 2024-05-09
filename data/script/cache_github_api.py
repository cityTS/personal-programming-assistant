import requests
import os

# 替换为你的GitHub个人访问令牌
GITHUB_TOKEN = 'your_github_token'
# GitHub API的基本URL
GITHUB_API_BASE_URL = 'https://api.github.com'
# 替换为你的目标仓库的用户名和仓库名
REPO_OWNER = 'username'
REPO_NAME = 'reponame'

# 设置请求头，包含认证信息
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
}


def get_github_file_content(owner, repo, path, token):
    # 构建获取仓库文件内容的API URL
    file_url = (
        f'{GITHUB_API_BASE_URL}/repos/{owner}'
        f'/{repo}/contents/{path}'
    )
    response = requests.get(file_url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 获取文件内容
        return response.content.decode('utf-8')
    else:
        print(
            f'Failed to retrieve the file {path}. '
            f'Status code: {response.status_code}'
        )
        return None


def list_contents(owner, repo, path='.', token):
    # 构建获取仓库内容的API URL
    contents_url = (
        f'{GITHUB_API_BASE_URL}/repos/{owner}'
        f'/{repo}/contents/{path}'
    )
    response = requests.get(contents_url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            item_path = os.path.join(path, item['name'])
            if item['type'] == 'file':
                # It's a file, get the content
                print(f"Fetching file: {item_path}")
                file_content = (
                    get_github_file_content(owner, repo, item_path, token)
                )
                if file_content:
                    # Process the file content
                    # (e.g., print, write to a file, etc.)
                    print(file_content)
            elif item['type'] == 'dir':
                # It's a directory, list contents recursively
                print(f"Found directory: {item_path}")
                list_contents(owner, repo, item_path, token)
    else:
        print(
            f'Failed to list the contents of {path}. '
            f'Status code: {response.status_code}'
        )


# 从仓库的根目录开始列出内容
list_contents(REPO_OWNER, REPO_NAME, token=GITHUB_TOKEN)
