/* eslint-disable */
export interface User {
  user_id: string;
  name: string;
  name_bn: string;
  role: 'principal' | 'vice_principal' | 'managing_director' | 'teacher' | 'staff' | 'guardian' | 'student';
  phone: string;
  photo?: string;
}

export const getUser = (): User | null => {
  if (typeof window === 'undefined') return null;
  const u = localStorage.getItem('user');
  return u ? JSON.parse(u) : null;
};

export const isLoggedIn = () => {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('access_token');
}

export const logout = () => {
    if (typeof window === 'undefined') return;
  localStorage.clear();
  window.location.href = '/login';
};
