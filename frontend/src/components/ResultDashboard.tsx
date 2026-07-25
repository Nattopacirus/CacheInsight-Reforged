"use client";

import React from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

interface ResultDashboardProps {
  result: {
    hits: number;
    misses: number;
    hit_rate: number;
    miss_rate: number;
    total_accesses: number;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    config: any;
  };
}

export default function ResultDashboard({ result }: ResultDashboardProps) {
  const chartData = {
    labels: ["Hits", "Misses"],
    datasets: [
      {
        data: [result.hits || 0, result.misses || 0],
        backgroundColor: ["#3b82f6", "#ef4444"],
        hoverBackgroundColor: ["#2563eb", "#dc2626"],
        borderWidth: 0,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom" as const,
        labels: {
          color: "#71717a",
        },
      },
    },
  };

  return (
    <div className="w-full max-w-4xl mt-8 flex flex-col md:flex-row gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Big Numbers Card */}
      <div className="flex-1 bg-white dark:bg-zinc-900 rounded-xl shadow-lg border border-zinc-200 dark:border-zinc-800 p-8 flex flex-col justify-center gap-6">
        <div>
          <p className="text-zinc-500 text-sm font-semibold uppercase tracking-wider">Hit Rate</p>
          <p className="text-5xl font-extrabold text-blue-600">{(result.hit_rate || 0).toFixed(2)}%</p>
        </div>
        <div>
          <p className="text-zinc-500 text-sm font-semibold uppercase tracking-wider">Miss Rate</p>
          <p className="text-4xl font-bold text-red-500">{(result.miss_rate || 0).toFixed(2)}%</p>
        </div>
        <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800">
          <p className="text-zinc-500 text-sm font-semibold uppercase tracking-wider">Total Accesses</p>
          <p className="text-2xl font-semibold text-zinc-800 dark:text-zinc-200">{(result.total_accesses || 0).toLocaleString()}</p>
        </div>
      </div>

      {/* Chart Card */}
      <div className="flex-1 bg-white dark:bg-zinc-900 rounded-xl shadow-lg border border-zinc-200 dark:border-zinc-800 p-8 flex flex-col items-center justify-center">
        <h3 className="text-lg font-semibold text-zinc-800 dark:text-zinc-200 mb-6 w-full text-left">Hits vs Misses</h3>
        <div className="relative w-full h-64">
          <Pie data={chartData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}
