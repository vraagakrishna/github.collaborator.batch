# GitHub Collaborator Batch

A browser-based tool to **bulk invite GitHub users as collaborators** to a repository.

Users can be provided as GitHub usernames or profile URLs. The tool handles duplicate users, existing invitations, and optionally expired invitations.

---

## Features

- Accepts GitHub profile URLs **or** usernames
- Automatically extracts usernames from GitHub URLs
- Supports users provided through:
  - Text input
  - `.txt` file upload
- Removes duplicate users after username extraction
- Bulk invites users to a GitHub repository
- Detects existing pending invitations
- Skips users who already have an active invitation
- Optionally deletes expired invitations before sending a new invitation
- Continues processing if an individual user fails
- Displays real-time processing logs
- Handles repository invitations across multiple API pages
- Uses GitHub's REST API directly from the browser
- No backend or database required

---

## Requirements

- A modern web browser
- A GitHub account with permission to manage collaborators
- A GitHub Personal Access Token (Fine-grained)

---

## Setup

Clone the repository

```bash
git clone https://github.com/vraagakrishna/github.collaborator.batch.git
cd github.collaborator.batch
```

---

## Creating a GitHub Token

Use a **Fine-grained Personal Access Token** on GitHub.

### Steps

1. Go to:
   - GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens

2. Click **Generate new token**

3. Configure:
   - **Repository access** → **All repositories**
   - **Permissions** → \* Set the following: **Administration** → **Read and write**
     > This permission is required to manage repository collaborators (invite/remove users)

---

## Using the Tool

Open the application in your browser.

You will be prompted for:

### 1. GitHub Personal Access Token

Enter your Fine-grained GitHub Personal Access Token.
`github_pat_xxxxxxxxxxxxxxxxxxxx`

### 2. Repository URL

Enter the GitHub repository URL: `https://github.com/owner/repository-name`

### 3. Collaborators

Enter the GitHub usernames or profile URLs, one per line.

For example:

```text
https://github.com/johnDoe
https://github.com/janeDoe/
alex123
```

You can also upload a `.txt` file containing the users.

---

## Expired Invitations

The application provides an option:

> Delete expired invitations and send a new invitation

When enabled, the tool checks the repository's existing invitations.

If an invitation for a user is found and GitHub reports it as expired:

1. The expired invitation is deleted.
2. A new collaborator invitation is sent.
3. Processing continues with the next user.

If the option is disabled, expired invitations are not deleted.

### Important

GitHub controls invitation expiration. The tool does not set or modify the expiration date of an invitation.

---

## Duplicate Users

Duplicates are removed **after extracting the GitHub username**.

This means the following are treated as the same user:

```text
johnDoe
https://github.com/johnDoe
https://github.com/johnDoe/
```

Only one invitation request will be made for `johnDoe`.

---

## Existing Invitations

If a user already has an active repository invitation, the tool does not send another invitation.

Example:

> ⚠️ Invitation already pending: johnDoe

This prevents unnecessary duplicate invitation requests.

---

## Processing Behaviour

Users are processed individually.

If one user fails, the tool does not stop the entire process.

For example:

```text
✅ Added: student1
❌ Failed: student2 | 404 | Not Found
✅ Added: student3
⚠️ Invitation already pending: student4
✅ Added: student5
```

The tool continues processing `student3`, `student4`, and `student5` even though `student2` failed.

---

# Invitation Pagination

GitHub limits the number of invitations returned in a single API response.

The application requests invitations using pagination and continues retrieving pages until all available invitations have been processed.

Therefore, repositories with more than 100 invitations are supported.

---

## Important Notes

- Users must provide their **GitHub username or profile URL**.
- Email addresses are not accepted as input.
- The GitHub API does not allow this application to choose a custom invitation expiration date.
- The GitHub token must have the required repository permissions.
- The token should have access to the repository being managed.
- Deleting an expired invitation is optional and controlled by the checkbox in the application.
- The tool does not store student GitHub usernames or profile URLs.
- The tool does not store the GitHub Personal Access Token.

---

## Security

This application operates entirely in the browser.

The GitHub Personal Access Token is entered by the user and used to authenticate requests to GitHub.

Do not use someone else's token.

Do not share your token.

If a token is accidentally exposed, revoke it immediately through GitHub and create a new one.

---
