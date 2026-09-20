/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import Link from 'next/link';
import { Plus } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function Notices() {
    const { user } = useAuth();
    
    const { data: notices, isLoading } = useQuery({
        queryKey: ['notices'],
        queryFn: async () => {
            const res = await api.get('/api/notices/');
            return res.data;
        }
    });

    return (
        <AppLayout title="নোটিশ বোর্ড">
            {isLoading ? <p>লোড হচ্ছে...</p> : (
                <div className="space-y-3">
                    {notices?.length ? notices.map((n: any) => (
                        <div key={n.id} className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-primary">
                            <h3 className="font-bold text-lg">{n.title}</h3>
                            <p className="text-sm text-gray-600 mt-1">{n.content}</p>
                            <p className="text-xs text-gray-400 mt-2">{new Date(n.created_at).toLocaleDateString('bn-BD')}</p>
                        </div>
                    )) : (
                        <div className="bg-white p-4 rounded-xl shadow-sm">
                            <p className="text-gray-500 text-center">কোনো নোটিশ নেই</p>
                        </div>
                    )}
                </div>
            )}
            
            {user && ['principal', 'vice_principal', 'managing_director', 'teacher'].includes(user.role) && (
                <Link href="/notices/add" className="fixed bottom-20 right-4 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary-dark z-50">
                    <Plus size={24} />
                </Link>
            )}
        </AppLayout>
    )
}
