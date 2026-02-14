import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Users, TrendingUp, CheckCircle, Clock } from 'lucide-react';

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

const Dashboard = () => {
    const [stats, setStats] = useState([]);
    const [totalLeads, setTotalLeads] = useState(0);

    useEffect(() => {
        fetch('http://localhost:8000/stats')
            .then(res => res.json())
            .then(data => {
                setStats(data);
                setTotalLeads(data.reduce((acc, curr) => acc + curr.count, 0));
            });
    }, []);

    const COLORS = ['#2563eb', '#f59e0b', '#22c55e', '#ef4444', '#64748b'];

    return (
        <div>
            <header style={{ marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '1.875rem', fontWeight: 'bold' }}>Welcome Back!</h1>
                <p style={{ color: 'var(--text-muted)' }}>Here's what's happening with your leads today.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
                <StatCard title="Total Leads" value={totalLeads} icon={Users} color="#2563eb" />
                <StatCard title="New Leads" value={stats.find(s => s.status === 'New')?.count || 0} icon={TrendingUp} color="#22c55e" />
                <StatCard title="In Progress" value={stats.find(s => s.status === 'Follow-Up')?.count || 0} icon={Clock} color="#f59e0b" />
                <StatCard title="Completed" value={stats.find(s => s.status === 'Finished')?.count || 0} icon={CheckCircle} color="#64748b" />
            </div>

            <div className="premium-card" style={{ height: '400px' }}>
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
        </div>
    );
};

export default Dashboard;
