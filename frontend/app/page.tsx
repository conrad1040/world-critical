import Link from "next/link";

type Event = {
  id: number;
  title: string;
  summary: string;
  category: string;
  importance_score: number;
  article_count: number;
  source_count: number;
};

export default async function Home() {
  const response = await fetch("http://127.0.0.1:8000/events", {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load events");
  }

  const data: { events: Event[] } = await response.json();

  return (
    <main className="min-h-screen bg-gray-100 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <h1 className="mb-8 text-4xl font-bold">World Critical</h1>

        <div className="space-y-6">
          {data.events.map((event) => (
            <Link
              key={event.id}
              href={`/events/${event.id}`}
              className="block"
            >
              <article className="rounded-xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md">
                <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-red-600">
                  {event.category}
                </p>

                <h2 className="text-2xl font-bold">{event.title}</h2>

                <p className="mt-3 leading-7 text-gray-700">
                  {event.summary}
                </p>

                <div className="mt-5 flex flex-wrap gap-5 text-sm text-gray-500">
                  <span>Importance: {event.importance_score}</span>
                  <span>{event.article_count} articles</span>
                  <span>{event.source_count} sources</span>
                </div>
              </article>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}