import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getNewsById } from "../api/api";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function NewsDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [news, setNews] = useState(null);
    const [loading, setLoading] = useState(true);
    const [sidebarOpen, setSidebarOpen] = useState(false);

    useEffect(() => {
        fetchNewsDetail();
    }, [id]);

    const fetchNewsDetail = async () => {
        setLoading(true);
        try {
            const res = await getNewsById(id);
            setNews(res.data.data); // backend now returns { title, ai_summary, url }
        } catch (err) {
            console.error("Error fetching news detail:", err.response?.data || err);
            setNews(null);
        } finally {
            setLoading(false);
        }
    };

    if (loading)
        return (
            <p className="p-6 text-gray-500 text-center text-lg">Loading news...</p>
        );

    if (!news)
        return (
            <p className="p-6 text-red-500 text-center text-lg">News not found.</p>
        );

    return (
        <div className="flex min-h-screen bg-gray-100 flex-col md:flex-row">
            {/* Sidebar */}
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            {/* Main Content */}
            <div className="flex-1 md:ml-64 transition-all duration-300 flex flex-col">
                <Navbar onSidebarToggle={() => setSidebarOpen(true)} />

                <div className="p-4 md:p-6 flex flex-col gap-6">
                    {/* Back Button */}
                    <button
                        onClick={() => navigate(-1)}
                        className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 w-max transition"
                    >
                        ← Back
                    </button>

                    {/* News Detail Card */}
                    <div className="bg-white p-6 md:p-8 rounded-3xl shadow-lg hover:shadow-2xl transition flex flex-col gap-4">
                        {/* Title */}
                        <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
                            {news.title}
                        </h1>

                        {/* AI Summary */}
                        {news.ai_summary && (
                            <div>
                                <h2 className="font-semibold text-gray-700 mb-1">AI Summary:</h2>
                                <p className="text-gray-600">{news.ai_summary}</p>
                            </div>
                        )}

                        {/* Original URL */}
                        {news.url && (
                            <a
                                href={news.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="mt-4 inline-block px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition w-max"
                            >
                                Read Original
                            </a>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}