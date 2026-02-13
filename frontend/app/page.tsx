"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]); 
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setHasSearched(true);
    setErrorMessage("");

    try {
      const response = await fetch("https://faculty-connect.onrender.com/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query }),
      });

      const data = await response.json();

      if (data && Array.isArray(data.results)) {
        setResults(data.results);
      } else {
        setResults([]);
        setErrorMessage(data.message || "Unexpected response from server.");
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("Failed to connect to the server. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-4 md:p-8 font-sans">
      {/* HEADER - Adjusted padding and text sizes for mobile */}
      <div className="max-w-4xl mx-auto text-center mb-8 md:mb-12 pt-6 md:pt-10">
        <h1 className="text-3xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-4 md:mb-6">
          🎓 Connect2Faculty
        </h1>
        <p className="text-base md:text-lg text-gray-600 mb-6 md:mb-8 max-w-2xl mx-auto leading-relaxed px-2">
          Don't just search for names. Search for <strong>ideas</strong>. <br className="hidden md:block" />
          Tell us what you want to learn, and we'll find the perfect mentor.
        </p>

        {/* SEARCH BAR - Changed from flex to responsive flex-col on mobile */}
        <div className="relative max-w-2xl mx-auto shadow-xl md:shadow-2xl rounded-2xl md:rounded-full bg-white p-2 flex flex-col md:flex-row items-stretch md:items-center border border-gray-100 gap-2 md:gap-0 transition-all duration-300">
          <div className="flex items-center flex-1">
            <span className="pl-4 md:pl-6 text-xl md:text-2xl">🔍</span>
            <input
              type="text"
              className="w-full px-3 md:px-4 py-3 md:py-4 outline-none text-gray-700 text-base md:text-lg placeholder-gray-400 rounded-lg"
              placeholder="E.g., 'I want to build a deep learning model...'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={loading}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 md:px-8 py-3 md:py-4 rounded-xl md:rounded-full font-bold text-base md:text-lg transition-all disabled:opacity-50 shadow-md active:scale-95"
          >
            {loading ? "Searching..." : "Find Faculty"}
          </button>
        </div>
      </div>

      {/* LOADING STATE */}
      {loading && (
        <div className="text-center py-12 md:py-20">
          <div className="animate-spin rounded-full h-12 w-12 md:h-16 md:w-16 border-t-4 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500 animate-pulse text-sm md:text-base">Consulting the AI Brain...</p>
        </div>
      )}

      {/* ERROR MESSAGE DISPLAY */}
      {errorMessage && !loading && (
        <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-50 border border-red-200 text-red-600 rounded-xl text-center text-sm md:text-base">
          {errorMessage}
        </div>
      )}

      {/* RESULTS GRID - 1 column mobile, 2 tablet, 3 desktop */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 pb-12 md:pb-20">
        {Array.isArray(results) && results.map((faculty, index) => (
          <div
            key={index}
            className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 border border-gray-100 overflow-hidden flex flex-col group"
          >
            {/* CARD HEADER */}
            <div className="p-4 md:p-6 flex items-start gap-3 md:gap-4 border-b border-gray-50 bg-gray-50/50">
              <img
                src={faculty.image_url && faculty.image_url.startsWith("http") 
                      ? faculty.image_url 
                      : `https://www.daiict.ac.in${faculty.image_url || ""}`
                    }
                alt={faculty.name}
                className="w-16 h-16 md:w-20 md:h-20 rounded-full object-cover border-2 md:border-4 border-white shadow-sm group-hover:scale-110 transition-transform duration-300"
                onError={(e: any) => { e.target.src = "https://via.placeholder.com/150?text=No+Img"; }}
              />
              <div className="flex-1 min-w-0">
                <h2 className="text-lg md:text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors truncate">
                  {faculty.name}
                </h2>
                <div className="mt-1 md:mt-2 inline-block bg-green-100 text-green-700 text-[10px] md:text-xs px-2 md:px-3 py-1 rounded-full font-bold">
                  {(faculty.score * 100).toFixed(0)}% Match
                </div>
              </div>
            </div>

            {/* CARD BODY */}
            <div className="p-4 md:p-6 flex-1 space-y-3 md:space-y-4">
              <div className="min-w-0">
                <p className="text-[10px] md:text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Specialization</p>
                <p className="text-xs md:text-sm text-gray-700 font-medium leading-snug break-words">{faculty.specialization || "N/A"}</p>
              </div>
              
              {faculty.teaching && (
                <div>
                  <p className="text-[10px] md:text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Teaching</p>
                  <p className="text-xs md:text-sm text-gray-600 line-clamp-2 md:line-clamp-3" title={faculty.teaching}>
                    {faculty.teaching}
                  </p>
                </div>
              )}
            </div>

            {/* CARD FOOTER */}
            <a
              href={faculty.profile_url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-50 p-3 md:p-4 text-center text-blue-600 font-bold hover:bg-blue-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-2 text-sm md:text-base"
            >
              View Full Profile <span>→</span>
            </a>
          </div>
        ))}
      </div>

      {/* EMPTY STATE */}
      {!loading && hasSearched && results.length === 0 && !errorMessage && (
        <div className="text-center py-12 md:py-20 text-gray-500 px-4">
          <p className="text-lg md:text-xl">No matches found. Try describing it differently!</p>
        </div>
      )}
    </div>
  );
}
