import { FaStar, FaShareAlt, FaEye } from "react-icons/fa";

export default function NewsCard({ news, onFavorite, onBroadcast, onView, isFavorite }) {
    return (
        <div className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition flex flex-col justify-between h-full">
            <h3 className="font-semibold text-lg line-clamp-2">{news.title}</h3>

            <div className="mt-4 flex flex-col md:flex-row md:justify-between md:items-center gap-2">
                <button
                    onClick={onFavorite}
                    className={`flex items-center justify-center gap-2 px-3 py-2 rounded border transition w-full md:w-auto
            ${isFavorite
                            ? "bg-yellow-100 text-yellow-600 border-yellow-400"
                            : "text-gray-700 border-gray-300 hover:bg-yellow-50"
                        }`}
                >
                    <FaStar /> {isFavorite ? "Favorited" : "Favorite"}
                </button>

                <button
                    onClick={onBroadcast}
                    className="flex items-center justify-center gap-2 px-3 py-2 rounded bg-blue-500 text-white hover:bg-blue-600 transition w-full md:w-auto"
                >
                    <FaShareAlt /> Broadcast
                </button>

                <button
                    onClick={onView}
                    className="flex items-center justify-center gap-2 px-3 py-2 rounded bg-green-500 text-white hover:bg-green-600 transition w-full md:w-auto"
                >
                    <FaEye /> View
                </button>
            </div>
        </div>
    );
}