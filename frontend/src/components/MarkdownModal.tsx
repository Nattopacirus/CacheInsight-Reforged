"use client";

import React, { useState, useEffect, useId } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import mermaid from "mermaid";

function MermaidGraph({ chart }: { chart: string }) {
  const [svg, setSvg] = useState<string>('');
  const id = useId(); 

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: 'default' });
    const renderChart = async () => {
      try {
        const uniqueId = `mermaid-${id.replace(/:/g, '')}-${Math.random().toString(36).substring(2, 7)}`;
        const { svg: renderedSvg } = await mermaid.render(uniqueId, chart);
        setSvg(renderedSvg);
      } catch (e) {
        console.error("Mermaid rendering failed:", e);
      }
    };
    renderChart();
  }, [chart, id]);

  if (!svg) return <div className="text-center py-4 text-zinc-500">Loading graph...</div>;
  return <div className="flex justify-center my-4" dangerouslySetInnerHTML={{ __html: svg }} />;
}

interface MarkdownModalProps {
  isOpen: boolean;
  onClose: () => void;
  markdownUrls: string[];
}

export default function MarkdownModal({ isOpen, onClose, markdownUrls }: MarkdownModalProps) {
  const [contents, setContents] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [currentPage, setCurrentPage] = useState<number>(0);

  useEffect(() => {
    if (!isOpen) return;

    let isMounted = true;
    setCurrentPage(0); // Reset page on open
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLoading(true);

    Promise.all(
      markdownUrls.map(url => {
        if (url.match(/\.(png|jpe?g|gif|webp)$/i)) {
          // If it's an image, just return a markdown image tag
          return Promise.resolve(`![Image](${url})`);
        }
        return fetch(url).then(res => {
          if (!res.ok) throw new Error(`Failed to load ${url}`);
          return res.text();
        });
      })
    )
      .then((texts) => {
        if (isMounted) {
          setContents(texts);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setContents(["Error loading content. " + (err instanceof Error ? err.message : "")]);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [isOpen, markdownUrls]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white dark:bg-zinc-900 rounded-xl shadow-2xl w-full max-w-3xl max-h-[85vh] overflow-hidden flex flex-col border border-zinc-200 dark:border-zinc-800">
        <div className="flex justify-between items-center p-4 border-b border-zinc-100 dark:border-zinc-800">
          <h3 className="text-lg font-bold text-zinc-900 dark:text-zinc-50">Information</h3>
          <button
            onClick={onClose}
            className="text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 transition-colors"
            aria-label="Close"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="p-6 overflow-y-auto flex-1">
          {loading ? (
            <div className="flex justify-center items-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <div className="prose prose-zinc dark:prose-invert max-w-none">
              <ReactMarkdown 
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex]}
                components={{
                  code(props) {
                    const { children, className, node, ...rest } = props;
                    const match = /language-(\w+)/.exec(className || "");
                    if (match && match[1] === "mermaid") {
                      return <MermaidGraph chart={String(children).replace(/\n$/, "")} />;
                    }
                    return (
                      <code {...rest} className={className}>
                        {children}
                      </code>
                    );
                  }
                }}
              >
                {contents[currentPage] || ""}
              </ReactMarkdown>
            </div>
          )}
        </div>
        {!loading && contents.length > 1 && (
          <div className="flex justify-between items-center p-4 border-t border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
            <button
              onClick={() => setCurrentPage(p => Math.max(0, p - 1))}
              disabled={currentPage === 0}
              className="px-4 py-2 bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium text-sm"
            >
              &larr; Previous
            </button>
            <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
              Page {currentPage + 1} of {contents.length}
            </span>
            <button
              onClick={() => setCurrentPage(p => Math.min(contents.length - 1, p + 1))}
              disabled={currentPage === contents.length - 1}
              className="px-4 py-2 bg-blue-600 text-white border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium text-sm"
            >
              Next &rarr;
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
