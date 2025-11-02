# FlowForge Enhancements - Based on Pipedash Analysis

## Overview

FlowForge has been enhanced with architectural improvements inspired by the [pipedash](https://github.com/hcavarsan/pipedash) project. These enhancements add multi-provider support, plugin architecture, and improved data management.

## ✅ Implemented Enhancements

### 1. Plugin Architecture System

**Location**: `src/providers/`

- **Base Provider Interface** (`base.py`):
  - Abstract base class `BaseProvider` with standard methods
  - Common data structures: `Pipeline`, `PipelineRun`, `PipelineStatus`
  - Provider configuration via `ProviderConfig` dataclass
  
- **Provider Registry** (`registry.py`):
  - Centralized management of provider instances
  - Methods to register, unregister, and query providers
  - Unified pipeline fetching across all providers

- **GitHub Provider** (`github.py`):
  - First implementation of the provider interface
  - Supports fetching workflows and runs
  - Placeholders for trigger, re-run, and cancel operations

### 2. Database Layer (SQLite)

**Location**: `src/database/`

- **Database Manager** (`db.py`):
  - SQLite connection management
  - Session handling with context managers
  - Automatic schema initialization

- **Data Models** (`models.py`):
  - `PipelineModel`: Stores pipeline information
  - `PipelineRunModel`: Stores run history
  - Timestamps and metadata tracking

### 3. Enhanced API Endpoints

**Location**: `src/api/pipelines.py`

New endpoints:
- `GET /api/v1/pipelines` - List all pipelines from all providers
- `GET /api/v1/pipelines/providers` - List registered providers
- `GET /api/v1/pipelines/<provider>/pipelines` - Get provider-specific pipelines
- `POST /api/v1/pipelines/<provider>/pipelines/<id>/trigger` - Trigger pipeline
- `POST /api/v1/pipelines/<provider>/runs/<id>/cancel` - Cancel run

### 4. Dependencies Updated

Added to `requirements.txt`:
- `sqlalchemy>=2.0.0` - Database ORM
- `keyring>=24.3.0` - Secure secret storage

## 🔄 Architecture Comparison

### Before (FlowForge Initial)
```
src/
├── api/
│   └── routes.py      # Basic Flask routes
├── config.py          # Configuration only
└── main.py            # Entry point
```

### After (Enhanced FlowForge)
```
src/
├── api/
│   ├── routes.py      # Main app + registered blueprints
│   └── pipelines.py   # Pipeline management endpoints
├── providers/          # Plugin architecture
│   ├── base.py        # Base provider interface
│   ├── registry.py    # Provider registry
│   ├── github.py      # GitHub Actions provider
│   └── __init__.py
├── database/          # Data persistence
│   ├── db.py          # Database manager
│   ├── models.py      # SQLAlchemy models
│   └── __init__.py
├── config.py          # Configuration
└── main.py            # Entry point
```

## 🎯 Key Features Added

### Multi-Provider Support

```python
from src.providers.registry import ProviderRegistry
from src.providers.github import GitHubProvider
from src.providers.base import ProviderConfig

# Register multiple providers
registry = ProviderRegistry()

# GitHub provider
github = GitHubProvider(ProviderConfig(
    name='github-main',
    provider_type='github',
    config={'token': '...', 'owner': 'org', 'repo': 'repo'}
))
registry.register(github)

# Fetch from all providers
pipelines = registry.fetch_all_pipelines()
```

### Unified Pipeline Interface

All providers implement the same interface:
- `fetch_pipelines()` - Get all pipelines
- `trigger_pipeline()` - Start a pipeline
- `cancel_pipeline()` - Stop a running pipeline
- `re_run_pipeline()` - Re-execute a pipeline

### Database Caching

```python
from src.database.db import get_db_manager

db = get_db_manager()

# Use database session
with db.get_session() as session:
    # Cache pipeline data
    # Query cached data
    pass
```

## 📋 Next Steps (To Implement)

### Phase 4: Keyring Integration
- Replace environment variable secrets with keyring
- Secure token storage per provider
- Configuration API for managing secrets

### Phase 5: Complete Pipeline Operations
- Implement `trigger_pipeline()` for GitHub Actions
- Implement `re_run_pipeline()` functionality
- Implement `cancel_pipeline()` functionality
- Add support for workflow parameters

### Phase 6: Additional Providers
- GitLab CI provider
- Jenkins provider
- Buildkite provider (like pipedash)
- CircleCI provider

### Phase 7: Background Polling
- Async task scheduling (Celery or asyncio)
- Configurable refresh intervals per provider
- Real-time updates via WebSocket/SSE

## 🔍 Usage Examples

### Setting Up a Provider

```python
from src.providers.base import ProviderConfig
from src.providers.github import GitHubProvider
from src.api.pipelines import get_registry

config = ProviderConfig(
    name='my-github',
    provider_type='github',
    enabled=True,
    refresh_interval=30,
    config={
        'token': os.getenv('GITHUB_TOKEN'),
        'owner': 'my-org',
        'repo': 'my-repo'
    }
)

provider = GitHubProvider(config)
if provider.validate_credentials():
    registry = get_registry()
    registry.register(provider)
```

### API Usage

```bash
# List all pipelines
curl http://localhost:8000/api/v1/pipelines

# List providers
curl http://localhost:8000/api/v1/pipelines/providers

# Get pipelines from specific provider
curl http://localhost:8000/api/v1/pipelines/my-github/pipelines

# Trigger a pipeline
curl -X POST http://localhost:8000/api/v1/pipelines/my-github/pipelines/123/trigger \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"env": "production"}}'
```

## 📚 Documentation

- **Pipedash Analysis**: `PIPEDASH_ANALYSIS.md` - Detailed comparison
- **Architecture**: `ARCHITECTURE.md` - Updated architecture docs
- **API Docs**: See code comments in `src/api/pipelines.py`

## ✨ Benefits

1. **Extensibility**: Easy to add new CI/CD providers
2. **Maintainability**: Each provider isolated in own module
3. **Scalability**: Support unlimited providers
4. **Performance**: SQLite caching reduces API calls
5. **Security**: Ready for keyring integration
6. **Unified Interface**: Same API for all providers

---

**Status**: Core plugin architecture and database layer implemented ✅
**Next**: Complete pipeline operations and add more providers

