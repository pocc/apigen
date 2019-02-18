# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Planned
* Tests
* Use logger instead of print

## [Unreleased]
* CLI options: \[--help, --show-generators, --version, --verbose\]

## [0.1.2] - 2019-02-19
### Added
* Verbosity levels accessible via CLI

## [0.1.1] - 2019-02-18
### Added
* OpenAPI to Postman conversion
* CLI is now properly integrated with other components

## [0.1.0] - 2019-02-18
### Fixed
* Issue #2: Missing API calls

## [0.0.0] - 2019-02-17
### Added
* Project Structure
* Fetch Meraki API JSON from API docs
* Direct user to create a github issue if there is a new API primitive 
  (i.e. Any new {path params} in endpoint: /this/{is}/an/{endpoint})
* CLI
* README / LICENSE / CHANGELOG

<!---
CHANGELOG TYPES

Added:      for new features. 
Changed:    for changes in existing functionality.
Deprecated: for soon-to-be removed features.
Removed:    for now removed features.
Fixed:      for any bug fixes.
Security:   for vulnerability fixes.
-->

[Unreleased]: https://github.com/pocc/mad-codegen/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/pocc/mad-codegen/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/pocc/mad-codegen/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/pocc/mad-codegen/compare/v0.0.0...v0.1.0
[0.0.0]: https://github.com/pocc/mad-codegen/commit/ba8dec9