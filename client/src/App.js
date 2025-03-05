import React, { Suspense, lazy, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { FaBars, FaHome, FaUser, FaShieldAlt } from "react-icons/fa";
import "./styles/main.scss";

const Home = lazy(() => import("./pages/Home"));
const UserInputs = lazy(() => import("./pages/UserInputs"));
const ProtectionRules = lazy(() => import("./pages/ProtectionRules"));


function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <Router>
      <div className="app-container">
        {/* Top Navigation Bar */}
        <header className="top-nav">
          <button className="menu-btn" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
            <FaBars />
          </button>
          <Link to="/" className="brand">
            <FaShieldAlt className="headline-icon" /> Web Application Firewall
          </Link>
        </header>

        {/* Main Layout */}
        <div className={`main-layout ${isSidebarOpen ? "" : "sidebar-closed"}`}>
          {/* Sidebar Navigation */}
          <aside className={`sidebar ${isSidebarOpen ? "" : "closed"}`}>
            <nav>
              <ul>
                <li>
                  <Link to="/">
                    <FaHome className="icon" />
                    <span>Home</span>
                  </Link>
                </li>
                <li>
                  <Link to="/userinputs">
                    <FaUser className="icon" />
                    <span>User Inputs</span>
                  </Link>
                </li>
                <li>
                  <Link to="/protectionrules">
                    <FaShieldAlt className="icon" />
                    <span>Protection Rules</span>
                  </Link>
                </li>
              </ul>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="content">
            <div className="page-wrapper">
              <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/userinputs" element={<UserInputs />} />
                  <Route path="/protectionrules" element={<ProtectionRules/>} />             
                </Routes>
              </Suspense>
            </div>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;