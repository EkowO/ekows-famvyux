# Project Structure Guide

## Directory Organization

### Core Application (`app/`)
- `config.py` - Application configuration
- `routes_*.py` - API route handlers
- `utils.py` - Utility functions

### Frontend (`static/` & `templates/`)
- `static/styles.css` - Main CSS file with MovieHub theme
- `templates/` - Jinja2 HTML templates

### Scripts (`scripts/`)
Organized by purpose:

#### Data Import (`scripts/data_import/`)
- Movie data importing and management
- CSV processing scripts
- Database update utilities

#### Setup (`scripts/setup/`)
- OAuth configuration
- Environment setup
- Initial project configuration

#### Testing (`scripts/testing/`)
- Unit tests and integration tests
- Manual testing scripts
- Debug utilities

#### Server (`scripts/server/`)
- Server startup scripts
- Production deployment helpers

#### Debugging (`scripts/debugging/`)
- Debug and diagnostic scripts
- Error analysis tools
- Troubleshooting utilities

#### Utilities (`scripts/utilities/`)
- File organization tools
- Development helpers
- Batch processing scripts

### Documentation (`docs/`)
- Setup guides and installation instructions
- Feature documentation
- Troubleshooting guides
- API documentation

### Data (`data/`)
- Movie databases
- Imported data files
- User data storage

## File Naming Conventions

- **Scripts**: Use descriptive names with underscores
- **Documentation**: Use UPPERCASE for markdown files
- **Templates**: Use lowercase with underscores
- **Static files**: Use lowercase with hyphens for CSS classes

## Development Workflow

1. Make changes in appropriate directories
2. Test using scripts in `scripts/testing/`
3. Update documentation in `docs/`
4. Use utility scripts for maintenance

## Maintenance

- Use `organize_all_files.py` to reorganize files
- Keep documentation updated
- Archive old files in `archive/` directory
