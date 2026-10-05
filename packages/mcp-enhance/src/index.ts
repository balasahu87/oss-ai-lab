#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

const MEM_DIR = process.env.MCP_ENHANCE_MEMORY_DIR || join(homedir(), ".oss-ai-lab", "memory");
mkdirSync(MEM_DIR, { recursive: true });

function memPath(key: string) {
  const safe = key.replace(/[^a-zA-Z0-9._-]/g, "_");
  return join(MEM_DIR, `${safe}.txt`);
}

const server = new McpServer({
  name: "mcp-enhance",
  version: "0.1.0",
});

server.tool(
  "memory_set",
  "Store a persistent note by key",
  { key: z.string(), value: z.string() },
  async ({ key, value }) => {
    writeFileSync(memPath(key), value, "utf8");
    return { content: [{ type: "text", text: `stored ${key}` }] };
  },
);

server.tool(
  "memory_get",
  "Read a persistent note by key",
  { key: z.string() },
  async ({ key }) => {
    const p = memPath(key);
    if (!existsSync(p)) {
      return { content: [{ type: "text", text: `missing: ${key}` }] };
    }
    return { content: [{ type: "text", text: readFileSync(p, "utf8") }] };
  },
);

server.tool(
  "memory_list",
  "List memory keys",
  {},
  async () => {
    const { readdirSync } = await import("node:fs");
    const keys = readdirSync(MEM_DIR)
      .filter((f) => f.endsWith(".txt"))
      .map((f) => f.replace(/\.txt$/, ""));
    return { content: [{ type: "text", text: keys.join("\n") || "(empty)" }] };
  },
);

server.tool(
  "web_fetch",
  "Fetch a URL and return truncated plain text (http/https only)",
  {
    url: z.string().url(),
    max_chars: z.number().int().min(200).max(50000).optional(),
  },
  async ({ url, max_chars }) => {
    const u = new URL(url);
    if (!["http:", "https:"].includes(u.protocol)) {
      return { content: [{ type: "text", text: "error: only http/https allowed" }], isError: true };
    }
    const res = await fetch(url, {
      headers: { "User-Agent": "mcp-enhance/0.1 (+oss-ai-lab)" },
      signal: AbortSignal.timeout(15000),
    });
    const text = await res.text();
    const stripped = text
      .replace(/<script[\s\S]*?<\/script>/gi, " ")
      .replace(/<style[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim();
    const limit = max_chars ?? 8000;
    return {
      content: [
        {
          type: "text",
          text: `status=${res.status}\n` + stripped.slice(0, limit),
        },
      ],
    };
  },
);

server.tool(
  "structured_repair",
  "Return a repair prompt for invalid JSON (host LLM should run it)",
  {
    broken: z.string(),
    schema_hint: z.string().optional(),
  },
  async ({ broken, schema_hint }) => {
    const prompt =
      "Fix the following into valid JSON only (no markdown fences).\n" +
      `Schema hint: ${schema_hint || "any object"}\n\n` +
      broken;
    return { content: [{ type: "text", text: prompt }] };
  },
);

server.tool(
  "rag_retrieve",
  "Retrieve grounded context via ragline CLI if installed",
  {
    question: z.string(),
    index: z.string().optional(),
  },
  async ({ question, index }) => {
    const idx = index || ".ragline_index";
    const r = spawnSync("ragline", ["ask", question, "--index", idx], {
      encoding: "utf8",
      timeout: 30000,
    });
    if (r.error) {
      return {
        content: [
          {
            type: "text",
            text:
              "ragline not available on PATH. Install Python package: " +
              "pip install -e packages/ragline && ragline index sample_docs",
          },
        ],
        isError: true,
      };
    }
    const out = (r.stdout || "") + (r.stderr || "");
    return { content: [{ type: "text", text: out || `exit=${r.status}` }] };
  },
);

async function main() {
  if (process.argv.includes("--help") || process.argv.includes("-h")) {
    console.log(`mcp-enhance — MCP capability server (stdio)

Tools: memory_set, memory_get, memory_list, web_fetch, structured_repair, rag_retrieve

Usage:
  node dist/index.js          # speak MCP on stdio
  MCP_ENHANCE_MEMORY_DIR=...  # optional memory path
`);
    process.exit(0);
  }
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
