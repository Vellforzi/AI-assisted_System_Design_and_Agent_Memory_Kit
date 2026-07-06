# Codex Connector Policy

Status: portable connector side-effect policy
Purpose: use Slack, Linear, GitHub, and similar connectors without making them
implicit authority or uncontrolled write channels.

---

## Core Rule

Connectors are forbidden by default.

Connector reads require explicit scope. Connector writes require explicit
Allowed scope, owner approval for the current task, and receipts.

Connector output is operational evidence until promoted through the project's
normal memory process. It is not durable project truth by itself.

## Read Scope Must Name

- system or workspace;
- repository, channel, project, issue, thread, file path, or query;
- time window where history matters;
- purpose of the read.

Vague permission such as "read Slack" or "check GitHub" is insufficient.

## Write Gates

Default outbound messaging is draft-first.

For a send/update/delete/create action, the task contract must name:

- target system;
- exact target channel/repo/project/issue/thread;
- allowed action;
- content source or summary;
- receipt requirement.

## Receipts

After an allowed connector write, record:

- system;
- action;
- target;
- returned URL/id/timestamp when available;
- short summary of the content;
- error if the write failed.

Do not record secret values in receipts.

## Source Authority

Connector output may inform a task result or proposed memory delta. Durable
project truth still requires owner approval or promotion into Project Map or an
equivalent owner-controlled memory layer.

## Local Git and GitHub Connector

Local git commands and GitHub connector writes are separate side-effect channels.
A task may allow one and forbid the other. State each explicitly.
