import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import NewsCard from "../components/NewsCard";
import BroadcastModal from "../components/BroadcastModal";
import { getNews, addFavorite, getFavorites, broadcastNews } from "../api/api";

export default function Dashboard() {
    const navigate = useNavigate();
    const [news, setNews] = useState([]);
    const [favorites, setFavorites] = useState([]);
    const [selected, setSelected] = useState(null);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [keyword, setKeyword] = useState("");
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const PAGE_SIZE = 40;

    useEffect(() => { fetchNews(); }, [page, keyword]);
    useEffect(() => { fetchFavorites(); }, []);

    const fetchNews = async () => {
        setLoading(true);
        try {
            const res = await getNews({ page, page_size: PAGE_SIZE, keyword });
            setNews(res.data.data || []);
        } catch (err) {
            console.error(err.response?.data || err);
            setNews([]);
        } finally { setLoading(false); }
    };

    const fetchFavorites = async () => {
        try {
            const res = await getFavorites();
            setFavorites(res.data.data || []);
        } catch (err) {
            console.error(err.response?.data || err);
            setFavorites([]);
        }
    };

    const handleFavorite = async (news_id) => {
        try {
            await addFavorite(news_id);
            fetchFavorites();
        } catch (err) {
            console.error(err.response?.data || err);
        }
    };

    const handleBroadcast = (news) => setSelected(news);
    const handleView = (news) => navigate(`/news/${news.id}`);

    return (
        <div className="flex min-h-screen bg-gray-100">
            {/* Sidebar */}
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            {/* Main Content */}
            <div className="flex-1 flex flex-col transition-all duration-300 md:ml-64">
                {/* Navbar */}
                <Navbar onSidebarToggle={() => setSidebarOpen(true)} />

                {/* Page Content */}
                <div className="p-4 md:p-6 flex flex-col gap-6">
                    {/* Search */}
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <input
                            type="text"
                            placeholder="Search news..."
                            value={keyword}
                            onChange={(e) => { setKeyword(e.target.value); setPage(1); }}
                            className="w-full md:w-1/3 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {/* News Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {loading ? (
                            <p className="col-span-full text-center text-gray-500">Loading news...</p>
                        ) : news.length === 0 ? (
                            <p className="col-span-full text-center text-gray-500">No news found.</p>
                        ) : (
                            news.map((n) => {
                                const isFav = favorites.some(f => f.news_id === n.id);
                                return (
                                    <NewsCard
                                        key={n.id}
                                        news={n}
                                        isFavorite={isFav}
                                        onFavorite={() => handleFavorite(n.id)}
                                        onBroadcast={() => handleBroadcast(n)}
                                        onView={() => handleView(n)}
                                    />
                                );
                            })
                        )}
                    </div>

                    {/* Pagination */}
                    {!loading && news.length > 0 && (
                        <div className="flex justify-center items-center gap-4 mt-4">
                            <button
                                disabled={page <= 1}
                                onClick={() => setPage((p) => p - 1)}
                                className="px-4 py-2 bg-white border rounded hover:bg-blue-50 disabled:opacity-50 transition"
                            >Prev</button>
                            <span className="px-4 py-2 bg-white border rounded">{page}</span>
                            <button
                                disabled={news.length < PAGE_SIZE}
                                onClick={() => setPage((p) => p + 1)}
                                className="px-4 py-2 bg-white border rounded hover:bg-blue-50 disabled:opacity-50 transition"
                            >Next</button>
                        </div>
                    )}
                </div>
            </div>

            {/* Broadcast Modal */}
            {selected && (
                <BroadcastModal
                    news={selected}
                    onClose={() => setSelected(null)}
                    onSend={async (id, channels) => {
                        try {
                            const res = await broadcastNews(id, channels);
                            return res.data;
                        } catch (err) {
                            console.error(err.response?.data || err);
                            throw err;
                        }
                    }}
                />
            )}
        </div>
    );
}