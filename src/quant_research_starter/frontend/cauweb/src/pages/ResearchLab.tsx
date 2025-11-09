import React from 'react';
import { Beaker, LineChart, BarChart3, Activity } from 'lucide-react';

export const ResearchLab: React.FC = () => {
  const factors = [
    { name: 'Momentum', description: 'Price momentum factors', icon: Activity, color: 'blue' },
    { name: 'Value', description: 'Valuation metrics', icon: BarChart3, color: 'green' },
    { name: 'Size', description: 'Market capitalization', icon: LineChart, color: 'purple' },
    { name: 'Volatility', description: 'Price volatility measures', icon: Activity, color: 'red' }
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Research Lab</h1>
        <p className="text-gray-600 mt-2">Explore and analyze alpha factors</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {factors.map((factor, index) => {
          const Icon = factor.icon;
          const colorClasses = {
            blue: 'bg-blue-100 text-blue-600',
            green: 'bg-green-100 text-green-600',
            purple: 'bg-purple-100 text-purple-600',
            red: 'bg-red-100 text-red-600'
          };

          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className={`w-12 h-12 ${colorClasses[factor.color as keyof typeof colorClasses]} rounded-lg flex items-center justify-center mb-4`}>
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{factor.name}</h3>
              <p className="text-gray-600 text-sm">{factor.description}</p>
              <button className="mt-4 w-full bg-gray-100 text-gray-700 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                Analyze Factor
              </button>
            </div>
          );
        })}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Factor Performance</h3>
        <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500">
          Factor performance charts will be displayed here
        </div>
      </div>
    </div>
  );
};