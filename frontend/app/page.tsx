"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]); 
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setHasSearched(true);
    setResults([]); 

    try {
      const response = await fetch("https://faculty-connect.onrender.com/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query }),
      });
      
      if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
      
      const data = await response.json();
      // Ensure we are setting an array even if the backend sends something else
      setResults(Array.isArray(data.results) ? data.results : []);
      
    } catch (error) {
      console.error("Connection Failed:", error);
      // Fallback for demo purposes if backend is down
      alert("The AI Engine is currently warming up on Render. Please wait 30 seconds and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-slate-200 font-sans selection:bg-blue-500/30 scroll-smooth flex flex-col">
      
      {/* 1. RESPONSIVE NAVIGATION */}
      <nav className="border-b border-white/5 bg-black/20 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 md:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative w-10 h-10 bg-[#080c17] rounded-xl flex items-center justify-center border border-white/20 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
              </svg>
            </div>
            <div className="flex flex-col">
              <h1 className="text-sm md:text-xl font-bold tracking-tight text-white leading-none">Connect2Faculty</h1>
              <span className="text-[7px] md:text-[8px] text-blue-300/50 font-mono tracking-[0.2em] uppercase mt-1">AI Research Collaboration</span>
            </div>
          </div>

          <div className="flex gap-4 md:gap-8 text-[9px] md:text-[10px] font-bold uppercase tracking-widest text-slate-400">
            <a href="#hero" className="hover:text-cyan-400 transition-all">Engine</a>
            <a href="#results" className="hover:text-cyan-400 transition-all">Directory</a>
            <a href="https://github.com/Kunal-Pramanik/Faculty-Finder" target="_blank" rel="noopener noreferrer" className="hidden sm:block text-cyan-500 border border-cyan-500/30 px-3 py-1 rounded-full hover:bg-cyan-500/10 transition-all">Repo</a>
          </div>
        </div>
      </nav>

      {/* 2. HERO SECTION */}
      <header id="hero" className="relative pt-8 md:pt-16 pb-8 md:pb-16 px-4 text-center">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/10 via-transparent to-transparent -z-10" />
        <div className="inline-block px-3 py-1 mb-4 rounded-full border border-blue-500/20 bg-blue-500/5 text-blue-400 text-[8px] md:text-[10px] font-bold uppercase tracking-widest">
          Semantic Intelligence Active
        </div>
        <h1 className="text-3xl md:text-6xl font-black text-white mb-6 leading-tight tracking-tight">
          Find The <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300"> Best Faculty </span>
        </h1>
        
        <div className="relative group max-w-2xl mx-auto">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
          <div className="relative flex flex-col md:flex-row gap-2 bg-[#0f172a] p-2 rounded-2xl border border-white/10 shadow-2xl">
            <input 
              id="search-input"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder="Describe your research vision..."
              className="flex-1 bg-transparent px-4 py-3 outline-none text-white text-sm md:text-base placeholder:text-slate-500"
            />
            <button 
              onClick={handleSearch} 
              disabled={loading} 
              className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-xl font-bold transition-all text-xs md:text-sm uppercase tracking-widest disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Ride The Data"}
            </button>
          </div>
        </div>
      </header>

      {/* 3. RESULTS AREA */}
      <main id="results" className="flex-1 max-w-7xl mx-auto px-4 md:px-6 py-8 w-full min-h-[300px]">
        {loading && (
          <div className="flex flex-col items-center py-12 animate-pulse">
            <div className="w-10 h-10 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-cyan-400 font-mono text-[10px] tracking-widest uppercase">Processing Semantic Vectors...</p>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((faculty, i) => (
            <div key={i} className="group bg-[#0f172a]/50 border border-white/5 rounded-2xl overflow-hidden hover:border-blue-500/40 transition-all duration-500 flex flex-col shadow-lg">
              <div className="p-4 flex gap-4 bg-white/5">
                <img 
                  src={faculty.image_url?.startsWith("http") ? faculty.image_url : `https://www.daiict.ac.in${faculty.image_url}`} 
                  className="w-12 h-12 rounded-lg object-cover border border-white/10"
                  alt={faculty.name}
                />
                <div className="flex-1">
                  <h3 className="font-bold text-white text-sm md:text-base leading-tight">{faculty.name}</h3>
                  <div className="mt-1 inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-[9px] font-black uppercase">
                    {(faculty.score * 100).toFixed(0)}% MATCH
                  </div>
                </div>
              </div>
              <div className="p-4 flex-1">
                <p className="text-[9px] text-slate-500 font-bold uppercase mb-2">Core Specialization</p>
                <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">{faculty.specialization}</p>
              </div>
              <a href={faculty.profile_url} target="_blank" rel="noopener noreferrer" className="p-3 text-center text-[10px] font-bold text-slate-400 hover:text-white border-t border-white/5 hover:bg-blue-600 transition-all uppercase tracking-widest">
                Access Profile →
              </a>
            </div>
          ))}
        </div>

        {hasSearched && !loading && results.length === 0 && (
          <div className="text-center py-20 border border-dashed border-white/10 rounded-3xl">
            <p className="text-slate-500 font-mono text-xs uppercase tracking-[0.3em]">Zero Matching Faculty Clusters Found</p>
            <p className="text-[10px] text-slate-600 mt-2">Tip: Try broader terms like "computer vision" or "IoT"</p>
          </div>
        )}
      </main>

      {/* 4. DATA RIDERS FOOTER */}
      <footer className="border-t border-white/5 bg-black/40 py-8 px-4 md:px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex flex-col items-center md:items-start text-center md:text-left">
            <h4 className="text-white font-bold text-sm mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">Developed by Data Riders</h4>
            <div className="flex flex-col sm:flex-row gap-4">
              <span className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-[11px] font-bold shadow-[0_0_15px_rgba(59,130,246,0.1)]">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"/> Kunal Pramanik
              </span>
              <span className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-[11px] font-bold shadow-[0_0_15px_rgba(34,211,238,0.1)]">
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"/> Jinal Sasiya
              </span>
            </div>
          </div>
          <div className="text-slate-500 text-[8px] font-mono uppercase tracking-[0.4em] opacity-40">© 2026 Semantic Intelligence Hub</div>
        </div>
      </footer>
    </div>
  );
}
