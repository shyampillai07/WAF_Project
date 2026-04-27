const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || (window.location.hostname === "localhost" ? "http://127.0.0.1:5000" : "");

if (!API_BASE_URL) {
  console.error("❌ API_BASE_URL is not defined! Check your environment variables.");
}

export default API_BASE_URL;