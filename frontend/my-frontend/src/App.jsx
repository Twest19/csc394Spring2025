import { useState } from "react";
import ArticleCard from "./ArticleCard";

function BasicCard({ text }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 w-full">
      <p className="text-gray-600">{text}</p>
    </div>
  );
}

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    if (loading) return;

    setLoading(true);
    setError(null);
    setArticle(null);
    setSearchQuery(searchQuery.trim());

    fetch(
      `http://localhost:8000/documents/random?topic=${encodeURIComponent(
        searchQuery
      )}`
    )
      .then((response) => response.json())
      .then((data) => {
        setArticle(data);
        setError(null);
      })
      .catch((err) => {
        console.log(err);
        setError("Failed to retrieve article with topic: " + searchQuery);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 w-screen">
      <header className="sticky top-0 bg-white shadow-md rounded-lg p-4">
        <h1 className="text-green-400 text-2xl font-bold">HW 4 - Frontend</h1>
      </header>
      <main className="flex justify-center items-start">
        <div className="space-y-5 mt-10">
          <div className="bg-white rounded-lg shadow-lg p-6 w-lg">
            <form className="space-y-4" onSubmit={handleSearch}>
              <label className="block text-gray-700">
                Enter Pub Med Topic:
                <input
                  type="text"
                  placeholder="e.g. Cancer, Stroke, etc."
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm px-2 py-1"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </label>
              <button
                type="submit"
                className="text-gray-900 bg-green-400 hover:bg-green-500 font-medium rounded-lg shadow-lg text-sm px-5 py-2.5 text-center w-md"
              >
                Get Random Article
              </button>
            </form>
          </div>
          {loading ? (
            <BasicCard text="Loading..." />
          ) : error ? (
            <BasicCard text={error} />
          ) : article ? (
            <ArticleCard article={article} />
          ) : null}
        </div>
      </main>
    </div>
  );
}

export default App;
