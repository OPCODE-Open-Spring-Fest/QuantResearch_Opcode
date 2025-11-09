import React from 'react';

interface ChartData {
  date: string;
  value: number;
}

interface PerformanceChartProps {
  portfolioData: ChartData[];
  benchmarkData: ChartData[];
  height?: number;
}

export const PerformanceChart: React.FC<PerformanceChartProps> = ({
  portfolioData,
  benchmarkData,
  height = 300
}) => {
  if (!portfolioData.length || !benchmarkData.length) {
    return (
      <div className="flex items-center justify-center h-64 bg-dark-50/50 border border-dark-300 rounded-xl">
        <div className="text-center text-dark-500">
          <div className="text-4xl mb-2">📊</div>
          <p>No chart data available</p>
        </div>
      </div>
    );
  }

  // Calculate chart dimensions and scales
  const chartWidth = 800;
  const chartHeight = height;
  const padding = { top: 40, right: 40, bottom: 40, left: 60 };

  // Find min and max values for scaling
  const allValues = [...portfolioData.map(d => d.value), ...benchmarkData.map(d => d.value)];
  const maxValue = Math.max(...allValues);
  const minValue = Math.min(...allValues);
  const valueRange = maxValue - minValue;

  // Scale functions
  const scaleX = (index: number) => 
    padding.left + (index / (portfolioData.length - 1)) * (chartWidth - padding.left - padding.right);
  
  const scaleY = (value: number) => 
    chartHeight - padding.bottom - ((value - minValue) / valueRange) * (chartHeight - padding.top - padding.bottom);

  // Generate SVG path data
  const generatePath = (data: ChartData[]) => {
    if (data.length === 0) return '';
    
    let path = `M ${scaleX(0)} ${scaleY(data[0].value)}`;
    
    for (let i = 1; i < data.length; i++) {
      path += ` L ${scaleX(i)} ${scaleY(data[i].value)}`;
    }
    
    return path;
  };

  const portfolioPath = generatePath(portfolioData);
  const benchmarkPath = generatePath(benchmarkData);

  // Generate grid lines and labels
  const gridLines = [];
  const yLabels = [];
  const numGridLines = 5;
  
  for (let i = 0; i <= numGridLines; i++) {
    const value = minValue + (i / numGridLines) * valueRange;
    const y = scaleY(value);
    
    gridLines.push(
      <line
        key={`grid-${i}`}
        x1={padding.left}
        y1={y}
        x2={chartWidth - padding.right}
        y2={y}
        className="stroke-dark-400/30 stroke-1"
      />
    );
    
    yLabels.push(
      <text
        key={`label-${i}`}
        x={padding.left - 10}
        y={y}
        className="fill-dark-500 text-xs font-inter"
        textAnchor="end"
        dominantBaseline="middle"
      >
        ${Math.round(value).toLocaleString()}
      </text>
    );
  }

  // Generate x-axis labels (dates)
  const xLabels = [];
  const labelInterval = Math.max(1, Math.floor(portfolioData.length / 6));
  
  for (let i = 0; i < portfolioData.length; i += labelInterval) {
    const date = new Date(portfolioData[i].date);
    const label = date.toLocaleDateString('en-US', { 
      year: '2-digit', 
      month: 'short' 
    });
    
    xLabels.push(
      <text
        key={`xlabel-${i}`}
        x={scaleX(i)}
        y={chartHeight - padding.bottom + 20}
        className="fill-dark-500 text-[10px] font-inter"
        textAnchor="middle"
      >
        {label}
      </text>
    );
  }

  // Calculate performance metrics
  const portfolioStart = portfolioData[0].value;
  const portfolioEnd = portfolioData[portfolioData.length - 1].value;
  const portfolioReturn = ((portfolioEnd - portfolioStart) / portfolioStart) * 100;

  const benchmarkStart = benchmarkData[0].value;
  const benchmarkEnd = benchmarkData[benchmarkData.length - 1].value;
  const benchmarkReturn = ((benchmarkEnd - benchmarkStart) / benchmarkStart) * 100;

  return (
    <div className="bg-gradient-to-br from-dark-50/95 to-dark-100/98 border border-dark-400/20 rounded-2xl p-6 backdrop-blur-xl transition-all duration-300 hover:border-blue-500/30 hover:shadow-2xl">
      {/* Chart Header */}
      <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-4 mb-6">
        <div>
          <h3 className="text-white text-xl font-semibold mb-1">Portfolio Performance vs Benchmark</h3>
          <div className="text-dark-500 text-sm">
            {portfolioData[0]?.date} to {portfolioData[portfolioData.length - 1]?.date}
          </div>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 sm:gap-6">
          <div className="flex flex-col gap-1">
            <span className="text-dark-500 text-xs uppercase tracking-wide">Portfolio Return:</span>
            <span className={`text-lg font-semibold ${portfolioReturn >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {portfolioReturn >= 0 ? '+' : ''}{portfolioReturn.toFixed(2)}%
            </span>
          </div>
          
          <div className="flex flex-col gap-1">
            <span className="text-dark-500 text-xs uppercase tracking-wide">Benchmark Return:</span>
            <span className={`text-lg font-semibold ${benchmarkReturn >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {benchmarkReturn >= 0 ? '+' : ''}{benchmarkReturn.toFixed(2)}%
            </span>
          </div>
          
          <div className="flex flex-col gap-1">
            <span className="text-dark-500 text-xs uppercase tracking-wide">Outperformance:</span>
            <span className={`text-lg font-semibold ${portfolioReturn >= benchmarkReturn ? 'text-green-400' : 'text-red-400'}`}>
              {(portfolioReturn - benchmarkReturn).toFixed(2)}%
            </span>
          </div>
        </div>
      </div>

      {/* Chart Container */}
      <div className="bg-white/5 border border-dark-400/10 rounded-xl p-4 my-4 transition-colors duration-300 hover:border-dark-400/20">
        <svg 
          width="100%" 
          height={chartHeight} 
          viewBox={`0 0 ${chartWidth} ${chartHeight}`}
          className="block max-w-full h-auto"
        >
          {/* Background */}
          <rect width="100%" height="100%" fill="transparent" />
          
          {/* Grid lines */}
          {gridLines}
          
          {/* Y-axis labels */}
          {yLabels}
          
          {/* X-axis labels */}
          {xLabels}
          
          {/* Axis lines */}
          <line
            x1={padding.left}
            y1={padding.top}
            x2={padding.left}
            y2={chartHeight - padding.bottom}
            className="stroke-dark-400/50 stroke-2"
          />
          <line
            x1={padding.left}
            y1={chartHeight - padding.bottom}
            x2={chartWidth - padding.right}
            y2={chartHeight - padding.bottom}
            className="stroke-dark-400/50 stroke-2"
          />
          
          {/* Portfolio line with glow effect */}
          <defs>
            <filter id="portfolioGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          <path
            d={portfolioPath}
            className="stroke-blue-500 fill-none stroke-[3]"
            strokeLinecap="round"
            strokeLinejoin="round"
            filter="url(#portfolioGlow)"
          />
          
          {/* Benchmark line */}
          <path
            d={benchmarkPath}
            className="stroke-green-500 fill-none stroke-2"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray="5,5"
          />
          
          {/* Portfolio points */}
          {portfolioData.map((point, index) => (
            <circle
              key={`portfolio-${index}`}
              cx={scaleX(index)}
              cy={scaleY(point.value)}
              r="4"
              className="fill-blue-500 stroke-white stroke-2 transition-all duration-200 hover:r-6 hover:fill-white hover:stroke-blue-500"
            />
          ))}
          
          {/* Benchmark points */}
          {benchmarkData.map((point, index) => (
            <circle
              key={`benchmark-${index}`}
              cx={scaleX(index)}
              cy={scaleY(point.value)}
              r="3"
              className="fill-green-500 stroke-white stroke-[1.5] transition-all duration-200 hover:r-5 hover:fill-white hover:stroke-green-500"
            />
          ))}
        </svg>
      </div>

      {/* Chart Legend */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-4 pt-4 border-t border-dark-400/20">
        <div className="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-lg border border-dark-400/10">
          <div className="w-4 h-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"></div>
          <span className="text-dark-500 text-sm">
            Strategy Portfolio (${portfolioEnd.toLocaleString()})
          </span>
        </div>
        
        <div className="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-lg border border-dark-400/10">
          <div className="w-4 h-1 bg-gradient-to-r from-green-500 to-green-600 rounded-full"></div>
          <span className="text-dark-500 text-sm">
            Benchmark - SPY (${benchmarkEnd.toLocaleString()})
          </span>
        </div>
      </div>
    </div>
  );
};