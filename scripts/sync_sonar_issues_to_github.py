#!/usr/bin/env python3
"""
Sync open SonarQube issues into GitHub Issues.

Behavior:
- Creates a GitHub issue for each open Sonar issue that does not exist yet.
- Reopens and updates existing GitHub issue when Sonar issue is still open.
- Closes GitHub issue when Sonar issue is no longer open.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional


SONAR_KEY_PATTERN = re.compile(r"Sonar Issue Key:\s*([A-Za-z0-9:_\-]+)")


@dataclass
class SonarIssue:
    key: str
    issue_type: str
    severity: str
    status: str
    rule: str
    component: str
    line: Optional[int]
    message: str
    effort: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


def _http_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    payload: Optional[dict] = None,
) -> dict:
    data = None
    req_headers = dict(headers)
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, method=method, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: {exc.code} {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc}") from exc


def fetch_sonar_open_issues(host_url: str, project_key: str, token: str) -> List[SonarIssue]:
    token_b64 = base64.b64encode(f"{token}:".encode("utf-8")).decode("ascii")
    headers = {"Authorization": f"Basic {token_b64}"}

    results: List[SonarIssue] = []
    page = 1
    page_size = 500

    while True:
        query = urllib.parse.urlencode(
            {
                "projects": project_key,
                "resolved": "false",
                "ps": str(page_size),
                "p": str(page),
            }
        )
        endpoint = f"{host_url.rstrip('/')}/api/issues/search?{query}"
        payload = _http_json("GET", endpoint, headers=headers)
        issues = payload.get("issues", [])
        total = int(payload.get("total", 0))

        for item in issues:
            results.append(
                SonarIssue(
                    key=item["key"],
                    issue_type=item.get("type", "CODE_SMELL"),
                    severity=item.get("severity", "MEDIUM"),
                    status=item.get("status", "OPEN"),
                    rule=item.get("rule", ""),
                    component=item.get("component", ""),
                    line=item.get("line"),
                    message=item.get("message", "").strip(),
                    effort=item.get("effort"),
                    created_at=item.get("creationDate"),
                    updated_at=item.get("updateDate"),
                )
            )

        if page * page_size >= total:
            break
        page += 1

    return results


def github_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "sonar-issue-sync",
    }


def ensure_label(
    api_base: str,
    repo: str,
    headers: Dict[str, str],
    name: str,
    color: str,
    description: str,
    dry_run: bool,
) -> None:
    label_url = f"{api_base}/repos/{repo}/labels/{urllib.parse.quote(name, safe='')}"
    try:
        _http_json("GET", label_url, headers=headers)
        return
    except RuntimeError as exc:
        if " 404 " not in str(exc):
            raise

    if dry_run:
        print(f"[dry-run] create label: {name}")
        return

    create_url = f"{api_base}/repos/{repo}/labels"
    _http_json(
        "POST",
        create_url,
        headers=headers,
        payload={"name": name, "color": color, "description": description},
    )


def fetch_github_issues(api_base: str, repo: str, headers: Dict[str, str]) -> List[dict]:
    issues: List[dict] = []
    page = 1
    while True:
        query = urllib.parse.urlencode(
            {"state": "all", "labels": "sonarqube", "per_page": "100", "page": str(page)}
        )
        url = f"{api_base}/repos/{repo}/issues?{query}"
        batch = _http_json("GET", url, headers=headers)
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected response when listing GitHub issues.")
        if not batch:
            break
        issues.extend(batch)
        page += 1
    return [item for item in issues if "pull_request" not in item]


def issue_title(sonar_issue: SonarIssue) -> str:
    location = sonar_issue.component.split(":")[-1]
    if sonar_issue.line:
        location = f"{location}:{sonar_issue.line}"
    message = sonar_issue.message
    if len(message) > 110:
        message = message[:107] + "..."
    return f"[Sonar] {sonar_issue.issue_type} {sonar_issue.severity} - {location} - {message}"


def issue_body(host_url: str, project_key: str, sonar_issue: SonarIssue) -> str:
    sonar_link = (
        f"{host_url.rstrip('/')}/project/issues?id={project_key}"
        f"&issues={sonar_issue.key}&open={sonar_issue.key}"
    )
    dashboard_link = f"{host_url.rstrip('/')}/dashboard?id={project_key}"
    line_str = str(sonar_issue.line) if sonar_issue.line is not None else "N/A"
    effort_str = sonar_issue.effort or "N/A"
    created = sonar_issue.created_at or "N/A"
    updated = sonar_issue.updated_at or "N/A"
    rule = sonar_issue.rule or "N/A"

    return (
        "Issue criada automaticamente a partir do SonarQube.\n\n"
        f"- Sonar Project: `{project_key}`\n"
        f"- Sonar Issue Key: `{sonar_issue.key}`\n"
        f"- Type: `{sonar_issue.issue_type}`\n"
        f"- Severity: `{sonar_issue.severity}`\n"
        f"- Status: `{sonar_issue.status}`\n"
        f"- Rule: `{rule}`\n"
        f"- Component: `{sonar_issue.component}`\n"
        f"- Line: `{line_str}`\n"
        f"- Effort: `{effort_str}`\n"
        f"- Created (Sonar): `{created}`\n"
        f"- Updated (Sonar): `{updated}`\n\n"
        "## Message\n\n"
        f"{sonar_issue.message}\n\n"
        "## Links\n\n"
        f"- Sonar Issue: {sonar_link}\n"
        f"- Sonar Dashboard: {dashboard_link}\n"
    )


def extract_sonar_key(body: str) -> Optional[str]:
    if not body:
        return None
    match = SONAR_KEY_PATTERN.search(body)
    return match.group(1) if match else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync SonarQube issues to GitHub issues.")
    parser.add_argument("--sonar-host-url", required=True)
    parser.add_argument("--sonar-project-key", required=True)
    parser.add_argument("--sonar-token", required=True)
    parser.add_argument("--github-repo", required=True, help="owner/repo")
    parser.add_argument("--github-token", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def map_github_issues_by_sonar_key(gh_issues: List[dict]) -> Dict[str, dict]:
    mapped: Dict[str, dict] = {}
    for gh_issue in gh_issues:
        key = extract_sonar_key(gh_issue.get("body", ""))
        if key:
            mapped[key] = gh_issue
    return mapped


def sync_open_sonar_issues(
    *,
    sonar_by_key: Dict[str, SonarIssue],
    gh_by_sonar_key: Dict[str, dict],
    api_base: str,
    github_repo: str,
    gh_headers: Dict[str, str],
    sonar_host_url: str,
    sonar_project_key: str,
    dry_run: bool,
) -> tuple[int, int, int]:
    created = 0
    updated = 0
    reopened = 0

    for key, sonar_issue in sonar_by_key.items():
        current = gh_by_sonar_key.get(key)
        desired_title = issue_title(sonar_issue)
        desired_body = issue_body(sonar_host_url, sonar_project_key, sonar_issue)

        if current is None:
            if dry_run:
                print(f"[dry-run] create issue for Sonar key {key}")
            else:
                create_url = f"{api_base}/repos/{github_repo}/issues"
                _http_json(
                    "POST",
                    create_url,
                    headers=gh_headers,
                    payload={
                        "title": desired_title,
                        "body": desired_body,
                        "labels": ["sonarqube"],
                    },
                )
            created += 1
            continue

        patch_payload: Dict[str, str] = {}
        if current.get("state") == "closed":
            patch_payload["state"] = "open"
            reopened += 1

        if current.get("title") != desired_title:
            patch_payload["title"] = desired_title
        if current.get("body") != desired_body:
            patch_payload["body"] = desired_body

        if patch_payload:
            if dry_run:
                print(f"[dry-run] update issue #{current['number']} for Sonar key {key}")
            else:
                update_url = f"{api_base}/repos/{github_repo}/issues/{current['number']}"
                _http_json("PATCH", update_url, headers=gh_headers, payload=patch_payload)
            updated += 1

    return created, updated, reopened


def close_resolved_sonar_issues(
    *,
    sonar_by_key: Dict[str, SonarIssue],
    gh_by_sonar_key: Dict[str, dict],
    api_base: str,
    github_repo: str,
    gh_headers: Dict[str, str],
    dry_run: bool,
) -> int:
    closed = 0

    for key, gh_issue in gh_by_sonar_key.items():
        if key in sonar_by_key:
            continue
        if gh_issue.get("state") != "open":
            continue

        number = gh_issue["number"]
        if dry_run:
            print(f"[dry-run] close issue #{number} (Sonar key {key} no longer open)")
        else:
            comment_url = f"{api_base}/repos/{github_repo}/issues/{number}/comments"
            _http_json(
                "POST",
                comment_url,
                headers=gh_headers,
                payload={
                    "body": (
                        "Fechando automaticamente: a issue correspondente no SonarQube "
                        "não está mais aberta."
                    )
                },
            )
            close_url = f"{api_base}/repos/{github_repo}/issues/{number}"
            _http_json("PATCH", close_url, headers=gh_headers, payload={"state": "closed"})
        closed += 1

    return closed


def main() -> int:
    args = parse_args()

    sonar_issues = fetch_sonar_open_issues(
        host_url=args.sonar_host_url,
        project_key=args.sonar_project_key,
        token=args.sonar_token,
    )
    sonar_by_key = {item.key: item for item in sonar_issues}
    print(f"Fetched {len(sonar_by_key)} open Sonar issues.")

    api_base = os.getenv("GITHUB_API_URL", "https://api.github.com").rstrip("/")
    gh_headers = github_headers(args.github_token)

    ensure_label(
        api_base=api_base,
        repo=args.github_repo,
        headers=gh_headers,
        name="sonarqube",
        color="1d76db",
        description="Issue synchronized from SonarQube",
        dry_run=args.dry_run,
    )

    gh_issues = fetch_github_issues(api_base=api_base, repo=args.github_repo, headers=gh_headers)
    gh_by_sonar_key = map_github_issues_by_sonar_key(gh_issues)

    created, updated, reopened = sync_open_sonar_issues(
        sonar_by_key=sonar_by_key,
        gh_by_sonar_key=gh_by_sonar_key,
        api_base=api_base,
        github_repo=args.github_repo,
        gh_headers=gh_headers,
        sonar_host_url=args.sonar_host_url,
        sonar_project_key=args.sonar_project_key,
        dry_run=args.dry_run,
    )
    closed = close_resolved_sonar_issues(
        sonar_by_key=sonar_by_key,
        gh_by_sonar_key=gh_by_sonar_key,
        api_base=api_base,
        github_repo=args.github_repo,
        gh_headers=gh_headers,
        dry_run=args.dry_run,
    )

    print(
        "Sync completed: "
        f"created={created}, updated={updated}, reopened={reopened}, closed={closed}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
