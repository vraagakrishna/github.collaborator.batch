# GitHub Collaborator Batch

A Python tool to **bulk add collaborators** to a GitHub repository using a list of GitHub profile URLs or usernames.

## Features

* Accepts GitHub profile URLs **or** usernames
* Automatically extracts usernames from URLs
* Adds collaborators via GitHub API
* CLI-based input (`--file`)
* Uses `.env` for secure configurations
* Removes duplicate users after normalisation
* Continues execution even if some users fail
* Safe to re-run (idempotent behaviour)

----

## Requirements

* Python 3.x
* GitHub Personal Access Token (Fine-grained recommended)

---

## Setup

1. Clone the repository

```bash
git clone https://github.com/vraagakrishna/github.collaborator.batch.git
cd github.collaborator.batch
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create your environment file by duplicating the example:

```bash
cp .env.example .env
```

Then update the values inside `.env` with your own credentials.

---

## Creating a GitHub Token

Use a **Fine-grained Personal Access Token** on GitHub.

### Steps

1. Go to:
    * GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens

2. Click **Generate new token**

3. Configure:
    * **Repository access** → **All repositories**
    * **Permissions** →
        * Set the following: **Administration** → **Read and write**
   > This permission is required to manage repository collaborators (invite/remove users)

---

## Input File Format

Create a file like `users.txt`:

```text
https://github.com/johnDoe
https://github.com/janeDoe/
alex123
```

### Supported formats:

* Full GitHub profile URL
* GitHub username
* URLs with query params are handled automatically

---

## Usage

```bash
python main.py --file users.txt --repo REPO_NAME
```

---

## How It Works?

1. Reads input file from CLI

2. Extracts username from URLs or raw input

3. Removed duplicate usernames

4. Calls GitHub API to add collaborators

5. Logs success or failure per user

---

## CLI Options

| Flag     | Description                                                 |
|:---------|-------------------------------------------------------------|
| `--file` | Path to file containing GitHub usernames or URLs (required) |
| `--repo` | Repo name                                                   | 

---

## Re-running the Script

Safe to run multiple times:

* Existing collaborators will not break execution
* New users will still be added

---

## Important Notes

* Emails are **not supported** by the GitHub API for collaborator invites
* Ensure users provide valid GitHub profile URLs
* Invalid usernames will be skipped with an error message

---
