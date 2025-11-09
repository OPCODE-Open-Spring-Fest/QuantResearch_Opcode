import { useState, useEffect } from 'react';
import { api } from '../utils/api';
export const useQuantData = () => {
    const [assets, setAssets] = useState([]);
    const [loading, setLoading] = useState(false);
    const [backtestResults, setBacktestResults] = useState(null);
    useEffect(() => {
        loadAssets();
    }, []);
    const loadAssets = async () => {
        try {
            const data = await api.getAssets();
            setAssets(data);
        }
        catch (error) {
            console.error('Failed to load assets:', error);
        }
    };
    const runBacktest = async (config) => {
        setLoading(true);
        try {
            const results = await api.runBacktest(config);
            setBacktestResults(results);
        }
        catch (error) {
            console.error('Backtest failed:', error);
        }
        finally {
            setLoading(false);
        }
    };
    return {
        assets,
        loading,
        backtestResults,
        runBacktest
    };
};
