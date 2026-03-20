import { Link, useLocation } from "react-router-dom";
import { FaTachometerAlt, FaStar, FaTimes } from "react-icons/fa";

export default function Sidebar({ isOpen, onClose }) {
    const location = useLocation();

    const links = [
        { name: "Dashboard", to: "/dashboard", icon: <FaTachometerAlt /> },
        { name: "Favorites", to: "/favorites", icon: <FaStar /> },
    ];

    return (
        <>
            {/* Mobile overlay */}
            <div
                className={`fixed inset-0 bg-black bg-opacity-30 z-30 transition-opacity md:hidden ${isOpen ? "opacity-100 visible" : "opacity-0 invisible"}`}
                onClick={onClose}
            ></div>

            {/* Sidebar */}
            <aside
                className={`
          fixed top-0 left-0 h-screen bg-white shadow-lg z-40 w-64
          transform transition-transform
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
          md:translate-x-0 md:block
        `}
            >
                <div className="flex items-center justify-between p-6 border-b md:border-b-0">
                    <h1 className="text-2xl font-bold text-gray-800 tracking-wide">AI Dashboard</h1>
                    <button className="md:hidden text-gray-600" onClick={onClose}>
                        <FaTimes />
                    </button>
                </div>

                <nav className="flex flex-col mt-6 gap-2 px-4">
                    {links.map((link) => {
                        const isActive = location.pathname === link.to;
                        return (
                            <Link
                                key={link.to}
                                to={link.to}
                                className={`flex items-center gap-3 px-4 py-2 rounded-lg transition
                  ${isActive
                                        ? "bg-blue-500 text-white"
                                        : "text-gray-700 hover:bg-blue-100 hover:text-blue-600"
                                    }`}
                            >
                                <span className="text-lg">{link.icon}</span>
                                <span className="font-medium">{link.name}</span>
                            </Link>
                        );
                    })}
                </nav>

                <div className="mt-auto p-6 text-sm text-gray-400">v1.0.0</div>
            </aside>
        </>
    );
}