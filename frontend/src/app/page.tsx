"use client";

import { useState } from "react";
import SimulationForm from "@/components/SimulationForm";
import ProgressBar from "@/components/ProgressBar";
import ResultDashboard from "@/components/ResultDashboard";
import HistoryTable from "@/components/HistoryTable";
import { useSimulationPolling } from "@/hooks/useSimulationPolling";

export default function Home() {
  const [jobId, setJobId] = useState<string | null>(null);
  const { progress, status, result } = useSimulationPolling(jobId);

  return (
    <div className="flex flex-col min-h-screen items-center justify-start bg-zinc-50 font-sans dark:bg-black p-8 pb-20">
      <header className="mt-8 mb-12 text-center">
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
          <div className="p-8 bg-white dark:bg-zinc-900 rounded-xl shadow-lg border border-zinc-200 dark:border-zinc-800 w-full text-center flex flex-col items-center">
            <h2 className="text-2xl font-bold mb-4 text-zinc-900 dark:text-white">Simulation Progress</h2>
            <p className="text-zinc-600 dark:text-zinc-400 mb-8">
              Job ID: <span className="font-mono bg-zinc-100 dark:bg-zinc-800 p-1 rounded text-sm">{jobId}</span>
            </p>
            
            {status !== "Completed" && (
              <ProgressBar progress={progress} status={status} />
            )}
            
            {status === "Completed" && result !== null && (
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              <ResultDashboard result={result as any} />
            )}
            
            {status === "Failed" && (
              <div className="mt-8 p-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg w-full max-w-2xl text-left shadow-sm">
                <h3 className="font-bold mb-1">Simulation Failed</h3>
                <p className="text-sm opacity-90">An error occurred during processing.</p>
              </div>
            )}

            <button 
              onClick={() => setJobId(null)}
              className="mt-10 px-6 py-2 border border-zinc-300 dark:border-zinc-700 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-zinc-800 dark:text-zinc-200"
            >
              Start New Simulation
            </button>
          </div>
        )}

        {/* History Table */}
        <div className="w-full mt-12 flex justify-center" key={status === "Completed" ? jobId : "default"}>
          <HistoryTable />
        </div>
      </main>
    </div>
  );
}
