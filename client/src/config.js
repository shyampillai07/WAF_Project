const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://waf-project.onrender.com";

if (!API_BASE_URL) {
  console.error("❌ API_BASE_URL is not defined! Check your environment variables.");
}

export default API_BASE_URL;