/* eslint-disable */
'use client';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
    const { user, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated) {
            router.push('/login');
        } else if (user) {
            if (['principal', 'vice_principal', 'managing_director', 'teacher', 'staff'].includes(user.role)) router.push('/dashboard');
            else if (user.role === 'guardian') router.push('/guardian');
            else router.push('/student');
        } else {
            // User is authenticated but user object is missing/broken, force re-login
            localStorage.clear();
            router.push('/login');
        }
    }, [user, isAuthenticated, router]);

    return <div className="min-h-screen flex items-center justify-center text-primary font-bold">লোড হচ্ছে...</div>;
}
