type SiteLogoProps = {
  className?: string;
};

export function SiteLogo({ className = "" }: SiteLogoProps) {
  return (
    <div
      className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-800 ring-1 ring-slate-700/80 ${className}`}
      aria-hidden
    >
      <span className="text-2xl leading-none">🌍</span>
    </div>
  );
}
