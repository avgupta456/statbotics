"use client";

import { useEffect, useState } from "react";

const API_URL =
  process.env.PROD === "True" ? "https://api.statbotics.io" : "http://127.0.0.1:8000";

const STORAGE_KEY = "statbotics_api_key";
const STORAGE_TS_KEY = "statbotics_api_key_ts";
const COOLDOWN_MS = 60 * 60 * 1000; // 1 hour

function getStoredKey(): string | null {
  try {
    const key = localStorage.getItem(STORAGE_KEY);
    const ts = localStorage.getItem(STORAGE_TS_KEY);
    if (!key || !ts) return null;
    if (Date.now() > parseInt(ts) + COOLDOWN_MS) return null;
    return key;
  } catch {
    return null;
  }
}

export default function ApiKeyPage() {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const stored = getStoredKey();
    if (stored) {
      setApiKey(stored);
      return;
    }
    const counter = Math.floor(Math.random() * 0xffffffff);
    fetch(`${API_URL}/generate_key/${counter}`)
      .then((res) => res.json())
      .then((data) => {
        localStorage.setItem(STORAGE_KEY, data.key);
        localStorage.setItem(STORAGE_TS_KEY, String(Date.now()));
        setApiKey(data.key);
      });
  }, []);

  const copyToClipboard = () => {
    if (apiKey) {
      navigator.clipboard.writeText(apiKey);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="w-full container mx-auto flex-grow p-8 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-4">API Key</h1>
      <p className="text-gray-600 mb-2 text-center max-w-lg">
        Use this key to access the Statbotics REST API. Include it in your requests via the{" "}
        <code className="bg-gray-100 px-1 rounded">X-API-Key</code> header.
      </p>
      <p className="text-gray-500 mb-6 text-center max-w-lg text-sm">
        Rate limited to 100 requests per minute per key.
      </p>
      {apiKey ? (
        <div className="flex flex-col items-center gap-2">
          <code className="bg-gray-100 px-4 py-2 rounded text-lg font-mono select-all">
            {apiKey}
          </code>
          <button onClick={copyToClipboard} className="btn btn-sm btn-outline">
            {copied ? "Copied!" : "Copy to clipboard"}
          </button>
        </div>
      ) : (
        <p className="text-gray-400 text-sm">Loading...</p>
      )}
    </div>
  );
}
