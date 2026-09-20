import { UserCircle } from 'lucide-react';
import Image from 'next/image';

interface StudentProps {
    photo?: string;
    name_bn: string;
    class_name: string;
    status: string;
}

export default function StudentCard({ student }: { student: StudentProps }) {
    return (
        <div className="bg-white p-3 rounded-xl shadow-sm flex items-center gap-3">
            {student.photo ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={student.photo} alt={student.name_bn} className="w-12 h-12 rounded-full object-cover" />
            ) : (
                <UserCircle size={48} className="text-gray-400" />
            )}
            <div className="flex-1">
                <h4 className="font-semibold">{student.name_bn}</h4>
                <p className="text-xs text-gray-500">{student.class_name}</p>
            </div>
            <span className={`px-2 py-1 text-[10px] rounded-full ${student.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                {student.status === 'active' ? 'সক্রিয়' : 'নিষ্ক্রিয়'}
            </span>
        </div>
    )
}
