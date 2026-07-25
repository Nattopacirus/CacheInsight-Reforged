"use client";

import React, { useEffect, useState } from "react";

interface Job {
  id: string;
  status: string;
  progress: number;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  result: any;
  created_at: string;
}

export default function HistoryTable() {
  const [history, setHistory] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/history");
      if (!res.ok) throw new Error("Failed to fetch history");
      const data = await res.json();
      setHistory(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error fetching history");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchHistory();
  }, []);

  return (
    <div className="w-full max-w-4xl bg-white dark:bg-zinc-900 rounded-xl shadow-lg border border-zinc-200 dark:border-zinc-800 p-8 mt-12">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">Simulation History</h2>
        <button 
          onClick={() => { setIsLoading(true); fetchHistory(); }}
          className="px-4 py-2 text-sm bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 rounded-lg transition-colors"
        >
          Refresh
        </button>
      </div>

      {isLoading ? (
        <p className="text-zinc-500 text-center py-8">Loading history...</p>
      ) : error ? (
        <p className="text-red-500 text-center py-8">{error}</p>
      ) : history.length === 0 ? (
        <p className="text-zinc-500 text-center py-8">No simulation history found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-zinc-600 dark:text-zinc-400">
            <thead className="text-xs uppercase bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300">
              <tr>
                <th className="px-6 py-3 rounded-tl-lg">Date</th>
                <th className="px-6 py-3">Configuration</th>
                <th className="px-6 py-3">Hit Rate</th>
                <th className="px-6 py-3 rounded-tr-lg">Status</th>
              </tr>
            </thead>
            <tbody>
              {history.map((job) => {
                const date = new Date(job.created_at).toLocaleString();
                const config = job.result?.config;
                const hitRate = job.result?.hit_rate;
                
                let statusColor = "text-zinc-500";
                if (job.status === "Completed") statusColor = "text-green-500 font-semibold";
                if (job.status === "Failed") statusColor = "text-red-500 font-semibold";

                return (
                  <tr key={job.id} className="border-b border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">{date}</td>
                    <td className="px-6 py-4">
                      {config ? (
                        <div className="text-xs font-mono bg-zinc-100 dark:bg-zinc-800 p-1 rounded">
                          {config.cache_size}KB, {config.block_size}B, {config.mapping_type}
                        </div>
                      ) : (
                        "-"
                      )}
                    </td>
                    <td className="px-6 py-4">
                      {hitRate !== undefined ? `${hitRate.toFixed(2)}%` : "-"}
                    </td>
                    <td className={`px-6 py-4 ${statusColor}`}>
                      {job.status}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
