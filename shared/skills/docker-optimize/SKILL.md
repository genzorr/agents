---
name: docker-optimize
description: Create, review, or optimize Dockerfiles and .dockerignore files for small, cache-efficient, maintainable, and production-usable images. Use when the user asks about Dockerfile best practices, image size, layer ordering, preserving build cache across rebuilds, RUN formatting, multi-stage builds, hadolint findings, BuildKit cache mounts, or container image cleanup.
---

# Docker Optimize

Create Dockerfiles that are boring to maintain, fast to rebuild, and small enough to ship.

## Workflow

1. Inspect the project before editing: language, package manager, lockfiles, build output, runtime command, ports, native dependencies, and existing Docker/Compose/CI files.
2. Decide the target image type: development, test/CI, production service, CLI tool, or builder-only artifact. Optimize for that target, not for a generic minimal image.
3. Use multi-stage builds when build tools, compilers, dev dependencies, test fixtures, or source trees are not needed at runtime.
4. Order layers by cache invalidation:
   - stable, expensive dependency setup before frequently changing source;
   - lockfiles/manifests before application code;
   - volatile build arguments, generated files, and source copies as late as practical.
5. Group related commands by lifecycle and volatility so reviewers can see the build shape and cache invalidation stays predictable.
6. Preserve build cache across repeated attempts. Treat Docker/BuildKit cache as useful state, not disposable output.
7. Keep the build context small with `.dockerignore`. Start from project reality; tools like `npx untracked > .dockerignore` can seed ignore rules for Node-style projects, but review the output before using it.
8. Format `RUN`, `COPY`, `ENV`, and package lists for reviewability and shell correctness.
9. Remove build-only dependencies, package indexes, temp files, caches, credentials, and test artifacts from the final image.
10. Validate with `hadolint`, a real `docker build`, and a smoke run when Docker is available.

## Design Rules

- Prefer trusted, minimal base images that match runtime needs. Avoid `latest`; pin meaningful version tags, and use digest pins when reproducibility or supply-chain auditability matters.
- Do not chase tiny images at the cost of unusable runtime behavior. Keep CA certificates, timezone/locale data, shared libraries, shells, or debugging hooks only when the application actually needs them.
- Do not install convenience tools in production images unless there is a concrete operational requirement.
- Use `COPY` for local files by default. Use `ADD` only when its extra behavior is intentional, such as local tar extraction or remote source handling.
- Use absolute `WORKDIR`.
- Use a non-root `USER` when the process can run without privileges. Avoid switching users repeatedly.
- Prefer exec-form `ENTRYPOINT`/`CMD`. If an entrypoint script starts the main process, end with `exec "$@"` or the explicit executable so signals reach the app.
- Never bake secrets, SSH keys, package tokens, or cloud credentials into layers. Use BuildKit `RUN --mount=type=secret` or `--mount=type=ssh`.
- Keep one runtime concern per image. Do not bundle databases, queue workers, cron, and web apps together unless the user explicitly needs that deployment shape.

## RUN Formatting

Use readable multi-line shell with one logical package/action per line:

```Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/*
```

Rules:

- Combine `apt-get update` and `apt-get install` in the same `RUN`.
- Use `--no-install-recommends` for Debian/Ubuntu packages unless recommends are required.
- Remove `/var/lib/apt/lists/*` in the same `RUN` that installs packages.
- Sort package names alphanumerically when the list is not order-dependent.
- Put continuation backslashes at line ends and align commands consistently.
- Use `set -eux;` for complex POSIX shell blocks when useful. Do not add `pipefail` unless the shell is known to support it.
- Use heredocs for long scripts when they improve readability, but keep build logic in normal project scripts if it is reused outside Docker.

## Layer Grouping

Group commands by purpose inside each stage. The default order is:

1. Base image, shell options if needed, labels, and stable environment.
2. OS runtime packages needed by that stage.
3. Language/package-manager setup.
4. Dependency manifests and lockfiles.
5. Dependency install/restore.
6. Application source and generated assets.
7. Build, test, prune, and runtime assembly.
8. Runtime user, exposed ports, healthcheck, entrypoint, and command.

Rules:

- Put apt/apk/dnf/yum installation for a stage near the beginning of that stage when the package set is stable.
- Keep build-only OS packages in builder stages. Do not install compilers or headers in the final runtime stage unless the app needs them at runtime.
- Combine one package-manager transaction with its cleanup in the same `RUN`; do not split install and cleanup across layers.
- Do not scatter apt installs throughout a stage. If a later step reveals another package requirement, move it into the existing package install block unless doing so would make a volatile feature invalidate a stable base.
- Do not merge unrelated volatile commands into stable dependency layers just to reduce layer count.
- Prefer `COPY --chown` over a separate recursive `chown` layer when ownership is needed.
- Prefer separate stages over large conditional shell blocks when build and runtime concerns differ.

## Cache Strategy

Cache optimization is about "expensive and stable first", not simply "heavy first".

The agent must preserve cache during iterative work:

- Do not use `--no-cache`, `docker builder prune`, `docker system prune`, change builders, delete local cache directories, or rewrite cache locations unless the user explicitly asks.
- Reuse the same Dockerfile, build context path, build args, target stage, local tag, and BuildKit builder while iterating unless the change requires otherwise.
- Keep broad `COPY . .` after dependency installation whenever possible. Do not copy the whole source tree before dependency restore/install if only lockfiles/manifests are needed.
- If source code used by a build step changes, expect that step and later steps to rerun. Preserve earlier layers and use cache mounts so rebuilds continue from the closest valid point instead of downloading or compiling everything again.
- If a changed build script is part of dependency resolution, the dependency layer may correctly invalidate. Use package-manager cache mounts to avoid full network re-downloads.

Common pattern:

```Dockerfile
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .
RUN npm run build
```

Use BuildKit cache mounts for package caches when available:

- npm: `/root/.npm`
- pnpm: pnpm store path, often `/root/.local/share/pnpm/store`
- pip: `/root/.cache/pip`
- Go: `/go/pkg/mod` and `/root/.cache/go-build`
- Cargo: `/usr/local/cargo/registry`, `/usr/local/cargo/git`, and project `target`
- apt: `/var/cache/apt` and `/var/lib/apt` with `sharing=locked`

Do not rely on cache mounts for final image contents; they speed builds but are not copied into the image.

For CI, remote builders, or projects built on multiple machines, configure an external cache instead of relying only on local state:

```bash
docker buildx build --push -t <registry>/<image>:<tag> \
  --cache-from type=registry,ref=<registry>/<image>:buildcache \
  --cache-to type=registry,ref=<registry>/<image>:buildcache,mode=max \
  .
```

Use `mode=max` when intermediate multi-stage layers are expensive and worth preserving. Use separate cache refs per branch or scope when concurrent builds would overwrite each other.

Prefer BuildKit features for expensive repeated work:

- Add `# syntax=docker/dockerfile:1` when using modern `RUN --mount` features.
- Use `RUN --mount=type=cache` for dependency downloads and compiler caches.
- Use `RUN --mount=type=bind` for large source inputs that are only needed to generate an artifact and should not become image layers.
- Use stable cache IDs or targets; include `sharing=locked` for package managers such as apt that need exclusive cache access.

## Cleanup Patterns

- Prefer multi-stage copies over deleting large build artifacts after the fact.
- Prefer same-layer cleanup and selective `COPY --from` over squashing layers.
- In final stages, install only runtime dependencies.
- For Node, use lockfile installs and prune/omit dev dependencies in the runtime stage (`npm ci --omit=dev`, `pnpm install --prod`, or the project-standard equivalent).
- For Python, avoid copying virtualenv/build caches accidentally; install wheels or runtime requirements into a clean final stage when practical.
- For compiled languages, copy only the binary/assets needed to run.
- Remove package-manager indexes, temp directories, downloaded archives, test output, `.git`, docs, examples, and source maps only when the app does not need them.
- Use `.dockerignore` to keep ignored files out of the context; deleting them inside the image is too late if they were copied into earlier layers.
- Do not use `docker build --squash` by default. Squashing can make the final image look smaller in some cases, but it can hide build structure, complicate caching/scanning/debugging, and Docker may still keep the unsquashed cache layers locally. Use it only when the target builder supports it, the user explicitly wants it, and normal multi-stage/same-layer cleanup is not enough.

## Validation

Run the strongest available checks:

```bash
hadolint Dockerfile
docker build --progress=plain -t <local-tag> .
docker run --rm <local-tag> <smoke-command>
docker image inspect <local-tag> --format '{{.Size}}'
docker history --no-trunc <local-tag>
```

If `hadolint` is not installed, use the container image:

```bash
docker run --rm -i hadolint/hadolint < Dockerfile
```

When Docker is unavailable, still inspect the Dockerfile, `.dockerignore`, lockfiles, and build scripts, then state that image build/smoke validation was not run.

During iterative Dockerfile work, prefer normal cached builds and inspect the plain progress output for cache hits. Only perform no-cache builds as a deliberate final verification when the user asks or when diagnosing cache-specific breakage.

## Review Checklist

- Does the final image contain only runtime necessities?
- Are dependency layers stable across source-only edits?
- Will repeated builds preserve local or exported BuildKit cache instead of restarting from scratch?
- Are common operations grouped by lifecycle, with OS packages and dependency restores near the start of their stage?
- Are package lists sorted and easy to diff?
- Are `apt-get update`, install, and cleanup in one layer?
- Is `.dockerignore` preventing accidental context bloat?
- Are secrets handled through BuildKit mounts or runtime injection?
- Does the image run as non-root where practical?
- Are `ENTRYPOINT` and `CMD` signal-safe and override-friendly?
- Has a real build and smoke run proved the image is usable?

## References

- Docker build best practices: https://docs.docker.com/build/building/best-practices/
- Docker multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- Docker cache optimization: https://docs.docker.com/build/cache/optimize/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker image build reference: https://docs.docker.com/reference/cli/docker/image/build/
- hadolint: https://github.com/hadolint/hadolint
- untracked: https://github.com/Kikobeats/untracked
