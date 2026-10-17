import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { approve, canonicalPath, existingWriteRoots, mayWrite, normalizeToolPath, sandboxArgs, sandboxOperations } from "../../pi/permissions/policy.mjs";

const fixture = mkdtempSync(path.join(os.tmpdir(), "pi-permissions-test-"));
const allowed = path.join(fixture, "allowed");
const outside = path.join(fixture, "outside");
mkdirSync(allowed); mkdirSync(outside);
process.on("exit", () => rmSync(fixture, { recursive: true, force: true }));

test("write policy resolves traversal, existing and dangling symlink escapes", () => {
  symlinkSync(outside, path.join(allowed, "escape"));
  symlinkSync(path.join(outside, "missing"), path.join(allowed, "dangling"));
  assert.equal(mayWrite(path.join(allowed, "new/deep/file"), [allowed]), true);
  assert.equal(mayWrite(`${allowed}/../outside/file`, [allowed]), false);
  assert.equal(mayWrite(path.join(allowed, "escape/file"), [allowed]), false);
  assert.equal(mayWrite(path.join(allowed, "dangling/file"), [allowed]), false);
  assert.equal(mayWrite(`${allowed}-lookalike/file`, [allowed]), false);
  assert.equal(canonicalPath(`${allowed}/escape/../new`), path.join(fixture, "new"));
  mkdirSync(path.join(outside, "subdir"));
  symlinkSync(path.join(outside, "subdir"), path.join(allowed, "nested"));
  symlinkSync("nested/../victim", path.join(allowed, "alias"));
  assert.equal(canonicalPath(path.join(allowed, "alias")), path.join(outside, "victim"));
  assert.equal(mayWrite(path.join(allowed, "alias"), [allowed]), false);
});

test("file tool spellings use Pi normalization before the write decision", () => {
  for (const input of ["@~/outside/file", `file://${outside}/file`, "../outside/file"]) {
    assert.equal(mayWrite(normalizeToolPath(input, allowed, fixture), [allowed]), false);
  }
  assert.throws(() => normalizeToolPath("bad\0path", allowed));
});

test("write roots include only existing configured directories and reject broad roots", () => {
  assert.deepEqual(existingWriteRoots({ writeRoots: [allowed, allowed, path.join(fixture, "missing")] }), [allowed]);
  assert.throws(() => existingWriteRoots({ writeRoots: ["/"] }));
  assert.throws(() => existingWriteRoots({ writeRoots: [os.homedir()] }));
});

test("manual exceptions require positive UI confirmation and cancellation fails closed", async () => {
  let prompts = 0;
  const ctx = { hasUI: true, ui: { confirm: async () => { prompts++; return true; } } };
  assert.equal(await approve(ctx, "title", "detail"), true);
  assert.equal(await approve(ctx, "title", "detail"), true);
  assert.equal(prompts, 2);
  assert.equal(await approve({ hasUI: false }, "title", "detail"), false);
  assert.equal(await approve({ hasUI: true, ui: { confirm: async () => undefined } }, "t", "d"), false);
  assert.equal(await approve(ctx, "t", "d", AbortSignal.abort()), false);
});

test("shell transport keeps command text quoted and clears host-shell startup hooks", async () => {
  let observed;
  const local = { exec: async (...args) => { observed = args; return { exitCode: 0 }; } };
  await sandboxOperations(local, [allowed]).exec("echo 'quoted'\n$(false)", allowed, { env: { BASH_ENV: "evil", ENV: "evil" }, onData() {} });
  assert.equal(observed[2].env.BASH_ENV, undefined);
  assert.equal(observed[2].env.ENV, undefined);
  assert.match(observed[0], /^exec \/usr\/bin\/bwrap /);
});

test("Linux sandbox blocks direct, traversal and symlink writes while allowing reads and network/local binding", { skip: process.env.PI_TEST_BWRAP !== "1" }, () => {
  symlinkSync(outside, path.join(allowed, "shell-escape"));
  const program = `
set -eu
cat /etc/os-release >/dev/null
printf allowed > '${allowed}/written'
if printf blocked > '${outside}/direct' 2>/dev/null; then exit 81; fi
if printf blocked > '${allowed}/../outside/traversal' 2>/dev/null; then exit 82; fi
if printf blocked > '${allowed}/shell-escape/symlink' 2>/dev/null; then exit 83; fi
python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); s.listen(); c=socket.create_connection(s.getsockname()); a,_=s.accept(); c.send(b"ok"); assert a.recv(2)==b"ok"; socket.getaddrinfo("example.com",443)'
`;
  const result = spawnSync("/usr/bin/bwrap", sandboxArgs(program, allowed, [allowed]), { encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(readFileSync(path.join(allowed, "written"), "utf8"), "allowed");
  for (const name of ["direct", "traversal", "symlink"]) assert.throws(() => readFileSync(path.join(outside, name)));
});
