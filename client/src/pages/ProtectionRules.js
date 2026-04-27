import React, { useState, useEffect } from "react";
import { FaDatabase, FaCode, FaTerminal, FaFolderOpen, FaTachometerAlt, FaShieldAlt } from "react-icons/fa";
import "../styles/protectionrules.scss";
import API_BASE_URL from "../config";

const iconMap = {
  SQLi: <FaDatabase />,
  XSS: <FaCode />,
  "Command Injection": <FaTerminal />,
  "Path Traversal": <FaFolderOpen />,
  "Rate Limiting": <FaTachometerAlt />,
};

const ProtectionRules = () => {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updatingRuleId, setUpdatingRuleId] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [password, setPassword] = useState("");
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");
  const [csrfToken, setCsrfToken] = useState("");

  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/admin/csrf-token`, {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to initialize security token.");
        }
        const data = await response.json();
        setCsrfToken(data.csrfToken || "");
      } catch (err) {
        setAuthError(err.message || "Failed to initialize security token.");
      }
    };

    const fetchAdminStatus = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/admin/status`, {
          credentials: "include",
        });
        if (!response.ok) return;
        const data = await response.json();
        setIsAdmin(Boolean(data.isAdmin));
      } catch (err) {
        console.error("❌ Error checking admin status:", err.message);
      }
    };

    const fetchRules = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/protection-rules`);

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();

        if (!data || !Array.isArray(data.rules)) {
          throw new Error("Invalid API response format: 'rules' should be an array.");
        }

        setRules(
          data.rules.map((rule) => ({
            ...rule,
            icon: iconMap[rule.name] || <FaShieldAlt />,
          }))
        );
      } catch (err) {
        console.error("❌ Error fetching protection rules:", err.message);
        setError(`Failed to load protection rules: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchCsrfToken();
    fetchAdminStatus();
    fetchRules();
  }, []);

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    if (!password.trim()) {
      setAuthError("Password is required.");
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/login`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrfToken,
        },
        body: JSON.stringify({ password }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Login failed.");
      }

      setIsAdmin(true);
      setPassword("");
    } catch (err) {
      setAuthError(err.message || "Login failed.");
    } finally {
      setAuthLoading(false);
    }
  };

  const handleAdminLogout = async () => {
    setAuthLoading(true);
    setAuthError("");
    try {
      await fetch(`${API_BASE_URL}/api/admin/logout`, {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRF-Token": csrfToken,
        },
      });
      setIsAdmin(false);
    } catch (err) {
      setAuthError("Logout failed. Please retry.");
    } finally {
      setAuthLoading(false);
    }
  };

  const toggleRule = async (id, currentStatus) => {
    if (!isAdmin) {
      setError("Admin login is required to update rules.");
      return;
    }
    if (updatingRuleId) return;
    setUpdatingRuleId(id);

    try {
      const response = await fetch(`${API_BASE_URL}/api/protection-rules/${id}`, {
        method: "PATCH",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrfToken,
        },
        body: JSON.stringify({ enabled: !currentStatus }),
      });

      if (!response.ok) throw new Error(`Failed to update rule (Status: ${response.status})`);

      setRules((prevRules) =>
        prevRules.map((rule) =>
          rule.id === id ? { ...rule, enabled: !currentStatus } : rule
        )
      );
    } catch (err) {
      console.error(`❌ Error updating rule ${id}:`, err.message);
      setError(`Failed to update rule: ${err.message}`);
    } finally {
      setUpdatingRuleId(null);
    }
  };

  return (
    <div className="protectionrules-container">
      <h1>Protection Rules</h1>
      <div className="admin-controls">
        {isAdmin ? (
          <div className="admin-session">
            <p>Admin session active.</p>
            <button type="button" onClick={handleAdminLogout} disabled={authLoading}>
              {authLoading ? "Processing..." : "Logout"}
            </button>
          </div>
        ) : (
          <form className="admin-login" onSubmit={handleAdminLogin}>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Admin password"
              disabled={authLoading}
            />
            <button type="submit" disabled={authLoading}>
              {authLoading ? "Signing in..." : "Admin Login"}
            </button>
          </form>
        )}
        {authError && <p className="error-message">{authError}</p>}
      </div>
      {loading ? (
        <p>Loading rules...</p>
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : (
        <div className="rules-grid">
          {rules.map((rule) => (
            <div key={rule.id} className={`rule-card ${rule.enabled ? "enabled" : "disabled"}`}>
              <div className="icon-wrapper">{rule.icon}</div>
              <div className="text-content">
                <h3>{rule.name}</h3>
                <p>{rule.description}</p>
              </div>
              <label className={`switch ${updatingRuleId === rule.id ? "disabled" : ""}`}>
                <input
                  type="checkbox"
                  checked={rule.enabled}
                  onChange={() => toggleRule(rule.id, rule.enabled)}
                  disabled={updatingRuleId === rule.id || !isAdmin}
                />
                <span className="slider round"></span>
              </label>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProtectionRules;