"use client";

import { useState } from "react";
import SimulationForm from "@/components/SimulationForm";

export default function Home() {
  const [jobId, setJobId] = useState<string | null>(null);

  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black p-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight text-zinc-900 dark:text-white sm:text-5xl mb-4">
          Cache<span className="text-blue-600">Insight</span> Reforged
        </h1>
        <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-xl mx-auto">
          High-performance cache simulator built with Next.js and FastAPI.
        </p>
      </header>

      <main className="flex w-full max-w-4xl flex-col items-center justify-center">
        {!jobId ? (
          <SimulationForm onJobStarted={(id) => setJobId(id)} />
        ) : (
          <div className="p-8 bg-white dark:bg-zinc-900 rounded-xl shadow-lg border border-zinc-200 dark:border-zinc-800 w-full text-center">
            <h2 className="text-2xl font-bold mb-4">Simulation Started</h2>
            <p className="text-zinc-600 dark:text-zinc-400 mb-6">
              Job ID: <span className="font-mono bg-zinc-100 dark:bg-zinc-800 p-1 rounded">{jobId}</span>
            </p>
            <p className="text-blue-600 animate-pulse">Progress bar coming soon in STORY-7...</p>
            <button 
              onClick={() => setJobId(null)}
              className="mt-8 px-6 py-2 border border-zinc-300 dark:border-zinc-700 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              Start New Simulation
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
