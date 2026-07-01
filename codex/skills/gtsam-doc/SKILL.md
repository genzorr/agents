---
name: gtsam-doc
description: Quickly answer questions about GTSAM classes, factors, methods, concepts, and examples using cache, local source, and official docs.
---

# GTSAM Doc

Use when the user asks about GTSAM APIs or concepts.

## Sources

Check in this order:

1. Cache: `~/.codex/skills/gtsam-doc/cache/<topic>.md`
2. Local source, if available (prefer `$GTSAM_SOURCE_DIR`):
   - `$GTSAM_SOURCE_DIR`
   - `~/bin/gtsam`
3. Official API docs: `https://gtsam.org/doxygen/`
4. Official tutorials: `https://borglab.github.io/gtsam/`

If the cache exists and is less than 7 days old, use it first. If you fetch or synthesize useful docs, cache a concise markdown note for future use.

## Common Direct Links

| Class | URL | Notes |
|-------|-----|-------|
| Pose3 | `https://gtsam.org/doxygen/a03288.html` | SE(3) transformation |
| Pose2 | `https://gtsam.org/doxygen/a03256.html` | SE(2) transformation |
| Rot3 | `https://gtsam.org/doxygen/a03336.html` | SO(3) rotation |
| Rot2 | `https://gtsam.org/doxygen/a03304.html` | SO(2) rotation |
| Point3 | `https://gtsam.org/doxygen/a02936.html` | 3D point |
| Point2 | `https://gtsam.org/doxygen/a02904.html` | 2D point |
| BatchFixedLagSmoother | `https://gtsam.org/doxygen/a05132.html` | Fixed-lag smoother |
| ISAM2 | `https://gtsam.org/doxygen/a04340.html` | Incremental smoothing |
| Values | `https://gtsam.org/doxygen/a04560.html` | Variable storage |
| Marginals | `https://gtsam.org/doxygen/a04396.html` | Marginal covariances |
| Symbol | `https://gtsam.org/doxygen/a03640.html` | Variable keys |
| PriorFactor | `https://gtsam.org/doxygen/a04976.html` | Prior constraint |
| BetweenFactor | `https://gtsam.org/doxygen/a04688.html` | Between constraint |

## Workflow

1. Normalize the topic to a cache key.
2. Check cache.
3. For implementation details, search local headers and examples before web docs. Skip local-source lookup if none of the candidate paths exists.
4. For concepts, prefer official tutorials.
5. For unlisted classes, search local headers first, then the Doxygen class index.

## Output

Keep answers focused on GTSAM only:

- class/function signature
- key methods or constructor forms
- Python example when applicable
- common gotchas, especially frame conventions
- link to official docs

Target 30-50 lines. If multiple matches exist, list the top options and ask which one the user means.
