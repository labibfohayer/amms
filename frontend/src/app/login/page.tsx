/* eslint-disable */
'use client';
import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { User, Lock, Eye, EyeOff } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function Login() {
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [showPass, setShowPass] = useState(false);
    const { setUser } = useAuth();
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await api.post('/api/auth/login/', { phone, password });
            localStorage.setItem('access_token', res.data.access);
            localStorage.setItem('refresh_token', res.data.refresh);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            setUser(res.data.user);
            
            const role = res.data.user.role;
            if (['principal', 'vice_principal', 'managing_director', 'teacher', 'staff'].includes(role)) router.push('/dashboard');
            else if (role === 'guardian') router.push('/guardian');
            else router.push('/student');
        } catch (error) {
            toast.error('লগইন ব্যর্থ হয়েছে। নম্বর ও পাসওয়ার্ড চেক করুন।');
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-gradient-to-b from-primary-dark to-primary">
            <div className="h-[45vh] flex flex-col items-center justify-center text-white relative">
                <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
                <div className="relative z-10 flex flex-col items-center">
                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mb-4 text-primary">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-12 h-12">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                        </svg>
                    </div>
                    <h2 className="text-gold italic font-serif text-sm">Al Modina Model Madrasah And Research Institute</h2>
                    <h1 className="text-xl font-bold mt-2 text-center">আল মদিনা মডেল মাদ্রাসা<br/>এন্ড রিসার্চ ইনস্টিটিউট</h1>
                </div>
            </div>
            
            <div className="flex-1 bg-white rounded-t-3xl p-6 pt-8">
                <h2 className="text-2xl font-bold text-primary-dark mb-6 text-center">লগইন করুন</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div className="relative">
                        <User className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input type="text" placeholder="ফোন নম্বর" value={phone} onChange={e=>setPhone(e.target.value)} className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
                    </div>
                    <div className="relative">
                        <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input type={showPass ? "text" : "password"} placeholder="পাসওয়ার্ড" value={password} onChange={e=>setPassword(e.target.value)} className="w-full pl-10 pr-10 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-primary" />
                        <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-3 top-3 text-gray-400">
                            {showPass ? <EyeOff size={20} /> : <Eye size={20} />}
                        </button>
                    </div>
                    <button type="submit" className="w-full bg-primary text-white py-3 rounded-xl font-bold text-lg hover:bg-primary-dark transition-colors">
                        লগইন
                    </button>
                    <div className="text-center mt-4">
                        <a href="#" className="text-primary text-sm font-medium">পাসওয়ার্ড ভুলে গেছেন?</a>
                    </div>
                </form>
            </div>
        </div>
    );
}
