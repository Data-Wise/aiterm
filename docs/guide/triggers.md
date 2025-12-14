# iTerm2 Triggers

Optional triggers for Claude Code notifications.

## What Are Triggers?

iTerm2 triggers watch terminal output and perform actions when patterns match.
Use them to get notified when Claude Code needs input.

## Setting Up Triggers

1. Open iTerm2 → Settings → Profiles → Default
2. Go to **Advanced** tab
3. Click **Edit** next to Triggers
4. Add triggers below

## Recommended Triggers

### Notification When Claude Waiting

| Field | Value |
|-------|-------|
| Regular Expression | `^> $` |
| Action | Post Notification |
| Parameters | `Claude waiting for input` |
| Instant | ✅ Check |

### Bounce Dock on Permission Prompt

| Field | Value |
|-------|-------|
| Regular Expression | `(Allow\|Deny)\?` |
| Action | Bounce Dock Icon |
| Parameters | *(leave empty)* |
| Instant | ✅ Check |

### Highlight Permission Lines (Optional)

| Field | Value |
|-------|-------|
| Regular Expression | `Do you want to` |
| Action | Highlight Line |
| Parameters | *(pick yellow)* |
| Instant | ✅ Check |

## Available Trigger Actions

| Action | Description |
|--------|-------------|
| Post Notification | macOS notification |
| Bounce Dock Icon | Bounces until focused |
| Ring Bell | Plays sound |
| Highlight Line | Colors the line |
| Highlight Text | Colors matched text |
| Set Title | Changes tab title |
| Show Alert | Popup alert box |
| Run Command | Execute shell command |

## Inheritance

Triggers set on the **Default** profile are inherited by child profiles
(R-Dev, Python-Dev, etc.) if they use `Dynamic Profile Parent Name: Default`.

Set triggers once on Default, they work everywhere.
