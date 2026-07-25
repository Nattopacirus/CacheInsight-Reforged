"use client";

import React, { useState } from "react";
import { isPowerOfTwo } from "@/utils/validation";
import PresetManager from "./PresetManager";
import MarkdownModal from "./MarkdownModal";

interface SimulationFormProps {
  onJobStarted: (jobId: string) => void;
}

export default function SimulationForm({ onJobStarted }: SimulationFormProps) {
  const [cacheSize, setCacheSize] = useState<number>(32);
  const [blockSize, setBlockSize] = useState<number>(64);
  const [mappingType, setMappingType] = useState<string>("Direct");
  const [nWay, setNWay] = useState<number>(4);
  const [file, setFile] = useState<File | null>(null);
  
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isModalOpen, setModalOpen] = useState(false);

  const isCacheSizeValid = isPowerOfTwo(cacheSize);
  const isBlockSizeValid = isPowerOfTwo(blockSize);
  const isNWayValid = isPowerOfTwo(nWay);

  const isFormValid = isCacheSizeValid && isBlockSizeValid && file !== null && (mappingType !== "Set" || isNWayValid);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFormValid || !file) return;

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const config = {
        cache_size: cacheSize,
        block_size: blockSize,
        mapping_type: mappingType,
        n_way: mappingType === "Set" ? nWay : undefined,
        replacement_policy: "LRU" // Default
      };

      const formData = new FormData();
      formData.append("file", file);
      formData.append("config", JSON.stringify(config));

      const res = await fetch("http://127.0.0.1:8000/api/simulate", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to start simulation");
      }

      const data = await res.json();
      onJobStarted(data.job_id);

    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-zinc-900 p-8 rounded-xl shadow-lg border border-zinc-200 dark:border-zinc-800 w-full max-w-2xl">
      <h2 className="text-2xl font-bold mb-6 text-zinc-900 dark:text-zinc-50">Cache Simulation Setup</h2>
      
      <PresetManager 
        onApplyPreset={(cSize, bSize, mType, nWay) => {
          setCacheSize(cSize);
          setBlockSize(bSize);
          setMappingType(mType);
          setNWay(nWay);
        }}
        currentConfig={{
          cacheSize,
          blockSize,
          mappingType,
          nWay
        }}
      />
      
      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          
          {/* Cache Size */}
          <div className="flex flex-col gap-2">
            <label className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Cache Size (KB)</label>
            <input 
              type="number" 
              value={cacheSize} 
              onChange={(e) => setCacheSize(Number(e.target.value))}
              className={`p-3 rounded-lg border focus:outline-none focus:ring-2 bg-transparent ${isCacheSizeValid ? 'border-zinc-300 focus:ring-blue-500' : 'border-red-500 focus:ring-red-500'}`}
              min="1"
            />
            {!isCacheSizeValid && <p className="text-sm text-red-500">Must be a power of 2 (e.g. 2, 4, 8, 16)</p>}
          </div>

          {/* Block Size */}
          <div className="flex flex-col gap-2">
            <label className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Block Size (Bytes)</label>
            <input 
              type="number" 
              value={blockSize} 
              onChange={(e) => setBlockSize(Number(e.target.value))}
              className={`p-3 rounded-lg border focus:outline-none focus:ring-2 bg-transparent ${isBlockSizeValid ? 'border-zinc-300 focus:ring-blue-500' : 'border-red-500 focus:ring-red-500'}`}
              min="1"
            />
            {!isBlockSizeValid && <p className="text-sm text-red-500">Must be a power of 2</p>}
          </div>

          {/* Mapping Type */}
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <label className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Mapping Type</label>
              <button
                type="button"
                onClick={() => setModalOpen(true)}
                className="text-blue-500 hover:text-blue-600 flex items-center justify-center rounded-full w-5 h-5 bg-blue-50 dark:bg-blue-900/30 text-xs font-bold transition-colors"
                title="What is this?"
              >
                i
              </button>
            </div>
            <select 
              value={mappingType} 
              onChange={(e) => setMappingType(e.target.value)}
              className="p-3 rounded-lg border border-zinc-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-transparent text-zinc-900 dark:text-zinc-50"
            >
              <option value="Direct" className="dark:bg-zinc-800">Direct-Mapped</option>
              <option value="Fully" className="dark:bg-zinc-800">Fully Associative</option>
              <option value="Set" className="dark:bg-zinc-800">Set-Associative</option>
            </select>
          </div>

          {/* N-way (Conditional) */}
          {mappingType === "Set" && (
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">N-way Associativity</label>
              <input 
                type="number" 
                value={nWay} 
                onChange={(e) => setNWay(Number(e.target.value))}
                className={`p-3 rounded-lg border focus:outline-none focus:ring-2 bg-transparent ${isNWayValid ? 'border-zinc-300 focus:ring-blue-500' : 'border-red-500 focus:ring-red-500'}`}
                min="2"
              />
              {!isNWayValid && <p className="text-sm text-red-500">Must be a power of 2</p>}
            </div>
          )}
        </div>

        {/* File Input */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Address Trace (.csv)</label>
          <input 
            type="file" 
            accept=".csv"
            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
            className="p-3 rounded-lg border border-zinc-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-transparent file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        {/* Error Message */}
        {errorMsg && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg text-sm">
            {errorMsg}
          </div>
        )}

        {/* Submit Button */}
        <button 
          type="submit" 
          disabled={!isFormValid || isLoading}
          className="mt-4 w-full p-4 rounded-lg bg-blue-600 text-white font-semibold shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? "Starting Simulation..." : "Run Simulation"}
        </button>

      </form>

      <MarkdownModal 
        isOpen={isModalOpen} 
        onClose={() => setModalOpen(false)} 
        markdownUrl="/docs/cache-mapping.md" 
      />
    </div>
  );
}
