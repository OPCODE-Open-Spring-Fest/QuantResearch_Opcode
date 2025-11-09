import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, PlayCircle, FlaskConical, PieChart, Settings, TrendingUp } from 'lucide-react';
export const Navigation = () => {
    const navItems = [
        { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
        { path: '/backtest', icon: PlayCircle, label: 'Backtest Studio' },
        { path: '/research', icon: FlaskConical, label: 'Research Lab' },
        { path: '/portfolio', icon: PieChart, label: 'Portfolio Analytics' },
        { path: '/settings', icon: Settings, label: 'Settings' }
    ];
    return (_jsxs("nav", { className: "fixed left-0 top-0 h-full w-64 bg-white shadow-xl border-r border-gray-200", children: [_jsx("div", { className: "p-6 border-b border-gray-200", children: _jsxs("div", { className: "flex items-center space-x-3", children: [_jsx("div", { className: "w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center", children: _jsx(TrendingUp, { className: "w-6 h-6 text-white" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-gray-900", children: "CAUQuant" }), _jsx("p", { className: "text-xs text-gray-500", children: "Research Platform" })] })] }) }), _jsx("div", { className: "p-4 space-y-2", children: navItems.map((item) => {
                    const Icon = item.icon;
                    return (_jsxs(NavLink, { to: item.path, className: ({ isActive }) => `flex items-center space-x-3 px-4 py-3 rounded-xl transition-colors ${isActive
                            ? 'bg-blue-50 text-blue-700 border border-blue-200'
                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}`, children: [_jsx(Icon, { className: "w-5 h-5" }), _jsx("span", { className: "font-medium", children: item.label })] }, item.path));
                }) }), _jsx("div", { className: "absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200", children: _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex justify-between text-sm", children: [_jsx("span", { className: "text-gray-500", children: "Strategies" }), _jsx("span", { className: "font-semibold", children: "12" })] }), _jsxs("div", { className: "flex justify-between text-sm", children: [_jsx("span", { className: "text-gray-500", children: "Assets" }), _jsx("span", { className: "font-semibold", children: "248" })] }), _jsxs("div", { className: "flex justify-between text-sm", children: [_jsx("span", { className: "text-gray-500", children: "Backtests" }), _jsx("span", { className: "font-semibold", children: "1.2K" })] })] }) })] }));
};
