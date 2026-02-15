import React, { useState, useEffect } from 'react';
import { Bell, CheckCircle, Clock } from 'lucide-react';
import { apiFetch } from '../api';

const NotificationsPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchNotifications = async () => {
        setIsLoading(true);
        try {
            const data = await apiFetch('/notifications');
            setNotifications(data);
        } catch (e) {
            console.error("Failed to fetch notifications", e);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchNotifications();
    }, []);

    const markAsRead = async (id) => {
        try {
            await apiFetch(`/notifications/${id}/read`, { method: 'PUT' });
            setNotifications(notifications.map(n =>
                n.notification_id === id ? { ...n, is_read: true } : n
            ));
        } catch (e) {
            alert("Failed to mark as read: " + e.message);
        }
    };

    if (isLoading) return <div style={{ padding: '2rem' }}>Loading notifications...</div>;

    const unreadCount = notifications.filter(n => !n.is_read).length;

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '1.875rem', fontWeight: 'bold' }}>Notifications</h1>
                {unreadCount > 0 && (
                    <span style={{ fontSize: '0.875rem', padding: '0.25rem 0.75rem', background: 'var(--danger)', color: 'white', borderRadius: '9999px' }}>
                        {unreadCount} Unread
                    </span>
                )}
            </div>

            <div className="premium-card" style={{ padding: '0', overflow: 'hidden' }}>
                {notifications.length === 0 ? (
                    <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                        <Bell size={48} style={{ marginBottom: '1rem', opacity: 0.2, margin: '0 auto' }} />
                        <p>No notifications yet.</p>
                    </div>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        {notifications.map((notif) => (
                            <div
                                key={notif.notification_id}
                                style={{
                                    padding: '1.25rem 1.5rem',
                                    borderBottom: '1px solid var(--border)',
                                    background: notif.is_read ? 'transparent' : '#f0f7ff',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'flex-start',
                                    gap: '1rem'
                                }}
                            >
                                <div style={{ display: 'flex', gap: '1rem' }}>
                                    <div style={{
                                        marginTop: '0.25rem',
                                        color: notif.is_read ? 'var(--text-muted)' : 'var(--primary)'
                                    }}>
                                        {notif.is_read ? <CheckCircle size={20} /> : <Bell size={20} />}
                                    </div>
                                    <div>
                                        <p style={{
                                            fontWeight: notif.is_read ? '400' : '600',
                                            color: notif.is_read ? 'var(--text-muted)' : 'var(--text)',
                                            fontSize: '1rem',
                                            marginBottom: '0.25rem'
                                        }}>
                                            {notif.message}
                                        </p>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                            <Clock size={12} />
                                            {new Date(notif.created_at).toLocaleString()}
                                        </div>
                                    </div>
                                </div>
                                {!notif.is_read && (
                                    <button
                                        onClick={() => markAsRead(notif.notification_id)}
                                        className="btn"
                                        style={{
                                            fontSize: '0.75rem',
                                            border: '1px solid var(--primary)',
                                            color: 'var(--primary)',
                                            background: 'white',
                                            padding: '0.25rem 0.5rem'
                                        }}
                                    >
                                        Mark as Read
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default NotificationsPage;
