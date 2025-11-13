import { useState } from 'react';
import { Save, Bell, Database, Cpu, Shield, BarChart3, TrendingUp } from 'lucide-react';

export const Settings = () => {
  const [settings, setSettings] = useState({
    timezone: 'UTC',
    currency: 'USD ($)',
    realTimeUpdates: false,
    emailReports: true,
    riskTolerance: 'medium',
    chartTheme: 'dark',
    dataRetention: '12',
    apiRateLimit: '1000'
  });

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    // Save settings logic here
    console.log('Saving settings:', settings);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 sm:mb-12">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900">
              Research Settings
            </h1>
          </div>
          <p className="text-gray-600 text-sm sm:text-base max-w-3xl">
            Configure your quantitative research environment, data preferences, and notification settings
          </p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 lg:gap-8">
          {/* Main Settings Column */}
          <div className="xl:col-span-2 space-y-6 lg:space-y-8">
            {/* General Preferences */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 sm:p-8">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Cpu className="w-5 h-5 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">General Preferences</h3>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Default Timezone
                  </label>
                  <select 
                    value={settings.timezone}
                    onChange={(e) => handleSettingChange('timezone', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    <option>UTC</option>
                    <option>EST</option>
                    <option>PST</option>
                    <option>GMT</option>
                    <option>CET</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Base Currency
                  </label>
                  <select 
                    value={settings.currency}
                    onChange={(e) => handleSettingChange('currency', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    <option>USD ($)</option>
                    <option>EUR (€)</option>
                    <option>GBP (£)</option>
                    <option>JPY (¥)</option>
                    <option>CNY (¥)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Risk Tolerance
                  </label>
                  <select 
                    value={settings.riskTolerance}
                    onChange={(e) => handleSettingChange('riskTolerance', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    <option value="low">Low Risk</option>
                    <option value="medium">Medium Risk</option>
                    <option value="high">High Risk</option>
                    <option value="aggressive">Aggressive</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Chart Theme
                  </label>
                  <select 
                    value={settings.chartTheme}
                    onChange={(e) => handleSettingChange('chartTheme', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    <option value="dark">Dark</option>
                    <option value="light">Light</option>
                    <option value="system">System</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Data & API Settings */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 sm:p-8">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Database className="w-5 h-5 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">Data & API Settings</h3>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Data Retention (months)
                  </label>
                  <select 
                    value={settings.dataRetention}
                    onChange={(e) => handleSettingChange('dataRetention', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    <option value="3">3 Months</option>
                    <option value="6">6 Months</option>
                    <option value="12">12 Months</option>
                    <option value="24">24 Months</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Rate Limit (requests/hour)
                  </label>
                  <select 
                    value={settings.apiRateLimit}
                    onChange={(e) => handleSettingChange('apiRateLimit', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    <option value="100">100</option>
                    <option value="500">500</option>
                    <option value="1000">1,000</option>
                    <option value="5000">5,000</option>
                  </select>
                </div>
              </div>

              <div className="mt-6 space-y-4">
                <label className="flex items-start gap-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors duration-200">
                  <input 
                    type="checkbox"
                    checked={settings.realTimeUpdates}
                    onChange={(e) => handleSettingChange('realTimeUpdates', e.target.checked)}
                    className="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500 transition duration-200"
                  />
                  <div>
                    <span className="block text-sm font-medium text-gray-700">
                      Enable real-time data updates
                    </span>
                    <span className="block text-sm text-gray-500 mt-1">
                      Get live market data and instant portfolio updates
                    </span>
                  </div>
                </label>

                <label className="flex items-start gap-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors duration-200">
                  <input 
                    type="checkbox"
                    checked={settings.emailReports}
                    onChange={(e) => handleSettingChange('emailReports', e.target.checked)}
                    className="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500 transition duration-200"
                  />
                  <div>
                    <span className="block text-sm font-medium text-gray-700">
                      Send performance reports via email
                    </span>
                    <span className="block text-sm text-gray-500 mt-1">
                      Receive daily summary reports and weekly analytics
                    </span>
                  </div>
                </label>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6 lg:space-y-8">
            {/* Performance Preview */}
            <div className="bg-gradient-to-br from-blue-600 to-purple-700 rounded-2xl shadow-lg p-6 text-white">
              <div className="flex items-center gap-3 mb-4">
                <TrendingUp className="w-6 h-6" />
                <h3 className="text-lg font-semibold">Performance Preview</h3>
              </div>
              
              {/* Mini Chart Placeholder */}
              <div className="bg-blue-500/20 rounded-xl p-4 mb-4">
                <div className="h-32 flex items-end justify-between space-x-1">
                  {[30, 45, 60, 75, 90, 75, 60, 45, 60, 75, 85, 70].map((height, index) => (
                    <div
                      key={index}
                      className="flex-1 bg-white/30 rounded-t transition-all duration-300 hover:bg-white/40"
                      style={{ height: `${height}%` }}
                    />
                  ))}
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <p className="text-blue-200 text-sm">Current ROI</p>
                  <p className="text-xl font-bold">+12.4%</p>
                </div>
                <div>
                  <p className="text-blue-200 text-sm">Sharpe Ratio</p>
                  <p className="text-xl font-bold">1.8</p>
                </div>
              </div>
            </div>

            {/* Security & Actions */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-red-100 rounded-lg">
                  <Shield className="w-5 h-5 text-red-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">Security</h3>
              </div>
              
              <div className="space-y-4">
                <button className="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors duration-200">
                  <span className="block text-sm font-medium text-gray-700">
                    Two-Factor Authentication
                  </span>
                  <span className="block text-sm text-gray-500 mt-1">
                    Enhanced security for your account
                  </span>
                </button>

                <button className="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors duration-200">
                  <span className="block text-sm font-medium text-gray-700">
                    API Keys Management
                  </span>
                  <span className="block text-sm text-gray-500 mt-1">
                    View and manage your API credentials
                  </span>
                </button>
              </div>

              {/* Save Button */}
              <button
                onClick={handleSave}
                className="w-full mt-6 bg-blue-600 text-white px-6 py-4 rounded-xl hover:bg-blue-700 transition-all duration-200 flex items-center justify-center gap-2 font-semibold shadow-lg shadow-blue-500/25"
              >
                <Save className="w-5 h-5" />
                <span>Save All Changes</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};