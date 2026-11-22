"""Jira Client for Faktura.uz (REST API v2)
Reads token and URL from jira_config.json in the project root.
"""
import sys
import os
import json
import urllib.request
import urllib.parse
import ssl

def find_project_root():
    cur = os.path.dirname(os.path.abspath(__file__))
    while cur and os.path.dirname(cur) != cur:
        if os.path.exists(os.path.join(cur, "jira_config.json")) or os.path.exists(os.path.join(cur, "TASK")):
            return cur
        cur = os.path.dirname(cur)
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
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def make_request(path, method="GET", data=None):
    config = load_config()
    url = f"{config['jiraUrl']}/rest/api/2/{path.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {config['token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(req, context=ctx) as response:
        return json.loads(response.read().decode("utf-8"))

def get_issue(issue_key, save_to_task_dir=True):
    issue_data = make_request(f"issue/{issue_key}")
    fields = issue_data.get("fields", {})
    
    summary = fields.get("summary", "")
    status = fields.get("status", {}).get("name", "")
    issue_type = fields.get("issuetype", {}).get("name", "")
    assignee = (fields.get("assignee") or {}).get("displayName", "Unassigned")
    description = fields.get("description", "")
    
    print(f"[{issue_key}] {summary}")
    print(f"Status: {status} | Type: {issue_type} | Assignee: {assignee}")
    print("-" * 60)
    print("Description:")
    print(description or "(No description)")
    
    if save_to_task_dir:
        task_dir = os.path.join(BASE_DIR, "TASK", issue_key)
        os.makedirs(task_dir, exist_ok=True)
        
        output_file = os.path.join(task_dir, "issue.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(issue_data, f, ensure_ascii=False, indent=2)
            
        desc_file = os.path.join(task_dir, "TASK-INFO.txt")
        with open(desc_file, "w", encoding="utf-8") as f:
            f.write(f"Key: {issue_key}\n")
            f.write(f"Summary: {summary}\n")
            f.write(f"Status: {status}\n")
            f.write(f"Type: {issue_type}\n")
            f.write(f"Assignee: {assignee}\n\n")
            f.write("=== DESCRIPTION ===\n")
            f.write(description or "")
            f.write("\n")
            
        print(f"\n[Saved to {task_dir}]")
        
    return issue_data

def search_issues(jql, max_results=20):
    res = make_request(f"search?jql={urllib.parse.quote(jql)}&maxResults={max_results}")
    issues = res.get("issues", [])
    print(f"Found {len(issues)} issues for query: {jql}")
    for item in issues:
        fields = item.get("fields", {})
        print(f"- {item.get('key')}: {fields.get('summary')} [{fields.get('status', {}).get('name')}]")
    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python jira_client.py [get <KEY> | search <JQL>]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    if cmd == "get" and len(sys.argv) > 2:
        get_issue(sys.argv[2])
    elif cmd == "search" and len(sys.argv) > 2:
        search_issues(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command or missing arguments: {cmd}")
