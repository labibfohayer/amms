/* eslint-disable */
'use client';
import AppLayout from '@/components/layout/AppLayout';
import StatCard from '@/components/ui/StatCard';
import { useAuth } from '@/contexts/AuthContext';
import { Users, UserCheck, UserX, UserPlus, DollarSign, FileText, Bell, BarChart } from 'lucide-react';
import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function Dashboard() {
    const { user, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated) router.push('/login');
        if (user && !['principal', 'vice_principal', 'managing_director', 'teacher', 'staff'].includes(user.role)) router.push('/');
    }, [user, isAuthenticated, router]);

    if (!user) return null;

    return (
        <AppLayout title="ড্যাশবোর্ড">
            <div className="mb-6">
                <h2 className="text-xl font-bold text-primary">আস-সালামু আলাইকুম, {user.name_bn}!</h2>
                <p className="text-sm text-gray-500">{new Date().toLocaleDateString('bn-BD', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
            </div>

            {['principal', 'vice_principal', 'managing_director'].includes(user.role) && (
                <PrincipalDashboard />
            )}

            {user.role === 'teacher' && (
                <>
                    <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500 mb-6">
                        <h3 className="text-gray-500 text-sm">এই মাসের বেতন</h3>
                        <p className="text-xl font-bold text-green-700">৳১৫,০০০ — পরিশোধিত ✓</p>
                    </div>
                    <h3 className="font-bold text-gray-700 mb-3">আজকের কাজ</h3>
                    <div className="grid grid-cols-2 gap-3">
                        <QuickAction href="/attendance" icon={<UserCheck />} text="উপস্থিতি নিন" />
                        <QuickAction href="/exams" icon={<FileText />} text="নম্বর দিন" />
                        <QuickAction href="/notices/add" icon={<Bell />} text="নোটিশ দিন" />
                    </div>
                </>
            )}

             {user.role === 'staff' && (
                <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500 mb-6">
                    <h3 className="text-gray-500 text-sm">এই মাসের বেতন</h3>
                    <p className="text-xl font-bold text-green-700">৳১০,০০০ — পরিশোধিত ✓</p>
                </div>
            )}
        </AppLayout>
    );
}

function QuickAction({ href, icon, text }: { href: string; icon: React.ReactNode; text: string }) {
    return (
        <Link href={href} className="flex flex-col items-center justify-center p-4 bg-white rounded-xl shadow-sm hover:bg-gray-50 border border-gray-100">
            <div className="text-primary mb-2">{icon}</div>
            <span className="text-sm font-medium text-gray-700">{text}</span>
        </Link>
    );
}

function PrincipalDashboard() {
    const { data, isLoading } = useQuery({
        queryKey: ['dashboard_stats'],
        queryFn: async () => {
            const res = await api.get('/api/reports/dashboard/');
            return res.data;
        }
    });

    if (isLoading) return <div className="text-center p-4 text-gray-500">লোড হচ্ছে...</div>;

    const stats = data || { total_students: 0, today_present: 0, today_absent: 0, total_due_fees: 0, total_teachers: 0, total_staff: 0 };

    return (
        <>
            <div className="grid grid-cols-3 gap-3 mb-6">
                <StatCard title="মোট ছাত্র" value={stats.total_students} color="blue" icon={<Users size={20} />} />
                <StatCard title="আজ উপস্থিত" value={stats.today_present} color="green" icon={<UserCheck size={20} />} />
                <StatCard title="আজ অনুপস্থিত" value={stats.today_absent} color="red" icon={<UserX size={20} />} />
            </div>
            
            <div className="space-y-4 mb-6">
                <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-red-500 flex justify-between items-center">
                    <div>
                        <h3 className="text-gray-500 text-sm">মোট বকেয়া ফি</h3>
                        <p className="text-xl font-bold text-red-600">৳{stats.total_due_fees}</p>
                    </div>
                    <DollarSign className="text-red-300" size={32} />
                </div>
                <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-orange-500 flex justify-between items-center">
                    <div>
                        <h3 className="text-gray-500 text-sm">স্টাফ</h3>
                        <p className="font-medium">শিক্ষক: {stats.total_teachers} | কর্মী: {stats.total_staff}</p>
                    </div>
                    <Users className="text-orange-300" size={32} />
                </div>
            </div>

            <h3 className="font-bold text-gray-700 mb-3">দ্রুত কাজ</h3>
            <div className="grid grid-cols-2 gap-3 mb-6">
                <QuickAction href="/students/add" icon={<UserPlus />} text="ছাত্র ভর্তি" />
                <QuickAction href="/attendance" icon={<UserCheck />} text="উপস্থিতি" />
                <QuickAction href="/fees" icon={<DollarSign />} text="ফি সংগ্রহ" />
                <QuickAction href="/exams" icon={<FileText />} text="রেজাল্ট" />
                <QuickAction href="/notices/add" icon={<Bell />} text="নোটিশ দিন" />
                <QuickAction href="/reports" icon={<BarChart />} text="রিপোর্ট" />
            </div>
        </>
    );
}
