import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { DrawdownDataPoint } from '../types';
import { formatNumber, formatDate } from '../utils/formatters';

interface DrawdownChartProps {
  data: DrawdownDataPoint[];
  height?: number;
  loading?: boolean;
}

const DrawdownChart: React.FC<DrawdownChartProps> = ({
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
    drawdown: item.drawdown * 100 // Convert to percentage
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-300 rounded-lg shadow-sm">
          <p className="text-sm font-medium text-gray-700 mb-1">{label}</p>
          <p className="text-sm text-red-600">
            Drawdown: {formatNumber(payload[0].value, 'percentage')}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Drawdown Chart</h3>
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
            tickFormatter={(value) => formatNumber(value, 'percentage')}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="drawdown"
            stroke="#ef4444"
            fill="#fecaca"
            fillOpacity={0.6}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DrawdownChart;