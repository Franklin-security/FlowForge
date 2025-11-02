# Pipedash Analysis & FlowForge Improvements

## Pipedash Architecture Analysis

Based on the [pipedash repository](https://github.com/hcavarsan/pipedash), here are the key architectural patterns:

### Core Features

1. **Plugin Architecture**
   - Each CI/CD provider (GitHub Actions, Buildkite, Jenkins) implemented as a plugin
   - Common interface (`Plugin` trait in Rust) for all providers
   - Easy to add new providers without modifying core code

2. **Data Caching**
   - SQLite database for local caching of pipeline data
   - Reduces API calls and improves performance
   - Stores pipeline status, run history, commit info

3. **Secure Secret Management**
   - System keyring integration (Keychain/Secret Service/Credential Manager)
   - Tokens stored separately from configuration
   - No secrets in code or config files

4. **Multi-Provider Support**
   - Support for multiple instances of same provider
   - Unified view across different CI/CD platforms
   - Configurable refresh intervals per provider

5. **Pipeline Operations**
   - Trigger workflows with parameters
   - Re-run previous executions
   - Cancel running builds
   - View run history with commit information

6. **Background Polling**
   - Automatic refresh loop
   - Configurable intervals per provider
   - Real-time UI updates when status changes

## FlowForge Improvements Plan

### Phase 1: Plugin System ✅ (Implementing)

- **Provider Plugin Interface**: Abstract base class for CI/CD providers
- **GitHub Actions Plugin**: First implementation
- **Plugin Registry**: Dynamic plugin loading and management
- **Unified API**: Common interface for all providers

### Phase 2: Database & Caching

- **SQLite Integration**: Local caching of pipeline data
- **Pipeline Models**: Data structures for pipelines, runs, commits
- **Cache Management**: TTL, invalidation, refresh strategies

### Phase 3: Enhanced Security

- **Keyring Integration**: Use Python keyring library
- **Secret Management**: Secure storage of API tokens
- **Configuration Separation**: Secrets separate from config

### Phase 4: Pipeline Operations

- **Trigger Pipelines**: Start workflows with parameters
- **Re-run Executions**: Re-execute previous runs
- **Cancel Builds**: Stop running pipelines
- **History Tracking**: Run history with metadata

### Phase 5: Monitoring & Polling

- **Background Tasks**: Async polling with Celery or asyncio
- **Event System**: Real-time updates via WebSocket or SSE
- **Status Monitoring**: Track pipeline status changes
- **Metrics**: Build duration, success rates

## Implementation Strategy

1. Start with plugin system (modular, extensible)
2. Add database layer for persistence
3. Implement secret management
4. Add pipeline operations
5. Build monitoring and polling

## Key Differences: Pipedash vs FlowForge

| Feature | Pipedash | FlowForge (Current) | FlowForge (Planned) |
|---------|----------|---------------------|---------------------|
| Language | Rust + TypeScript | Python | Python |
| Architecture | Desktop App (Tauri) | Web API (Flask) | Web API + Plugins |
| UI | Desktop GUI | REST API | REST API + Future UI |
| Providers | 3 (GitHub, Buildkite, Jenkins) | 1 (GitHub) | Multiple (Plugin-based) |
| Caching | SQLite | None | SQLite |
| Secrets | System Keyring | Environment vars | Keyring + Env |
| Polling | Background loop | Manual | Background tasks |

## Benefits of Plugin Architecture

1. **Extensibility**: Add new providers without core changes
2. **Maintainability**: Each provider isolated in own module
3. **Testability**: Easy to mock and test providers
4. **Flexibility**: Different providers can have different refresh rates
5. **Scalability**: Add unlimited providers

---

This analysis guides the enhancement of FlowForge with best practices from pipedash.

