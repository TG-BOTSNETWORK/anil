import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
});

// ✅ Interceptor
API.interceptors.response.use(
    (res) => res,
    (err) => {
        console.error("API Error:", err.response?.data || err.message);
        return Promise.reject(err);
    }
);

// ===== AUTH =====
export const signup = (data) => API.post("/auth/signup", data);
export const login = (data) => API.post("/auth/login", data);
export const logout = () => API.post("/auth/logout");

// ===== NEWS =====
export const getNews = ({ page = 1, page_size = 40, keyword = "", source_id = null, sort_by = "impact" } = {}) => {
    const params = { page, page_size, sort_by };
    if (keyword) params.keyword = keyword;
    if (source_id) params.source_id = source_id;

    return API.get("/news/", { params }); // ✅ matches router.get("/")
};

export const getSourcesSummary = () => {
    return API.get("/news/sources"); // ✅ matches router.get("/sources")
};

export const getNewsById = (id) => {
    return API.get(`/news/${id}`); // ✅ matches router.get("/{news_id}")
};


// ===== FAVORITES =====
export const getFavorites = () => API.get("/favorites/");
export const addFavorite = (news_id) => API.post("/favorites/", null, { params: { news_id } });

// ===== BROADCAST =====
export const broadcastNews = (news_id, channels) =>
    API.post("/broadcast/", null, { params: { news_id, channels } });

export default API;