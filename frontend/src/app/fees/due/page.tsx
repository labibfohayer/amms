/* eslint-disable */
"use client";
import AppLayout from '@/components/layout/AppLayout';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function DueFees() {
    const { data, isLoading } = useQuery({
        queryKey: ['due-fees'],
        queryFn: async () => {
            const res = await api.get('/api/fees/due/');
            return res.data;
        }
    });

    if (isLoading) return <AppLayout title="বকেয়া ফি"><p>লোড হচ্ছে...</p></AppLayout>;

    const totalDue = data?.reduce((acc: number, item: any) => acc + parseFloat(item.due_amount), 0) || 0;

    return (
        <AppLayout title="বকেয়া ফি">
            <div className="text-center mb-6">
                <h2 className="text-lg font-medium text-gray-600">মোট বকেয়া</h2>
                <p className="text-3xl font-bold text-red-600">৳{totalDue}</p>
            </div>
            <div className="space-y-3">
                {data?.map((fee: any) => (
                    <div key={fee.id} className="bg-white p-4 rounded-xl shadow-sm">
                        <h4 className="font-bold">{fee.student?.name_bn || 'Student'}</h4>
                        <p className="text-sm text-gray-500">{fee.fee_type?.name} - {fee.month}</p>
                        <p className="text-red-500 font-bold mt-2">বকেয়া: ৳{fee.due_amount}</p>
                    </div>
                ))}
            </div>
        </AppLayout>
    )
}
