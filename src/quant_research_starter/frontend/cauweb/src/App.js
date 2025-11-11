import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { BacktestStudio } from './pages/BacktestStudio';
import { ResearchLab } from './pages/ResearchLab';
import { PortfolioAnalytics } from './pages/PortfolioAnalytics';
import { Settings } from './pages/Settings';
import './styles/globals.css';

export const App = () => {
    return (
        _jsx(Router, { 
            children: _jsxs("div", { 
                className: "min-h-screen bg-gray-50", 
                children: [
                    _jsx(Navigation, {}), 
                    _jsxs("div", { 
                        className: "ml-64", 
                        children: [
                            _jsx(Header, {}), 
                            _jsxs(Routes, { 
                                children: [
                                    _jsx(Route, { path: "/", element: _jsx(Dashboard, {}) }),
                                    _jsx(Route, { path: "/backtest", element: _jsx(BacktestStudio, {}) }),
                                    _jsx(Route, { path: "/research", element: _jsx(ResearchLab, {}) }),
                                    _jsx(Route, { path: "/portfolio", element: _jsx(PortfolioAnalytics, {}) }),
                                    _jsx(Route, { path: "/settings", element: _jsx(Settings, {}) })
                                ] 
                            })
                        ] 
                    })
                ] 
            }) 
        })
    );
};
