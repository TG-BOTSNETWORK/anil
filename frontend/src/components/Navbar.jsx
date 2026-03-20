import { useNavigate } from "react-router-dom";
import { FaBars } from "react-icons/fa";

export default function Navbar({ onSidebarToggle }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Optional: clear any auth token
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="bg-white shadow px-4 md:px-6 py-4 flex items-center justify-between">
            {/* Left side */}
            <div className="flex items-center gap-4">
                <button
                    className="text-gray-700 md:hidden hover:text-blue-500 transition"
                    onClick={onSidebarToggle}
                >
                    <FaBars size={20} />
                </button>
                <h1 className="font-bold text-lg md:text-xl">AI News System</h1>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-4">
                <input
                    type="text"
                    placeholder="Search news..."
                    className="hidden md:block px-3 py-2 border rounded shadow-sm focus:outline-none w-full max-w-xs"
                />
                <button
                    onClick={handleLogout}
                    className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
                >
                    Logout
                </button>
            </div>
        </div>
    );
}