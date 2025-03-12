'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { TweetCard } from '@/components/TweetCard';
import { TweetForm } from '@/components/TweetForm';
import { Tweet } from '@/types';
import { useAuth } from '@/context/AppContext';
import { motion } from 'framer-motion';
import { getTweets, createTweet } from '@/services/api';

const HomePage = () => {
  const { user, isAuthenticated, loading: authLoading, isDarkMode } = useAuth();
  const [tweets, setTweets] = useState<Tweet[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Redirection si non authentifié
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Fetch tweets
  useEffect(() => {
    const fetchTweets = async () => {
      if (!isAuthenticated) return;
      
      setIsLoading(true);
      setError(null);
      try {
        const data = await getTweets();
        setTweets(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error('Error fetching tweets:', error);
        setError('Failed to load tweets');
        setTweets([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTweets();
  }, [isAuthenticated]);

const handleTweetSubmit = async (content: string, mediaFile?: File, tags: string[] = []) => {
  console.log("📩 Tags reçus dans handleTweetSubmit :", tags);

  if (!user) return;

  try {
    const newTweet = await createTweet(content, mediaFile, tags);
    setTweets(prev => [newTweet, ...prev]);
  } catch (error) {
    console.error('Error creating tweet:', error);
  }
};



  const handleTweetUpdate = (updatedTweet: Tweet) => {
    setTweets(prev =>
      prev.map(tweet => (tweet.id === updatedTweet.id ? updatedTweet : tweet))
    );
  };

  // Loader component
  const Loader = () => (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gray-900' : 'bg-white'} flex justify-center items-center`}>
      <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
    </div>
  );

  // Error component
  const ErrorDisplay = () => (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gray-900' : 'bg-white'} flex justify-center items-center`}>
      <div className="text-red-500 flex flex-col items-center">
        <p>{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-purple-500 rounded-full text-white hover:bg-purple-600 transition-colors"
        >
          Réessayer
        </button>
      </div>
    </div>
  );

  if (authLoading) return <Loader />;
  if (!isAuthenticated) return null;
  if (isLoading) return <Loader />;
  if (error) return <ErrorDisplay />;

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gray-900' : 'bg-white'}`}>
      <main className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className={`sticky top-0 z-10 ${
            isDarkMode 
              ? 'bg-gray-900/80 border-gray-800' 
              : 'bg-white/80 border-gray-200'
          } backdrop-blur-md`}>
            <div className={`px-4 py-3 border-b ${
              isDarkMode ? 'border-gray-800' : 'border-gray-200'
            }`}>
              <h1 className={`text-xl font-bold ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}>Accueil</h1>
            </div>
            <TweetForm onSubmit={handleTweetSubmit} />
          </div>

          <div className={`divide-y ${
            isDarkMode ? 'divide-gray-800' : 'divide-gray-200'
          }`}>
            {tweets.length > 0 ? (
              tweets.map(tweet => (
                <motion.div
                  key={tweet.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  <TweetCard
                    tweet={tweet}
                    onTweetUpdate={handleTweetUpdate}
                  />
                </motion.div>
              ))
            ) : (
              <div className={`flex flex-col items-center justify-center py-8 ${
                isDarkMode ? 'text-gray-400' : 'text-gray-500'
              }`}>
                <p className="text-xl font-semibold">Aucun tweet pour le moment</p>
                <p className="mt-2">Soyez le premier à tweeter !</p>
              </div>
            )}
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default HomePage;