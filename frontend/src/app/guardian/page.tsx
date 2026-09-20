/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function GuardianDashboard() {
    const { user } = useAuth();
    
    const { data: students, isLoading } = useQuery({
        queryKey: ['my_students'],
        queryFn: async () => {
            const res = await api.get('/api/students/');
            return res.data;
        }
    });

    return (
        <AppLayout title="অভিভাবক ড্যাশবোর্ড">
            {isLoading ? <p>লোড হচ্ছে...</p> : (
                students?.map((student: any) => (
                    <div key={student.id} className="mb-6">
                        <h2 className="text-lg font-bold mb-4">আপনার সন্তান: {student.name_bn}</h2>
                        <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                            <p className="text-gray-500 text-sm">স্ট্যাটাস: {student.status}</p>
                            <p className="text-gray-500 text-sm">আইডি: {student.student_id}</p>
                        </div>
                    </div>
                ))
            )}
        </AppLayout>
    )
}
