import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { PerformanceDataPoint } from '../types';
import { formatNumber, formatDate } from '../utils/formatters';

interface PerformanceChartProps {
  data: PerformanceDataPoint[];
  height?: number;
  loading?: boolean;
}

const PerformanceChart: React.FC<PerformanceChartProps> = ({
  data,
  height = 300,
  loading = false
}) => {
  if (loading) {
    return (
      <div 
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse"
        style={{ height }}
      >
        <div className="h-full bg-gray-200 rounded"></div>
      </div>
    );
  }

  const chartData = data.map(item => ({
    ...item,
    date: formatDate(item.date),
    portfolio: item.value,
    benchmark: item.benchmark
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-300 rounded-lg shadow-sm">
          <p className="text-sm font-medium text-gray-700 mb-1">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {formatNumber(entry.value, 'currency')}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Performance Chart</h3>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="date" 
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 12 }}
            interval="preserveStartEnd"
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => formatNumber(value, 'currency')}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="portfolio"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            name="Portfolio"
          />
          <Line
            type="monotone"
            dataKey="benchmark"
            stroke="#6b7280"
            strokeWidth={2}
            strokeDasharray="3 3"
            dot={false}
            name="Benchmark"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceChart;