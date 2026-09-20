/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function StudentDashboard() {
    const { user } = useAuth();
    
    const { data: studentInfo, isLoading } = useQuery({
        queryKey: ['student_info'],
        queryFn: async () => {
            const res = await api.get('/api/students/me/');
            return res.data;
        },
        retry: false
    });

    return (
        <AppLayout title="ছাত্র ড্যাশবোর্ড">
            <h2 className="text-lg font-bold mb-4 text-primary">আস-সালামু আলাইকুম, {user?.name_bn || 'ছাত্র'}!</h2>
            {isLoading ? <p>লোড হচ্ছে...</p> : (
                <div className="bg-white p-4 rounded-xl shadow-sm mb-4 text-center">
                    <p className="text-gray-500 text-sm mb-2">স্ট্যাটাস</p>
                    <h3 className="text-2xl font-bold text-gray-800">{studentInfo?.status || 'N/A'}</h3>
                    <p className="text-sm font-medium text-gray-700 mt-1">আইডি: {studentInfo?.student_id || 'N/A'}</p>
                </div>
            )}
        </AppLayout>
    )
}
