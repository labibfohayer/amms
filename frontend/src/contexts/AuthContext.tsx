/* eslint-disable */
"use client";
import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, getUser, isLoggedIn, logout } from '../lib/auth';
import { usePathname } from 'next/navigation';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  logoutUser: () => void;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  logoutUser: logout,
  setUser: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUserState] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const pathname = usePathname();

  useEffect(() => {
    let mounted = true;
    if (mounted) {
        const u = getUser();
        setUserState(u);
        setIsAuthenticated(isLoggedIn());
        setLoading(false);
    }
    return () => { mounted = false; };
  }, [pathname]);

  const logoutUser = () => {
    logout();
    setUserState(null);
    setIsAuthenticated(false);
  };

  const setUser = (u: User | null) => {
      setUserState(u);
      setIsAuthenticated(!!u);
  }

  if (loading) return null;

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, logoutUser, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
