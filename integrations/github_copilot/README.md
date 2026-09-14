# FishyLLAMA GitHub Copilot Integration

This directory defines FishyLLAMA's integration layer for GitHub Copilot-style coding assistance.

## Important

The uploaded `GitHub-Copilot-windows-arm64-setup.exe` is an installer binary. FishyLLAMA should not execute or embed the installer in the server. Keep the installer outside the repository unless you have verified its provenance and licensing.

FishyLLAMA instead exposes a provider interface that can connect to coding-assistant services through their supported APIs/CLI integrations.

## Goals

- code completion and generation
- explain and refactor code
- review diffs
- generate tests
- repository-aware context
- selectable coding model/provider
- optional user-provided API credentials

See `copilot_provider.py` for the provider contract.