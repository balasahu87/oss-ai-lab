import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

test("dist entry exists and mentions tools", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const src = readFileSync(join(here, "index.js"), "utf8");
  assert.match(src, /memory_set/);
  assert.match(src, /web_fetch/);
  assert.match(src, /rag_retrieve/);
});
