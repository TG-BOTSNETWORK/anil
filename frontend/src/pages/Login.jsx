import { useState } from "react";
import { login } from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import { FaEnvelope, FaLock } from "react-icons/fa";

export default function Login() {
    const [form, setForm] = useState({ email: "", password: "" });
    const [loading, setLoading] = useState(false);
    const nav = useNavigate();

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await login(form);
            nav("/dashboard");
        } catch (err) {
            alert("Invalid credentials");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen justify-center items-center bg-gradient-to-br from-blue-50 via-blue-100 to-blue-200 px-4">
            <div className="bg-white/90 backdrop-blur-md p-8 md:p-10 rounded-3xl shadow-2xl w-full max-w-md transition-all hover:shadow-3xl">
                <h2 className="text-3xl md:text-4xl font-extrabold mb-8 text-center text-gray-800">
                    Login
                </h2>

                {/* Email input with icon */}
                <div className="relative mb-4">
                    <FaEnvelope className="absolute top-1/2 left-3 -translate-y-1/2 text-gray-400" />
                    <input
                        placeholder="Email"
                        type="email"
                        value={form.email}
                        onChange={(e) => setForm({ ...form, email: e.target.value })}
                        className="w-full pl-10 p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 shadow-sm transition"
                    />
                </div>

                {/* Password input with icon */}
                <div className="relative mb-6">
                    <FaLock className="absolute top-1/2 left-3 -translate-y-1/2 text-gray-400" />
                    <input
                        placeholder="Password"
                        type="password"
                        value={form.password}
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                        className="w-full pl-10 p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 shadow-sm transition"
                    />
                </div>

                {/* Login button */}
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className={`w-full py-4 rounded-xl text-white font-semibold text-lg transition-all ${loading
                            ? "bg-blue-400 cursor-not-allowed"
                            : "bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 shadow-md hover:shadow-lg"
                        }`}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>

                {/* Signup link */}
                <p className="mt-6 text-center text-gray-600 text-base">
                    Don’t have an account?{" "}
                    <Link
                        to="/signup"
                        className="text-blue-600 font-medium hover:underline transition"
                    >
                        Signup
                    </Link>
                </p>
            </div>
        </div>
    );
}