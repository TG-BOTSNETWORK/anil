import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import { getFavorites } from "../api/api";

export default function Favorites() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        getFavorites()
            .then((res) => setData(res.data.data || []))
            .catch((err) => {
                console.error(err);
                setData([]);
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return <p className="p-6 text-gray-500 text-center">Loading favorites...</p>;
    }

    return (
        <div className="p-4 md:p-6 flex flex-col gap-6">
            {/* Back Button */}
            <button
                onClick={() => navigate(-1)}
                className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 w-max transition"
            >
                <FaArrowLeft /> Back
            </button>

            {/* Content */}
            {data.length === 0 ? (
                <p className="text-gray-500 text-center mt-6">No favorites yet</p>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {data.map((n) => (
                        <div
                            key={n.favorite_id}
                            className="flex flex-col justify-between p-4 bg-white shadow hover:shadow-lg rounded-xl transition h-full"
                        >
                            <div className="flex-1">
                                <h2 className="font-semibold text-lg line-clamp-2">{n.title}</h2>
                                <p className="text-sm text-gray-500 mt-1">{n.source}</p>
                            </div>
                            <a
                                href={n.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="mt-4 px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm text-center transition"
                            >
                                View
                            </a>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}