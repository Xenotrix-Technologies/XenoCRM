import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Mail, Phone, Calendar, User, Send, RefreshCw, MessageSquare } from 'lucide-react';
import { apiFetch } from '../api';

const ReplyForm = ({ onSend }) => {
    const [subject, setSubject] = useState('');
    const [body, setBody] = useState('');
    const [isSending, setIsSending] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSending(true);
        try {
            await onSend({ subject, body });
            setSubject('');
            setBody('');
        } catch (e) {
            alert("Failed to send: " + e.message);
        } finally {
            setIsSending(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ marginTop: '2rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>Quick Reply</h3>
            <input
                type="text"
                placeholder="Subject"
                required
                style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border)', marginBottom: '1rem' }}
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
            />
            <textarea
                placeholder="Write your message here..."
                required
                rows={4}
                style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border)', marginBottom: '1rem', fontFamily: 'inherit' }}
                value={body}
                onChange={(e) => setBody(e.target.value)}
            />
            <button type="submit" disabled={isSending} className="btn btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                {isSending ? <RefreshCw size={16} className="animate-spin" /> : <Send size={16} />}
                {isSending ? 'Sending...' : 'Send Message'}
            </button>
        </form>
    );
};

const LeadDetails = () => {
    const { id } = useParams();
    const [lead, setLead] = useState(null);
    const [emails, setEmails] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchLeadData = async () => {
        setLoading(true);
        try {
            const foundLead = await apiFetch(`/leads/${id}`);
            setLead(foundLead);

            const emailsData = await apiFetch(`/leads/${id}/emails`);
            setEmails(emailsData);
        } catch (e) {
            console.error("Failed to fetch lead details", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLeadData();
    }, [id]);

    const handleSync = async () => {
        try {
            await apiFetch('/emails/sync', { method: 'POST' });
            fetchLeadData();
        } catch (e) {
            console.error("Sync failed", e);
        }
    };

    const handleSendEmail = async ({ subject, body }) => {
        await apiFetch('/emails/send', {
            method: 'POST',
            body: JSON.stringify({
                to_email: lead.email,
                subject: subject,
                body: body
            })
        });
        fetchLeadData(); // Refresh history
    };

    if (loading) return <div style={{ padding: '2rem' }}>Loading...</div>;
    if (!lead) return <div style={{ padding: '2rem' }}>Lead not found</div>;

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
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <Link to="/leads" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', marginBottom: '1.5rem', textDecoration: 'none' }}>
                <ArrowLeft size={20} /> Back to Leads
            </Link>

            <div className="premium-card" style={{ marginBottom: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                        <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>{lead.customer_name}</h1>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.5rem', color: 'var(--text-muted)' }}>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Mail size={16} /> {lead.email}</span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Phone size={16} /> {lead.phone}</span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Calendar size={16} /> {new Date(lead.created_at).toLocaleDateString()}</span>
                            {lead.service && <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><MessageSquare size={16} /> {lead.service}</span>}
                        </div>
                    </div>
                    <span className={`status-badge ${getStatusClass(lead.status)}`}>
                        {lead.status}
                    </span>
                </div>
                {lead.message && (
                    <div style={{ marginTop: '1.5rem', padding: '1rem', background: '#f8fafc', borderRadius: '8px', fontSize: '0.9375rem' }}>
                        <p style={{ fontWeight: '600', color: 'var(--text-muted)', marginBottom: '0.5rem', fontSize: '0.75rem', textTransform: 'uppercase' }}>Initial Inquiry Message</p>
                        {lead.message}
                    </div>
                )}
            </div>

            <div className="premium-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Communication History</h2>
                    <button onClick={handleSync} className="btn btn-secondary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'white', border: '1px solid var(--border)' }}>
                        <RefreshCw size={16} /> Sync Emails
                    </button>
                </div>

                <div className="timeline" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {emails.length === 0 ? (
                        <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>No communication history found.</p>
                    ) : (
                        emails.map((email) => (
                            <div key={email.email_id} style={{
                                alignSelf: email.direction === 'Outbound' ? 'flex-end' : 'flex-start',
                                maxWidth: '85%',
                                background: email.direction === 'Outbound' ? '#f0f7ff' : '#ffffff',
                                border: `1px solid ${email.direction === 'Outbound' ? '#dbeafe' : 'var(--border)'}`,
                                borderRadius: '12px',
                                padding: '1.25rem'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                    {email.direction === 'Outbound' ? <Send size={14} /> : <Mail size={14} />}
                                    <strong>{email.direction === 'Outbound' ? 'You' : lead.customer_name}</strong>
                                    <span>•</span>
                                    <span>{new Date(email.sent_at).toLocaleString()}</span>
                                </div>
                                <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.5rem' }}>{email.subject}</h3>
                                <p style={{ whiteSpace: 'pre-wrap', color: 'var(--text)', fontSize: '0.9375rem', lineHeight: '1.5' }}>
                                    {email.body}
                                </p>
                            </div>
                        ))
                    )}
                </div>

                <div style={{ borderTop: '1px solid var(--border)', marginTop: '2rem', paddingTop: '1rem' }}>
                    <ReplyForm onSend={handleSendEmail} />
                </div>
            </div>
        </div>
    );
};

export default LeadDetails;
