import React from 'react';
import { PieChart, BarChart, TrendingUp, Users } from 'lucide-react';

export const PortfolioAnalytics: React.FC = () => {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Portfolio Analytics</h1>
        <p className="text-gray-600 mt-2">Deep dive into portfolio performance and risk</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Asset Allocation</h3>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <PieChart className="w-12 h-12 opacity-50 mr-4" />
            <span>Allocation chart will be displayed here</span>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sector Exposure</h3>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <BarChart className="w-12 h-12 opacity-50 mr-4" />
            <span>Sector exposure chart will be displayed here</span>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Analysis</h3>
          <div className="space-y-4">
            {[
              { metric: 'Value at Risk (95%)', value: '-5.2%' },
              { metric: 'Expected Shortfall', value: '-7.8%' },
              { metric: 'Beta to Market', value: '1.12' },
              { metric: 'Tracking Error', value: '4.5%' }
            ].map((item, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-gray-700">{item.metric}</span>
                <span className="font-semibold text-gray-900">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Attribution</h3>
          <div className="space-y-3">
            {[
              { factor: 'Stock Selection', contribution: '+3.2%' },
              { factor: 'Sector Allocation', contribution: '+1.8%' },
              { factor: 'Currency Effects', contribution: '-0.4%' },
              { factor: 'Transaction Costs', contribution: '-0.9%' }
            ].map((item, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-gray-600">{item.factor}</span>
                <span className={`font-medium ${
                  item.contribution.startsWith('+') 
                    ? 'text-green-600' 
                    : item.contribution.startsWith('-')
                    ? 'text-red-600'
                    : 'text-gray-600'
                }`}>
                  {item.contribution}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};