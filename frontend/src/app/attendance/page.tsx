"use client";
import AppLayout from '@/components/layout/AppLayout';

export default function Attendance() {
    return (
        <AppLayout title="উপস্থিতি">
            <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                <select className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary mb-3">
                    <option>শ্রেণী নির্বাচন করুন</option>
                    <option>প্রথম শ্রেণী</option>
                </select>
                <input type="date" className="w-full p-2 border border-gray-200 rounded-lg focus:outline-none focus:border-primary" />
            </div>
            <div className="space-y-2">
                {[1,2,3].map(i => (
                    <div key={i} className="bg-white p-3 rounded-lg shadow-sm flex items-center justify-between hover:bg-gray-50 transition-colors">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                                <span className="text-gray-500 font-bold text-xs">{i}</span>
                            </div>
                            <div>
                                <h4 className="font-medium text-sm">ছাত্রের নাম {i}</h4>
                                <p className="text-xs text-gray-500">রোল: {i}</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button className="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center font-bold hover:bg-green-200 transition-colors">✓</button>
                            <button className="w-8 h-8 bg-gray-100 text-gray-400 rounded-full flex items-center justify-center font-bold hover:bg-red-100 hover:text-red-600 transition-colors">✗</button>
                        </div>
                    </div>
                ))}
            </div>
            <button className="w-full mt-6 bg-primary text-white py-3 rounded-xl font-bold hover:bg-primary-dark transition-colors shadow-lg hover:shadow-xl">উপস্থিতি সাবমিট করুন</button>
        </AppLayout>
    )
}
