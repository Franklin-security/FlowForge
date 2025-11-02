# FlowForge CLI Guide

## Overview

FlowForge provides a beautiful command-line interface built with Click and Rich for managing CI/CD pipelines.

## Installation

After installing FlowForge:

```bash
pip install -e .
```

The CLI will be available as `flowforge` command.

## Available Commands

### Main Commands

```bash
flowforge --help              # Show help
flowforge --version           # Show version
flowforge status              # Show status and providers
flowforge serve               # Start API server
```

### Provider Management

```bash
# Add a provider
flowforge provider add

# List providers
flowforge provider list

# Remove provider
flowforge provider remove <name>
```

### Pipeline Management

```bash
# List all pipelines
flowforge pipeline list

# List pipelines from specific provider
flowforge pipeline list --provider github-main

# Trigger a pipeline
flowforge pipeline trigger <provider> <pipeline_id> --ref main
```

## Examples

### Adding a GitHub Provider

```bash
$ flowforge provider add
Provider name: github-main
Provider type [github]: github
API token: ************
Owner/Organization: myorg
Repository: myrepo
Enable this provider? [Y/n]: y
Refresh interval [30]: 30

✓ Provider 'github-main' added successfully
```

### Viewing Status

```bash
$ flowforge status

Registered Providers
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃ Name          ┃ Type   ┃ Status ┃ Refresh ┃ Token  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│ github-main   │ github │   ✓    │   30s   │   ✓    │
└───────────────┴────────┴────────┴─────────┴────────┘
```

### Listing Pipelines

```bash
$ flowforge pipeline list

Pipelines
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ ID          ┃ Name             ┃ Status ┃ Repository   ┃ Branch  ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 12345678    │ CI Pipeline      │ SUCCESS│ myorg/myrepo │ main    │
│ 87654321    │ Deploy           │ RUNNING│ myorg/myrepo │ main    │
└─────────────┴──────────────────┴────────┴──────────────┴─────────┘
```

### Triggering a Pipeline

```bash
$ flowforge pipeline trigger github-main 12345678 --ref main

✓ Pipeline triggered successfully
Run ID: 78901234
Status: pending
```

## Integration with API

The CLI uses the same provider registry as the API server. You can:

1. Start API server: `flowforge serve`
2. Use CLI for management: `flowforge provider add`
3. Both share the same providers and configuration

## Keyboard Shortcuts

- `Ctrl+C` - Cancel current operation
- Tab completion - Available for commands and options (when supported)

## Output Formatting

The CLI uses Rich library for beautiful terminal output:
- Color-coded status indicators
- Tables for structured data
- Progress bars for long operations
- Syntax highlighting

## Error Handling

All errors are displayed with clear messages:
- Validation errors show what's wrong
- API errors show HTTP status and message
- Provider errors show provider-specific details

---

**Note**: All CLI commands require FlowForge to be installed and configured.

