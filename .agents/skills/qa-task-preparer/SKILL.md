---
name: qa-task-preparer
description: Automatically prepares Faktura.uz QA tasks from Jira (jira.faktura.uz). Creates folder structure, downloads all attachments (IMG, FILE, JSON), creates TEST-INFO.txt, and generates complete TEST-CASE.txt.
---

# QA Task Preparer Skill for Faktura.uz

This skill automates the routine QA workflow when a new task is received.

## Triggers
- User sends a Jira task key (e.g. `FA-5871`, `FA-5839`).
- User sends a Jira URL (`https://jira.faktura.uz/...`).
- User asks: "Подготовь задачу FA-xxxx", "Составь тест-кейсы для FA-xxxx".

## Automated Pipeline:

1. **Execute Task Preparation Script:**
   ```powershell
   python "C:\Users\Acer\Desktop\FACTURA.uz\.agents\script\prepare_task.py" <KEY>
   ```
   This will:
   - Query Jira API at `https://jira.faktura.uz/rest/api/2/issue/<KEY>`.
   - Create `TASK/<KEY>/` with subfolders: `IMG/`, `FILE/`, `JSON/`.
   - Automatically download images into `IMG/`.
   - Automatically download documents (.pdf, .xlsx) into `FILE/`.
   - Automatically download JSONs into `JSON/`.
   - Create `issue.json` and `TEST-INFO.txt`.

2. **Generate Exhaustive TEST-CASE.txt:**
   Read `TEST-INFO.txt` and generate `TEST-CASE.txt` in the task directory with:
   - **A. Основные позитивные сценарии:** Core feature functionality based on acceptance criteria.
   - **B. Граничные значения и негативные проверки:** Empty fields, nulls, long strings, invalid characters, boundary numbers.
   - **C. Права / Роли / Доступы:** Verification with and without specific permissions (if applicable).
   - **D. Регрессионное тестирование:** Checks that other document types (Счета-фактуры, Акты, Доверенности, ТТН) and existing functionality are not broken.
   - Format: `TC-XX | Название`, `Предусловие`, `Шаги`, `Ожидаемый результат`, `Результат: ` (empty for manual QA execution).

3. **Respond to User:**
   - Provide direct clickable links to the created folder and files.
   - Summarize downloaded files and key test scenarios.
