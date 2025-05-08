

function ArticleCard({ article }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-5 w-lg">
      <h2 className="text-gray-700 text-xl font-semibold">Random Article</h2>
      <div className="mt-4">
        <h3 className="text-green-400 text-lg font-semibold">Title:</h3>
        <p className="text-gray-600">{article.title}</p>
        <h3 className="text-green-400 text-lg font-semibold mt-2">PMC ID:</h3>
        <p className="text-gray-600">{article.pmcId}</p>
        <h3 className="text-green-400 text-lg font-semibold mt-2">Convert PMC ID using:</h3>
        <a
          href={`https://www.ncbi.nlm.nih.gov/pmc/tools/idconv`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:underline"
        >https://www.ncbi.nlm.nih.gov/pmc/tools/idconv</a>
      </div>
    </div>
  );
}

export default ArticleCard;