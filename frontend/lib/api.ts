const DEFAULT_API_URL = "http://127.0.0.1:8000";

export function getApiUrl(path: string): string {
  const base =
    process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ??
    DEFAULT_API_URL;

  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  return `${base}${normalizedPath}`;
}
