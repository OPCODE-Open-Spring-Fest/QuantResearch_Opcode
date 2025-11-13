import React from 'react';
import { MetricCardProps } from '../types';
import { formatNumber, formatChange, getColorForValue } from '../utils/formatters';
import { TrendingUp, TrendingDown, HelpCircle } from 'lucide-react';

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  format = 'number',
  description
}) => {
  const formattedValue = typeof value === 'number' ? formatNumber(value, format) : value;
  const changeColor = change && change >= 0 ? 'text-green-600' : 'text-red-600';
  const valueColor = getColorForValue(typeof value === 'number' ? value : 0, title.toLowerCase());

  return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-600 flex items-center gap-1">
          {title}
          {description && (
            <HelpCircle className="w-3 h-3 text-gray-400" title={description} />
          )}
        </h3>
        {change !== undefined && (
          <div className={`flex items-center text-xs font-medium ${changeColor}`}>
            {change >= 0 ? (
              <TrendingUp className="w-3 h-3 mr-1" />
            ) : (
              <TrendingDown className="w-3 h-3 mr-1" />
            )}
            {formatChange(change)}
          </div>
        )}
      </div>
      
      <div className={`text-2xl font-bold ${valueColor}`}>
        {formattedValue}
      </div>
      
      {description && (
        <p className="text-xs text-gray-500 mt-2 hidden sm:block">
          {description}
        </p>
      )}
    </div>
  );
};

export default MetricCard;