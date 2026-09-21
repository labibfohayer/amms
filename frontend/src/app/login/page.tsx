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
      const { access, refresh, role, user_id, name_bn } = res.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify({ role, user_id, name_bn }));
      toast.success('সফলভাবে লগ-ইন হয়েছে!');
      if (['principal', 'vice_principal', 'managing_director', 'teacher', 'staff'].includes(role)) {
        router.push('/dashboard');
      } else if (role === 'guardian') {
        router.push('/guardian');
      } else {
        router.push('/student');
      }
    } catch {
      toast.error('মোবাইল নম্বর বা পাসওয়ার্ড ভুল হয়েছে!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-[#1B5E20] to-[#2E7D32]">
      {/* TOP - Green Islamic Header */}
      <div className="flex-none h-[45vh] flex flex-col items-center justify-center relative overflow-hidden px-6">
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
        
        <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-lg mb-4 z-10">
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
        
        <h1 className="text-lg font-bold text-center z-10" style={{color: '#F9A825', fontStyle: 'italic'}}>
          Al Modina Model Madrasah And Research Institute
        </h1>
        <p className="text-white text-center text-sm mt-1 z-10">
          আল-মদিনা মডেল মাদ্রাসা এন্ড রিসার্চ ইনস্টিটিউট
        </p>
        <p className="text-green-200 text-center text-xs mt-1 z-10">ডিজিটাল ম্যানেজমেন্ট সিস্টেম</p>
      </div>

      {/* BOTTOM - White Login Card */}
      <div className="flex-1 bg-white rounded-t-3xl px-6 pt-8 pb-6 z-20 shadow-[-0_10px_40px_rgba(0,0,0,0.2)]">
        <h2 className="text-2xl font-bold mb-6 text-[#1B5E20] text-center">লগ-ইন করুন</h2>
        
        <form onSubmit={handleLogin} className="space-y-4 max-w-sm mx-auto">
          {/* Phone */}
          <div className="relative">
            <User className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="মোবাইল নম্বর বা স্টুডেন্ট আইডি"
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
              placeholder="পাসওয়ার্ড"
              className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          
          {/* Login Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded-xl text-white font-bold text-lg shadow-lg disabled:opacity-70 mt-4 bg-gradient-to-r from-[#1B5E20] to-[#2E7D32] hover:shadow-xl transition-all hover:-translate-y-0.5"
          >
            {loading ? 'লগ-ইন হচ্ছে...' : 'লগ-ইন করুন'}
          </button>
        </form>
        
        <div className="text-center mt-6">
          <p className="text-xs text-gray-500 font-medium bg-gray-50 p-3 rounded-lg border border-gray-100 max-w-sm mx-auto shadow-sm">
            🎓 <span className="text-primary font-bold">ছাত্র-ছাত্রীদের জন্য:</span><br/>
            স্টুডেন্ট আইডি এবং জন্ম তারিখ (DDMMYYYY)<br/>দিয়ে লগিন করো।
          </p>
        </div>
        
        <div className="text-center mt-4 text-xs text-gray-400">
          &copy; 2026 আল-মদিনা মডেল মাদ্রাসা
        </div>
      </div>
    </div>
  );
}
