import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Stats {
    total_words: number;
    correct_percentage: number;
    trend: string;
}

const Stats: React.FC = () => {
    const [stats, setStats] = useState<Stats | null>(null);

    const fetchStats = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/stats`);
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching stats:', error);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    if (!stats) {
        return <div>Loading stats...</div>;
    }

    return (
        <div>
            <h2>Statistics</h2>
            <p>Total Words: {stats.total_words}</p>
            <p>Correct Percentage: {stats.correct_percentage}%</p>
            <p>Trend: {stats.trend}</p>
        </div>
    );
};

export default Stats;
