"""Automation for Faktura.uz QA Tasks:
1. Fetches Jira issue data via REST API
2. Creates folder structure: TASK/<KEY>/ (IMG/, FILE/, JSON/)
3. Automatically downloads all attachments from Jira to their respective folders
4. Generates clean TEST-INFO.txt
5. Saves raw issue.json
"""

import sys
import os
import re
import json
import ssl
import urllib.request
import urllib.parse
from datetime import datetime

def find_project_root():
    cur = os.path.dirname(os.path.abspath(__file__))
    while cur and os.path.dirname(cur) != cur:
        if os.path.exists(os.path.join(cur, "jira_config.json")) or os.path.exists(os.path.join(cur, "TASK")):
            return cur
        cur = os.path.dirname(cur)
    # Default fallback to C:\Users\Acer\Desktop\FACTURA.uz
    return r"C:\Users\Acer\Desktop\FACTURA.uz"

BASE_DIR = find_project_root()

def get_config_path():
    candidates = [
        os.path.join(BASE_DIR, ".agents", "config", "jira_config.json"),
        os.path.join(BASE_DIR, "jira_config.json")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]

CONFIG_PATH = get_config_path()

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_jira_markup(text):
    if not text:
        return ""
    text = re.sub(r"^h[1-6]\.\s*", "### ", text, flags=re.MULTILINE)
    text = re.sub(r"\*([^*\n]+)\*", r"\1", text)
    text = re.sub(r"_([^_\n]+)_", r"\1", text)
    text = re.sub(r"\{color:[^}]+\}", "", text)
    text = re.sub(r"\{color\}", "", text)
    text = re.sub(r"\{noformat\}", "```", text)
    text = re.sub(r"\{code:[^}]+\}", "```", text)
    text = re.sub(r"\{code\}", "```", text)
    return text

def extract_issue_key(query):
    match = re.search(r"([A-Za-z]+-\d+)", query)
    if match:
        return match.group(1).upper()
    return query.strip().upper()

def make_request(path, config):
    url = f"{config['jiraUrl']}/rest/api/2/{path.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {config['token']}",
        "Accept": "application/json",
        "User-Agent": "Antigravity-QA-Agent/1.0"
    }
    req = urllib.request.Request(url, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

def download_file(url, target_path, config):
    headers = {
        "Authorization": f"Bearer {config['token']}",
        "User-Agent": "Antigravity-QA-Agent/1.0"
    }
    if config["jiraUrl"].startswith("https://") and url.startswith("http://"):
        url = "https://" + url[len("http://"):]

    req = urllib.request.Request(url, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(req, context=ctx) as resp:
        with open(target_path, "wb") as f:
            f.write(resp.read())

def prepare_task(query, custom_folder_name=None):
    config = load_config()
    issue_key = extract_issue_key(query)
    
    print(f"[*] Fetching Jira issue {issue_key}...")
    issue = make_request(f"issue/{issue_key}", config)
    fields = issue.get("fields", {})

    summary = fields.get("summary", "")
    description = fields.get("description", "")
    status = fields.get("status", {}).get("name", "Unknown")
    issue_type = fields.get("issuetype", {}).get("name", "Task")
    priority = (fields.get("priority") or {}).get("name", "Normal")
    assignee = (fields.get("assignee") or {}).get("displayName", "Unassigned")
    reporter = (fields.get("reporter") or {}).get("displayName", "Unknown")
    components = [c.get("name") for c in fields.get("components", [])]

    task_root = os.path.join(BASE_DIR, "TASK")
    os.makedirs(task_root, exist_ok=True)
    
    target_dir = None
    if custom_folder_name:
        target_dir = os.path.join(task_root, custom_folder_name)
    else:
        for existing in os.listdir(task_root):
            if issue_key in existing:
                target_dir = os.path.join(task_root, existing)
                break
        if not target_dir:
            today_str = datetime.now().strftime("%d.%m.%Y")
            target_dir = os.path.join(task_root, f"{today_str} {issue_key}")

    img_dir = os.path.join(target_dir, "IMG")
    file_dir = os.path.join(target_dir, "FILE")
    json_dir = os.path.join(target_dir, "JSON")

    for d in [target_dir, img_dir, file_dir, json_dir]:
        os.makedirs(d, exist_ok=True)

    print(f"[+] Task folder ready: {target_dir}")

    attachments = fields.get("attachment", [])
    downloaded_files = []
    print(f"[*] Found {len(attachments)} attachments in Jira.")

    img_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

    for att in attachments:
        filename = att.get("filename", "")
        content_url = att.get("content", "")
        size = att.get("size", 0)
        ext = os.path.splitext(filename)[1].lower()

        if ext in img_exts:
            dest = os.path.join(img_dir, filename)
            rel = f"IMG/{filename}"
        elif ext == ".json":
            dest = os.path.join(json_dir, filename)
            rel = f"JSON/{filename}"
        else:
            dest = os.path.join(file_dir, filename)
            rel = f"FILE/{filename}"

        if not os.path.exists(dest):
            try:
                download_file(content_url, dest, config)
                print(f"    -> Downloaded: {rel} ({size} bytes)")
                downloaded_files.append((filename, rel, size))
            except Exception as e:
                print(f"    [!] Failed to download {filename}: {e}")
        else:
            downloaded_files.append((filename, rel, size))

    with open(os.path.join(target_dir, "issue.json"), "w", encoding="utf-8") as f:
        json.dump(issue, f, ensure_ascii=False, indent=2)

    test_info_path = os.path.join(target_dir, "TEST-INFO.txt")
    with open(test_info_path, "w", encoding="utf-8") as f:
        f.write(f"Задача: {issue_key} — {summary}\n")
        f.write(f"Ссылка: {config['jiraUrl']}/browse/{issue_key}\n")
        f.write(f"Тип: {issue_type} | Статус: {status} | Приоритет: {priority}\n")
        f.write(f"Исполнитель: {assignee} | Автор: {reporter}\n")
        if components:
            f.write(f"Компоненты: {', '.join(components)}\n")
        f.write("=" * 80 + "\n\n")
        f.write("ОПИСАНИЕ И ТРЕБОВАНИЯ:\n")
        f.write(clean_jira_markup(description) + "\n\n")
        if downloaded_files:
            f.write("=" * 80 + "\n")
            f.write("СКАЧАННЫЕ ВЛОЖЕНИЯ:\n")
            for fn, rel, sz in downloaded_files:
                f.write(f"  - [{rel}] ({sz} bytes)\n")

    print(f"[+] Saved TEST-INFO.txt and issue.json")
    return {
        "key": issue_key,
        "summary": summary,
        "status": status,
        "description": description,
        "target_dir": target_dir,
        "attachments": downloaded_files
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prepare_task.py <ISSUE_KEY_OR_URL>")
        sys.exit(1)
    res = prepare_task(sys.argv[1])
    print(json.dumps({"status": "OK", "dir": res["target_dir"]}, ensure_ascii=False))
