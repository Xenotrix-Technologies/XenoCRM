import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Mail, Phone, Calendar, MessageSquare, Plus } from 'lucide-react';
import { apiFetch } from '../api';

const LeadsPage = () => {
    const [leads, setLeads] = useState([]);
    const [filter, setFilter] = useState('All');
    const [searchTerm, setSearchTerm] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    const fetchLeads = async () => {
        setIsLoading(true);
        try {
            const data = await apiFetch(`/leads?status=${filter}`);
            setLeads(data);
        } catch (e) {
            console.error("Failed to fetch leads", e);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchLeads();
    }, [filter]);

    const handleStatusChange = async (leadId, newStatus) => {
        try {
            await apiFetch(`/leads/${leadId}/status`, {
                method: 'PUT',
                body: JSON.stringify({ status: newStatus })
            });
            fetchLeads(); // Refresh list
        } catch (e) {
            alert("Failed to update status: " + e.message);
        }
    };

    const filteredLeads = leads.filter(lead =>
    (lead.customer_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.phone?.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    const getStatusClass = (status) => {
        switch (status) {
            case 'New': return 'status-new';
            case 'Follow-Up': return 'status-followup';
            case 'Contract': return 'status-contract';
            case 'Project Given': return 'status-project';
            case 'Finished': return 'status-finished';
            default: return '';
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '1.875rem', fontWeight: 'bold' }}>Lead Management</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <div style={{ position: 'relative' }}>
                        <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                        <input
                            type="text"
                            placeholder="Search leads..."
                            style={{ padding: '0.6rem 1rem 0.6rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border)', width: '250px' }}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <select
                        className="btn btn-secondary"
                        style={{ background: 'white', border: '1px solid var(--border)', color: 'var(--text)' }}
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    >
                        <option value="All">All Status</option>
                        <option value="New">New</option>
                        <option value="Follow-Up">Follow-Up</option>
                        <option value="Contract">Contract</option>
                        <option value="Project Given">Project Given</option>
                        <option value="Finished">Finished</option>
                    </select>
                </div>
            </div>

            {/* Google Forms Integration Info Banner */}
            <div style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '1rem 1.5rem',
                borderRadius: '12px',
                marginBottom: '1.5rem',
                display: 'flex',
                alignItems: 'center',
                gap: '1rem',
                boxShadow: '0 4px 6px rgba(102, 126, 234, 0.2)'
            }}>
                <MessageSquare size={24} />
                <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>
                        📋 Leads from Google Forms
                    </div>
                    <div style={{ fontSize: '0.875rem', opacity: 0.9 }}>
                        New leads are automatically captured from your Google Form. Check the setup guide for integration instructions.
                    </div>
                </div>
            </div>

            <div className="premium-card" style={{ padding: '0', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ background: '#f8fafc', borderBottom: '1px solid var(--border)' }}>
                        <tr>
                            <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: '600', fontSize: '0.875rem' }}>Customer Name</th>
                            <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: '600', fontSize: '0.875rem' }}>Contact Info</th>
                            <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: '600', fontSize: '0.875rem' }}>Service</th>
                            <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: '600', fontSize: '0.875rem' }}>Status</th>
                            <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: '600', fontSize: '0.875rem' }}>Date & Time</th>
                            <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: '600', fontSize: '0.875rem' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredLeads.map(lead => (
                            <tr key={lead.lead_id} style={{ borderBottom: '1px solid var(--border)' }}>
                                <td style={{ padding: '1.25rem 1.5rem' }}>
                                    <div style={{ fontWeight: '600' }}>
                                        <Link to={`/leads/${lead.lead_id}`} style={{ color: 'inherit', textDecoration: 'none', cursor: 'pointer' }} onMouseOver={(e) => e.target.style.color = 'var(--primary)'} onMouseOut={(e) => e.target.style.color = 'inherit'}>
                                            {lead.customer_name}
                                        </Link>
                                    </div>
                                </td>
                                <td style={{ padding: '1.25rem 1.5rem' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        <Mail size={14} /> {lead.email}
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                                        <Phone size={14} /> {lead.phone}
                                    </div>
                                </td>
                                <td style={{ padding: '1.25rem 1.5rem' }}>
                                    <span style={{ fontSize: '0.875rem' }}>{lead.service || 'N/A'}</span>
                                </td>
                                <td style={{ padding: '1.25rem 1.5rem' }}>
                                    <span className={`status-badge ${getStatusClass(lead.status)}`}>
                                        {lead.status}
                                    </span>
                                </td>
                                <td style={{ padding: '1.25rem 1.5rem' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        <Calendar size={14} /> {new Date(lead.created_at).toLocaleDateString()}
                                    </div>
                                </td>
                                <td style={{ padding: '1.25rem 1.5rem' }}>
                                    <select
                                        style={{ padding: '0.4rem', borderRadius: '6px', border: '1px solid var(--border)', fontSize: '0.875rem' }}
                                        value={lead.status}
                                        onChange={(e) => handleStatusChange(lead.lead_id, e.target.value)}
                                    >
                                        <option value="New">New</option>
                                        <option value="Follow-Up">Follow-Up</option>
                                        <option value="Contract">Contract</option>
                                        <option value="Project Given">Project Given</option>
                                        <option value="Finished">Finished</option>
                                    </select>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {filteredLeads.length === 0 && (
                    <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                        No leads found for the selected criteria.
                    </div>
                )}
            </div>
        </div>
    );
};

export default LeadsPage;
