import type { NextConfig } from "next";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

function readRootEnv(): Record<string, string> {
  const rootEnvPath = resolve(process.cwd(), "../../.env.local");
  if (!existsSync(rootEnvPath)) return {};

  return Object.fromEntries(
    readFileSync(rootEnvPath, "utf8")
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("#") && line.includes("="))
      .map((line) => {
        const [key, ...valueParts] = line.split("=");
        return [key.trim(), valueParts.join("=").trim().replace(/^['"]|['"]$/g, "")];
      }),
  );
}

const rootEnv = readRootEnv();

const nextConfig: NextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_BASE_URL:
      process.env.NEXT_PUBLIC_API_BASE_URL ??
      rootEnv.NEXT_PUBLIC_API_BASE_URL ??
      "http://localhost:8000",
    NEXT_PUBLIC_GOOGLE_MAPS_API_KEY:
      process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ??
      rootEnv.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ??
      rootEnv.GOOGLE_MAPS_API_KEY ??
      "",
  },
};

export default nextConfig;
