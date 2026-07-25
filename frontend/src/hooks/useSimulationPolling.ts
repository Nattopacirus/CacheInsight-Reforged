import { useEffect, useState } from 'react';

export function useSimulationPolling(jobId: string | null) {
  const [progress, setProgress] = useState<number>(0);
  const [status, setStatus] = useState<string>("Idle");
  const [result, setResult] = useState<unknown>(null);
  const [prevJobId, setPrevJobId] = useState<string | null>(null);

  if (jobId !== prevJobId) {
    setPrevJobId(jobId);
    setProgress(0);
    setStatus("Idle");
    setResult(null);
  }

  useEffect(() => {
    if (!jobId) return;

    
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/simulate/${jobId}`);
        const data = await res.json();
        
        setProgress(data.progress);
        setStatus(data.status);
        
        if (data.status === "Completed" || data.status === "Failed") {
          setResult(data.result);
          clearInterval(interval);
        }
      } catch (err) {
        console.error("Polling error", err instanceof Error ? err.message : err);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [jobId]);

  return { progress, status, result };
}
