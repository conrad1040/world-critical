import Link from "next/link";

import { SearchForm } from "./search-form";
import { SiteLogo } from "./site-logo";

type SiteHeaderProps = {
  defaultSearchQuery?: string;
  showSearch?: boolean;
};

function formatToday(): string {
  return new Intl.DateTimeFormat("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  }).format(new Date());
}

export function SiteHeader({
  defaultSearchQuery = "",
  showSearch = true,
}: SiteHeaderProps) {
  return (
    <header className="border-b border-slate-800 bg-slate-900 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-6 py-4 sm:flex-row sm:items-center sm:justify-between sm:gap-6">
        <Link href="/" className="group min-w-0">
          <div className="flex items-center gap-3.5 sm:gap-4">
            <SiteLogo />

            <p className="text-3xl font-black tracking-tight text-white transition group-hover:text-slate-200 sm:text-4xl">
              World Critical
            </p>
          </div>

          <div className="mt-1 ml-[3.625rem] space-y-0.5 sm:ml-[3.75rem]">
            <p className="text-sm font-medium text-slate-200">
              The few stories that matter today.
            </p>

            <p className="text-xs text-slate-300">{formatToday()}</p>
          </div>
        </Link>

        {showSearch && (
          <div className="w-full sm:w-auto sm:min-w-[15rem] sm:max-w-sm lg:max-w-md">
            <SearchForm
              defaultQuery={defaultSearchQuery}
              variant="header"
            />
          </div>
        )}
      </div>
    </header>
  );
}
