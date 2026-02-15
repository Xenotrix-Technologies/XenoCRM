import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Users, TrendingUp, CheckCircle, Clock, ArrowRight } from 'lucide-react';
import { apiFetch } from '../api';
import { Link } from 'react-router-dom';

const StatCard = ({ title, value, icon: Icon, color }) => (
    <div className="premium-card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ padding: '1rem', background: `${color}15`, borderRadius: '12px', color: color }}>
            <Icon size={24} />
        </div>
        <div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{title}</p>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{value}</h3>
        </div>
    </div>
);

const RecentLeads = ({ leads }) => (
    <div className="premium-card" style={{ flex: 1 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h3 style={{ fontWeight: '600' }}>Recent Leads</h3>
            <Link to="/leads" style={{ fontSize: '0.875rem', color: 'var(--primary)', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                View All <ArrowRight size={14} />
            </Link>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {leads.slice(0, 5).map(lead => (
                <div key={lead.lead_id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '0.75rem', borderBottom: '1px solid #f1f5f9' }}>
                    <div>
                        <p style={{ fontWeight: '600', fontSize: '0.9375rem' }}>{lead.customer_name}</p>
                        <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{new Date(lead.created_at).toLocaleDateString()}</p>
                    </div>
                    <span className={`status-badge status-${lead.status.toLowerCase().replace(' ', '-')}`} style={{ fontSize: '0.75rem' }}>
                        {lead.status}
                    </span>
                </div>
            ))}
            {leads.length === 0 && <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '1rem' }}>No new leads.</p>}
        </div>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState([]);
    const [totalLeads, setTotalLeads] = useState(0);
    const [recentLeads, setRecentLeads] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const statsData = await apiFetch('/stats');
                setStats(statsData);
                setTotalLeads(statsData.reduce((acc, curr) => acc + curr.count, 0));

                const leadsData = await apiFetch('/leads');
                setRecentLeads(leadsData);
            } catch (e) {
                console.error("Dashboard fetch failed", e);
            }
        };
        fetchData();
    }, []);

    const COLORS = ['#2563eb', '#f59e0b', '#22c55e', '#ef4444', '#64748b'];

    return (
        <div>
            <header style={{ marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '1.875rem', fontWeight: 'bold' }}>Intelligence Dashboard</h1>
                <p style={{ color: 'var(--text-muted)' }}>Overview of your sales pipeline and lead engagement.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
                <StatCard title="Total Leads" value={totalLeads} icon={Users} color="#2563eb" />
                <StatCard title="New Leads" value={stats.find(s => s.status === 'New')?.count || 0} icon={TrendingUp} color="#22c55e" />
                <StatCard title="In Progress" value={stats.find(s => s.status === 'Follow-Up')?.count || 0} icon={Clock} color="#f59e0b" />
                <StatCard title="Completed" value={stats.find(s => s.status === 'Finished')?.count || 0} icon={CheckCircle} color="#64748b" />
            </div>

            <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
                <div className="premium-card" style={{ flex: 2, minWidth: '400px', height: '450px' }}>
                    <h3 style={{ marginBottom: '1.5rem', fontWeight: '600' }}>Leads by Status</h3>
                    <ResponsiveContainer width="100%" height="85%">
                        <BarChart data={stats}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                            <XAxis dataKey="status" axisLine={false} tickLine={false} />
                            <YAxis axisLine={false} tickLine={false} />
                            <Tooltip
                                cursor={{ fill: 'rgba(0,0,0,0.05)' }}
                                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
                            />
                            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                                {stats.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                <RecentLeads leads={recentLeads} />
            </div>
        </div>
    );
};

export default Dashboard;
