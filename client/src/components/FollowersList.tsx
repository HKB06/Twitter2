'use client';

import React, { useState, useEffect } from 'react';
import { getUserFollowers } from '@/services/api';
import { User } from '@/types';
import Link from 'next/link';
import FollowButton from './FollowButton';
import { motion, AnimatePresence } from 'framer-motion';
import { FiX } from 'react-icons/fi';

interface FollowersListProps {
  username: string;
  isVisible: boolean;
  onClose: () => void;
  isDarkMode: boolean;
}

const FollowersList: React.FC<FollowersListProps> = ({ username, isVisible, onClose, isDarkMode }) => {
  const [followers, setFollowers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchFollowers = async () => {
      if (!isVisible) return;

      try {
        setLoading(true);
        const data = await getUserFollowers(username);
        setFollowers(data);
        setError('');
      } catch (error) {
        console.error('Erreur lors de la récupération des abonnés:', error);
        setError('Impossible de charger les abonnés');
      } finally {
        setLoading(false);
      }
    };

    fetchFollowers();
  }, [username, isVisible]);

  if (!isVisible) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50 p-4"
      >
        <motion.div
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0.95 }}
          className={`w-full max-w-md max-h-[80vh] flex flex-col rounded-xl shadow-lg ${
            isDarkMode ? 'bg-gray-900' : 'bg-white'
          }`}
        >
          <div className={`p-4 border-b flex justify-between items-center ${
            isDarkMode ? 'border-gray-800' : 'border-gray-200'
          }`}>
            <h2 className={`text-xl font-bold ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Abonnés de @{username}
            </h2>
            <button 
              onClick={onClose}
              className={`p-2 rounded-full transition-colors ${
                isDarkMode 
                  ? 'text-gray-400 hover:text-white hover:bg-gray-800' 
                  : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <FiX className="w-5 h-5" />
            </button>
          </div>

          <div className="overflow-y-auto flex-grow">
            {loading ? (
              <div className="flex justify-center p-8">
                <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : error ? (
              <div className="p-4 text-red-500 text-center">{error}</div>
            ) : followers.length > 0 ? (
              <ul className={`divide-y ${
                isDarkMode ? 'divide-gray-800' : 'divide-gray-200'
              }`}>
                {followers.map((follower) => (
                  <li key={follower.id} className={`p-4 transition-colors ${
                    isDarkMode ? 'hover:bg-gray-800/50' : 'hover:bg-gray-50'
                  }`}>
                    <div className="flex items-center justify-between">
                      <Link 
                        href={`/profile/${follower.username}`}
                        className="flex items-center"
                      >
                        <div className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center">
                          <span className="text-white font-bold">
                            {follower.username.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div className="ml-3">
                          <p className={`font-semibold ${
                            isDarkMode ? 'text-white' : 'text-gray-900'
                          }`}>
                            {follower.username}
                          </p>
                          <p className={`text-sm ${
                            isDarkMode ? 'text-gray-400' : 'text-gray-500'
                          }`}>
                            @{follower.username}
                          </p>
                        </div>
                      </Link>
                      <FollowButton 
                        username={follower.username}
                        isDarkMode={isDarkMode}
                      />
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <div className={`p-8 text-center ${
                isDarkMode ? 'text-gray-400' : 'text-gray-500'
              }`}>
                Aucun abonné pour le moment
              </div>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default FollowersList;