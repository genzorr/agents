import { lstatSync, readlinkSync, realpathSync, statSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function normalizeToolPath(raw, cwd, home = homedir()) {
  if (typeof raw !== "string" || raw.includes("\0")) throw new Error("Invalid file path");
  let value = raw.replace(/[\u00A0\u2000-\u200A\u202F\u205F\u3000]/g, " ");
  if (value.startsWith("@")) value = value.slice(1);
  if (value === "~") value = home;
  else if (value.startsWith("~/")) value = path.join(home, value.slice(2));
  else if (value.startsWith("file://")) value = fileURLToPath(value);
  return path.resolve(cwd, value);
}

// Resolve each component before consuming '..', including dangling symlinks.
export function canonicalPath(value, hops = 0) {
  if (hops > 40) throw new Error("Too many symlinks");
  const absolute = path.isAbsolute(value) ? value : `${process.cwd()}/${value}`;
  let current = path.parse(absolute).root;
  const parts = absolute.slice(current.length).split(path.sep);
  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (!part || part === ".") continue;
    if (part === "..") { current = path.dirname(current); continue; }
    current = path.join(current, part);
    try {
      if (lstatSync(current).isSymbolicLink()) {
        const link = readlinkSync(current);
        const target = path.isAbsolute(link) ? link : `${path.dirname(current)}/${link}`;
        return canonicalPath(`${target}/${parts.slice(i + 1).join("/")}`, hops + 1);
      }
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  return current;
}

export function existingWriteRoots(profile, { home = homedir(), temporary = tmpdir() } = {}) {
  const roots = [];
  for (const entry of profile.writeRoots) {
    const expanded = entry === "$TMPDIR" ? temporary : entry.startsWith("~/") ? path.join(home, entry.slice(2)) : entry;
    if (!path.isAbsolute(expanded)) throw new Error("Write roots must be absolute");
    try {
      if (!statSync(expanded).isDirectory()) continue;
      const root = realpathSync(expanded);
      if (root === "/" || root === realpathSync(home)) throw new Error("Refusing a broad write root");
      if (!roots.includes(root)) roots.push(root);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  return roots;
}

export function mayWrite(target, roots) {
  const resolved = canonicalPath(target);
  return roots.some((root) => resolved === root || resolved.startsWith(`${root}${path.sep}`));
}

export function sandboxArgs(command, cwd, roots) {
  const args = ["--die-with-parent", "--new-session", "--unshare-user", "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--cap-drop", "ALL", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc"];
  for (const root of roots) args.push("--bind", root, root);
  args.push("--chdir", cwd, "--", "/bin/bash", "--noprofile", "--norc", "-c", command);
  return args;
}

export const shellQuote = (value) => `'${value.replaceAll("'", `'"'"'`)}'`;

export function sandboxOperations(local, roots) {
  return {
    exec(command, cwd, options) {
      const env = { ...process.env, ...options.env };
      // Pi's local backend starts a host shell before executing bubblewrap.
      delete env.BASH_ENV;
      delete env.ENV;
      const wrapped = ["exec", "/usr/bin/bwrap", ...sandboxArgs(command, cwd, roots).map(shellQuote)].join(" ");
      return local.exec(wrapped, cwd, { ...options, env });
    },
  };
}

export async function approve(ctx, title, detail, signal) {
  if (!ctx.hasUI || signal?.aborted) return false;
  return (await ctx.ui.confirm(title, detail, { signal, timeout: 60_000 })) === true;
}
