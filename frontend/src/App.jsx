import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Favorites from "./pages/Favorites";
import NewsDetail from "./components/NewsDetail";

export default function App() {
  return (
    <Routes>
      {/* Login routes */}
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} /> {/* ✅ Added this */}

      {/* Signup */}
      <Route path="/signup" element={<Signup />} />

      {/* Dashboard */}
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/favorites" element={<Favorites />} />
      <Route path="/news/:id" element={<NewsDetail />} />

      {/* Fallback route (optional) */}
      <Route path="*" element={<Login />} />
    </Routes>
  );
}