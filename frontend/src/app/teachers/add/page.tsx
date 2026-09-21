'use client';
import AppLayout from '@/components/layout/AppLayout';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import api from '@/lib/api';

export default function AddTeacher() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        name_bn: '',
        phone: '',
        staff_type: 'teacher',
        designation: 'Teacher',
        designation_bn: 'শিক্ষক',
        qualification: '',
        joining_date: new Date().toISOString().split('T')[0],
        monthly_salary: '',
        address: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await api.post('/api/teachers/', formData);
            toast.success('শিক্ষক/স্টাফ সফলভাবে যুক্ত করা হয়েছে!');
            router.push('/teachers');
        } catch (error) {
            toast.error('শিক্ষক যোগ করতে সমস্যা হয়েছে! তথ্যগুলো চেক করুন।');
        } finally {
            setLoading(false);
        }
    };

    return (
        <AppLayout title="নতুন শিক্ষক/স্টাফ যোগ করুন">
            <div className="max-w-3xl mx-auto bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100 mb-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">নাম (ইংরেজিতে) *</label>
                            <input type="text" name="name" required value={formData.name} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">নাম (বাংলায়)</label>
                            <input type="text" name="name_bn" value={formData.name_bn} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">মোবাইল নম্বর (লগ-ইন আইডি) *</label>
                            <input type="tel" name="phone" required value={formData.phone} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                            <p className="text-xs text-gray-500 mt-1">এই নম্বরটি দিয়ে তিনি সিস্টেমে লগ-ইন করতে পারবেন</p>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">স্টাফ টাইপ *</label>
                            <select name="staff_type" value={formData.staff_type} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all">
                                <option value="teacher">শিক্ষক (Teacher)</option>
                                <option value="staff">স্টাফ (Staff)</option>
                                <option value="accountant">হিসাবরক্ষক (Accountant)</option>
                                <option value="other">অন্যান্য (Other)</option>
                            </select>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">পদবী (ইংরেজিতে) *</label>
                            <input type="text" name="designation" required value={formData.designation} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">পদবী (বাংলায়)</label>
                            <input type="text" name="designation_bn" value={formData.designation_bn} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">যোগ্যতা (Qualification) *</label>
                            <input type="text" name="qualification" required value={formData.qualification} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">যোগদানের তারিখ *</label>
                            <input type="date" name="joining_date" required value={formData.joining_date} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">মাসিক বেতন (টাকা) *</label>
                            <input type="number" name="monthly_salary" required value={formData.monthly_salary} onChange={handleChange} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                        </div>
                    </div>
                    
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">ঠিকানা *</label>
                        <textarea name="address" required value={formData.address} onChange={handleChange} rows={2} className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"></textarea>
                    </div>

                    <div className="pt-4 border-t border-gray-100 flex gap-4">
                        <button type="button" onClick={() => router.back()} className="w-1/3 py-3 rounded-xl font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 transition-colors">
                            বাতিল করুন
                        </button>
                        <button type="submit" disabled={loading} className="w-2/3 bg-primary text-white py-3 rounded-xl font-bold hover:bg-primary-dark transition-colors shadow-lg hover:shadow-xl disabled:opacity-70">
                            {loading ? 'সংরক্ষণ হচ্ছে...' : 'শিক্ষক যোগ করুন'}
                        </button>
                    </div>
                </form>
            </div>
        </AppLayout>
    )
}
