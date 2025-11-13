import React, { useState } from 'react';
import {
  LineChart,
  BarChart3,
  Activity,
  TrendingUp,
  DollarSign,
  Shield,
  Zap,
  Search,
  Filter,
  Download,
  Play,
  Plus,
  Clock,
  ArrowRight,
  Brain,
  PieChart,
  BarChart,
} from 'lucide-react';

// ✅ Chart.js imports
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement, // ✅ Required for Doughnut charts
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

// ✅ Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement, // ✅ Add this line
  Title,
  Tooltip,
  Legend,
  Filler
);

export const ResearchLab = () => {
  const [activeFactor, setActiveFactor] = useState('momentum');
  const [timeRange, setTimeRange] = useState('1Y');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFactors, setSelectedFactors] = useState(['momentum']);

  // ✅ Factor data
  const factors = [
    {
      id: 'momentum',
      name: 'Momentum',
      description: 'Price momentum and trend following factors',
      icon: TrendingUp,
      color: 'blue',
      performance: 0.234,
      volatility: 0.182,
      sharpe: 1.284,
      correlation: 0.12,
      lastUpdated: '2 hours ago',
      status: 'active',
    },
    {
      id: 'value',
      name: 'Value',
      description: 'Valuation metrics and fundamental analysis',
      icon: DollarSign,
      color: 'green',
      performance: 0.156,
      volatility: 0.154,
      sharpe: 1.012,
      correlation: -0.08,
      lastUpdated: '1 day ago',
      status: 'active',
    },
    {
      id: 'size',
      name: 'Size',
      description: 'Market capitalization and small-cap premium',
      icon: BarChart,
      color: 'purple',
      performance: 0.089,
      volatility: 0.198,
      sharpe: 0.449,
      correlation: 0.23,
      lastUpdated: '3 days ago',
      status: 'active',
    },
    {
      id: 'volatility',
      name: 'Volatility',
      description: 'Price volatility and risk measures',
      icon: Activity,
      color: 'red',
      performance: -0.045,
      volatility: 0.267,
      sharpe: -0.168,
      correlation: 0.31,
      lastUpdated: '5 hours ago',
      status: 'active',
    },
    {
      id: 'quality',
      name: 'Quality',
      description: 'Profitability and financial health metrics',
      icon: Shield,
      color: 'orange',
      performance: 0.187,
      volatility: 0.142,
      sharpe: 1.316,
      correlation: 0.05,
      lastUpdated: '1 week ago',
      status: 'active',
    },
    {
      id: 'liquidity',
      name: 'Liquidity',
      description: 'Trading volume and market liquidity factors',
      icon: BarChart3,
      color: 'indigo',
      performance: 0.112,
      volatility: 0.173,
      sharpe: 0.647,
      correlation: 0.18,
      lastUpdated: '2 days ago',
      status: 'active',
    },
  ];

  const researchProjects = [
    {
      id: 1,
      title: 'Momentum Crash Protection',
      description: 'Developing strategies to protect against momentum factor crashes',
      status: 'in-progress',
      progress: 65,
      contributors: 3,
      lastActivity: '2 hours ago',
    },
    {
      id: 2,
      title: 'Multi-Factor Optimization',
      description: 'Optimizing factor weights using machine learning',
      status: 'completed',
      progress: 100,
      contributors: 5,
      lastActivity: '1 week ago',
    },
    {
      id: 3,
      title: 'Factor Timing Model',
      description: 'Building predictive models for factor timing',
      status: 'in-progress',
      progress: 30,
      contributors: 2,
      lastActivity: '1 day ago',
    },
  ];

  // ✅ Chart options
  const performanceChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: {
        ticks: {
          callback: (value) => (value * 100).toFixed(1) + '%',
        },
      },
    },
  };

  const correlationChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
  };

  // ✅ Helper functions
  const getColorClass = (color) => {
    const colors = {
      blue: { background: 'rgba(59,130,246,0.1)', border: 'rgb(59,130,246)', text: 'text-blue-600', light: 'bg-blue-100' },
      green: { background: 'rgba(16,185,129,0.1)', border: 'rgb(16,185,129)', text: 'text-green-600', light: 'bg-green-100' },
      purple: { background: 'rgba(139,92,246,0.1)', border: 'rgb(139,92,246)', text: 'text-purple-600', light: 'bg-purple-100' },
      red: { background: 'rgba(239,68,68,0.1)', border: 'rgb(239,68,68)', text: 'text-red-600', light: 'bg-red-100' },
      orange: { background: 'rgba(245,158,11,0.1)', border: 'rgb(245,158,11)', text: 'text-orange-600', light: 'bg-orange-100' },
      indigo: { background: 'rgba(99,102,241,0.1)', border: 'rgb(99,102,241)', text: 'text-indigo-600', light: 'bg-indigo-100' },
    };
    return colors[color] || colors.blue;
  };

  const getPerformanceData = () => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const selectedFactor = factors.find((f) => f.id === activeFactor);
    const color = getColorClass(selectedFactor?.color || 'blue');

    return {
      labels: months,
      datasets: [
        {
          label: `${selectedFactor?.name} Factor`,
          data: months.map(() => Math.random() * 0.1 - 0.02),
          borderColor: color.border,
          backgroundColor: color.background,
          fill: true,
          tension: 0.4,
        },
        {
          label: 'Benchmark',
          data: months.map(() => Math.random() * 0.08 - 0.03),
          borderColor: 'rgb(75,85,99)',
          backgroundColor: 'rgba(75,85,99,0.1)',
          borderDash: [5, 5],
          fill: true,
          tension: 0.4,
        },
      ],
    };
  };

  const getCorrelationData = () => {
    const selectedFactorsData = factors.filter((f) => selectedFactors.includes(f.id));
    return {
      labels: selectedFactorsData.map((f) => f.name),
      datasets: [
        {
          label: 'Factor Correlation',
          data: selectedFactorsData.map(() => Math.random() * 2 - 1),
          backgroundColor: selectedFactorsData.map((f) => getColorClass(f.color).background),
          borderColor: selectedFactorsData.map((f) => getColorClass(f.color).border),
          borderWidth: 2,
        },
      ],
    };
  };

  const getExposureData = () => ({
    labels: ['Technology', 'Healthcare', 'Financials', 'Consumer', 'Energy', 'Industrial'],
    datasets: [
      {
        label: 'Sector Exposure',
        data: [25, 18, 15, 12, 8, 22],
        backgroundColor: [
          'rgba(59,130,246,0.8)',
          'rgba(16,185,129,0.8)',
          'rgba(139,92,246,0.8)',
          'rgba(245,158,11,0.8)',
          'rgba(239,68,68,0.8)',
          'rgba(99,102,241,0.8)',
        ],
        borderColor: [
          'rgb(59,130,246)',
          'rgb(16,185,129)',
          'rgb(139,92,246)',
          'rgb(245,158,11)',
          'rgb(239,68,68)',
          'rgb(99,102,241)',
        ],
        borderWidth: 2,
      },
    ],
  });

  const formatPercent = (value) => (value * 100).toFixed(2) + '%';

  const toggleFactorSelection = (factorId) => {
    setSelectedFactors((prev) =>
      prev.includes(factorId) ? prev.filter((id) => id !== factorId) : [...prev, factorId]
    );
  };

  // ✅ Main return
  return (
    <div className="min-h-screen bg-gray-50 p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Research Lab</h1>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
        {/* Sidebar */}
        <div className="xl:col-span-1 space-y-6">
          <div className="bg-white p-6 rounded-xl border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Alpha Factors</h3>
            <div className="space-y-3">
              {factors.map((factor) => {
                const Icon = factor.icon;
                const colorClass = getColorClass(factor.color);
                const isSelected = selectedFactors.includes(factor.id);
                return (
                  <div
                    key={factor.id}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition ${
                      isSelected ? 'bg-gray-50 border-gray-400' : 'bg-white border-gray-200'
                    }`}
                    onClick={() => setActiveFactor(factor.id)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 ${colorClass.light} rounded-lg flex items-center justify-center`}>
                          <Icon className={`w-5 h-5 ${colorClass.text}`} />
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-900">{factor.name}</h4>
                          <p className="text-sm text-gray-500">{factor.description}</p>
                        </div>
                      </div>
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={(e) => {
                          e.stopPropagation();
                          toggleFactorSelection(factor.id);
                        }}
                        className="w-4 h-4 text-blue-600"
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="xl:col-span-3 space-y-8">
          {/* Performance */}
          <div className="bg-white rounded-xl p-6 border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Factor Performance</h3>
            <div className="h-80">
              <Line data={getPerformanceData()} options={performanceChartOptions} />
            </div>
          </div>

          {/* Sector Exposure */}
          <div className="bg-white rounded-xl p-6 border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Sector Exposure</h3>
            <div className="h-80">
              <Doughnut data={getExposureData()} />
            </div>
          </div>

          {/* Correlation */}
          <div className="bg-white rounded-xl p-6 border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Factor Correlation</h3>
            <div className="h-80">
              <Bar data={getCorrelationData()} options={correlationChartOptions} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResearchLab;
