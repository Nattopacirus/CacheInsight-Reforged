"use client";

import React, { useState, useEffect } from "react";

interface Preset {
  id: string;
  name: string;
  cache_size: number;
  block_size: number;
  mapping_type: string;
  n_way: number;
  replacement_policy: string;
  created_at: string;
}

interface PresetManagerProps {
  onApplyPreset: (cacheSize: number, blockSize: number, mappingType: string, nWay: number) => void;
  currentConfig: {
    cacheSize: number;
    blockSize: number;
    mappingType: string;
    nWay: number;
  };
}

export default function PresetManager({ onApplyPreset, currentConfig }: PresetManagerProps) {
  const [presets, setPresets] = useState<Preset[]>([]);
  const [selectedPresetId, setSelectedPresetId] = useState<string>("");
  const [isSaving, setIsSaving] = useState(false);

  const fetchPresets = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/presets");
      if (res.ok) {
        const data = await res.json();
        setPresets(data);
      }
    } catch (err) {
      console.error("Failed to fetch presets", err);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchPresets();
  }, []);

  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const id = e.target.value;
    setSelectedPresetId(id);
    
    if (id === "") return;

    const preset = presets.find(p => String(p.id) === id);
    if (preset) {
      onApplyPreset(preset.cache_size, preset.block_size, preset.mapping_type, preset.n_way);
    }
  };

  const handleSave = async () => {
    const name = window.prompt("Enter a name for this new preset:");
    if (!name || name.trim() === "") return;

    setIsSaving(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/presets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name.trim(),
          cache_size: currentConfig.cacheSize,
          block_size: currentConfig.blockSize,
          mapping_type: currentConfig.mappingType,
          n_way: currentConfig.nWay,
          replacement_policy: "LRU"
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        alert(`Failed to save preset: ${errData.detail || "Unknown error"}`);
      } else {
        alert("Preset saved successfully!");
        await fetchPresets();
        setSelectedPresetId(""); // reset selection to custom so user knows it's saved
      }
    } catch (err: unknown) {
      alert(`Error saving preset: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 bg-zinc-50 dark:bg-zinc-800/50 p-4 rounded-lg mb-6 border border-zinc-100 dark:border-zinc-800">
      <div className="flex-1 w-full">
        <label className="block text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-1">Load Preset</label>
        <select 
          value={selectedPresetId}
          onChange={handleSelect}
          className="w-full p-2 rounded-lg border border-zinc-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-50"
        >
          <option value="">-- Custom (No Preset) --</option>
          {presets.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>
      <div className="flex-none w-full sm:w-auto self-end sm:self-auto">
        <button 
          onClick={handleSave}
          disabled={isSaving}
          type="button"
          className="w-full sm:w-auto px-4 py-2 mt-1 sm:mt-5 text-sm font-medium bg-white dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 rounded-lg transition-colors disabled:opacity-50"
        >
          {isSaving ? "Saving..." : "Save as Preset"}
        </button>
      </div>
    </div>
  );
}
