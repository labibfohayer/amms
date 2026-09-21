"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';
import toast from 'react-hot-toast';

export default function Profile() {
    const { user, login } = useAuth();
    const [name, setName] = useState(user?.name_bn || '');
    const [phone, setPhone] = useState(user?.phone || '');
    const [loading, setLoading] = useState(false);

    const handleSave = (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setTimeout(() => {
            toast.success('প্রোফাইল সফলভাবে আপডেট হয়েছে!');
            // Update local user context for visual feedback
            if (user) {
                const updatedUser = { ...user, name_bn: name, phone: phone };
                localStorage.setItem('user', JSON.stringify(updatedUser));
                login(updatedUser.phone, 'admin123'); // Hack to force refresh context
            }
            setLoading(false);
            window.location.reload();
        }, 1000);
    };

    if (!user) return null;

    return (
        <AppLayout title="প্রোফাইল সেটিংস">
            <div className="max-w-2xl mx-auto bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
                <div className="flex items-center gap-4 mb-8">
                    <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center text-primary font-bold text-3xl shadow-inner border-2 border-primary/20">
                        {user.name_bn?.charAt(0) || 'U'}
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800">{user.name_bn || 'Admin'}</h2>
                        <p className="text-gray-500 capitalize">{user.role.replace('_', ' ')}</p>
                    </div>
                </div>

                <form onSubmit={handleSave} className="space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">আপনার নাম (বাংলায়)</label>
                        <input type="text" value={name} onChange={e=>setName(e.target.value)} className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">মোবাইল নম্বর</label>
                        <input type="text" value={phone} onChange={e=>setPhone(e.target.value)} className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all bg-gray-50" readOnly />
                        <p className="text-xs text-gray-400 mt-1">লগইন আইডি পরিবর্তনযোগ্য নয়</p>
                    </div>
                    <div className="pt-4">
                        <button type="submit" disabled={loading} className="w-full bg-primary text-white py-3 rounded-xl font-bold hover:bg-primary-dark transition-colors shadow-md disabled:opacity-70">
                            {loading ? 'আপডেট হচ্ছে...' : 'সেভ করুন'}
                        </button>
                    </div>
                </form>
            </div>
        </AppLayout>
    )
}
