import { useState } from "react";
import { signup } from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import { FaEnvelope, FaLock, FaWhatsapp } from "react-icons/fa";

export default function Signup() {
    const [form, setForm] = useState({
        email: "",
        password: "",
        whatsapp_number: "",
    });
    const [loading, setLoading] = useState(false);
    const nav = useNavigate();

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await signup(form);
            alert("Signup successful! Please login.");
            nav("/login");
        } catch (err) {
            alert(err.response?.data?.detail || "Signup failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen justify-center items-center bg-gradient-to-br from-blue-50 via-blue-100 to-blue-200 px-4">
            <div className="bg-white/90 backdrop-blur-md p-8 md:p-10 rounded-3xl shadow-2xl w-full max-w-md transition-all hover:shadow-3xl">
                <h2 className="text-3xl md:text-4xl font-extrabold mb-8 text-center text-gray-800">
                    Signup
                </h2>

                {/* Email */}
                <div className="relative mb-4">
                    <FaEnvelope className="absolute top-1/2 left-4 -translate-y-1/2 text-gray-400" />
                    <input
                        type="email"
                        placeholder="Email"
                        value={form.email}
                        onChange={(e) => setForm({ ...form, email: e.target.value })}
                        className="w-full pl-12 p-4 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 shadow-sm transition"
                    />
                </div>

                {/* Password */}
                <div className="relative mb-4">
                    <FaLock className="absolute top-1/2 left-4 -translate-y-1/2 text-gray-400" />
                    <input
                        type="password"
                        placeholder="Password"
                        value={form.password}
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                        className="w-full pl-12 p-4 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 shadow-sm transition"
                    />
                </div>

                {/* WhatsApp Number */}
                <div className="relative mb-6">
                    <FaWhatsapp className="absolute top-1/2 left-4 -translate-y-1/2 text-green-500" />
                    <input
                        type="tel"
                        placeholder="WhatsApp Number (10 digits)"
                        value={form.whatsapp_number}
                        onChange={(e) =>
                            setForm({ ...form, whatsapp_number: e.target.value })
                        }
                        className="w-full pl-12 p-4 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-400 shadow-sm transition"
                    />
                </div>

                {/* Signup Button */}
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className={`w-full py-4 rounded-2xl text-white font-semibold text-lg transition-all ${loading
                            ? "bg-green-400 cursor-not-allowed"
                            : "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 shadow-md hover:shadow-lg"
                        }`}
                >
                    {loading ? "Signing up..." : "Signup"}
                </button>

                {/* Login Link */}
                <p className="mt-6 text-center text-gray-600 text-base">
                    Already have an account?{" "}
                    <Link
                        to="/login"
                        className="text-blue-600 font-medium hover:underline transition"
                    >
                        Login
                    </Link>
                </p>
            </div>
        </div>
    );
}