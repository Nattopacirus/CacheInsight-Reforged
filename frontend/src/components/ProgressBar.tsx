"use client";

import React from "react";

interface ProgressBarProps {
  progress: number;
  status: string;
}

export default function ProgressBar({ progress, status }: ProgressBarProps) {
  let barColor = "bg-blue-600";
  let textColor = "text-blue-600";
  
  if (status === "Completed") {
    barColor = "bg-green-500";
    textColor = "text-green-500";
  } else if (status === "Failed") {
    barColor = "bg-red-500";
    textColor = "text-red-500";
  }

  return (
    <div className="w-full max-w-2xl flex flex-col gap-3">
      <div className="flex justify-between items-center text-sm font-semibold">
        <span className="text-zinc-700 dark:text-zinc-300">Status: <span className={textColor}>{status}</span></span>
        <span className="text-zinc-700 dark:text-zinc-300">{progress}%</span>
      </div>
      <div className="w-full bg-zinc-200 dark:bg-zinc-800 rounded-full h-4 overflow-hidden shadow-inner">
        <div 
          className={`${barColor} h-4 rounded-full transition-all duration-500 ease-out`} 
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
}
