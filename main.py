import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = os.getenv('GITHUB_OWNER')


if not all([GITHUB_TOKEN, OWNER]):
    raise ValueError('Missing required environment variables')


HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}


def parse_args():
    parser = argparse.ArgumentParser(description='GitHub Collaborator Batch Tool')

    parser.add_argument(
        '--file',
        required=True,
        help='Path to file containing GitHub usernames or URLs'
    )

    parser.add_argument(
        '--repo',
        required=True,
        help='Repo name'
    )

    return parser.parse_args()


def extract_username(entry):
    entry = entry.strip()

    if 'github.com' not in entry:
        return entry  # already a username

    path = urlparse(entry).path  # /username/repo/...
    parts = [p for p in path.split('/') if p]

    if len(parts) == 0:
        return None

    return parts[0]


def extract_error_message(response):
    try:
        data = response.json()
    except Exception:
        return response.text

    # Sometimes GitHub returns errors list
    errors = data.get('errors')
    if isinstance(errors, list) and len(errors) > 0:
        first = errors[0]
        if isinstance(first, dict):
            return first.get('message') or str(first)

    # Most common case
    if 'message' in data:
        return data['message']

    # Fallback
    return 'Unknown error'


def add_collaborator(username, repo_name):
    url = f'https://api.github.com/repos/{OWNER}/{repo_name}/collaborators/{username}'

    response = requests.put(url, headers=HEADERS, json={
        'permission': 'push'
    })

    if response.status_code in [201, 204]:
        print(f'✅ Added: {username}')
    else:
        error_message = extract_error_message(response)

        print(f'❌ Failed: {username} \t| {response.status_code} \t| {error_message}')


def process_file(file_path, repo_name):
    print(f'🚀 Sharing GitHub repo: {OWNER}/{repo_name}')
    print(f'📂 Processing file: {file_path}\n')

    with open(file_path, 'r') as f:
        entries = [line.strip() for line in f if line.strip()]

    print(f'👥 Total users to process: {len(entries)}\n')

    seen_usernames = set()
    unique_entries = []

    for entry in entries:
        username = extract_username(entry)

        if not username:
            print(f'⚠️ Skipping invalid entry: {entry}')
            continue

        username = username.strip()

        if username in seen_usernames:
            print(f'🔁 Duplicate skipped: {username}')
            continue

        seen_usernames.add(username)
        unique_entries.append(username)

    print(f'\n👥 Unique users: {len(unique_entries)}\n')

    for username in unique_entries:
        try:
            add_collaborator(username, repo_name)
        except Exception as e:
            print(f'⚠️ Error with {username}: {str(e)}')


if __name__ == '__main__':
    args = parse_args()
    process_file(args.file, args.repo)
