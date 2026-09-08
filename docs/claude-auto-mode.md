# Claude Code Auto Mode Configuration

[config/claude-auto-mode.example.json](../config/claude-auto-mode.example.json) is a generic starting point, not a record of an installed configuration. Agents does not install, update, or prune auto-mode settings. Keep personal repository lists, infrastructure names, and machine-specific settings outside this public repository.

## Customize and apply

Review the [official configuration reference](https://code.claude.com/docs/en/auto-mode-config) for your Claude Code version. The example retains built-in environment context through `$defaults` and adds visibility and sharing boundaries. It grants no additional repository or service trust and leaves the classifier's allow/block lists unchanged.

1. Back up your Claude settings outside the repository.
2. Adapt the example to your environment in a private file. Name only destinations and audiences you intend to trust.
3. With explicit operator approval, merge the intended `autoMode` keys into your user settings. Preserve unrelated keys, including installer-managed hooks. Review existing `permissions.allow` rules separately; this example does not replace them.
4. Inspect the effective configuration with `claude auto-mode config` and review it with `claude auto-mode critique`.

Repository trust does not establish that a destination is suitable for confidential material. Keep a private environment record for comparison with the effective configuration, and update it deliberately when your infrastructure changes.

## Rollback

Restore the backed-up settings or remove only the auto-mode changes you applied. Preserve later unrelated settings and installer-managed hooks. No Agents installer rollback applies to these manually managed settings.
