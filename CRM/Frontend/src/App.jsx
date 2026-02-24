import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Bell, LogOut, RefreshCw } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import LeadsPage from './pages/LeadsPage';
import LeadDetails from './pages/LeadDetails';
import NotificationsPage from './pages/NotificationsPage';
import { apiFetch } from './api';
import './index.css';

const Navigation = ({ unreadCount }) => {
  const location = useLocation();

  return (
    <nav>
      <div style={{ display: 'flex', alignItems: 'center', gap: '2.5rem' }}>
        <h2 style={{ color: 'var(--primary)', fontWeight: 'bold' }}>Xeno CRM</h2>
        <div className="nav-links">
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
            <LayoutDashboard size={20} style={{ verticalAlign: 'middle', marginRight: '5px' }} />
            Dashboard
          </Link>
          <Link to="/leads" className={location.pathname.startsWith('/leads') ? 'active' : ''}>
            <Users size={20} style={{ verticalAlign: 'middle', marginRight: '5px' }} />
            Leads
          </Link>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <Link to="/notifications" style={{ position: 'relative', cursor: 'pointer', color: 'inherit', textDecoration: 'none' }}>
          <Bell size={24} color={location.pathname === '/notifications' ? 'var(--primary)' : 'var(--secondary)'} />
          {unreadCount > 0 && <span className="notification-badge">{unreadCount}</span>}
        </Link>
        <LogOut size={24} color="var(--secondary)" style={{ cursor: 'pointer' }} />
      </div>
    </nav>
  );
};

function App() {
  const [unreadCount, setUnreadCount] = useState(0);

  // Fetch notifications periodically
  useEffect(() => {
    const fetchNotifs = async () => {
      try {
        const data = await apiFetch('/notifications');
        setUnreadCount(data.filter(n => !n.is_read).length);
      } catch (e) {
        console.error("Failed to fetch notifications", e);
      }
    };
    fetchNotifs();
    const interval = setInterval(fetchNotifs, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <div className="App">
        <Navigation unreadCount={unreadCount} />
        <main style={{ padding: '2rem' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/leads" element={<LeadsPage />} />
            <Route path="/leads/:id" element={<LeadDetails />} />
            <Route path="/notifications" element={<NotificationsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
