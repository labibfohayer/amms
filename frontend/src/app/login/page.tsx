'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, User, Lock } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '@/lib/api';

export default function LoginPage() {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/api/auth/login/', { phone, password });
      const { access, refresh, role, user_id } = res.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify({ role, user_id }));
      toast.success('লগইন সফল হয়েছে!');
      if (['principal', 'vice_principal', 'managing_director', 'teacher', 'staff'].includes(role)) {
        router.push('/dashboard');
      } else if (role === 'guardian') {
        router.push('/guardian');
      } else {
        router.push('/student');
      }
    } catch {
      toast.error('ফোন নম্বর বা পাসওয়ার্ড ভুল হয়েছে!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-[#1B5E20] to-[#2E7D32]">
      {/* TOP - Green Islamic Header */}
      <div className="flex-none h-[45vh] flex flex-col items-center justify-center relative overflow-hidden px-6">
        {/* Islamic geometric pattern overlay */}
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
        
        {/* Mosque SVG */}
        <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-lg mb-4">
          <svg viewBox="0 0 100 100" className="w-16 h-16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 10 C50 10, 35 25, 35 35 L65 35 C65 25, 50 10, 50 10Z" fill="#2E7D32"/>
            <rect x="20" y="35" width="60" height="5" fill="#F9A825"/>
            <rect x="15" y="40" width="70" height="40" fill="#2E7D32"/>
            <rect x="40" y="55" width="20" height="25" rx="10" fill="#F9A825"/>
            <rect x="20" y="50" width="15" height="15" rx="2" fill="#F9A825"/>
            <rect x="65" y="50" width="15" height="15" rx="2" fill="#F9A825"/>
            <rect x="10" y="35" width="5" height="45" fill="#F9A825"/>
            <rect x="85" y="35" width="5" height="45" fill="#F9A825"/>
          </svg>
        </div>
        
        <h1 className="text-lg font-bold text-center" style={{color: '#F9A825', fontStyle: 'italic'}}>
          Al Modina Model Madrasah And Research Institute
        </h1>
        <p className="text-white text-center text-sm mt-1">
          আল মদিনা মডেল মাদ্রাসা এন্ড রিসার্চ ইনস্টিটিউট
        </p>
        <p className="text-green-200 text-center text-xs mt-1">মহাখালী দক্ষিণ পাড়া, ঢাকা</p>
      </div>

      {/* BOTTOM - White Login Card */}
      <div className="flex-1 bg-white rounded-t-3xl px-6 pt-8 pb-6">
        <h2 className="text-2xl font-bold mb-6" style={{color: '#1B5E20'}}>লগইন করুন</h2>
        
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Phone */}
          <div className="relative">
            <User className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="ফোন নম্বর (01XXXXXXXXX)"
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          
          {/* Password */}
          <div className="relative">
            <Lock className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="পাসওয়ার্ড"
              className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-3.5 text-gray-400"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          
          {/* Login Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded-full text-white font-bold text-lg shadow-lg disabled:opacity-70 mt-4 bg-gradient-to-r from-[#1B5E20] to-[#2E7D32]"
          >
            {loading ? 'লগইন হচ্ছে...' : 'লগইন করুন'}
          </button>
        </form>
        
        <div className="text-center mt-4">
          <button className="text-sm" style={{color: '#2E7D32'}}>পাসওয়ার্ড ভুলে গেছেন?</button>
        </div>
        
        <div className="text-center mt-8 text-xs text-gray-400">
          © 2026 আল মদিনা মডেল মাদ্রাসা
        </div>
      </div>
    </div>
  );
}
