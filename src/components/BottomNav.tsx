'use client';

import { usePathname, useRouter } from 'next/navigation';
import { Home, Bell, Clock, User } from 'lucide-react';

const tabs = [
  { href: '/dashboard', icon: Home, label: 'Accueil' },
  { href: '/alerts', icon: Bell, label: 'Alertes' },
  { href: '/history', icon: Clock, label: 'Historique' },
  { href: '/profile', icon: User, label: 'Profil' },
];

export default function BottomNav() {
  const pathname = usePathname();
  const router = useRouter();

  return (
    <nav style={{
      position: 'fixed',
      bottom: 0,
      left: '50%',
      transform: 'translateX(-50%)',
      width: '100%',
      maxWidth: 430,
      height: 80,
      borderRadius: '30px 30px 0 0',
      background: 'white',
      boxShadow: '0 -10px 30px rgba(0,0,0,0.1)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-around',
      zIndex: 50,
      padding: '0 10px',
    }}>
      {tabs.map((tab) => {
        const isActive = pathname === tab.href || pathname.startsWith(tab.href + '/');
        const Icon = tab.icon;
        return (
          <button
            key={tab.href}
            onClick={() => router.push(tab.href)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 4,
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '8px 16px',
            }}
          >
            <Icon size={24} color={isActive ? '#7B61FF' : '#8D91B5'} strokeWidth={isActive ? 2.5 : 1.5} />
            <span style={{
              fontSize: 11,
              fontWeight: isActive ? 700 : 500,
              color: isActive ? '#7B61FF' : '#8D91B5',
            }}>
              {tab.label}
            </span>
          </button>
        );
      })}
    </nav>
  );
}